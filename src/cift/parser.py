from collections import defaultdict
import cift as cf

def to_int(string):
    return int(string.lstrip('0'))

class Parser:
    """
    CIF Parser.
    """

    layers: cf.types.layers

    def __init__(self) -> None:
        self.layers = defaultdict(set)

        self._this_layer = None
        self._this_rout = None
        self._this_line_no = None

    def parse(self, what):
        if isinstance(what, str):
            return self.parse_string(what)

        raise NotImplementedError(
            "Eventually this will support paths and file objects, "
            "but for now please pass a string."
            )

    def parse_string(self, cif: str) -> None:
        for self._this_line_no, line in enumerate(cif.splitlines('\n')):

            if (match := cf.re.layer.match(line)):
                self._this_layer = match.groups()[0]

            elif (match := cf.re.box.match(line)):
                self._handle_box(match)

            elif (match := cf.re.polygon.match(line)):
                self._handle_polygon(match)

    def _assert_layer(self):
        if self._this_layer is None:
            raise cf.err.NoLayerError(
                f"CIF Error at line {self._this_line_no}: "
                "tried adding geometry before any layer was selected."
                )

    def _handle_box(self, match):
        self._assert_layer()

        length, width, xpos, ypos = map(to_int, match.groups())

        x1 = xpos - width / 2
        y1 = ypos - length / 2
        x2 = xpos + width / 2
        y2 = ypos + length / 2

        self.layers[self._this_layer].add((
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
            ))

    def _handle_polygon(self, match):
        self._assert_layer()

        coords = tuple(map(to_int, cf.re.points.findall(match.groups()[0])))
        points = tuple(zip(coords[0::2], coords[1::2]))

        self.layers[self._this_layer].add(points)


