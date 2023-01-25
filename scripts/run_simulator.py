## a simple script that you can modify to debug/test your simulators
import numpy as np
from qps.direct import Direct
from qps.circuits import generate_random_circuit, GATES

# Run a random circuit
circuit = generate_random_circuit(10, 100)
simulator = Direct(10)
simulator.simulate_circuit(circuit)
print(simulator.statevector)

# Run a layer of H gates
circuit = generate_random_circuit(10, 100)
simulator = Direct()
for i in range(10):
    simulator.simulate_gate(GATES["H"], [i])
print(simulator.statevector)
