import streamlit as st
import pandas as pd
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# Title of the app
st.title("Qiskit Quantum Circuit Bar Chart")

# Input box for Python code (default example Qiskit code)
code = st.text_area("Enter Qiskit code here", """
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)

qc.h(0)

qc.measure([0, 1], [0, 1])

sim = AerSimulator()
compiled = transpile(qc, sim)
result = sim.run(compiled).result()
counts = result.get_counts()
""", height=600)

# Execute button
if st.button("Run Code"):
    try:
        # Create a local namespace for the executed code
        exec_globals = {}

        # Execute the user's inputted code
        exec(code, exec_globals)

        # Check if the user has defined a quantum circuit
        if 'qc' in exec_globals:
            # If they have, simulate the circuit
            sim = AerSimulator()
            compiled = transpile(exec_globals['qc'], sim)
            result = sim.run(compiled).result()
            counts = result.get_counts()

            # Convert counts dictionary to a pandas DataFrame
            counts_df = pd.DataFrame(list(counts.items()), columns=["State", "Counts"])

            # Plot the counts using Streamlit's bar_chart
            st.bar_chart(counts_df.set_index('State')['Counts'])

    except Exception as e:
        st.error(f"Error: {e}")
