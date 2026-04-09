import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default ({ mode }) => {
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };

  return defineConfig({
    plugins: [react(), tailwindcss()],
    base: './',
    server: {
      port: 5173,
      strictPort: true,
      watch: {
        usePolling: true,
      },
      hmr: {
        overlay: true,
      },
      proxy: {
        '/api': {
          target: process.env.VITE_API_BASE_URL || 'http://localhost:5000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/api/, '/api')  // Optional: keeps '/api' prefix
        }
      },
    },
  });
}