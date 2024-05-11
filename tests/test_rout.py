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
            "   L Lone;\n"
            "   P 10 10 10 20 30 30 10 30;\n"
            "DF;\n"
            "L Ltwo;\n"
            "C 1;\n"
            "P 10 10 0 10 10 0;\n"
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
                        (0, 10),
                        (10, 0),
                        ),
                    ]
                },
            )

    def test_rout_deep(self):
        parser = cf.Parser(
            )
        parser.parse(
            "DS 1;\n"
            "   L Lone;\n"
            "   P 10 10 10 20 30 30 10 30;\n"
            "DF;\n"
            "DS 2;\n"
            "   L Ltwo;\n"
            "   P 20 20 0 10 10 0;\n"
            "   C 1;\n"
            "DF;\n"
            "DS 3;\n"
            "   C 1;\n"
            "   C 2;\n"
            "DF;\n"
            "C 3;\n"
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
                    ] * 2,  # <-- pay attention here
                'Ltwo': [
                    (
                        (20, 20),
                        (0, 10),
                        (10, 0),
                        ),
                    ],
                },
            )

    def test_rout_transform(self):
        parser = cf.Parser(
            )
        parser.parse(
            "DS 1 1 1;\n"
            "    L Lone;\n"
            "    P 0 0 0 10 10 0;\n"
            "DF;\n"
            "DS 2 1 1;\n"
            "    C 1 R 0 -1 T 2 3;\n"
            "DF;\n"
            "C 2;\n"
            "E\n"
            )
        # So apparently subroutine call transforms at the toplevel get
        # ignored? Is this a klayout bug/feature?
        # am I dumb?
        # Regardless, this is why this test uses two subroutines.
        self.assertEqual(
            parser.layers,
            {
                'Lone': [
                    (
                        (0 + 2, 0 + 3),
                        (10 + 2, 0 + 3),
                        (0 + 2, -10 + 3),
                        ),
                    ],
                },
            )

# TODO anti-tests


if __name__ == '__main__':
    unittest.main()

