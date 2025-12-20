import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector, circuit_drawer, plot_histogram
from qiskit_aer import AerSimulator


qc = QuantumCircuit(1, 1)
qc.x(0)
qc.y(0)
state = Statevector(qc)
bloch = plot_bloch_multivector(state)
plt.show()
circuit = circuit_drawer(qc, output='mpl')
plt.show()
qc.measure(0, 0)
backend = AerSimulator()
tqc = transpile(qc, backend)
job = backend.run(tqc, shots=1024)
result = job.result()
counts = result.get_counts()

plot_histogram(counts)
