"""
Compiled regexes for parsing CIF files
"""

import re

box = re.compile(
    r"^\s"
    r"*B(?:OX)?"
    r"\s+(-?\d+)"
    r"\s+(-?\d+)"
    r"\s+(-?\d+)"
    r"\s+(-?\d+)"
    r"(?:\s+(-?\d+)\s+(-?\d+))?"
    r"\s?;\s*$"
    )

