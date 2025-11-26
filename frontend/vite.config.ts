import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    host: '0.0.0.0',
    allowedHosts: [
      'fx.adamlibra.cz',
      'localhost',
      '192.168.1.204'
    ],
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',  // Dev proxy target
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'esbuild',
    target: 'es2015',
  },
})


