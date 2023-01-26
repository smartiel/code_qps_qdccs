"""
A submodule that contains some basic circuits generators
"""

import numpy as np

XM = np.array([[0, 1], [1, 0]])
ZM = np.diag([1, -1])
YM = np.array([[0, -1j], [1j, 0]])
GATES = {
    "CNOT": np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]),
    "CZ": np.diag([1, 1, 1, -1]),
    "H": np.array([[1, 1], [1, -1]]) / np.sqrt(2.0),
    "RX": lambda theta: np.cos(theta / 2) * np.eye(2) - 1j * np.sin(theta / 2) * XM,
    "RY": lambda theta: np.cos(theta / 2) * np.eye(2) - 1j * np.sin(theta / 2) * YM,
    "RZ": lambda theta: np.cos(theta / 2) * np.eye(2) - 1j * np.sin(theta / 2) * ZM,
}


def generate_random_circuit(nqbits, ngates, gates=None):
    """
    Generates a random circuit
    """
    gates = gates or list(GATES.keys())
    qbits = list(range(nqbits))
    circuit = []
    for _ in range(ngates):
        gate = GATES[np.random.choice(gates)]
        if callable(gate):
            gate = gate(np.random.random() * 2 * np.pi)
        arity = int(np.log2(gate.shape[0]))
        qbs = np.random.choice(qbits, size=arity, replace=False)
        circuit.append((gate, qbs))
    return circuit
