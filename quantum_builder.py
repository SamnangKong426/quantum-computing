import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import circuit_drawer, plot_histogram
from qiskit_aer import AerSimulator
from io import BytesIO
import base64
import matplotlib.pyplot as plt

# --- APP TITLE ---
st.title("Interactive Quantum Circuit Builder + Simulator (Qiskit)")

# --- SESSION STATE INITIALIZATION ---
if "qc" not in st.session_state:
    num_qubits = st.number_input("Choose number of qubits", 1, 10, 2)
    st.session_state.qc = QuantumCircuit(num_qubits, num_qubits)

qc = st.session_state.qc

# --- UI CONTROLS ---
gate = st.selectbox("Select a quantum gate:", ["H", "X", "Y", "Z", "CX", "CZ", "Measure"])
target = st.number_input("Target qubit:", 0, qc.num_qubits - 1, 0)

control = None
if gate in ["CX", "CZ"]:
    control = st.number_input("Control qubit:", 0, qc.num_qubits - 1, 0)

if st.button("Add Gate"):
    if gate == "H":
        qc.h(target)
    elif gate == "X":
        qc.x(target)
    elif gate == "Y":
        qc.y(target)
    elif gate == "Z":
        qc.z(target)
    elif gate == "CX":
        qc.cx(control, target)
    elif gate == "CZ":
        qc.cz(control, target)
    elif gate == "Measure":
        qc.measure(target, target)

# --- DRAW CIRCUIT ---
st.subheader("Current Quantum Circuit")

img = circuit_drawer(qc, output="mpl")
buf = BytesIO()
img.savefig(buf, format="png")
buf.seek(0)
encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
st.image(f"data:image/png;base64,{encoded}")

# --- SIMULATION ---
st.subheader("Run Simulation")

if st.button("Simulate Circuit"):
    sim = AerSimulator()
    compiled = transpile(qc, sim)
    result = sim.run(compiled).result()
    counts = result.get_counts()

    st.write("### Measurement Counts")
    st.json(counts)

    # Histogram
    st.write("### Histogram")
    fig = plot_histogram(counts)
    st.pyplot(fig)

# --- RESET BUTTON ---
if st.button("Reset circuit"):
    st.session_state.qc = QuantumCircuit(qc.num_qubits, qc.num_qubits)
    st.experimental_rerun()
