import inspect
from weakref import WeakKeyDictionary

def escape_dot_label(s: str) -> str:
    """
    chatgpt code, no clue whether this is exhaustive or not
    """
    return '"' + s.replace('\\', '\\\\') \
                  .replace('"', '\\"') \
                  .replace('\n', '\\l') \
                  .replace('\r', '') + '"'

ascii_chars = set(map(chr, range(128)))

class NorxondorGorgonax:
    def __init__(self):
        self.line = self.get_instantiation_line_text()

    def get_instantiation_line_text(self):
        # Inspect the call stack to get the line of code of the instantiation
        stack = inspect.stack()
        # The line text is in the caller's frame
        frame = stack[3]
        line_number = frame.lineno
        filename = frame.filename

        # Open the file and get the line of code
        with open(filename, 'r') as f:
            lines = f.readlines()
            return lines[line_number - 1].strip()  # Line numbers are 1-based

class Symbol:
    def __init__(self, name = None):
        self.name = name

    def __repr__(self):
        return f"<Symbol {self.name}>"

class _SingleWrapper(NorxondorGorgonax):
    def __init__(self, what):
        super().__init__()
        self.what = what

class _TupleWrapper(NorxondorGorgonax):
    def __init__(self, *what):
        super().__init__()
        self.what = what

class Seq(_TupleWrapper):
    pass

class Or(_TupleWrapper):
    pass

class Maybe(_SingleWrapper):
    pass

class Many(_SingleWrapper):
    pass

class ASTNode:
    def __init__(self, symbol, children):
        self.symbol = symbol
        self.children = children
        self.string = None

        if True in self.children:
            assert False
        if False in self.children:
            assert False

    def __repr__(self):
        return f"<ASTNode {self.symbol}>"

    def __bool__(self):
        return True

    def descend(
            self,
            callback,
            callback_terminal = None,
            depth = 0,
            number = None
            ):

        if number is None:
            number = [0]

        if callback_terminal is None:
            callback_terminal = callback
            
        callback(self, depth, number[0])
        number[0] += 1
        for child in self.children:
            if isinstance(child, type(self)):
                if callback is not False:
                    child.descend(
                        callback,
                        callback_terminal,
                        depth + 1,
                        number
                        )
            elif isinstance(child, str):
                if callback_terminal is not False:
                    callback_terminal(child, depth + 1, number[0])
            else:
                assert False

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
            yield f'N{number} [label={escape_dot_label(node.string)}]'

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

    def compute_string(self):
        self.string = ''.join(
            child if isinstance(child, str) else child.compute_string()
            for child in self.children
            )
        return self.string

class Parser:
    def __init__(self, grammar, string):
        self.grammar = grammar
        self.string = string

        self.index = 0
        self.tree = None

        self.fullcst = False

    def parse(self, symbol = None):

        if symbol is None:
            symbol = tuple(self.grammar.keys())[0]

        self.tree = self._parse(symbol)
        
        return self.tree

    def _parse(self, symbol):
        
        node = ASTNode(symbol, [])

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

