import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import unquote

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="Quantum Blockly")

# --- UI HEADER ---
st.title("⚛️ Quantum Circuit Designer")

# --- BRIDGE LOGIC ---
# We check if the URL contains code sent from the JavaScript side
query_params = st.query_params
current_code = query_params.get("code", "from qiskit import QuantumCircuit\nqc = QuantumCircuit(2, 2)")

# --- HTML/JS COMPONENT ---
blockly_html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://unpkg.com/blockly/blockly_compressed.js"></script>
  <script src="https://unpkg.com/blockly/blocks_compressed.js"></script>
  <script src="https://unpkg.com/blockly/python_compressed.js"></script>
  <script src="https://unpkg.com/blockly/msg/en.js"></script>
  <style>
    body {{ margin: 0; padding: 0; overflow: hidden; background-color: #ffffff; }}
    #blocklyDiv {{ height: 100vh; width: 100vw; }}
  </style>
</head>
<body>
  <div id="blocklyDiv"></div>

  <xml id="toolbox" style="display: none">
    <category name="Qubits" colour="160"><block type="quantum_circuit"></block></category>
    <category name="Gates" colour="230">
      <block type="apply_gate"><field name="GATE">H</field></block>
      <block type="apply_gate"><field name="GATE">X</field></block>
      <block type="apply_gate"><field name="GATE">CNOT</field></block>
    </category>
    <category name="Measurement" colour="120"><block type="measure_qubit"></block></category>
  </xml>

  <script>
    // --- Block Definitions ---
    Blockly.Blocks["quantum_circuit"] = {{
      init: function () {{
        this.appendDummyInput().appendField("Circuit")
          .appendField(new Blockly.FieldNumber(2, 1), "QUBITS")
          .appendField("q,")
          .appendField(new Blockly.FieldNumber(2, 0), "CLASSICAL_BITS")
          .appendField("c");
        this.setNextStatement(true);
        this.setColour(160);
      }}
    }};

    Blockly.Blocks["apply_gate"] = {{
      init: function () {{
        this.appendDummyInput().appendField("apply")
          .appendField(new Blockly.FieldDropdown([["H","H"],["X","X"],["CNOT","CNOT"]]), "GATE")
          .appendField("on")
          .appendField(new Blockly.FieldTextInput("0"), "QUBIT");
        this.setPreviousStatement(true);
        this.setNextStatement(true);
        this.setColour(230);
      }}
    }};

    Blockly.Blocks["measure_qubit"] = {{
      init: function () {{
        this.appendDummyInput().appendField("measure qubit")
          .appendField(new Blockly.FieldTextInput("0"), "QUBIT")
          .appendField("to bit")
          .appendField(new Blockly.FieldTextInput("0"), "CBIT");
        this.setPreviousStatement(true);
        this.setNextStatement(true);
        this.setColour(120);
      }}
    }};

    const pythonGenerator = python.pythonGenerator;

    pythonGenerator.forBlock["quantum_circuit"] = function (block) {{
      return "from qiskit import QuantumCircuit\\nqc = QuantumCircuit(" + block.getFieldValue("QUBITS") + ", " + block.getFieldValue("CLASSICAL_BITS") + ")\\n";
    }};

    pythonGenerator.forBlock["apply_gate"] = function (block) {{
      return "qc." + block.getFieldValue("GATE").toLowerCase() + "(" + block.getFieldValue("QUBIT") + ")\\n";
    }};

    pythonGenerator.forBlock["measure_qubit"] = function (block) {{
      return "qc.measure(" + block.getFieldValue("QUBIT") + ", " + block.getFieldValue("CBIT") + ")\\n";
    }};

    const workspace = Blockly.inject("blocklyDiv", {{
      toolbox: document.getElementById("toolbox"),
      trashcan: true
    }});

    // --- Update Logic ---
    function syncToStreamlit() {{
      const code = pythonGenerator.workspaceToCode(workspace);
      // We use URL search params to send the code back to the parent Streamlit app
      const parentUrl = new URL(window.parent.location.href);
      parentUrl.searchParams.set("code", code);
      window.parent.history.replaceState({{}}, '', parentUrl);
      
      // Trigger a light refresh if needed, or use postMessage for more advanced setups
      window.parent.postMessage({{type: 'streamlit:setComponentValue', value: code}}, "*");
    }}

    workspace.addChangeListener((e) => {{
      if (!e.isUiEvent) syncToStreamlit();
    }});
  </script>
</body>
</html>
"""

# --- LAYOUT ---
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Visual Editor")
    # This renders the Blockly workspace
    components.html(blockly_html, height=500)

with col2:
    st.subheader("Generated Qiskit Code")
    # Display the code captured from the URL or state
    st.code(current_code, language="python")
    
    if st.button("Simulate Circuit"):
        st.balloons()
        st.success("Executing code on Aer Simulator...")
        # In a real app, you'd use exec(current_code) here
        st.image("https://qiskit.org/documentation/_images/qiskit-metapackage.png", caption="Circuit Visualization")

st.info("Note: If the code doesn't update, ensure your browser allows the iframe to communicate with the parent window.")