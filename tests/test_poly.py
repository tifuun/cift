"""
"""

import unittest

import cift as cf

from .utils import PrettyEqual

class TestPoly(unittest.TestCase, PrettyEqual):

    def test_single_poly(self):
        layers = cf.parse(
            "L LFOO;\n"
            "P 10 10 10 20 30 30 10 30;\n"
            "E\n"
            )
        self.assertPrettyEqual(
            layers,
            {
                'LFOO': [
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
        layers = cf.parse(
            "L LFOO;\n"
            "P 10 10 10 20 30 30 10 30;\n"
            "P 50 20 40 10 30 30 10 30;\n"
            "E\n"
            )
        self.assertPrettyEqual(
            layers,
            {
                'LFOO': [
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
        layers = cf.parse(
            "L LONE;\n"
            "P 10 10 10 20 30 30 10 30;\n"
            "L LTWO;\n"
            "P 50 20 40 10 30 30 10 30;\n"
            "L LONE;\n"
            "P 60 20 40 10 30 30 10 30;\n"
            "E\n"
            )
        self.assertPrettyEqual(
            layers,
            {
                'LONE': [
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
                'LTWO': [
                    (
                        (50, 20),
                        (40, 10),
                        (30, 30),
                        (10, 30),
                        ),
                    ]
                },
            )

    #def test_box(self):
    #    layers = cf.parse(
    #        "L TEST;\n"
    #        "B 10 20 3 4;\n"
    #        "E\n"
    #        )
    #    self.assertPrettyEqual(
    #        layers,
    #        {
    #            'TEST': [
    #                (
    #                    (-10 // 2 + 3, -20 // 2 + 4),
    #                    (+10 // 2 + 3, -20 // 2 + 4),
    #                    (+10 // 2 + 3, +20 // 2 + 4),
    #                    (-10 // 2 + 3, +20 // 2 + 4),
    #                    ),
    #                ]
    #            },
    #        )

    #def test_unrotated_box(self):
    #    layers = cf.parse(
    #        "L TEST;\n"
    #        "B 10 20 3 4 1 0;\n"
    #        "E\n"
    #        )
    #    self.assertPrettyEqual(
    #        layers,
    #        {
    #            'TEST': [
    #                (
    #                    (-10 // 2 + 3, -20 // 2 + 4),
    #                    (+10 // 2 + 3, -20 // 2 + 4),
    #                    (+10 // 2 + 3, +20 // 2 + 4),
    #                    (-10 // 2 + 3, +20 // 2 + 4),
    #                    ),
    #                ]
    #            },
    #        )

    #def test_rotated_box(self):
    #    layers = parser.parse(
    #        "L TEST;\n"
    #        "B 10 20 3 4 0 -1;\n"
    #        "E\n"
    #        )
    #    self.assertPrettyEqual(
    #        layers,
    #        {
    #            'LEST': [
    #                (  # Pay attention to the order here
    #                    (-20 // 2 + 3, +10 // 2 + 4),
    #                    (-20 // 2 + 3, -10 // 2 + 4),
    #                    (+20 // 2 + 3, -10 // 2 + 4),
    #                    (+20 // 2 + 3, +10 // 2 + 4),
    #                    ),
    #                ]
    #            },
    #        )


if __name__ == '__main__':
    unittest.main()

