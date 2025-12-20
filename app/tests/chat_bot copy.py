
import os
import streamlit as st
from google import genai

API_KEY = "AIzaSyCi3IrQ5J_0NyBQ9i0WeXqhn4XY9WQrZYI"

st.set_page_config(
    page_title="Phyrom",
    page_icon=":robot_face:",  
    layout="wide",
)

client = genai.Client(api_key=API_KEY)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = []

st.title("🤖 Phyrom")

# Display the chat history if present
for msg in st.session_state.chat_session:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input field for user's message
user_input = st.chat_input("Ask Gemini-Pro...")
if user_input:
    st.chat_message("user").markdown(user_input)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=user_input
    )

    gemini_response = response.text
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    st.session_state.chat_session.append({"role": "user", "content": user_input})
    st.session_state.chat_session.append({"role": "assistant", "content": gemini_response})
