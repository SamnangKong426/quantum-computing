import streamlit as st
from funcs.blockly_gen import blockly_ui
from funcs.chat_bot import chat_bot_ui
from funcs.qiskit_sim import qiskit_sim_ui, qiskit_bar_chart, update_code

st.set_page_config(page_icon="⚛️", page_title="QuantumEdu", layout="wide")
st.title("⚛️ Quantum Blockly Simulator", text_alignment="left")

update_code()

chat_bot_ui()

with st.container(border=True, horizontal=True):
    code = blockly_ui()
    st.space()
    qiskit_sim_ui()

qiskit_bar_chart()
