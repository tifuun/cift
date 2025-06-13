"""
semir.py: Semantic Intermediate Representation of CIF files.

This file is not yet complete. Only some CIF commands are handled.

"""

from dataclasses import dataclass

from cift.grammars import strict as gr

class CSTMonad:
    def __init__(self, *nodes):
        self.nodes = nodes

    def __repr__(self):
        return '\n\t'.join((
            '<CSTMonad ',
            *map(repr, self.nodes),
            '>'
            ))

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
class RoutDef:
    # TODO the scale thing?
    num: int
    commands: list  # TODO type

    def __init__(self, cstmonad):
        self.commands = []

        #tree.self_is(gr.command)

        tree.nth(0, gr.def_start_command)

        self.num = int(
            tree
            .nth(0, gr.def_start_command)
            .only(gr.integer)
            .only(gr.integer_d)
            .string
            )

        for child in tree.children[1:-1]:
            try:
                self.commands.append(LayerSwitch(child))
            except CSTError:
                pass

            try:
                self.commands.append(RoutCall(child))
            except CSTError:
                pass
            try:
                self.commands.append(Poly(child))
            except CSTError:
                pass

    def __repr__(self):
        return f"<RoutDef {self.num}>"


@dataclass
class RoutCall:
    # TODO rotation/position
    num: int

    def __init__(self, node):
        self.num = int(
            node
            .oftype(gr.call_command)
            .single_child(gr.integer)
            .single_child(gr.integer_d)
            .nodes[0]
            .string
            )

    def __repr__(self):
        return f"<RoutCall {self.num}>"

@dataclass
class Poly:
    # TODO `types` module???
    points: list[tuple[int, int]]

    def __init__(self, tree):
        self.points = []

        tree.self_is(gr.command)

        self.name = (
            tree
            .single(gr.polygon_command)
            .only(gr.path)
            .forevery(gr.point)
            .only(gr.shortname)
            .string
            )

    def __repr__(self):
        return f"<Poly>"

@dataclass
class LayerSwitch:
    name: str

    def __init__(self, tree):
        tree.self_is(gr.command)

        self.name = (
            tree
            .single(gr.layer_command)
            .only(gr.shortname)
            .string
            )

    def __repr__(self):
        return f"<LayerSwitch '{self.name}'>"

@dataclass
class CIFFile:
    commands: list[LayerSwitch, RoutDef, RoutCall, Poly]

    def __init__(self, node):
        self.commands = []

        commands = (
            node
            .oftype(gr.cif_file)
            .unroll()
            .oftype(gr.command)
            .nodes
            )
        print('\n'.join(map(str, commands)))

        (
            node
            .oftype(gr.cif_file)
            .unroll()
            .oftype(gr.command)
            .singledispatch(RoutDef, RoutCall, Poly, LayerSwitch)
            # TODO here we need a second monad type for IR?
            )

    # TODO dispatch method

    def print(self):
        print('CIFFile')
        for child in self.commands:
            print(child)



