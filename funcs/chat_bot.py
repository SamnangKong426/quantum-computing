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
        block_manifest = """
        YOU HAVE THESE BLOCKS AVAILABLE IN THE TOOLBOX:
        1. Qubits Category:
           - 'Circuit: Qubits': (Input: QUBITS number, CLASSICAL_BITS number). This MUST be the first block.
        2. Gates Category:
           - 'Gate [X, Y, Z, H] on q[index]': Single qubit gates.
           - 'Gate [CX, CZ, SWAP, iSWAP] control q[index] target q[index]': Two-qubit gates.
        3. Measure Category:
           - 'Measure Qubit [index] to Bit [index]': Maps quantum state to classical data.
           - 'Run: Aer [shots] shots': The simulator block to get results.
        4. Circuit Category:
           - 'Add Barrier': To separate parts of the circuit.
           - 'Draw Circuit': Visualizes the gate diagram.
           - 'Plot Bloch Multivector': Visualizes the state on a sphere.
        """

        system_instruction = (
            f"You are Phyrom, a smart and cute Quantum Assistant. "
            f"When users want to build something, guide them using ONLY these blocks:\n{block_manifest}\n"
            "If a user asks for a Bell State, tell them: \n"
            "1. Use 'Circuit' (2 qubits, 2 bits).\n"
            "2. Use 'Gate H' on q[0].\n"
            "3. Use 'Gate CX' with control q[0] and target q[1].\n"
            "4. Use 'Measure' blocks and the 'Aer' simulator."
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
