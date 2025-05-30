
ascii_chars = set(map(chr, range(128)))

class Symbol:
    def __init__(self, name = None):
        self.name = name

    def __repr__(self):
        return f"<Symbol {self.name}>"

class _SingleWrapper:
    def __init__(self, what):
        self.what = what

class _TupleWrapper:
    def __init__(self, *what):
        self.what = what

class Seq(_TupleWrapper):
    pass

class Or(_TupleWrapper):
    pass

class Maybe(_SingleWrapper):
    pass

class Many(_SingleWrapper):
    pass

class CSTNode:
    def __init__(self, symbol, children):
        self.symbol = symbol
        self.children = children
        if True in self.children:
            assert False
        if False in self.children:
            assert False

    def __repr__(self):
        return f"<CSTNode {self.symbol}>"

    def print(self, depth = 0):
        print(" " * depth, self)
        for child in self.children:
            if isinstance(child, type(self)):
                child.print(depth + 1)
            else:
                print(child)

class Foundit:
    def __bool__(self):
        return True
foundit = Foundit()

class Parser:
    def __init__(self, grammar, string):
        self.grammar = grammar
        self.string = string

        self.index = 0
        self.tree = None

    def parse(self, symbol = None):

        if symbol is None:
            symbol = tuple(self.grammar.keys())[0]

        self.tree = CSTNode(None, [])

        try:
            result = self._parse(symbol, self.tree)
        except ValueError:
            pass
        
        print(f"Huh???, {result}")

        return self.tree

    def _parse(self, symbol, node):
        
        if isinstance(symbol, Symbol):
            mark = self.index

            child = CSTNode(symbol, [])
            result = self._parse(self.grammar[symbol], child)

            if result:
                node.children.append(child)
            else:
                self.index = mark

            return result

        elif isinstance(symbol, Seq):
            mark = self.index

            results = []
            children = []
            for elem in symbol.what:
                children.append(CSTNode(f"From seq! {elem}", []))
                #results.append(self._parse(elem, children[-1]))
                results.append(self._parse(elem, node))

            if all(results):
                node.children.extend(children)
                return True

            self.index = mark
            print('bt a')
            return False


        elif isinstance(symbol, Or):

            for elem in symbol.what:

                child = CSTNode("From or!", [])
                mark = self.index

                result = self._parse(elem, node)

                if result:
                    node.children.extend(child.children)
                    return True

                else:
                    self.index = mark

            print('bt a')
            return False

        elif isinstance(symbol, Maybe):

            child = CSTNode("From maybe!", [])

            if self.is_consumed():
                return True

            mark = self.index

            result = self._parse(symbol.what, node)

            if result:
                node.children.extend(child.children)
            else:
                self.index = mark

            return True

        elif isinstance(symbol, Many):

            if self.is_consumed():
                return True

            while True:
                child = CSTNode("from many!", [])
                mark = self.index

                result = self._parse(symbol.what, node)

                if result:
                    node.children.extend(child.children)
                else:
                    self.index = mark
                    break

                if self.is_consumed():
                    return True

            return True

        elif isinstance(symbol, str):
            result = self.try_consume(symbol)
            if result:
                node.children.append(symbol)
            return result

        assert False, type(symbol)

    def try_consume(self, symbol):
        if self.index > len(self.string):
            assert False

        if self.index == len(self.string):
            print(f'foundit, {symbol}, {len(symbol)}')
            return len(symbol) == 0

        if not symbol:
            return True

        if self.string[self.index:].startswith(symbol):
            self.index += len(symbol)
            print("Ate ", symbol)

            return True


        return False

    def is_consumed(self):
        return self.index >= len(self.string)

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
        def_finish_command: Seq("S", Many(blank), "F"),
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


    #Parser(grammar, "L Lone; P 10 10 10 20 30 30 10 30; E").parse()

    #return

    mycif = """
    DS 1;
    L Lone;
    P 10 10 10 20 30 30 10 30;
    DF;
    L Ltwo;
    C 1;
    P 10 10 0 10 10 0;
    E
    """

    mycif = """L Lone; E"""

    parser = Parser(grammar, mycif)
    cst = parser.parse()
    cst.print()

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

