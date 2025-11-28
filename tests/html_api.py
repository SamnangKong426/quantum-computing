import streamlit as st
import streamlit.components.v1 as components

# Initialize session state for storing input data
if 'input_data' not in st.session_state:
    st.session_state.input_data = ""

# Function to handle incoming data from localStorage (via JavaScript)
def handle_message(message):
    if message.get('funcName') == 'update_input_data':
        st.session_state.input_data = message.get('data', '')

# HTML + JavaScript for localStorage handling and sending data to Streamlit
html_code = """
<html>
  <body>
    <h2>Enter some data:</h2>
    <input type="text" id="inputData" value="" />
    <button onclick="saveData()">Save Data to Local Storage</button>
    <button onclick="loadData()">Load Data from Local Storage</button>

    <script>
      function saveData() {
        var inputData = document.getElementById('inputData').value;
        // Save data to the browser's localStorage
        localStorage.setItem('user_input', inputData);
        // Send data to Streamlit (via postMessage)
        window.parent.postMessage({funcName: 'update_input_data', data: inputData}, '*');
      }

      function loadData() {
        var savedData = localStorage.getItem('user_input');
        // If there's data, update the input field
        if (savedData) {
          document.getElementById('inputData').value = savedData;
          // Send data to Streamlit (via postMessage)
          window.parent.postMessage({funcName: 'update_input_data', data: savedData}, '*');
        } else {
          alert('No data in localStorage!');
        }
      }
    </script>
  </body>
</html>
"""

# Embed the HTML + JavaScript into Streamlit
components.html(html_code, height=300)

# Listen for messages from JavaScript (via postMessage)
st.experimental_set_query_params()  # Necessary for event capture (works with `st.query_params`)
components.html('<script>window.addEventListener("message", function(event) { \
  if (event.origin !== window.location.origin) return; \
  window.parent.postMessage(event.data, "*"); }, false);</script>', height=0)

# Show the stored data (from localStorage, loaded through the JavaScript interaction)
if st.session_state.input_data:
    st.write(f"Data retrieved from localStorage: {st.session_state.input_data}")
else:
    st.write("No data stored in localStorage yet.")
