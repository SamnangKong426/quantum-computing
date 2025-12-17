<template>
  <div class="w-full h-full overflow-hidden">
    <div class="p-2">
      <button @click="generateCode">Generate Python Code</button>
    </div>

    <div ref="blocklyDiv" id="blocklyDiv"></div>

    <div id="codeDiv">{{ pythonCode }}</div>

    <!-- Toolbox -->
    <xml id="toolbox" style="display:none">
      <category name="Qubits" colour="160">
        <block type="quantum_circuit"></block>
      </category>

      <category name="Quantum Gates" colour="230">
        <category name="Single-Qubit Gates" colour="210">
          <block type="apply_gate"><field name="GATE">H</field></block>
        </category>
        <category name="Multi-Qubit Gates" colour="190">
          <block type="apply_gate"><field name="GATE">CNOT</field></block>
          <block type="apply_gate"><field name="GATE">CZ</field></block>
          <block type="apply_gate"><field name="GATE">SWAP</field></block>
        </category>
      </category>

      <category name="Measurement" colour="120">
        <block type="measure_qubit"></block>
      </category>

      <category name="Extras" colour="60">
        <block type="reset_qubit"></block>
        <block type="barrier"></block>
        <block type="conditional_gate"></block>
        <block type="run_circuit"></block>
      </category>

      <category name="Views" colour="100">
        <block type="draw_mpl"></block>
      </category>
    </xml>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const blocklyDiv = ref(null);
const pythonCode = ref("");
let workspace = null;

