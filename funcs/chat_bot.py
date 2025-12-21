import streamlit as st
from google import genai
from google.genai import types
from google.genai import errors

API_KEY = st.secrets["api_key"]
GEMINI_MODEL = st.secrets["gemini_model"]

client = genai.Client(api_key=API_KEY)
@st.fragment
def chat_fragment():
    st.title("🤖 Phyrom Quantum Assistant")
    
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = []

    chat_container = st.container(height=500)
    
    with chat_container:
        for msg in st.session_state.chat_session:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    user_input = st.chat_input("Ask Phyrom...", key="sidebar_chat")

    if user_input:
        st.session_state.chat_session.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)

        with chat_container:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                with placeholder.container():
                    st.caption("Phyrom is thinking...")
                
                full_response = st.write_stream(chat_streamer(user_input))
                
                placeholder.empty()
        
        if full_response:
            st.session_state.chat_session.append({"role": "assistant", "content": full_response})
            st.rerun(scope="fragment")

def chat_streamer(user_input):
    """A generator function that yields text chunks with a defined personality."""
    try:
        system_instruction = (
            "You are Phyrom, a Quantum Assistant. You are smart and cute. "
            "Your goal is to help users and explain things they don't understand "
            "on the QuantumEdu website. Be helpful, insightful, and maintain "
            "your personality as a friendly quantum expert."
        )

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)],
            ),
        ]

        for chunk in client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,  
                temperature=0.7,
            ),
        ):
            if chunk.text:
                yield chunk.text

    except errors.ClientError as e:
        if "429" in str(e):
            yield "⚠️ **Rate limit reached.** Please wait a moment for my circuits to cool down."
        else:
            yield f"⚠️ **API Error:** {str(e)}"
    except Exception as e:
        yield f"⚠️ **Unexpected Error:** {str(e)}"
