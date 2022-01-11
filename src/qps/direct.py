"""
Implementation of a naive quantum circuit simulator
"""
from .simulator import StrongSimulator, WeakSimulator


class Direct(StrongSimulator, WeakSimulator):
    """
    A naive quantum circuit simulator based on matrix-vector multiplication.
    """
    def __init__(self, nqbits):
        pass
