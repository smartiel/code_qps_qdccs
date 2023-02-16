"""
Implementation of a quantum circuit simulator based on tensor network contraction
"""
import numpy as np
import networkx as nx
import itertools
from .simulator import StrongSimulator, WeakSimulator
import opt_einsum as oe


class TensorNetwork(nx.Graph):
    """
    A class describing a tensor network: i.e. a collection of tensors and tensordot operations.
    """

    def __init__(self):
        self.node_count = 0
        self.edge_generator = map(oe.get_symbol, itertools.count())
        super().__init__()

    def add_tensor(self, tensor):
        """
        Adds a new tensor to the network.
        The tensor is not connected to any other tensor, all its legs are dangling

        The number of "legs" of the tensor is deduced from its shape
        E.g: a tensor with shape (2, 3, 2) has 3 legs

        """
        e_labels = [next(self.edge_generator) for _ in range(len(tensor.shape))]
        self.add_node(self.node_count, tensor=tensor, e_labels=e_labels)
        self.node_count += 1
        return self.node_count - 1

    def add_tensordot(self, tindex1: int, tindex2: int, lindex1: int, lindex2: int):
        """
        Add an edge/a tensordot to the network
        """
        assert (
            self.nodes[tindex1]["tensor"].shape[lindex1] == self.nodes[tindex2]["tensor"].shape[lindex2]
        ), "Shape mismatch: can't dot two legs with different width"
        label = self.nodes[tindex1]["e_labels"][lindex1]
        self.nodes[tindex2]["e_labels"][lindex2] = label
        self.add_edge(tindex1, tindex2)

    def get_einsum_expression(self):
        """
        Get all the tensordot operations as an einsum expression
        """
        einsum_string = ",".join("".join(data["e_labels"]) for _, data in self.nodes(data=True))
        return einsum_string + "->"

    def get_tensors(self):
        """
        Get the list of all tensors in the network
        """
        return [data["tensor"] for _, data in self.nodes(data=True)]

    def find_order(self):
        """
        Returns a contraction order as a list of pairs of tensors.

        You should use:
        - nx.algorithms.approximation.treewidth_min_degree to compute a decent tree decomposition of the graph
        - you should then implement the algorithm seen during the lecture that pops the decomposition into a contraction order

        BONUS: implement an EXACT tree decomposition solver.
        You can google "quickbb" which is a branch and bound algorithm with an available python implementation.
        """
        treewidth, tree_dec = nx.algorithms.approximation.treewidth_min_degree(nx.line_graph(self))
        return edge_order_to_path(decomposition_to_order(tree_dec), self.order())

    def contract(self):
        """Contracts the network via opt_einsum and find_order"""
        order = self.find_order()
        return oe.contract(self.get_einsum_expression(), *self.get_tensors(), optimize=order)


def _find_in_list(elem, positions):
    for i, bucket in enumerate(positions):
        if elem in bucket:
            return i


def edge_order_to_path(order, ninit):
    positions = [{i} for i in range(ninit)]
    path = []
    for a, b in order:
        true_a = _find_in_list(a, positions)
        true_b = _find_in_list(b, positions)
        if true_a == true_b:
            # Skipping, this is a self loop
            continue
        path.append((true_a, true_b))
        new_bucket = positions[true_a] | positions[true_b]
        positions.pop(max(true_a, true_b))
        positions.pop(min(true_a, true_b))
        positions.append(new_bucket)
    return path


def decomposition_to_order(tree_decomposition):
    """
    TODO: implement the algorithm of the lecture
    """


KET_0 = np.array([1, 0], dtype=np.complex128)
KET_1 = np.array([0, 1], dtype=np.complex128)
EMPTY = np.zeros((2,))


class TensorContraction(StrongSimulator, WeakSimulator):
    """
    A quantum circuit simulator based on tensor network contraction.
    """

    def __init__(self, nqbits):
        self.network = TensorNetwork()
        self.wires = [(self.network.add_tensor(KET_0), 0) for _ in range(nqbits)]
        self.end_projectors = None
        self.order = None

    def simulate_gate(self, gate, qubits):
        """TODO : add the gate to the network"""
        tensorindex, legindex = self.wires[qubits[0]]

    def get_probability(self, classical_state):
        """TODO contract the network"""

    def get_sample(self):
        return super().get_sample()
