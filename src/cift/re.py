"""
Compiled regexes for parsing CIF files
"""

import re

box = re.compile(
    r"^\s*"
    r"B(?:OX)?"
    r"\s+(-?\d+)"
    r"\s+(-?\d+)"
    r"\s+(-?\d+)"
    r"\s+(-?\d+)"
    r"(?:\s+(-?\d+)\s+(-?\d+))?"
    r"\s*;\s*$"
    )

polygon = re.compile(
    r"^\s*"
    r"P(?:OLYGON)?"
    r"((?:\s+-?\d+\s+-?\d+)+)"
    r"\s*;\s*$"
    )

layer = re.compile(
    r"^\s*"
    r"L(?:AYER)?"
    r"\s+(\w+)"
    r"\s*;\s*$"
    )

points = re.compile(r"-?\d+")

