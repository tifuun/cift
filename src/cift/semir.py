"""
semir.py: Semantic Intermediate Representation of CIF files.

This file is not yet complete. Only some CIF commands are handled.

"""

from dataclasses import dataclass
from enum import StrEnum

from cift.grammars import strict as gr
from cift.parser import terminal
from cift.parser import CSTNode

def merge_layers(dest, source):
    for k, v in source.items():
        if k not in dest.keys():
            dest[k] = []
        dest[k].extend(v)

class CSTMonad:
    def __init__(self, *nodes):
        self.nodes = nodes

    def __repr__(self):
        return '\n\t'.join((
            '<CSTMonad ',
            *map(repr, self.nodes),
            '>'
            ))

    def __bool__(self):
        return len(self.nodes) > 0

    def and_(self, other):
        if not bool(self):
            return self
        return other

    def or_(self, other):
        if bool(self):
            return self
        return other

    def map(self, func):
        return tuple(map(func, self.nodes))

    def mapn(self, num, func, fallback=None):
        if len(self.nodes) != num:
            return fallback
        return tuple(map(func, self.nodes))

    def mapn_wrap(self, num, func, fallback=None):
        if len(self.nodes) != num:
            return fallback
        return tuple(func(type(self)(node)) for node in self.nodes)

    def mapsingle(self, func, fallback=None):
        if len(self.nodes) != 1:
            return fallback
        return func(self.nodes[0])

    def unroll(self):
        return type(self)(*(
            child
            for node in self.nodes
            for child in node.children
            ))

    def oftype(self, symbol):
        return type(self)(*(
            node
            for node in self.nodes
            if node.symbol is symbol
            ))

    def assert_len(self, n):
        if len(self.nodes) == n:
            return self
        else:
            return type(self)()

    def slice(self, a=None, b=None, c=None):
        return type(self)(*self.nodes[slice(a,b,c)])

    def sole_child(self, symbol):
        return self.unroll().assert_len(1).oftype(symbol)

    def single_child(self, symbol):
        return self.unroll().oftype(symbol).assert_len(1)

    def singledispatch(self, *methods):
        return type(self)(*(
            method(type(self)(node))
            for node in self.nodes
            )).unroll().assert_length(1)

class SemType(StrEnum):
    FILE = 'FILE'
    DEF = 'DEF'
    CALL = 'CALL'
    LAYER = 'LAYER'
    POLY = 'POLY'

@dataclass
class SemIR:

    def __init__(self, monad):
        self.toplevel_children = []
        self.symb_children = []
        self.semtype = None
        self.monad = monad

        self.toplevel_commands = (
            monad
            .oftype(gr.cif_file)
            .unroll()
            .oftype(gr.command)
            .nodes
            )

        self.target_layer = (
            monad
            .sole_child(gr.prim_command)
            .sole_child(gr.layer_command)
            .single_child(gr.shortname)
            .mapsingle(lambda node: node.string)
            )

        self.called_symb = (
            monad
            .sole_child(gr.prim_command)
            .sole_child(gr.call_command)
            .single_child(gr.integer)
            .single_child(gr.integer_d)
            .mapsingle(lambda node: int(node.string))
            )  # TODO transformation

        self.defined_symb = (
            monad
            .single_child(gr.def_start_command)
            .single_child(gr.integer)
            .single_child(gr.integer_d)
            .mapsingle(lambda node: int(node.string))
            )

        self.symb_commands = (
            monad
            .single_child(gr.def_start_command)
            .and_(
                monad
                .unroll()
                .oftype(gr.prim_command)
                )
            .nodes
            )

        # polygon
        self.points = (
            monad
            .sole_child(gr.prim_command)
            .sole_child(gr.polygon_command)
            .single_child(gr.path)
            .unroll()
            .oftype(gr.point)
            .map(lambda point: (
                CSTMonad(point)
                .unroll()
                .oftype(gr.sinteger)
                .mapn_wrap(2, lambda sint:
                    [1, -1][bool(sint.single_child(terminal))]  # minus sign
                    *
                    sint.single_child(gr.integer_d).mapsingle(
                        lambda node: int(node.string)
                        )
                    )
                ))
            )

        box_monad = (
            monad
            .sole_child(gr.prim_command)
            .sole_child(gr.box_command)
            )

        if box_monad:
            # TODO still some potential errors here if some
            # constructs cst by hand,
            # we need to go FULLY MONADIC!!!!
            width, height = (
                box_monad
                .unroll()
                .oftype(gr.integer)
                .unroll()
                .oftype(gr.integer_d)
                .mapn(2, lambda node: int(node.string))
                )
            cx, cy = (
                box_monad
                .unroll()
                .oftype(gr.point)
                .slice(0) # index 1 is rotation
                .unroll()
                .oftype(gr.sinteger)
                .mapn_wrap(2, lambda sint:  # TODO copypasta
                    [1, -1][bool(sint.single_child(terminal))]  # minus sign
                    *
                    sint.single_child(gr.integer_d).mapsingle(
                        lambda node: int(node.string)
                        )
                    )
                )
            # TODO rotation
            self.points = (
                (cx - width // 2, cy - height // 2),  # TODO rounding??
                (cx + width // 2, cy - height // 2),
                (cx + width // 2, cy + height // 2),
                (cx - width // 2, cy + height // 2),
                )

    
    def __repr__(self):
        return ''.join((
            '<SemIR',
            f' {self.target_layer=}' if self.target_layer is not None else '',
            f' {self.called_symb=}' if self.called_symb is not None else '',
            f' {self.defined_symb=}' if self.defined_symb is not None else '',
            f' {self.points=}' if self.points else '',
            '>'
            ))


    def eval(self, depth=0):
        for node in self.toplevel_commands:
            monad = CSTMonad(node)
            child = type(self)(monad)
            child.eval(depth=depth+1)

            self.toplevel_children.append(child)

        for node in self.symb_commands:
            # init expects command -> prim_command
            # but we have just prim_command
            # so wrap it
            node_wrapped = CSTNode(gr.command)
            node_wrapped.children.append(node)

            monad = CSTMonad(node_wrapped)
            child = type(self)(monad)
            child.eval(depth=depth+1)

            self.symb_children.append(child)

    def classify(self):
        if self.toplevel_commands:
            assert self.semtype is None
            self.semtype = SemType.FILE

        if self.target_layer is not None:
            assert self.semtype is None
            self.semtype = SemType.LAYER

        if self.called_symb is not None:
            assert self.semtype is None
            self.semtype = SemType.CALL

        if self.defined_symb is not None:
            assert self.semtype is None
            self.semtype = SemType.DEF

        if self.points:
            assert self.semtype is None
            self.semtype = SemType.POLY

        assert self.semtype is not None

    def build(self, symbs = None):
        if symbs is None:
            symbs = {}
        layers = {}

        layer = None
        for child in (*self.symb_children, *self.toplevel_children):
            if child.target_layer is not None:
                layer = child.target_layer
                if layer not in layers.keys():
                    layers[layer] = []

            if child.points:
                assert layer is not None
                layers[layer].append(child.points)

            if child.defined_symb is not None:
                symbs[child.defined_symb] = child.build(symbs)

            if child.called_symb is not None:
                merge_layers(layers, symbs[child.called_symb])

        return layers

    def print(self):
        print('SemIR')
        for child in self.commands:
            print(child)



