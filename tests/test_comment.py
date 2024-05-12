"""
"""

import unittest

import cift as cf

class TestComment(unittest.TestCase):

    def test_comment(self):
        parser = cf.Parser(
            )
        parser.parse(
            "L Ltest;\n"
            "(this is a comment)\n"
            "P 10 10 10 20 30 30 10 30;\n"
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


if __name__ == '__main__':
    unittest.main()

