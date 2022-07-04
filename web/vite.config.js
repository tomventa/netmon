import { resolve } from 'path';
import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

const root = resolve(__dirname, 'src/pages')
const outDir = resolve(__dirname, 'dist')
const publicDir = resolve(__dirname, 'public')

// https://vitejs.dev/config/
export default defineConfig({
  root,
  plugins: [svelte()],
  publicDir: publicDir,
  build: {
    outDir,
    assetsDir: 'static',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(root, 'index.html'),
        test: resolve(root, 'test', 'index.html'),
        logs: resolve(root, 'logs', 'index.html'),
        login: resolve(root, 'login', 'index.html'),
        device: resolve(root, 'device', 'index.html'),
        devices: resolve(root, 'devices', 'index.html'),
        settings: resolve(root, 'settings', 'index.html'),
      }
    }
  },
  preview: {
    port: 3000,
    strictPort: true
  }
})