import * as Blockly from "blockly";

export function useQuantumTheme() {
  function createQuantumTheme() {
    return Blockly.Theme.defineTheme("quantum", {
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
    });
  }

  return {
    createQuantumTheme,
  };
}
