"""
"""

import unittest

import cift as cf

from .utils import PrettyEqual

class TestPoly(unittest.TestCase, PrettyEqual):

    def test_single_poly(self):
        parser = cf.Parser(
            )
        parser.parse(
            "L Ltest;\n"
            "P 10 10 10 20 30 30 10 30;\n"
            "E\n"
            )
        self.assertPrettyEqual(
            parser.layers,
            {
                'Ltest': [
                    (
                        (10, 10),
                        (10, 20),
                        (30, 30),
                        (10, 30),
                        ),
                    ]
                },
            )

    def test_multi_poly(self):
        parser = cf.Parser(
            )
        parser.parse(
            "L Ltest;\n"
            "P 10 10 10 20 30 30 10 30;\n"
            "P 50 20 40 10 30 30 10 30;\n"
            "E\n"
            )
        self.assertPrettyEqual(
            parser.layers,
            {
                'Ltest': [
                    (
                        (10, 10),
                        (10, 20),
                        (30, 30),
                        (10, 30),
                        ),
                    (
                        (50, 20),
                        (40, 10),
                        (30, 30),
                        (10, 30),
                        ),
                    ]
                },
            )

    def test_multi_layer(self):
        parser = cf.Parser(
            )
        parser.parse(
            "L Lone;\n"
            "P 10 10 10 20 30 30 10 30;\n"
            "L Ltwo;\n"
            "P 50 20 40 10 30 30 10 30;\n"
            "L Lone;\n"
            "P 60 20 40 10 30 30 10 30;\n"
            "E\n"
            )
        self.assertPrettyEqual(
            parser.layers,
            {
                'Lone': [
                    (
                        (10, 10),
                        (10, 20),
                        (30, 30),
                        (10, 30),
                        ),
                    (
                        (60, 20),
                        (40, 10),
                        (30, 30),
                        (10, 30),
                        ),
                    ],
                'Ltwo': [
                    (
                        (50, 20),
                        (40, 10),
                        (30, 30),
                        (10, 30),
                        ),
                    ]
                },
            )

    def test_box(self):
        parser = cf.Parser(
            )
        parser.parse(
            "L Ltest;\n"
            "B 10 20 3 4;\n"
            "E\n"
            )
        self.assertPrettyEqual(
            parser.layers,
            {
                'Ltest': [
                    (
                        (-10 // 2 + 3, -20 // 2 + 4),
                        (+10 // 2 + 3, -20 // 2 + 4),
                        (+10 // 2 + 3, +20 // 2 + 4),
                        (-10 // 2 + 3, +20 // 2 + 4),
                        ),
                    ]
                },
            )

    def test_unrotated_box(self):
        parser = cf.Parser(
            )
        parser.parse(
            "L Ltest;\n"
            "B 10 20 3 4 1 0;\n"
            "E\n"
            )
        self.assertPrettyEqual(
            parser.layers,
            {
                'Ltest': [
                    (
                        (-10 // 2 + 3, -20 // 2 + 4),
                        (+10 // 2 + 3, -20 // 2 + 4),
                        (+10 // 2 + 3, +20 // 2 + 4),
                        (-10 // 2 + 3, +20 // 2 + 4),
                        ),
                    ]
                },
            )

    def test_rotated_box(self):
        parser = cf.Parser(
            )
        parser.parse(
            "L Ltest;\n"
            "B 10 20 3 4 0 -1;\n"
            "E\n"
            )
        self.assertPrettyEqual(
            parser.layers,
            {
                'Ltest': [
                    (  # Pay attention to the order here
                        (-20 // 2 + 3, +10 // 2 + 4),
                        (-20 // 2 + 3, -10 // 2 + 4),
                        (+20 // 2 + 3, -10 // 2 + 4),
                        (+20 // 2 + 3, +10 // 2 + 4),
                        ),
                    ]
                },
            )


if __name__ == '__main__':
    unittest.main()

