"""
Utilities for testing
"""

from pprint import pprint
from sys import stderr

class RegexTester:
    """
    Mixin for unittest.TestCase for testing regexes
    """

    def assertMatches(self, re, string, expected):
        return self.assertEqual(re.match(string).groups(), expected)

    def assertNotMatches(self, re, string):
        return self.assertIsNone(re.match(string))


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

