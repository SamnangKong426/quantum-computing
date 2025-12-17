<template>
  <div
    class="flex gap-6 p-6 w-full min-h-screen bg-gradient-to-br from-blue-50 to-purple-50"
  >
    <!-- Sidebar -->
    <div class="w-64 bg-white rounded-2xl p-5 shadow-lg h-fit">
      <h3 class="font-bold text-xl mb-4 text-gray-800">Code Blocks</h3>

      <div class="space-y-3">
        <div
          v-for="block in availableBlocks"
          :key="block.type"
          class="cursor-grab active:cursor-grabbing transition-transform hover:scale-105"
          draggable="true"
          @dragstart="onDragStart(block)"
        >
          <ScratchBlock :color="block.color" :is-template="true">
            <span class="font-semibold">{{ block.label }}</span>
            <span v-if="block.type === 'move'" class="ml-2">_ steps</span>
            <span v-else-if="block.type === 'turn'" class="ml-2"
              >_ degrees</span
            >
            <span v-else-if="block.type === 'say'" class="ml-2">_</span>
            <span v-else-if="block.type === 'wait'" class="ml-2"
              >_ seconds</span
            >
            <span v-else-if="block.type === 'repeat'" class="ml-2"
              >_ times</span
            >
          </ScratchBlock>
        </div>
      </div>
    </div>

    <!-- Workspace -->
    <div
      ref="workspaceRef"
      class="flex-1 bg-white rounded-2xl p-6 shadow-lg flex flex-col overflow-hidden"
      @dragover.prevent
      @drop="onDrop"
      @wheel="handleWheel"
    >
      <h3 class="font-bold text-xl mb-4 text-gray-800">
        Workspace
        <span class="text-sm text-gray-500 ml-2"
          >(Ctrl + Scroll to zoom: {{ Math.round(zoomLevel * 100) }}%)</span
        >
      </h3>

      <div
        v-if="blocks.length === 0"
        class="text-gray-400 text-center py-16 text-lg"
      >
        🎯 Drag blocks here to start coding!
      </div>

      <div
        class="space-y-1 flex-1 overflow-y-auto"
        :style="{
          transform: `scale(${zoomLevel})`,
          transformOrigin: 'top left',
        }"
      >
        <div
          v-for="(b, idx) in blocks"
          :key="b.id"
          class="relative group inline-block"
        >
          <ScratchBlock :color="b.color">
            <div class="flex items-center gap-2">
              <!-- MOVE -->
              <template v-if="b.type === 'move'">
                <span class="font-semibold">move</span>
                <input
                  type="number"
                  v-model.number="b.steps"
                  class="w-12 px-1 py-0.5 rounded bg-white text-gray-800 border border-blue-300 text-center text-xs"
                />
                <span>steps</span>
              </template>

              <!-- TURN -->
              <template v-else-if="b.type === 'turn'">
                <span class="font-semibold">turn</span>
                <input
                  type="number"
                  v-model.number="b.deg"
                  class="w-12 px-1 py-0.5 rounded bg-white text-gray-800 border border-blue-300 text-center text-xs"
                />
                <span>degrees</span>
              </template>

              <!-- SAY -->
              <template v-else-if="b.type === 'say'">
                <span class="font-semibold">say</span>
                <input
                  type="text"
                  v-model="b.text"
                  class="w-32 px-1 py-0.5 rounded bg-white text-gray-800 border border-purple-300 text-xs"
                />
              </template>

              <!-- WAIT -->
              <template v-else-if="b.type === 'wait'">
                <span class="font-semibold">wait</span>
                <input
                  type="number"
                  v-model.number="b.seconds"
                  class="w-12 px-1 py-0.5 rounded bg-white text-gray-800 border border-orange-300 text-center text-xs"
                />
                <span>seconds</span>
              </template>

              <!-- REPEAT -->
              <template v-else-if="b.type === 'repeat'">
                <span class="font-semibold">repeat</span>
                <input
                  type="number"
                  v-model.number="b.times"
                  class="w-12 px-1 py-0.5 rounded bg-white text-gray-800 border border-orange-300 text-center text-xs"
                />
                <span>times</span>
              </template>

              <button
                @click="removeBlock(idx)"
                class="opacity-0 group-hover:opacity-100 transition-opacity ml-2 text-white hover:text-red-200 font-bold text-lg"
              >
                ✕
              </button>
            </div>
          </ScratchBlock>
        </div>
      </div>

      <!-- Controls -->
      <div class="mt-6 flex gap-3 flex-wrap">
        <button
          @click="generateScript"
          class="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:scale-105"
        >
          🎬 Generate Script
        </button>

        <button
          @click="copyToClipboard"
          :disabled="!generated"
          class="px-6 py-3 bg-gradient-to-r from-gray-600 to-gray-700 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          📋 Copy
        </button>

        <button
          @click="downloadScript"
          :disabled="!generated"
          class="px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          💾 Download
        </button>
      </div>

      <!-- Output -->
      <div
        v-if="generated"
        class="mt-6 bg-gray-50 rounded-xl p-4 border-2 border-gray-200"
      >
        <h4 class="font-bold mb-3 text-gray-800">Generated Script:</h4>
        <textarea
          class="w-full border-2 border-gray-300 p-4 rounded-xl bg-white font-mono text-sm"
          rows="8"
          readonly
          v-model="generated"
        />
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, defineComponent, h } from "vue";

