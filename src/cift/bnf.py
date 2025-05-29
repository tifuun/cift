
ascii_chars = set(map(chr, range(128)))

class Symbol:
    pass

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

class Parser:
    def __init__(self, grammar, string):
        self.grammar = grammar
        self.string = string

        self.index = 0

    def parse(self, symbol = None, depth = 40):
        if self.index >= len(self.string):
            raise ValueError("End!")

        if symbol is None:
            symbol = self.grammar[tuple(self.grammar.keys())[0]]

        if isinstance(symbol, Seq):
            mark = self.index

            results = [self.parse(elem, depth - 1) for elem in symbol.what]

            if all(results):
                return True

            self.index = mark
            return False

        elif isinstance(symbol, Or):
            mark = self.index

            results = [self.parse(elem, depth - 1) for elem in symbol.what]

            if any(results):
                return True

            self.index = mark
            print("backtrack")
            return False

        elif isinstance(symbol, Maybe):
            self.parse(symbol.what)
            return True

        elif isinstance(symbol, Many):
            while (self.parse(symbol.what)):
                pass
            return True

        elif isinstance(symbol, Symbol):
            return self.parse(self.grammar[symbol], depth - 1)

        elif isinstance(symbol, str):
            if not symbol:
                #print(" " * depth, "String!", symbol)
                return True
            return self.try_consume(symbol)

        assert False, type(symbol)

    def try_consume(self, symbol):
        if self.string[self.index:].startswith(symbol):
            self.index += len(symbol)
            print("Ate ", symbol)
            return True
        #print("didnt Ate ", symbol)
        return False

def CIF():
    ascii_all = set(map(chr, range(128)))
    ascii_digits = set("0123456789")
    ascii_upper = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    cif_file = Symbol()
    command = Symbol()
    prim_command = Symbol()
    polygon_command = Symbol()
    box_command = Symbol()
    round_flash_command = Symbol()
    wire_command = Symbol()
    layer_command = Symbol()
    def_start_command = Symbol()
    def_finish_command = Symbol()
    def_delete_command = Symbol()
    call_command = Symbol()
    user_extension_command = Symbol()
    comment_command = Symbol()
    end_command = Symbol()

    transformation = Symbol()

    path = Symbol()
    point = Symbol()

    sinteger = Symbol()
    integer = Symbol()
    integer_d = Symbol()
    shortname = Symbol()
    c = Symbol()
    user_text = Symbol()
    comment_text = Symbol()

    semi = Symbol()
    sep = Symbol()
    digit = Symbol()
    upper_char = Symbol()
    blank = Symbol()
    user_char = Symbol()
    comment_char = Symbol()

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

    parser = Parser(grammar, mycif)
    parser.parse()

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

