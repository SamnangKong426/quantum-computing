from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt

# Build a simple circuit
qc = QuantumCircuit(1, 1)
state = Statevector(qc)

# Get the Bloch sphere figure
fig = plot_bloch_multivector(state)

plt.show()
