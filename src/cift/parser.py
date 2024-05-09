from collections import defaultdict
import cift as cf

class Parser:
    """
    CIF Parser.
    """

    layers: cf.types.layers

    def __init__(self) -> None:
        self.layers = defaultdict(list)

    def parse(self, what):
        if isinstance(what, str):
            return self.parse_string(what)

        raise NotImplementedError(
            "Eventually this will support paths and file objects, "
            "but for now please pass a string."
            )

    def parse_string(self, cif: str) -> None:
        pass

