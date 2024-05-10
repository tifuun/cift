"""
"""

import unittest

import cift as cf

class TestPoly(unittest.TestCase):

    def test_single_poly(self):
        parser = cf.Parser(
            )
        parser.parse(
            "L Ltest;\n"
            "P 10 10 10 20 30 30 10 30;\n"
            "E\n"
            )
        self.assertEqual(
            parser.layers,
            {
                'Ltest': {
                    (
                        (10, 10),
                        (10, 20),
                        (30, 30),
                        (10, 30),
                        ),
                    }
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
        self.assertEqual(
            parser.layers,
            {
                'Ltest': {
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
                    }
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
        self.assertEqual(
            parser.layers,
            {
                'Lone': {
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
                    },
                'Ltwo': {
                    (
                        (50, 20),
                        (40, 10),
                        (30, 30),
                        (10, 30),
                        ),
                    }
                },
            )


if __name__ == '__main__':
    unittest.main()