let id = 1;

const availableBlocks = [
  { type: "move", label: "move", category: "motion", color: "#4C97FF" },
  { type: "turn", label: "turn", category: "motion", color: "#4C97FF" },
  { type: "say", label: "say", category: "looks", color: "#9966FF" },
  { type: "wait", label: "wait", category: "control", color: "#FFAB19" },
  { type: "repeat", label: "repeat", category: "control", color: "#FFAB19" },
];

// ScratchBlock Component
const ScratchBlock = defineComponent({
  name: "ScratchBlock",
  props: {
    color: String,
    isTemplate: { type: Boolean, default: false },
  },
  setup(props, { slots }) {
    return () =>
      h("div", { class: "relative" }, [
        !props.isTemplate &&
          h("div", {
            class: "absolute left-6 w-8 h-1 rounded-t",
            style: {
              top: "0px",
              backgroundColor: props.color,
            },
          }),

        // MAIN BLOCK
        h(
          "div",
          {
            class: "relative text-white select-none",
            style: {
              backgroundColor: props.color,
              borderRadius: "8px",
              padding: "12px 16px",
              fontSize: "14px",
              lineHeight: "1.3",
              boxShadow: "0 3px 0 rgba(0,0,0,0.25)",
            },
          },
          slots.default?.()
        ),

        !props.isTemplate &&
          h("div", {
            class: "absolute left-6 w-8 h-1",
            style: {
              bottom: "-4px",
              backgroundColor: props.color,
            },
          }),
      ]);
  },
});

const blocks = ref([]);
const dragPayload = ref(null);
const generated = ref("");
const zoomLevel = ref(1);
const workspaceRef = ref(null);

function handleWheel(e) {
  if (e.ctrlKey) {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -0.1 : 0.1;
    zoomLevel.value = Math.max(0.5, Math.min(2, zoomLevel.value + delta));
  }
}

function onDragStart(block) {
  dragPayload.value = block.type;
}

function onDrop(e) {
  e.preventDefault();
  if (!dragPayload.value) return;
  const newBlock = createBlock(dragPayload.value);
  blocks.value.push(newBlock);
  dragPayload.value = null;
}

function createBlock(type) {
  const base = { id: id++, type };
  const block = availableBlocks.find((b) => b.type === type);
  if (type === "move")
    return { ...base, label: "move", steps: 10, color: block.color };
  if (type === "turn")
    return { ...base, label: "turn", deg: 90, color: block.color };
  if (type === "say")
    return { ...base, label: "say", text: "Hello!", color: block.color };
  if (type === "wait")
    return { ...base, label: "wait", seconds: 1, color: block.color };
  if (type === "repeat")
    return { ...base, label: "repeat", times: 10, color: block.color };
  return base;
}

function removeBlock(idx) {
  blocks.value.splice(idx, 1);
}

function generateScript() {
  const code = [];
  for (const b of blocks.value) {
    if (b.type === "move") code.push(`move(${b.steps});`);
    if (b.type === "turn") code.push(`turn(${b.deg});`);
    if (b.type === "say") code.push(`say("${b.text}");`);
    if (b.type === "wait") code.push(`wait(${b.seconds});`);
    if (b.type === "repeat") code.push(`repeat(${b.times}) { ... }`);
  }
  generated.value = code.join("\n");
}

async function copyToClipboard() {
  try {
    await navigator.clipboard.writeText(generated.value);
    alert("Copied to clipboard!");
  } catch (err) {
    alert("Failed to copy to clipboard");
  }
}

function downloadScript() {
  const blob = new Blob([generated.value], { type: "text/javascript" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "script.js";
  a.click();
  URL.revokeObjectURL(url);
}
</script>
