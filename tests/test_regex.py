"""
"""

import unittest

import cift as cf

from .utils import RegexTester

class TestRegex(unittest.TestCase, RegexTester):

    def test_regex_box(self):
        self.assertMatches(
            cf.re.box,
            "B 10 10 20 30;",
            ('10', '10', '20', '30', None, None)
            )

        self.assertMatches(
            cf.re.box,
            "BOX        10    10   20 30 ;   ",
            ('10', '10', '20', '30', None, None)
            )

        self.assertMatches(
            cf.re.box,
            "BOX        10    010   20 00030 ;   ",
            ('10', '010', '20', '00030', None, None)
            )

        self.assertMatches(
            cf.re.box,
            "B 10 10 20 30 ;",
            ('10', '10', '20', '30', None, None)
            )

        self.assertMatches(
            cf.re.box,
            "B 10 10 20 30 ;",
            ('10', '10', '20', '30', None, None)
            )

        self.assertMatches(
            cf.re.box,
            "B 10 10 20 30 10 10;",
            ('10', '10', '20', '30', '10', '10')
            )

        self.assertMatches(
            cf.re.box,
            "B 10 -10 20 30 10 -10;",
            ('10', '-10', '20', '30', '10', '-10')
            )

        self.assertNotMatches(
            cf.re.box,
            "BOOX 10 10 20 30;",
            )

        self.assertNotMatches(
            cf.re.box,
            "BOX 10 10 20 30",
            )

        self.assertNotMatches(
            cf.re.box,
            "BO 10 10 20 30;",
            )

        self.assertNotMatches(
            cf.re.box,
            "BXO 10 10 20 30;",
            )

        self.assertNotMatches(
            cf.re.box,
            "BOX10 10 20 30;",
            )

        self.assertNotMatches(
            cf.re.box,
            "BOX 10 10 30;",
            )

        self.assertNotMatches(
            cf.re.box,
            "BOX 10 10.1 10 30;",
            )

        self.assertNotMatches(
            cf.re.box,
            "BOX 10 10 30 10 10;",
            )

        self.assertNotMatches(
            cf.re.box,
            "BOX;",
            )


if __name__ == '__main__':
    unittest.main()

