import streamlit as st
import pandas as pd
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

counts_df = pd.DataFrame(columns=["State", "Counts"])

def run_sim(code: str) -> dict:
    # Create a local namespace for the executed code
    exec_globals = {}

    # Execute the user's inputted code
    exec(code, exec_globals)

    if 'qc' in exec_globals:
        sim = AerSimulator()
        compiled = transpile(exec_globals['qc'], sim)
        result = sim.run(compiled).result()
        counts = result.get_counts()
        return counts
    return {}

def qiskit_sim_ui():
    code = """
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)

qc.h(0)

qc.measure([0, 1], [0, 1])

sim = AerSimulator()
compiled = transpile(qc, sim)
result = sim.run(compiled).result()
counts = result.get_counts()
"""

    # st.text_area("Enter Qiskit code here", code, height=500)
    col1, col2 = st.columns(2, vertical_alignment="center")
    with col1:
        st.write("Qiskit Python")
    with col2:
        button = st.empty()

    st.code(code, language='python',line_numbers=True, wrap_lines=True, width="content", height="content")

    global counts_df
    
    if button.button("Run Code"):
        try:
            counts = run_sim(code)
            counts_df = pd.DataFrame(list(counts.items()), columns=["State", "Counts"])

        except Exception as e:
            st.error(f"Error: {e}")

def qiskit_bar_chart():
    global counts_df
    st.bar_chart(counts_df.set_index('State')['Counts'])


