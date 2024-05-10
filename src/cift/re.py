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

rout_start = re.compile(
    r"^\s*"
    r"DS"
    r"\s+(-?\d+)"
    r"\s*;\s*$"
    )

rout_finish = re.compile(
    r"^\s*"
    r"DF"
    r"\s*;\s*$"
    )

rout_call = re.compile(
    r"^\s*"
    r"C(?:ALL)?"
    r"\s*(\d+)"
    r"\s*(.*)"
    r"\s*;\s*$"
    )

