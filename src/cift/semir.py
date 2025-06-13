"""
semir.py: Semantic Intermediate Representation of CIF files.

This file is not yet complete. Only some CIF commands are handled.

"""

from dataclasses import dataclass

from cift.grammars import strict as gr
from cift.parser import CSTError

@dataclass
class RoutDef:
    # TODO the scale thing?
    num: int
    commands: list  # TODO type

    def __init__(self, tree):
        self.commands = []

        tree.self_is(gr.command)

        tree.nth(0, gr.def_start_command)

        self.num = int(
            tree
            .nth(0, gr.def_start_command)
            .only(gr.integer)
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

    def __init__(self, tree):
        tree.self_is(gr.command)

        self.num = int(
            tree
            .single(gr.call_command)
            .only(gr.integer)
            .string
            )

    def __repr__(self):
        return f"<RoutCall {self.num}>"

@dataclass
class Poly:
    # TODO `types` module???
    points: list[tuple[int, int]]

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

    def __init__(self, tree):
        tree.self_is(gr.cif_file)

        self.commands = []

        for child in tree.children:
            try:
                self.commands.append(LayerSwitch(child))
            except CSTError:
                pass

            try:
                self.commands.append(RoutDef(child))
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

    def print(self):
        print('CIFFile')
        for child in self.commands:
            print(child)



