"""
A module for tests.
If I've worked correctly, it should grab the various simulators we will code and run some tests on them.
"""
import pytest
import numpy as np


SIMULATORS = []

try:
    from qps.mps import MPS

    SIMULATORS.append(MPS)
except ImportError:
    pass


try:
    from qps.direct import Direct

    SIMULATORS.append(Direct)
except ImportError:
    pass

HADAMARD = np.array([[1, 1], [1, -1]]) / np.sqrt(2.0)
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
PAULI_X = np.array([[0, 1], [1, 0]])
ID = np.eye(2)
CONTROLED_Z = np.diag([1, 1, 1, -1])


def rotation_x(theta):
    """
    Rotation around the X axis of a qubit
    """
    return np.cos(theta / 2) * np.eye(2) - 1j * np.sin(theta / 2) * np.array([[0, 1], [1, 0]])


def rotation_z(theta):
    """
    Rotation around the Z axis of a qubit
    """
    return np.diag([np.exp(1j * theta / 2), np.exp(-1j * theta / 2)])


def get_random_lnn_circuit(dim, depth):
    """
    Generates a random Linear Nearest Neighbor circuit of fixed depth and width.
    """
    _circuit = []
    for _ in range(depth):
        for qbit in range(dim):
            _circuit.append((rotation_x(np.random.random_sample() * 2 * np.pi), [qbit]))
            _circuit.append((rotation_z(np.random.random_sample() * 2 * np.pi), [qbit]))
            _circuit.append((rotation_x(np.random.random_sample() * 2 * np.pi), [qbit]))
        for i in range(dim - 1):
            _circuit.append((CONTROLED_Z, [i, i + 1]))
    return _circuit


def get_ghz_circuit(dim):
    circuit = []
    circuit.append((HADAMARD, [0]))
    for i in range(1, dim):
        circuit.append((CNOT, [0, i]))
    return circuit


CIRCUITS = []
RESULTS = []
NAMES = []

# Some tests that only works when qubit indexes are ignored
circuit = [(HADAMARD, [0]), (CNOT, [0, 1])]
result = [("00", 1 / 2.0), ("11", 1 / 2.0)]
CIRCUITS.append(circuit)
RESULTS.append(result)
NAMES.append("simple")
# Some boring tests to check that the bit ordering is correct
for nqbits in range(2, 10):
    circuit = [(PAULI_X, [0]), (ID, [nqbits - 1])]

    result = [("1" + "0" * (nqbits - 1), 1)]
    CIRCUITS.append(circuit)
    RESULTS.append(result)
    NAMES.append(f"bitorder_n={nqbits}")

# GHZ state/Bell tests, we expect state |0...0> + |1..1> (up to normalization)
for nqbits in range(2, 20):
    circuit = [(HADAMARD, [0])]
    circuit.extend(list((CNOT, [i, i + 1]) for i in range(nqbits - 1)))
    CIRCUITS.append(circuit)
    # We will just check these two probabilities :) it should be enough :p
    result = [("0" * nqbits, 0.5), ("1" * nqbits, 0.5)]
    RESULTS.append(result)
    NAMES.append(f"ghz_n={nqbits}")

# Pure uniform state
for nqbits in range(2, 15):
    circuit = [(HADAMARD, [i]) for i in range(nqbits)]
    CIRCUITS.append(circuit)
    result = [
        (
            "".join(map(str, np.random.choice(["0", "1"], size=nqbits, replace=True))),
            1 / (1 << nqbits),
        )
        for _ in range(100)
    ]
    RESULTS.append(result)
    NAMES.append(f"uniform_distrib_n={nqbits}")

# GHZ but with non consecutive gates
for nqbits in range(2, 15):
    CIRCUITS.append(get_ghz_circuit(nqbits))
    NAMES.append(f"ghz_non_consec_{nqbits}")
    RESULTS.append([("1" * nqbits, 0.5), ("0" * nqbits, 0.5)])


@pytest.mark.parametrize("data", zip(CIRCUITS, RESULTS), ids=NAMES)
@pytest.mark.parametrize("simulator_class", SIMULATORS)
def test_strong_simulation(simulator_class: type, data):
    """
    Generic test for strong simulator. It simulates a circuit
    and compares the result to an expected vector
    """
    _circuit, expected_results = data
    _nqbits = max(max(qbits) for _, qbits in _circuit) + 1
    simulator = simulator_class(_nqbits)
    simulator.simulate_circuit(_circuit)
    for state, proba in expected_results:
        assert np.isclose(simulator.get_probability(state), proba)


@pytest.mark.parametrize("nqbits", range(2, 10))
@pytest.mark.parametrize("simulator_class", SIMULATORS)
def test_weak_simulation_ghz(simulator_class, nqbits):
    """
    Checks that sampling a Bell pair does only yield correct samples
    """
    circuit = get_ghz_circuit(nqbits)
    simulator = simulator_class(nqbits)
    simulator.simulate_circuit(circuit)
    samples = [simulator.get_sample() for _ in range(23)]
    for sample in samples:
        assert all(sample) or not any(sample)
