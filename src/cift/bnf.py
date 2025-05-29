
ascii_chars = set(map(chr, range(128)))

class Symbol:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Symbol {self.name}"

class Container:
    def __init__(self, *args):
        self.data = args

    def __iter__(self):
        return iter(self.data)

class Seq(Container):
    pass

class Or(Container):
    pass

#def many(grammar, what):
#    #return Or("", what, Seq(what, what))
#    sym = Symbol("foo")
#    #new = Or(Seq(what, sym), what, "")
#    new = Or("", what, Seq(what, sym))
#    grammar[sym] = new
#    return sym

class many:
    def __init__(self, _, what):
        self.what = what

def maybe(what):
    return Or("", what)

class Parser:
    def __init__(self, grammar, string):
        self.grammar = grammar
        self.string = string

        self.index_mark = 0
        self.index = 0

    def parse(self, symbol = None, depth = 40):
        #print(self.string)
        if self.index >= len(self.string):
            raise ValueError("End!")

        #if depth == 0:
        #    return False

        if symbol is None:
            symbol = self.grammar[tuple(self.grammar.keys())[0]]
            #print(" " * depth, "Auto", tuple(self.grammar.keys())[0])

        if isinstance(symbol, Seq):
            #print(" " * depth, "Sequence!", symbol)
            mark = self.index

            results = [self.parse(elem, depth - 1) for elem in symbol]

            if all(results):
                return True

            self.index = mark
            print("backtrack")
            return False

        elif isinstance(symbol, Or):
            #print(" " * depth, "Or!", symbol)
            mark = self.index

            #for elem in symbol:
            #    if self.parse(elem, depth - 1):
            #        return True
            results = [self.parse(elem, depth - 1) for elem in symbol]

            if any(results):
                return True

            self.index = mark
            print("backtrack")
            return False

        elif isinstance(symbol, many):
            while (self.parse(symbol.what)):
                pass
            return True

        elif isinstance(symbol, Symbol):
            #print(" " * depth, "Symbol!", symbol)
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

    def back(self):
        self.index = self.index_mark

    def mark(self):
        self.index_mark = self.index

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

    extra = {}
    grammar = {
        cif_file: Seq(
            many(extra, 
                Seq(many(extra, blank), maybe(command), semi)
                ),
            end_command,
            many(extra, blank)
            ),

        command: Or(
            prim_command,
            def_delete_command,
            Seq(
                def_start_command,
                semi,
                many(extra, 
                    Seq(
                        many(extra, blank),
                        maybe(prim_command),
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
            maybe(Seq(sep, point)),
            ),
        round_flash_command: Seq("R", integer, sep, point),
        wire_command: Seq("W", integer, sep, path),
        layer_command: Seq("L", many(extra, blank), shortname),
        def_start_command: Seq(
            "D", many(extra, blank), "S", integer,
            maybe(Seq(sep, integer, sep, integer))
            ),
        def_finish_command: Seq("S", many(extra, blank), "F"),
        def_delete_command: Seq("D", many(extra, blank), "D", integer),
        call_command: Seq("C", integer, transformation),
        user_extension_command: Seq(digit, user_text),
        comment_command: Seq("(", comment_text, ")"),
        end_command: "E",

        transformation: many(extra, 
            Seq(
                many(extra, blank),
                Or(
                    Seq("T", point),
                    Seq("M", many(extra, blank), "X"),
                    Seq("M", many(extra, blank), "Y"),
                    Seq("R", point),
                    )
                )
            ),

        path: Seq(point, many(extra, Seq(sep, point))),
        point: Seq(sinteger, sep, sinteger),

        sinteger: Seq(many(extra, sep), maybe("-"), integer_d),
        integer: Seq(many(extra, sep), integer_d),
        integer_d: Seq(digit, many(extra, digit)),

        shortname: Seq(c, maybe(c), maybe(c), maybe(c)),
        c: Or(digit, upper_char),
        user_text: many(extra, user_char),
        comment_text: Or(
            many(extra, comment_char),
            Seq(comment_text, "(", comment_text, ")", comment_text)
            ),

        semi: Seq(many(extra, blank), ";", many(extra, blank)),
        sep: Or(upper_char, blank),
        digit: Or(*ascii_digits),
        upper_char: Or(*ascii_upper),
        blank: Or(*(ascii_all - ascii_digits - ascii_upper - set("-();"))),
        user_char: Or(*(ascii_all - set(";"))),
        comment_char: Or(*(ascii_all - set("()"))),
        }

    grammar.update(extra)



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

