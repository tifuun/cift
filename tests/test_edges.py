"""
"""

import unittest

import cift as cf

class TestEdges(unittest.TestCase):

    def test_edges(self):
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
            len(set(parser.edges)),
            len(parser.edges)
            )

        self.assertEqual(
            set(parser.edges),
            {
                (-1, 3),
                (3, 1),
                (3, 2),
                (2, 1),
                },
            )


if __name__ == '__main__':
    unittest.main()

