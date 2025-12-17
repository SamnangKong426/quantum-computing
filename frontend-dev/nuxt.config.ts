// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  modules: ["@nuxt/icon", "@nuxt/image", "@nuxtjs/tailwindcss"],
  head: {
    script: [
      { src: "https://unpkg.com/blockly/blockly_compressed.js" },
      { src: "https://unpkg.com/blockly/python_compressed.js" },
    ],
  },
  devServer: {
    port: 7000,
  },
});
