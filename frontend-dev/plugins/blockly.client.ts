export default defineNuxtPlugin(() => {
  // Load Blockly globally
  return {
    provide: {
      blockly: (window as any).Blockly
    }
  }
})
