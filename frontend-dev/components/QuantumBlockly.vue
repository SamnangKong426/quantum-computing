<template>
  <div class="flex flex-col h-screen bg-gray-50">
    <!-- Header -->
    <div
      class="flex items-center justify-between border-b bg-white px-6 py-4 shadow-sm"
    >
      <!-- Title -->
      <h1 class="flex items-center gap-3 text-xl font-bold text-indigo-600">
        <span class="text-3xl">⚛️</span>
        Quantum Block Code Builder
      </h1>

      <!-- Actions -->
      <div class="flex items-center gap-3">
        <!-- Generate -->
        <button
          @click="generateCode"
          class="inline-flex items-center gap-2 rounded-lg border border-indigo-200 bg-indigo-50 px-4 py-2 text-sm font-semibold text-indigo-600 transition hover:bg-indigo-100 active:scale-95"
        >
          ▶️ Generate
        </button>

        <!-- Run (primary) -->
        <button
          @click="executeCode"
          class="inline-flex items-center gap-2 rounded-lg bg-emerald-500 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-600 active:scale-95"
        >
          🚀 Run
        </button>

        <!-- Copy -->
        <button
          @click="copyToClipboard"
          :disabled="!generatedCode"
          class="inline-flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-gray-600 transition hover:bg-gray-100 active:scale-95 disabled:cursor-not-allowed disabled:opacity-40"
        >
          📋 Copy
        </button>
      </div>
    </div>

    <div class="flex flex-1 overflow-hidden">
      <!-- Blockly -->
      <div class="flex-1 bg-gradient-to-br from-gray-50 to-white">
        <div ref="blocklyDiv" class="w-full h-full"></div>
      </div>

      <!-- Code panel -->
      <div class="w-96 bg-gray-900 flex flex-col shadow-2xl">
        <div
          class="p-4 bg-gray-800 border-b border-gray-700 flex justify-between items-center"
        >
          <h2 class="text-lg font-bold text-white">💻 Python Code</h2>
        </div>
        <div class="flex-1 overflow-auto p-4">
          <pre v-if="generatedCode" class="text-green-400 text-sm">{{
            generatedCode
          }}</pre>
          <div v-else class="text-gray-500 text-center mt-10">
            Build your quantum circuit and click Generate!
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import * as Blockly from "blockly";
import { pythonGenerator } from "blockly/python";
import { useQuantumBlocks } from "../composables/useQuantumBlocks";
import { useQuantumGenerators } from "../composables/useQuantumGenerators";

const blocklyDiv = ref(null);
const generatedCode = ref("");
let workspace = null;

const { defineQuantumBlocks } = useQuantumBlocks();
const { defineQuantumGenerators } = useQuantumGenerators();

/* ✅ JSON TOOLBOX (NO SVG BACKGROUND) */
const toolbox = {
  kind: "categoryToolbox",
  contents: [
    {
      kind: "category",
      name: "Circuit",
      categorystyle: "circuit_category",
      contents: [{ kind: "block", type: "quantum_circuit" }],
    },
    {
      kind: "category",
      name: "Single Gates",
      categorystyle: "single_gate_category",
      contents: [
        { kind: "block", type: "gate_h" },
        { kind: "block", type: "gate_x" },
        { kind: "block", type: "gate_y" },
        { kind: "block", type: "gate_z" },
      ],
    },
    {
      kind: "category",
      name: "Multi Gates",
      categorystyle: "multi_gate_category",
      contents: [
        { kind: "block", type: "gate_cnot" },
        { kind: "block", type: "gate_swap" },
        { kind: "block", type: "gate_toffoli" },
      ],
    },
    {
      kind: "category",
      name: "Measure",
      categorystyle: "measure_category",
      contents: [{ kind: "block", type: "measure_qubit" }],
    },
    {
      kind: "category",
      name: "Operations",
      categorystyle: "ops_category",
      contents: [{ kind: "block", type: "reset_qubit" }],
    },
  ],
};

/* ✅ CLEAN THEME */
const quantumTheme = Blockly.Theme.defineTheme("quantumTheme", {
  base: Blockly.Themes.Classic,
  blockStyles: {
    circuit_blocks: {
      colourPrimary: "#7C3AED",
      colourSecondary: "#A78BFA",
      colourTertiary: "#6D28D9",
    },
    single_gate_blocks: {
      colourPrimary: "#06B6D4",
      colourSecondary: "#67E8F9",
      colourTertiary: "#0891B2",
    },
    multi_gate_blocks: {
      colourPrimary: "#8B5CF6",
      colourSecondary: "#C4B5FD",
      colourTertiary: "#7C3AED",
    },
    measure_blocks: {
      colourPrimary: "#10B981",
      colourSecondary: "#6EE7B7",
      colourTertiary: "#059669",
    },
    operation_blocks: {
      colourPrimary: "#F59E0B",
      colourSecondary: "#FCD34D",
      colourTertiary: "#D97706",
    },
  },

  circuit_blocks: {
    colourPrimary: "#7C3AED",
  },
  categoryStyles: {
    circuit_category: { colour: "white" },
    single_gate_category: { colour: "white" },
    multi_gate_category: { colour: "white" },
    measure_category: { colour: "white" },
    ops_category: { colour: "white" },
  },
  componentStyles: {
    toolboxBackgroundColour: "transparent",
    toolboxForegroundColour: "transparent",
    toolboxSelectedItemBackgroundColour: "gray",
    toolboxSelectedItemBorderColour: "transparent",
    toolboxHoverBackgroundColour: "transparent",
  },
});

onMounted(() => {
  defineQuantumBlocks();
  defineQuantumGenerators();

  workspace = Blockly.inject(blocklyDiv.value, {
    toolbox,
    theme: quantumTheme,
    zoom: { controls: true, wheel: true },
    trashcan: true,
    grid: { spacing: 10, snap: true },
  });
});

function generateCode() {
  generatedCode.value = pythonGenerator.workspaceToCode(workspace);
}

function executeCode() {
  alert("Execute quantum circuit here");
}

async function copyToClipboard() {
  await navigator.clipboard.writeText(generatedCode.value);
}
</script>
<style>
/* Toolbox container */
.blocklyToolboxCategoryContainer {
  padding: 8px !important;
  background: transparent !important;
}
.blocklyToolboxCategoryLabel {
  font-weight: 500 !important;
  font-size: 20px !important;
  color: black !important;
}
.blocklyTreeRowContentContainer {
  text-align: center !important;
}
.blocklyToolboxCategoryIcon {
  display: none !important;
}
/* Category card */
.blocklyTreeRowContentContainer {
  margin: 16px 16px !important;
  padding: 12px 2.5rem !important;
  border-radius: 8px !important;
  border: #6d28d9 1px solid !important;
  background: rgb(255, 255, 255) !important;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06) !important;
  transition: all 0.25s ease !important;
  cursor: pointer;
}

/* Label */
.blocklyTreeLabel {
  font-weight: 600 !important;
  font-size: 14px !important;
}

/* Hover */
.blocklyToolboxCategoryContainer:hover .blocklyTreeRowContentContainer {
  transform: translateY(-1px) scale(1.01);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08) !important;
}
/* 
/* Active category */
.blocklyToolboxCategoryContainer.blocklyActiveFocus
  .blocklyTreeRowContentContainer {
  background: #6d28d9 !important;
  color: white !important;
  box-shadow: 0 14px 30px rgba(124, 58, 237, 0.35) !important;
}

/* Active label */
.blocklyToolboxCategoryContainer.blocklyActiveFocus .blocklyTreeLabel {
  color: white !important;
}
</style>
