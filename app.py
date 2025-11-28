import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(layout="wide")

with open("frontend/index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, width=1800, height=800)