def CIF():
    ascii_all = set(map(chr, range(128)))
    ascii_digits = set("0123456789")
    ascii_upper = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    cif_file = Symbol("cif_file")
    command = Symbol("command")
    prim_command = Symbol("prim_command")
    polygon_command = Symbol("polygon_command")
    box_command = Symbol("box_command")
    round_flash_command = Symbol("round_flash_command")
    wire_command = Symbol("wire_command")
    layer_command = Symbol("layer_command")
    def_start_command = Symbol("def_start_command")
    def_finish_command = Symbol("def_finish_command")
    def_delete_command = Symbol("def_delete_command")
    call_command = Symbol("call_command")
    user_extension_command = Symbol("user_extension_command")
    comment_command = Symbol("comment_command")
    end_command = Symbol("end_command")

    transformation = Symbol("transformation")

    path = Symbol("path")
    point = Symbol("point")

    sinteger = Symbol("sinteger")
    integer = Symbol("integer")
    integer_d = Symbol("integer_d")
    shortname = Symbol("shortname")
    c = Symbol("c")
    user_text = Symbol("user_text")
    comment_text = Symbol("comment_text")

    semi = Symbol("semi")
    sep = Symbol("sep")
    digit = Symbol("digit")
    upper_char = Symbol("upper_char")
    blank = Symbol("blank")
    user_char = Symbol("user_char")
    comment_char = Symbol("comment_char")

    grammar = {
        cif_file: Seq(
            Many(
                Seq(Many(blank), Maybe(command), semi)
                ),
            end_command,
            Many(blank)
            ),

        command: Or(
            prim_command,
            def_delete_command,
            Seq(
                def_start_command,
                semi,
                Many(
                    Seq(
                        Many(blank),
                        Maybe(prim_command),
                        semi
                        ),
                    ),
                def_finish_command,
                ),
            ),

        prim_command: Or(
            polygon_command,
            box_command,
            round_flash_command,
            wire_command,
            layer_command,
            call_command,
            user_extension_command,
            comment_command
            ),

        polygon_command: Seq('P', path),
        box_command: Seq(
            'B', integer, sep, integer, sep, point,
            Maybe(Seq(sep, point)),
            ),
        round_flash_command: Seq("R", integer, sep, point),
        wire_command: Seq("W", integer, sep, path),
        layer_command: Seq("L", Many(blank), shortname),
        def_start_command: Seq(
            "D", Many(blank), "S", integer,
            Maybe(Seq(sep, integer, sep, integer))
            ),
        def_finish_command: Seq("D", Many(blank), "F"),
        def_delete_command: Seq("D", Many(blank), "D", integer),
        call_command: Seq("C", integer, transformation),
        user_extension_command: Seq(digit, user_text),
        comment_command: Seq("(", comment_text, ")"),
        end_command: "E",

        transformation: Many(
            Seq(
                Many(blank),
                Or(
                    Seq("T", point),
                    Seq("M", Many(blank), "X"),
                    Seq("M", Many(blank), "Y"),
                    Seq("R", point),
                    )
                )
            ),

        path: Seq(point, Many(Seq(sep, point))),
        point: Seq(sinteger, sep, sinteger),

        sinteger: Seq(Many(sep), Maybe("-"), integer_d),
        integer: Seq(Many(sep), integer_d),
        integer_d: Seq(digit, Many(digit)),

        shortname: Seq(c, Maybe(c), Maybe(c), Maybe(c)),
        c: Or(digit, upper_char),
        user_text: Many(user_char),
        comment_text: Or(
            Many(comment_char),
            Seq(comment_text, "(", comment_text, ")", comment_text)
            ),

        semi: Seq(Many(blank), ";", Many(blank)),
        sep: Or(upper_char, blank),
        digit: Or(*ascii_digits),
        upper_char: Or(*ascii_upper),
        blank: Or(*(ascii_all - ascii_digits - ascii_upper - set("-();"))),
        user_char: Or(*(ascii_all - set(";"))),
        comment_char: Or(*(ascii_all - set("()"))),
        }

    def reduce(node):
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


    #Parser(grammar, "L Lone; P 10 10 10 20 30 30 10 30; E").parse()

    #return

    mycif = """
    L L01;
    DS 1;
    P 10 10 10 20 30 30 10 30;
    DF;
    E
    """

    mycif = """
    DS 1;
    L L01;
    P 10 10 10 20 30 30 10 30;
    DF;
    L L02;
    C 1;
    P 10 10 0 10 10 0;
    E
    """

    #mycif = """L LO1; E"""

    parser = Parser(grammar, mycif)
    cst = parser.parse()
    cst.compute_string()
    cst.descend(lambda node, depth, number: reduce(node), False)
    cst.print_dot()

if __name__ == '__main__':
    CIF()


def foo():
    sentence = Symbol("sentence")
    noun = Symbol("noun")
    verb = Symbol("verb")
    adverbs = Symbol("verb")

    extra = {}
    grammar = {
        sentence: Seq("the ", noun, verb, adverbs),
        noun: Or("cat ", "dog "),
        verb: Or("meows ", "barks "),
        adverbs: many(extra, "loudly "),
        }
    grammar.update(extra)

    string = "the dog meows loudly loudly loudly loudly "

    parser = Parser(grammar, string)
    parser.parse()

#foo()

