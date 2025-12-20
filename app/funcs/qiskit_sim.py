import io
import os
import sys
import tempfile

import pandas as pd
import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from rope.base.project import Project
from rope.refactor.importutils import ImportOrganizer

CARD_HEIGHT = 450


def init_session_state():
    if "code" not in st.session_state:
        st.session_state.code = ""

    if "result" not in st.session_state:
        st.session_state.result = {}


def fix_imports(code_str: str) -> str:
    with tempfile.TemporaryDirectory(prefix="rope_project_") as project_root:
        file_path = os.path.join(project_root, "temp.py")

        with open(file_path, "w") as f:
            f.write(code_str)

        project = Project(project_root)
        resource = project.get_file("temp.py")

        organizer = ImportOrganizer(project)
        changes = organizer.organize_imports(resource)

        if changes:
            project.do(changes)

        with open(file_path) as f:
            new_code = f.read()

        project.close()

    return new_code


def run_sim(code: str) -> dict:
    exec_globals = {}
    output_buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output_buffer

    try:
        exec(code, exec_globals)
        sys.stdout = old_stdout

        # st.write(exec_globals)

        return {
            "type": "success",
            "stdout": output_buffer.getvalue(),
            "qc": exec_globals.get("qc"),
            "circuit": exec_globals.get("circuit"),
            "counts": exec_globals.get("counts"),
            "bloch": exec_globals.get("bloch"),
        }
    except Exception as e:
        sys.stdout = old_stdout
        return {"type": "error", "data": str(e)}


@st.fragment(run_every="1s")
def sync_url_params():
    url_code = st.query_params.get("code", "")
    if url_code != st.session_state.code:
        st.session_state.code = url_code
        st.rerun()


def qiskit_sim():
    code = fix_imports(st.session_state.code)

    with st.container():
        with st.container(horizontal=True):
            st.subheader("Qiskit Python Generation")
            with st.container(horizontal=True, horizontal_alignment="right"):
                st.download_button(
                    label="Download",
                    file_name="quantum_edu.py",
                    data=code,
                    mime="text/x-python",
                    disabled=not st.session_state.code,
                    width="stretch",
                )
                button = st.empty()

        st.code(code if code else "", language="python", line_numbers=True)

        if button.button("Run", type="primary", width="stretch"):
            if not code:
                return

            with st.spinner():
                result = run_sim(code)

                if result["type"] == "success":
                    st.success("Success", icon="✅")
                    st.session_state.result = result
                elif result["type"] == "error":
                    e = RuntimeError(result["data"])
                    st.exception(e)

def vertical_divider():
    st.markdown(
        """
        <div style="border-left: 1px solid #ccc; height: 15px; margin: 10px auto;"></div>
        """,
        unsafe_allow_html=True
    )


def render_result():
    result = st.session_state.result

    if result and result["type"] != "success":
        st.error("Error: " + result["data"])
        return

    with st.container(border=True, horizontal=True, horizontal_alignment="distribute"):
        with st.container():
            st.subheader("Circuit")
            if result.get("circuit"):
                st.pyplot(result["circuit"])

        vertical_divider()
        with st.container():
            st.subheader("Bloch Sphere")
            if result.get("bloch"):
                st.pyplot(result["bloch"])

        vertical_divider()
        with st.container():
            st.subheader("Histogram")
            if result.get("counts"):
                counts_df = pd.DataFrame(
                    list(result["counts"].items()), columns=["State", "Counts"]
                )
                st.bar_chart(counts_df.set_index("State")["Counts"])