onMounted(() => {
  const Blockly = window.Blockly;
  const python = Blockly.Python;

  // ---------------- BLOCK DEFINITIONS ----------------
  Blockly.Blocks["quantum_circuit"] = {
    init: function () {
      this.appendDummyInput()
        .appendField("Circuit")
        .appendField(new Blockly.FieldNumber(2, 1), "QUBITS")
        .appendField("q,")
        .appendField(new Blockly.FieldNumber(2, 0), "CLASSICAL_BITS")
        .appendField("c");
      this.setPreviousStatement(false);
      this.setNextStatement(true);
      this.setColour(160);
    },
  };

  Blockly.Blocks["apply_gate"] = {
    init: function () {
      this.appendDummyInput()
        .appendField("apply")
        .appendField(
          new Blockly.FieldDropdown([
            ["H", "H"],
            ["X", "X"],
            ["Y", "Y"],
            ["Z", "Z"],
            ["S", "S"],
            ["T", "T"],
            ["CNOT", "CNOT"],
            ["CZ", "CZ"],
            ["SWAP", "SWAP"],
          ]),
          "GATE"
        )
        .appendField("on")
        .appendField(new Blockly.FieldTextInput("q0"), "QUBIT");
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setColour(230);
    },
  };

  Blockly.Blocks["measure_qubit"] = {
    init: function () {
      this.appendDummyInput()
        .appendField("measure qubit")
        .appendField(new Blockly.FieldTextInput("q0"), "QUBIT")
        .appendField("into classical bit")
        .appendField(new Blockly.FieldTextInput("c0"), "CBIT");
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setColour(120);
    },
  };

  Blockly.Blocks["reset_qubit"] = {
    init: function () {
      this.appendDummyInput()
        .appendField("reset qubit")
        .appendField(new Blockly.FieldTextInput("q0"), "QUBIT");
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setColour(120);
    },
  };

  Blockly.Blocks["barrier"] = {
    init: function () {
      this.appendDummyInput().appendField("barrier");
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setColour(60);
    },
  };

  Blockly.Blocks["conditional_gate"] = {
    init: function () {
      this.appendDummyInput()
        .appendField("if")
        .appendField(new Blockly.FieldTextInput("c0==1"), "COND")
        .appendField("then apply")
        .appendField(
          new Blockly.FieldDropdown([
            ["X", "X"],
            ["Y", "Y"],
            ["Z", "Z"],
            ["H", "H"],
          ]),
          "GATE"
        )
        .appendField("on")
        .appendField(new Blockly.FieldTextInput("q1"), "QUBIT");
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setColour(60);
    },
  };

  Blockly.Blocks["run_circuit"] = {
    init: function () {
      this.appendDummyInput()
        .appendField("run circuit on")
        .appendField(
          new Blockly.FieldDropdown([
            ["simulator", "simulator"],
            ["real device", "real"],
          ]),
          "BACKEND"
        );
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setColour(20);
    },
  };

  Blockly.Blocks["draw_mpl"] = {
    init: function () {
      this.appendDummyInput().appendField("view circuit");
      this.setPreviousStatement(true);
      this.setNextStatement(false);
      this.setColour(20);
    },
  };

  // ---------------- PYTHON GENERATORS ----------------
  python.forBlock["quantum_circuit"] = function (block) {
    const q = block.getFieldValue("QUBITS");
    const c = block.getFieldValue("CLASSICAL_BITS");
    return `from qiskit import QuantumCircuit\nqc = QuantumCircuit(${q}, ${c})\n`;
  };

  python.forBlock["apply_gate"] = function (block) {
    const gate = block.getFieldValue("GATE");
    const qubit = block.getFieldValue("QUBIT");
    if (["CNOT", "CZ", "SWAP"].includes(gate)) {
      const qubits = qubit.split(",");
      return `qc.${gate.toLowerCase()}(${qubits.join(",")})\n`;
    }
    return `qc.${gate.toLowerCase()}(${qubit})\n`;
  };

  python.forBlock["measure_qubit"] = function (block) {
    return `qc.measure(${block.getFieldValue("QUBIT")}, ${block.getFieldValue(
      "CBIT"
    )})\n`;
  };

  python.forBlock["reset_qubit"] = block =>
    `qc.reset(${block.getFieldValue("QUBIT")})\n`;

  python.forBlock["barrier"] = () => `qc.barrier()\n`;

  python.forBlock["conditional_gate"] = function (block) {
    return `if ${block.getFieldValue(
      "COND"
    )}:\n    qc.${block.getFieldValue("GATE").toLowerCase()}(${block.getFieldValue(
      "QUBIT"
    )})\n`;
  };

  python.forBlock["run_circuit"] = function (block) {
    const backend = block.getFieldValue("BACKEND");
    if (backend === "simulator") {
      return `from qiskit import Aer, execute\nbackend = Aer.get_backend('qasm_simulator')\nresult = execute(qc, backend).result()\nprint(result.get_counts(qc))\n`;
    }
    return `# Real quantum device\nfrom qiskit import IBMQ, execute\nIBMQ.load_account()\nbackend = IBMQ.get_backend('your_backend')\nresult = execute(qc, backend).result()\nprint(result.get_counts(qc))\n`;
  };

  python.forBlock["draw_mpl"] = () => `qc.draw("mpl")\n`;

  // ---------------- INIT WORKSPACE ----------------
  workspace = Blockly.inject(blocklyDiv.value, {
    toolbox: document.getElementById("toolbox"),
    zoom: {
      controls: true,
      wheel: true,
      startScale: 1,
      maxScale: 3,
      minScale: 0.5,
    },
    trashcan: true,
  });
});

// ---------------- GENERATE PYTHON CODE ----------------
function generateCode() {
  pythonCode.value = window.Blockly.Python.workspaceToCode(workspace);
  localStorage.setItem("quantum_blockly_code", pythonCode.value);
}
</script>

<style>
#blocklyDiv {
  height: 70vh;
  width: 100%;
}
#codeDiv {
  height: 30vh;
  width: 100%;
  border-top: 1px solid #ccc;
  background: #f9f9f9;
  padding: 10px;
  white-space: pre;
  overflow: auto;
  font-family: monospace;
}
</style>
