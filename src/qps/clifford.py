
import numpy as np

class Tableau:
    """
    A class representing the stabilizer group of a stabilizer quantum state.
    """
    def __init__(self, dim):
        # TODO: We want to initialize the Tableau to the stabilizer group of |0...0>
        pass


    def hadamard(self, qbit):
        """
        Conjugates the group by a H gate
        """
        # TODO :)

    def phase(self, qbit):
        """
        Conjugates the group by a S gate
        """
        # TODO :)


    def cnot(self, control, target):
        """
        Conjugates the group by a CNOT gate
        """
        pass
        # TODO :)


    def measure(self, qbit):
        """
        Measures a qbit.
        """
        # TODO :)

    def get_circuit(self):
        """
        Generate a circuit that prepares the stabilizer state.
        """
        # TODO :)




