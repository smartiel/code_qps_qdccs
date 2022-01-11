"""
Implementation of a quantum circuit simulator based on tensor network contraction
"""
from .simulator import StrongSimulator, WeakSimulator


class TensorContraction(StrongSimulator, WeakSimulator):
    """
    A quantum circuit simulator based on tensor network contraction.
    """
    def __init__(self, nqbits):
        pass