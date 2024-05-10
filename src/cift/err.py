"""
Errors for CIFT
"""

class CIFError(Exception):
    """
    Generic CIF parsing error
    """

class NoLayerError(CIFError):
    """
    Tried adding geometry before any layer was specified
    """

