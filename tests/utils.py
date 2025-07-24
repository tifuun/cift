"""
Utilities for testing
"""

from pprint import pprint
from sys import stderr

class PrettyEqual():
    def assertPrettyEqual(self, actual, desired):
        try:
            self.assertEqual(actual, desired)

        except AssertionError as err:
            pprint("ACTUAL: ", stream=stderr)
            pprint(actual, stream=stderr)
            pprint("DESIRED: ", stream=stderr)
            pprint(desired, stream=stderr)
            raise err

    def assertGeomsEqualStrict(self, actual, desired):
        """
        Compare geometries strictly:
        same layer order, same order of polygons
        within layer, same order of points
        within polygon
        """
        for (name_a, layer_a), (name_b, layer_b) in zip(
                actual.items(), desired.items(), strict=True):
            self.assertEqual(name_a, name_b)
            for poly_a, poly_b in zip(layer_a, layer_b, strict=True):
                for point_a, point_b in zip(poly_a, poly_b, strict=True):
                    for coord_a, coord_b in zip(point_a, point_b, strict=True):
                        self.assertAlmostEqual(coord_a, coord_b)

    def assertGeomsEqualStrictPretty(self, actual, desired):
        try:
            self.assertGeomsEqualStrict(actual, desired)
        except AssertionError as err:
            pprint("ACTUAL: ", stream=stderr)
            pprint(actual, stream=stderr)
            pprint("DESIRED: ", stream=stderr)
            pprint(desired, stream=stderr)
            raise err
