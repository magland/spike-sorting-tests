import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "https://magland.github.io/spike-sorting-tests",
  resolve: {
    alias: {
      "simple-peer": "simple-peer/simplepeer.min.js"
    }
  }
})
