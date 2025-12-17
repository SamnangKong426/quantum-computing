import streamlit as st
from google import genai

API_KEY = "AIzaSyCi3IrQ5J_0NyBQ9i0WeXqhn4XY9WQrZYI"

client = genai.Client(api_key=API_KEY)

def chat_bot_ui():
    with st.sidebar:
        st.title("🤖  Niron")
        for msg in st.session_state.get("chat_session", []):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask Niron...")
        if user_input:
            st.chat_message("user").markdown(user_input)

            gemini_response = chat_bot(user_input)

            with st.chat_message("assistant"):
                st.markdown(gemini_response)


def chat_bot(user_input):
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = []

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=user_input
    )
    
    gemini_response = response.text
    
    st.session_state.chat_session.append({"role": "user", "content": user_input})
    st.session_state.chat_session.append({"role": "assistant", "content": gemini_response})

    return gemini_response
