"""
Main interface for simulators.
"""
import abc


class Simulator(abc.ABC):
    """
    Interface for a basic simulator. At this stage, its just a black box that eats
    gates and does stuff with them.
    """

    @abc.abstractmethod
    def simulate_gate(self, gate, qubits):
        """
        Simulates a single gate
        """

    def simulate_circuit(self, circuit):
        """
        Simulates a sequence of gates
        """
        for gate, qubits in circuit:
            self.simulate_gate(gate, qubits)


class StrongSimulator(Simulator, abc.ABC):
    """
    This class describes the basic interface of a simulator.
    It has two abstract methods:
    - simulate_gate(...): updates the internal representation of the simulator
        to account for a new gate
    - get_state(...)
    """

    @abc.abstractmethod
    def get_probability(self, classical_state):
        """
        Returns a numpy array describing the current state vector
        """

    def strongly_simulate_circuit(self, circuit, classical_state):
        """
        Simulates a complete circuit and return the final state of the system
        """
        self.simulate_circuit(circuit)
        return self.get_probability(classical_state)


class WeakSimulator(Simulator, abc.ABC):
    """
    This class describes the basic interface of a simulator.
    It has two abstract methods:
    - simulate_gate(...): updates the internal representation of the simulator
        to account for a new gate
    - get_state(...)
    """

    @abc.abstractmethod
    def get_sample(self):
        """
        Produce a sample
        """

    def weakly_simulate_circuit(self, circuit: list, nbsamples: int):
        """
        Weakly simulates a quantum circuit.

        Paramters:
            circuit (list): a list of pairs (gate, qubits)
            nbsamples (int): the number of samples to draw

        Return:
            list: a list of bitstrings
        """
        self.simulate_circuit(circuit)
        return [self.get_sample() for _ in range(nbsamples)]
