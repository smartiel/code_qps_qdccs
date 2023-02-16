from qps.tensor import TensorNetwork
import numpy as np

G = TensorNetwork()
print(G)

ket_0 = np.array([1, 0])

first_tensor = G.add_tensor(ket_0)
print(G)
h = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
second_tensor = G.add_tensor(h)
print(G)

G.add_tensordot(first_tensor, second_tensor, 0, 1)
print(G)
