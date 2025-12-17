import streamlit as st
import pandas as pd
from qiskit import transpile
from qiskit_aer import AerSimulator

counts_df = pd.DataFrame(columns=["State", "Counts"])


def run_sim(code: str) -> dict:
    exec_globals = {}
    exec(code, exec_globals)

    if "qc" in exec_globals:
        sim = AerSimulator()
        compiled = transpile(exec_globals["qc"], sim)
        result = sim.run(compiled).result()
        counts = result.get_counts()
        return counts
    return {}


@st.fragment(run_every="1s")
def update_code():
    if "code" not in st.session_state:
        st.session_state.code = ""
        
    query_params = st.query_params
    code = query_params.get("code", "")
    if code != st.session_state.get("code", ""):
        st.session_state.code = code
        st.rerun()


def qiskit_sim_ui():
    code = st.session_state.code
    with st.container():
        with st.container(horizontal=True, vertical_alignment="bottom"):
            st.subheader("Qiskit Python Generation")
            st.space()
            button = st.empty()

        st.code(
            code,
            language="python",
            line_numbers=True,
            wrap_lines=True,
            height="stretch",
        )

        global counts_df

        if button.button("Run Code"):
            try:
                counts = run_sim(code)
                counts_df = pd.DataFrame(
                    list(counts.items()), columns=["State", "Counts"]
                )

            except Exception as e:
                st.error(f"Error: {e}")


def qiskit_bar_chart():
    global counts_df
    with st.container(border=True):
        st.subheader("Histogram")
        st.bar_chart(counts_df.set_index("State")["Counts"])
