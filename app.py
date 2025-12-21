import streamlit as st

from funcs.blockly_gen import blockly_ui
from funcs.chat_bot import chat_fragment
from funcs.qiskit_sim import (
    init_session_state,
    qiskit_sim,
    render_result,
    sync_url_params,
)

st.set_page_config(page_icon="⚛️", page_title="QuantumEdu", layout="wide")
st.subheader("⚛️ Quantum Blockly Simulator", text_alignment="left")


init_session_state()

sync_url_params()

with st.sidebar:
    chat_fragment()

cols = st.columns([7, 4], border=True)
with cols[0]:
    blockly_ui()

with cols[1]:
    qiskit_sim()

render_result()

# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
            .stMainBlockContainer{
                padding: 3rem 1rem 10rem
            }
        </style>
        """, unsafe_allow_html=True)