import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector, circuit_drawer, plot_histogram
from qiskit_aer import AerSimulator


# Initialize quantum and classical registers
qc = QuantumCircuit(2, 2)

# Apply single-qubit H gate
qc.h(0)

# Apply two-qubit CX gate
qc.cx(0, 1)

# Add visual barrier for circuit optimization
qc.barrier()

# Visualize state on Bloch Sphere
state = Statevector(qc)
bloch = plot_bloch_multivector(state)
plt.show()

# Map qubit [0,1] to classical bit [0,1]
qc.measure([0,1], [0,1])
circuit = circuit_drawer(qc, output='mpl')
plt.show()

# Run simulation using Aer backend
backend = AerSimulator()
tqc = transpile(qc, backend)
job = backend.run(tqc, shots=1024)
counts = job.result().get_counts()
histogram = plot_histogram(counts)
plt.show()