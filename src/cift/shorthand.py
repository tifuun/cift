"""shorthand.py: shorthand functions for cift"""

import cift as cf

def parse(what: str):
        if isinstance(what, str):
            return parse_string(what)

        raise NotImplementedError(
            "Eventually this will support paths and file objects, "
            "but for now please pass a string."
            )

def parse_string(cifstring: str):
    parser = cf.Parser(cf.grammars.strict.grammar, cifstring)
    cst = parser.parse()
    cst.compute_string()
    monad = cf.semir.CSTMonad(cst)
    semir = cf.semir.SemIR(monad)
    semir.eval()
    layers = semir.build()
    return layers

