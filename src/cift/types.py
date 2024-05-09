"""
Type aliases for CIFT
"""

from typing import TypeAlias

point: TypeAlias = tuple[int, int]
poly: TypeAlias = tuple[point]
polys: TypeAlias = tuple[poly]
layers: TypeAlias = dict[str, polys]

