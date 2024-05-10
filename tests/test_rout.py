"""
"""

import unittest

import cift as cf

class TestRout(unittest.TestCase):

    def test_rout_single(self):
        parser = cf.Parser(
            )
        parser.parse(
            "DS 1;\n"
            "   L Ltest;\n"
            "   P 10 10 10 20 30 30 10 30;\n"
            "DF;\n"
            "C 1;\n"
            "E\n"
            )
        self.assertEqual(
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

    def test_rout_layers(self):
        parser = cf.Parser(
            )
        parser.parse(
            "DS 1;\n"
            "   P 10 10 10 20 30 30 10 30;\n"
            "DF;\n"
            "L Lone;\n"
            "C 1;\n"
            "L Ltwo;\n"
            "C 1;\n"
            "E\n"
            )
        self.assertEqual(
            parser.layers,
            {
                'Lone': [
                    (
                        (10, 10),
                        (10, 20),
                        (30, 30),
                        (10, 30),
                        ),
                    ],
                'Ltwo': [
                    (
                        (10, 10),
                        (10, 20),
                        (30, 30),
                        (10, 30),
                        ),
                    ]
                },
            )

    def test_rout_deep(self):
        parser = cf.Parser(
            )
        parser.parse(
            "DS 1;\n"
            "   L Lesp;\n"
            "   P 10 10 10 20 30 30 10 30;\n"
            "DF;\n"
            "DS 2;\n"
            "   P 20 20 0 10 10 0;\n"
            "   C 1;\n"
            "DF;\n"
            "DS 3;\n"
            "   C 1;\n"
            "   C 2;\n"
            "DF;\n"
            "L Lone;\n"
            "C 3;\n"
            "L Ltwo;\n"
            "C 3;\n"
            "E\n"
            )
        self.assertEqual(
            parser.layers,
            {
                'Lesp': [
                    (
                        (10, 10),
                        (10, 20),
                        (30, 30),
                        (10, 30),
                        ),
                    ] * 4,  # <-- pay attention here
                'Lone': [
                    (
                        (20, 20),
                        (0, 10),
                        (10, 0),
                        ),
                    ],
                'Ltwo': [
                    (
                        (20, 20),
                        (0, 10),
                        (10, 0),
                        ),
                    ],
                },
            )

# TODO anti-tests


if __name__ == '__main__':
    unittest.main()

