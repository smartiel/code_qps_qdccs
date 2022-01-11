"""
Implementation of a MPS-based quantum circuit simulator
"""

from .simulator import StrongSimulator, WeakSimulator


class MPS(StrongSimulator, WeakSimulator):
    """
    A quantum circuit simulator based on Matrix Product State data structure.
    """
    def __init__(self, nqbits):
        pass