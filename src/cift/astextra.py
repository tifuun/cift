"""astextra: extra utilities for processing `ASTNode`s."""

from cift.parser import ASTNode

def reduce(node):
    """
    Remove some nodes from AST to make it more readable.
    """
    new_children = []
    for child in node.children:
        if isinstance(child, str):
            continue

        if child.symbol is blank:
            continue

        if child.symbol is sep:
            continue

        if child.symbol is semi:
            continue

        #if child.symbol is command:
        #    assert len(child.children) == 1
        #    child = child.children[0]

        if child.symbol is prim_command:
            assert len(child.children) == 1
            child = child.children[0]

        
        new_children.append(child)

    node.children = new_children


def print(self, depth = 0):
    self.descend(
        lambda obj, depth, number:
        print(f"{number}:{' ' * depth}{repr(obj)}"),
        )

def yield_dot(self, depth = 0):
    yield 'digraph D {'
    yield 'node [shape=box]'

    ordering = WeakKeyDictionary()
    self.descend(
        lambda obj, depth, number, ordering = ordering:
        ordering.update({obj: number}),
        False
        )

    for node, number in ordering.items():
        #yield f'N{number} [label="{node.symbol.name}"]'
        yield fr'N{number} [label="{node.symbol.name}\l{escape_dot_label(node.string)}"]'

    edges = []
    self.descend(
        lambda obj, depth, number, ordering = ordering:
        edges.extend(
            f"N{number} -> N{ordering[child]}"
            for child in obj.children if isinstance(child, type(self))
            ),
        False
        )
    yield from edges
    yield '}'

def print_dot(self):
    print('\n'.join(self.yield_dot()))

