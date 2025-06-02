"""parser.py: contains Parser class and relevant utils"""

class Symbol:
    """A symbol in a context-free grammar"""
    def __init__(self, name = None):
        self.name = name

    def __repr__(self):
        return f"<Symbol {self.name}>"

class _SingleWrapper():
    """Helper class: takes in a single object and stores it"""
    def __init__(self, what):
        super().__init__()
        self.what = what

class _TupleWrapper():
    """Helper class: takes in a tuple and stores it"""
    def __init__(self, *what):
        super().__init__()
        self.what = what

class Seq(_TupleWrapper):
    """Context-free grammar definition helper: a sequence of symbols"""

class Or(_TupleWrapper):
    """Context-free grammar definition helpers: one of multiple symbols"""

class Maybe(_SingleWrapper):
    """Grammar helper: Zero or one of this symbol"""

class Many(_SingleWrapper):
    """Grammar helper: Zero, one, or more of this symbol"""

class ASTNode:
    """Node in a syntax tree."""
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

        if True in self.children:
            assert False
        if False in self.children:
            assert False

    def __repr__(self):
        return f"<ASTNode {self.symbol}>"

    def __bool__(self):
        return True

class Parser:
    """Parses string according to a context-free grammar definition"""
    def __init__(self, grammar, string):
        self.grammar = grammar
        self.string = string

        self.index = 0
        self.tree = None

        self.fullcst = False

    def parse(self, symbol = None):

        if symbol is None:
            symbol = self.grammar[tuple(self.grammar.keys())[0]]

        self.tree = self._parse(symbol)
        
        return self.tree

    def _parse(self, symbol):
        
        node = ASTNode(symbol)

        self.check_over_consumed()

        if isinstance(symbol, Symbol):
            mark = self.index

            child = self._parse(self.grammar[symbol])

            if child:
                node.children.append(child)
                child.symbol = symbol
                return node

            self.index = mark
            return False


        elif isinstance(symbol, Seq):
            mark = self.index

            children = []
            for elem in symbol.what:
                children.append(self._parse(elem))

            if all(children):
                if self.fullcst:
                    node.children.extend(child)
                else:
                    for child in children:
                        node.children.extend(child.children)

                return node

            self.index = mark
            return False


        elif isinstance(symbol, Or):

            mark = self.index

            for elem in symbol.what:

                child = self._parse(elem)

                if child:
                    if self.fullcst:
                        node.children.append(child)
                    else:
                        node.children.extend(child.children)
                    return node

                else:
                    self.index = mark

            return False

        elif isinstance(symbol, Maybe):

            if self.is_consumed():
                return node

            mark = self.index

            child = self._parse(symbol.what)

            if child:
                if self.fullcst:
                    node.children.append(child)
                else:
                    node.children.extend(child.children)
            else:
                self.index = mark

            return node

        elif isinstance(symbol, Many):

            if self.is_consumed():
                return node

            while True:
                mark = self.index

                child = self._parse(symbol.what)

                if child:
                    if self.fullcst:
                        node.children.append(child)
                    else:
                        node.children.extend(child.children)
                else:
                    self.index = mark
                    break

                if self.is_consumed():
                    return node

            return node

        elif isinstance(symbol, str):
            result = self.try_consume(symbol)
            if result:
                node.children.append(symbol)
                return node

            return False

        assert False, type(symbol)

    def try_consume(self, symbol):
        if self.index > len(self.string):
            assert False

        if self.index == len(self.string):
            return len(symbol) == 0

        if not symbol:
            return True

        if self.string[self.index:].startswith(symbol):
            self.index += len(symbol)

            return True

        return False

    def is_consumed(self):
        return self.index == len(self.string)

    def check_over_consumed(self):
        if self.index > len(self.string):
            assert False

