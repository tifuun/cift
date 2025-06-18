

class Frame:
    pass

class Builder:
    def __init__(self):
        self.symbols
        self.layer = None

    def build(self, toplevel):
        toplevel.classify()

        assert toplevel.semtype is SemType.FILE

        for child in toplevel.toplevel_children:
            child.classify()

            self._handle_semir(child)

    def _handle_semir(self, semir):
        if semir.semtype is SemType.DEF:
            pass
        elif semir.semtype is SemType.CALL:
            pass
        elif semir.semtype is SemType.LAYER:
            self.layer = 
            pass
        elif semir.semtype is SemType.POLY:
            pass
        else:
            assert False



class Builder:

    layers: cf.types.layers

    #routs_lines: dict[int, list[str]]
    #edges: cf.types.edges
    #routs_start_lines: dict[int, int]

    def __init__(self) -> None:
        self.layers = defaultdict(list)

        #self._stack = [Frame(
        #    layer=None,
        #    line=0,
        #    rout_num=-1,
        #    transform=Transform()
        #    )]

        #self._this_rout = -1
        #self.routs_lines = {}
        #self.routs_start_lines = {}
        #self.edges = []

    #@property
    #def _frame(self) -> Frame:
    #    return self._stack[-1]

    def _traceback(self) -> str:
        return '\ncalled by\n'.join((
            f"subroutine {frame.rout_num or '<toplevel>'} "
            f"at line {frame.line} "
            for frame in reversed(self._stack)
            ))

    def _assert_layer(self) -> str:
        if self._frame.layer is None:
            raise cf.err.NoLayerError(''.join((
                "Error in ",
                self._traceback(),
                "Error: tried adding geometry before any layer was selected."
                )))

        return self._frame.layer

    def _handle_box(self, match: re.Match[str]) -> None:
        layer = self._assert_layer()

        width, height, xpos, ypos = map(to_int, match.groups()[:4])
        rot_x, rot_y = match.groups()[4:]

        x1 = -width // 2
        y1 = -height // 2
        x2 = width // 2
        y2 = height // 2

        points: cf.types.poly = (
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
            )

        if rot_x is not None:
            assert rot_y is not None
            rot_x = to_int(rot_x)
            rot_y = to_int(rot_y)
            points = Rotate(rot_x, rot_y).transform_points(points)

        points = tuple(
            (point[0] + xpos, point[1] + ypos)
            for point in points
            )

        points = self._frame.transform.transform_points(points)

        self.layers[layer].append(points)

    def _handle_polygon(self, match: re.Match['str']) -> None:
        layer = self._assert_layer()

        coords = tuple(map(to_int, cf.re.points.findall(match.groups()[0])))
        points = self._frame.transform.transform_points(
            tuple(zip(coords[0::2], coords[1::2]))
            )

        self.layers[layer].append(points)

    def _handle_rout_start(self, match: re.Match['str']) -> None:
        # TODO redefinition
        rout_num = to_int(match.groups()[0])

        assert len(self._stack) == 1

        if self._this_rout != -1:
            raise cf.err.RoutStartError(
                f"tried defining subroutine number {rout_num}. "
                f"before definition of routine number {self._this_rout} "
                "was terminated. "
                )

        self._this_rout = rout_num
        self.routs_lines[rout_num] = []
        self.routs_start_lines[rout_num] = self._frame.line

    def _handle_rout_finish(self, match: re.Match['str']) -> None:

        assert len(self._stack) == 1

        if self._this_rout == -1:
            raise cf.err.RoutFinishError(''.join((
                "Error in ",
                self._traceback(),
                "tried ending a subroutine definition before it was started. "
                )))

        self._this_rout = -1

    def _handle_rout_call(self, match: re.Match['str']) -> None:
        rout_num, rout_transform = match.groups()
        transform = Transform()
        if rout_transform:
            for kind, x, y in cf.re.rout_transform.findall(rout_transform):
                x = to_int(x)
                y = to_int(y)
                if kind == 'T':
                    transform.append(Translate(x, y))
                elif kind == 'R':
                    transform.append(Rotate(x, y))
                else:
                    assert False

        rout_num = to_int(rout_num)

        self.edges.append(
            cf.types.Edge(self._frame.rout_num, rout_num)
            )

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

