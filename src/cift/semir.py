"""
semir.py: Semantic Intermediate Representation of CIF files.

This file is not yet complete. Only some CIF commands are handled.

"""

from dataclasses import dataclass

from cift.grammars import strict as gr
from cift.parser import terminal

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

@dataclass
class CIFCommand:

    def __init__(self, node):
        self.inner_commands = (
            node
            .oftype(gr.cif_file)
            .unroll()
            .oftype(gr.command)
            .nodes
            )
        #print('\n'.join(map(str, self.inner_commands)))

        self.target_layer = (
            node
            .sole_child(gr.prim_command)
            .sole_child(gr.layer_command)
            .single_child(gr.shortname)
            .mapsingle(lambda node: node.string)
            )

        self.called_rout = (
            node
            .sole_child(gr.prim_command)
            .sole_child(gr.call_command)
            .single_child(gr.integer)
            .single_child(gr.integer_d)
            .mapsingle(lambda node: int(node.string))
            )  # TODO transformation

        self.defined_rout = (
            node
            .single_child(gr.def_start_command)
            .single_child(gr.integer)
            .single_child(gr.integer_d)
            .mapsingle(lambda node: int(node.string))
            )

        self.points = (
            node
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


    def eval(self):
        print(f"{self.target_layer = }")
        print(f"{self.called_rout = }")
        print(f"{self.defined_rout = }")
        print(f"{self.points = }")
        print()
        for node in self.inner_commands:
            monad = CSTMonad(node)
            child = CIFCommand(monad)
            child.eval()



    def print(self):
        print('CIFFile')
        for child in self.commands:
            print(child)



