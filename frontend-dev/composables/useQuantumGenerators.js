import { pythonGenerator } from "blockly/python";

export function useQuantumGenerators() {
  // Define Python code generators
  function defineQuantumGenerators() {
    pythonGenerator.forBlock["quantum_circuit"] = function (block) {
      const qubits = block.getFieldValue("QUBITS");
      const classical = block.getFieldValue("CLASSICAL");
      return `from qiskit import QuantumCircuit\nqc = QuantumCircuit(${qubits}, ${classical})\n`;
    };

    pythonGenerator.forBlock["gate_h"] = function (block) {
      const qubit = block.getFieldValue("QUBIT");
      return `qc.h(${qubit})\n`;
    };

    pythonGenerator.forBlock["gate_x"] = function (block) {
      const qubit = block.getFieldValue("QUBIT");
      return `qc.x(${qubit})\n`;
    };

    pythonGenerator.forBlock["gate_y"] = function (block) {
      const qubit = block.getFieldValue("QUBIT");
      return `qc.y(${qubit})\n`;
    };

    pythonGenerator.forBlock["gate_z"] = function (block) {
      const qubit = block.getFieldValue("QUBIT");
      return `qc.z(${qubit})\n`;
    };

    pythonGenerator.forBlock["gate_s"] = function (block) {
      const qubit = block.getFieldValue("QUBIT");
      return `qc.s(${qubit})\n`;
    };

    pythonGenerator.forBlock["gate_t"] = function (block) {
      const qubit = block.getFieldValue("QUBIT");
      return `qc.t(${qubit})\n`;
    };

    pythonGenerator.forBlock["gate_cnot"] = function (block) {
      const control = block.getFieldValue("CONTROL");
      const target = block.getFieldValue("TARGET");
      return `qc.cx(${control}, ${target})\n`;
    };

    pythonGenerator.forBlock["gate_cz"] = function (block) {
      const control = block.getFieldValue("CONTROL");
      const target = block.getFieldValue("TARGET");
      return `qc.cz(${control}, ${target})\n`;
    };

    pythonGenerator.forBlock["gate_swap"] = function (block) {
      const qubit1 = block.getFieldValue("QUBIT1");
      const qubit2 = block.getFieldValue("QUBIT2");
      return `qc.swap(${qubit1}, ${qubit2})\n`;
    };

    pythonGenerator.forBlock["gate_toffoli"] = function (block) {
      const control1 = block.getFieldValue("CONTROL1");
      const control2 = block.getFieldValue("CONTROL2");
      const target = block.getFieldValue("TARGET");
      return `qc.ccx(${control1}, ${control2}, ${target})\n`;
    };

    pythonGenerator.forBlock["measure_qubit"] = function (block) {
      const qubit = block.getFieldValue("QUBIT");
      const classical = block.getFieldValue("CLASSICAL");
      return `qc.measure(${qubit}, ${classical})\n`;
    };

    pythonGenerator.forBlock["measure_all"] = function (block) {
      return `qc.measure_all()\n`;
    };

    pythonGenerator.forBlock["barrier"] = function (block) {
      return `qc.barrier()\n`;
    };

    pythonGenerator.forBlock["reset_qubit"] = function (block) {
      const qubit = block.getFieldValue("QUBIT");
      return `qc.reset(${qubit})\n`;
    };
  }

  return {
    defineQuantumGenerators,
  };
}
