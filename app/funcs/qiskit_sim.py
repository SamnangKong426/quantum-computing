import io
import sys
import streamlit as st
import pandas as pd
from qiskit import transpile
from qiskit_aer import AerSimulator

if "counts_df" not in st.session_state:
    st.session_state.counts_df = pd.DataFrame(columns=["State", "Counts"])


def run_sim(code: str) -> dict:
    exec_globals = {}
    output_buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output_buffer

    try:
        exec(code, exec_globals)
        sys.stdout = old_stdout

        if "qc" in exec_globals:
            sim = AerSimulator()
            compiled = transpile(exec_globals["qc"], sim)
            result = sim.run(compiled).result()
            return {"type": "quantum", "data": result.get_counts()}

        print_val = output_buffer.getvalue()
        return {"type": "print", "data": print_val if print_val else "Success"}

    except Exception as e:
        sys.stdout = old_stdout
        return {"type": "error", "data": str(e)}


@st.fragment(run_every="1s")
def sync_url_params():
    url_code = st.query_params.get("code", "")
    if url_code != st.session_state.code:
        st.session_state.code = url_code
        st.rerun()


def qiskit_sim_ui():
    with st.container():
        with st.container(horizontal=True):
            st.subheader("Qiskit Python Generation")
            with st.container(horizontal=True, horizontal_alignment="right"):
                st.download_button(
                    label="Download",
                    file_name="quantum_edu.py",
                    data=st.session_state.code,
                    mime="text/x-python",
                    disabled=not st.session_state.code,
                    width="stretch"
                )
                button = st.empty()

        st.code(
            st.session_state.code if st.session_state.code else "",
            language="python",
            line_numbers=True,
        )
        if button.button("Run", type="primary",  width="stretch"):
            if not st.session_state.code:
                return

            with st.spinner():
                output = run_sim(st.session_state.code)

                if output["type"] == "quantum":
                    counts = output["data"]
                    counts_df = pd.DataFrame(
                        list(counts.items()), columns=["State", "Counts"]
                    )
                    with st.container(border=True):
                        st.subheader("Histogram")
                        st.bar_chart(counts_df.set_index("State")["Counts"])
                elif output["type"] == "print":
                    st.info(f"\>>> {output['data']}")
                elif output["type"] == "error":
                    st.error("You may some blocks")
                    st.error(output["data"])
