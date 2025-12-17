# main.py

import streamlit as st
from funcs.blockly_gen import blockly_ui
from funcs.chat_bot import chat_bot_ui
from funcs.qiskit_sim import qiskit_sim_ui, qiskit_bar_chart

st.set_page_config(layout="wide")


col1, col2 = st.columns([5, 2])

chat_bot_ui()

with col1:
    blockly_ui()

with col2:
    qiskit_sim_ui()

qiskit_bar_chart()





