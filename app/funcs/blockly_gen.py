import streamlit.components.v1 as components
import streamlit as st

with open("ui/index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

def blockly_ui():
    components.html(html_content, height=500, tab_index=0)
    query_params = st.query_params

    if "codeContent" in query_params:
        st.write("Code Content:", query_params["codeContent"])
    else:
        st.write("No 'codeContent' query parameter found.")

    if "codeContent" in query_params:
        all_code_content = query_params.get_all("codeContent")
        st.write("All 'codeContent' values:", all_code_content)
