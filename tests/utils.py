"""
Utilities for testing
"""

class RegexTester:
    """
    Mixin for unittest.TestCase for testing regexes
    """

    def assertMatches(self, re, string, expected):
        return self.assertEqual(re.match(string).groups(), expected)

    def assertNotMatches(self, re, string):
        return self.assertIsNone(re.match(string))

