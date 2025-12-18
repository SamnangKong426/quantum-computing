import streamlit as st
from funcs.blockly_gen import blockly_ui
from funcs.chat_bot import chat_bot_ui
from funcs.qiskit_sim import qiskit_sim_ui, sync_url_params

st.set_page_config(page_icon="⚛️", page_title="QuantumEdu", layout="wide")
st.title("⚛️ Quantum Blockly Simulator", text_alignment="left")


if "code" not in st.session_state:
    st.session_state.code = ""

sync_url_params()

chat_bot_ui()

cols = st.columns([7, 4], border=True)
with cols[0]:
    blockly_ui()
    
with cols[1]:
    qiskit_sim_ui()
