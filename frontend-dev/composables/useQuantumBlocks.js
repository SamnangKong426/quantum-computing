import * as Blockly from "blockly";

export function useQuantumBlocks() {
  // Define custom quantum blocks
  function defineQuantumBlocks() {
    // Quantum Circuit
    Blockly.Blocks["quantum_circuit"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("Quantum Circuit")
          .appendField(new Blockly.FieldNumber(2, 1, 100), "QUBITS")
          .appendField("qubits,")
          .appendField(new Blockly.FieldNumber(2, 0, 100), "CLASSICAL")
          .appendField("classical bits");
        this.setNextStatement(true, null);
        this.setStyle("circuit_blocks");
        this.setTooltip("Create a quantum circuit");
      },
    };

    // Hadamard Gate
    Blockly.Blocks["gate_h"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("H Gate on qubit")
          .appendField(new Blockly.FieldNumber(0, 0), "QUBIT");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("single_gate_blocks");
        this.setTooltip("Apply Hadamard gate");
      },
    };

    // Pauli-X Gate
    Blockly.Blocks["gate_x"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("X Gate on qubit")
          .appendField(new Blockly.FieldNumber(0, 0), "QUBIT");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("single_gate_blocks");
        this.setTooltip("Apply Pauli-X gate (NOT gate)");
      },
    };

    // Pauli-Y Gate
    Blockly.Blocks["gate_y"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("Y Gate on qubit")
          .appendField(new Blockly.FieldNumber(0, 0), "QUBIT");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("single_gate_blocks");
        this.setTooltip("Apply Pauli-Y gate");
      },
    };

    // Pauli-Z Gate
    Blockly.Blocks["gate_z"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("Z Gate on qubit")
          .appendField(new Blockly.FieldNumber(0, 0), "QUBIT");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("single_gate_blocks");
        this.setTooltip("Apply Pauli-Z gate");
      },
    };

    // S Gate
    Blockly.Blocks["gate_s"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("S Gate on qubit")
          .appendField(new Blockly.FieldNumber(0, 0), "QUBIT");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("single_gate_blocks");
        this.setTooltip("Apply S gate (Phase gate)");
      },
    };

    // T Gate
    Blockly.Blocks["gate_t"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("T Gate on qubit")
          .appendField(new Blockly.FieldNumber(0, 0), "QUBIT");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("single_gate_blocks");
        this.setTooltip("Apply T gate (π/8 gate)");
      },
    };

    // CNOT Gate
    Blockly.Blocks["gate_cnot"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("CNOT Gate: control")
          .appendField(new Blockly.FieldNumber(0, 0), "CONTROL")
          .appendField("target")
          .appendField(new Blockly.FieldNumber(1, 0), "TARGET");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("multi_gate_blocks");
        this.setTooltip("Apply CNOT gate");
      },
    };

    // CZ Gate
    Blockly.Blocks["gate_cz"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("CZ Gate: control")
          .appendField(new Blockly.FieldNumber(0, 0), "CONTROL")
          .appendField("target")
          .appendField(new Blockly.FieldNumber(1, 0), "TARGET");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("multi_gate_blocks");
        this.setTooltip("Apply Controlled-Z gate");
      },
    };

    // SWAP Gate
    Blockly.Blocks["gate_swap"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("SWAP Gate: qubit")
          .appendField(new Blockly.FieldNumber(0, 0), "QUBIT1")
          .appendField("↔")
          .appendField(new Blockly.FieldNumber(1, 0), "QUBIT2");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("multi_gate_blocks");
        this.setTooltip("Swap two qubits");
      },
    };

    // Toffoli Gate
    Blockly.Blocks["gate_toffoli"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("Toffoli (CCX): controls")
          .appendField(new Blockly.FieldNumber(0, 0), "CONTROL1")
          .appendField(",")
          .appendField(new Blockly.FieldNumber(1, 0), "CONTROL2")
          .appendField("target")
          .appendField(new Blockly.FieldNumber(2, 0), "TARGET");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("multi_gate_blocks");
        this.setTooltip("Apply Toffoli (CCNOT) gate");
      },
    };

    // Measure Single Qubit
    Blockly.Blocks["measure_qubit"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("Measure qubit")
          .appendField(new Blockly.FieldNumber(0, 0), "QUBIT")
          .appendField("→ bit")
          .appendField(new Blockly.FieldNumber(0, 0), "CLASSICAL");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("measure_blocks");
        this.setTooltip("Measure a single qubit");
      },
    };

    // Measure All
    Blockly.Blocks["measure_all"] = {
      init: function () {
        this.appendDummyInput().appendField("Measure All Qubits");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("measure_blocks");
        this.setTooltip("Measure all qubits");
      },
    };

    // Barrier
    Blockly.Blocks["barrier"] = {
      init: function () {
        this.appendDummyInput().appendField("Barrier");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("operation_blocks");
        this.setTooltip("Add a barrier to the circuit");
      },
    };

    // Reset Qubit
    Blockly.Blocks["reset_qubit"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("Reset qubit")
          .appendField(new Blockly.FieldNumber(0, 0), "QUBIT");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setStyle("operation_blocks");
        this.setTooltip("Reset a qubit to |0⟩");
      },
    };
  }

  return {
    defineQuantumBlocks,
  };
}
