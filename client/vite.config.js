import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // Allows you to use import ... from '@/views/...'
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    rollupOptions: {
      input: {
        ebic: path.resolve(__dirname, 'ebic/index.html'),
        i19: path.resolve(__dirname, 'i19/index.html'),
        zone4: path.resolve(__dirname, 'zone4/index.html'),
        stores: path.resolve(__dirname, 'stores/index.html'),
        lab14: path.resolve(__dirname, 'lab14/index.html'),
        cage: path.resolve(__dirname, 'cage/index.html'),
      },
    },
  },
})
