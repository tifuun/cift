from dataclasses import dataclass
from collections import defaultdict
import cift as cf

def to_int(string):
    return int(string.lstrip('0') or '0')

class Transform:
    def __init__(self):
        self.next = None

    def append(self, new):
        if self.next is None:
            self.next = new
        else:
            self.next.append(new)

    def transform_point(self, x, y):
        if self.next is not None:
            x, y = self.next.transform_point(x, y)

        return x, y

    def transform_points(self, points):
        return tuple(self.transform_point(*point) for point in points)

class Rotate(Transform):
    def __init__(self, rx, ry):
        super().__init__()

        magnitude = (rx ** 2 + ry ** 2) ** (1 / 2)
        self.ux = rx / magnitude
        self.uy = ry / magnitude

    def transform_point(self, x, y):
        x, y = map(int, (
            x * self.ux - y * self.uy,
            x * self.uy + y * self.ux
            ))
        # TODO this is not correct, as far as I understand,
        # the result of a rotation in CIF does not need to be
        # quantized to the grid. So this should be float.

        if self.next is not None:
            x, y = self.next.transform_point(x, y)

        return x, y

class Translate(Transform):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

    def transform_point(self, x, y):
        x += self.x
        y += self.y

        if self.next is not None:
            x, y = self.next.transform_point(x, y)

        return x, y

@dataclass
class Frame:
    layer: str | None
    line: int
    rout_num: int | None
    transform: Transform

class Parser:
    """
    CIF Parser.
    """

    layers: cf.types.layers
    routs_lines: dict[int, list[str]]
    _stack: list[Frame]

    def __init__(self) -> None:
        self.layers = defaultdict(list)

        self._stack = [Frame(
            layer=None,
            line=0,
            rout_num=None,
            transform=Transform()
            )]

        self._this_rout = None
        self.routs_lines = {}
        self.routs_start_lines = {}

    @property
    def _frame(self):
        return self._stack[-1]

    def parse(self, what):
        if isinstance(what, str):
            return self.parse_string(what)

        raise NotImplementedError(
            "Eventually this will support paths and file objects, "
            "but for now please pass a string."
            )

    def parse_string(self, cif: str) -> None:
        for line in cif.splitlines('\n'):
            self._parse_line(line)
            self._frame.line += 1

    def _parse_line(self, line: str) -> None:

        if (match := cf.re.rout_finish.match(line)):
            self._handle_rout_finish(match)

        elif (match := cf.re.rout_start.match(line)):
            self._handle_rout_start(match)

        elif self._this_rout is not None:
            assert self._this_rout in self.routs_lines.keys()
            self.routs_lines[self._this_rout].append(line)

        elif (match := cf.re.rout_call.match(line)):
            self._handle_rout_call(match)

        elif (match := cf.re.layer.match(line)):
            self._frame.layer = match.groups()[0]

        elif (match := cf.re.box.match(line)):
            self._handle_box(match)

        elif (match := cf.re.polygon.match(line)):
            self._handle_polygon(match)

        elif line == 'E\n':
            # TODO
            pass

        else:
            raise Exception(line)

    def _traceback(self):
        return '\ncalled by\n'.join((
            f"subroutine {frame.rout_num or '<toplevel>'} "
            f"at line {frame.line} "
            for frame in reversed(self._stack)
            ))

    def _assert_layer(self):
        if self._frame.layer is None:
            raise cf.err.NoLayerError(''.join((
                "Error in ",
                self._traceback(),
                "Error: tried adding geometry before any layer was selected."
                )))

    def _handle_box(self, match):
        self._assert_layer()

        length, width, xpos, ypos = map(to_int, match.groups())

        x1 = xpos - width / 2
        y1 = ypos - length / 2
        x2 = xpos + width / 2
        y2 = ypos + length / 2

        points = (
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
            )

        points = self._frame.transform.transform_points(points)

        self.layers[self._frame.layer].append(points)

    def _handle_polygon(self, match):
        self._assert_layer()

        coords = tuple(map(to_int, cf.re.points.findall(match.groups()[0])))
        points = tuple(zip(coords[0::2], coords[1::2]))
        points = self._frame.transform.transform_points(points)

        self.layers[self._frame.layer].append(points)

    def _handle_rout_start(self, match):
        # TODO redefinition
        rout_num = to_int(match.groups()[0])

        assert len(self._stack) == 1

        if self._this_rout is not None:
            raise cf.err.RoutStartError(
                f"tried defining subroutine number {rout_num}. "
                f"before definition of routine number {self._this_rout} "
                "was terminated. "
                )

        self._this_rout = rout_num
        self.routs_lines[rout_num] = []
        self.routs_start_lines[rout_num] = self._frame.line

    def _handle_rout_finish(self, match):

        assert len(self._stack) == 1

        if self._this_rout is None:
            raise cf.err.RoutFinishError(
                f"CIF Error at line {self._this_line_no}: "
                "tried ending a subroutine definition before it was started. "
                )

        self._this_rout = None

    def _handle_rout_call(self, match):
        rout_num, rout_transform = match.groups()
        transform = Transform()
        if rout_transform:
            for match in cf.re.rout_transform.findall(rout_transform):
                kind, x, y = match
                x = to_int(x)
                y = to_int(y)
                if kind == 'T':
                    transform.append(Translate(x, y))
                elif kind == 'R':
                    transform.append(Rotate(x, y))
                else:
                    assert False

        rout_num = to_int(rout_num)

        self._stack.append(Frame(
            line=self.routs_start_lines[rout_num],
            layer=None,
            rout_num=rout_num,
            transform=transform
            ))

        for line in self.routs_lines[rout_num]:
            self._frame.line += 1
            self._parse_line(line)

        self._stack.pop()


