// vite.config.mjs
import { defineConfig } from "file:///Users/ruoqingcheng/Desktop/digitaldiary_flask_webpage/code_after_refactor/digitaldiary/frontend/node_modules/vite/dist/node/index.js";
import react from "file:///Users/ruoqingcheng/Desktop/digitaldiary_flask_webpage/code_after_refactor/digitaldiary/frontend/node_modules/@vitejs/plugin-react/dist/index.mjs";
import tailwindcss from "file:///Users/ruoqingcheng/Desktop/digitaldiary_flask_webpage/code_after_refactor/digitaldiary/frontend/node_modules/@tailwindcss/vite/dist/index.mjs";
var vite_config_default = defineConfig({
  plugins: [react(), tailwindcss()],
  base: "./",
  server: {
    watch: {
      usePolling: true
    },
    hmr: {
      overlay: true
    },
    proxy: {
      "/api": {
        target: "http://localhost:5001",
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, "/api")
        // Optional: keeps '/api' prefix
      }
    }
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcubWpzIl0sCiAgInNvdXJjZXNDb250ZW50IjogWyJjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZGlybmFtZSA9IFwiL1VzZXJzL3J1b3FpbmdjaGVuZy9EZXNrdG9wL2RpZ2l0YWxkaWFyeV9mbGFza193ZWJwYWdlL2NvZGVfYWZ0ZXJfcmVmYWN0b3IvZGlnaXRhbGRpYXJ5L2Zyb250ZW5kXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvVXNlcnMvcnVvcWluZ2NoZW5nL0Rlc2t0b3AvZGlnaXRhbGRpYXJ5X2ZsYXNrX3dlYnBhZ2UvY29kZV9hZnRlcl9yZWZhY3Rvci9kaWdpdGFsZGlhcnkvZnJvbnRlbmQvdml0ZS5jb25maWcubWpzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9Vc2Vycy9ydW9xaW5nY2hlbmcvRGVza3RvcC9kaWdpdGFsZGlhcnlfZmxhc2tfd2VicGFnZS9jb2RlX2FmdGVyX3JlZmFjdG9yL2RpZ2l0YWxkaWFyeS9mcm9udGVuZC92aXRlLmNvbmZpZy5tanNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJ1xuaW1wb3J0IHJlYWN0IGZyb20gJ0B2aXRlanMvcGx1Z2luLXJlYWN0J1xuaW1wb3J0IHRhaWx3aW5kY3NzIGZyb20gJ0B0YWlsd2luZGNzcy92aXRlJ1xuXG4vLyBodHRwczovL3ZpdGVqcy5kZXYvY29uZmlnL1xuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKHtcbiAgcGx1Z2luczogW3JlYWN0KCksIHRhaWx3aW5kY3NzKCldLFxuICBiYXNlOiAnLi8nLFxuICBzZXJ2ZXI6IHtcbiAgICB3YXRjaDoge1xuICAgICAgdXNlUG9sbGluZzogdHJ1ZSxcbiAgICB9LFxuICAgIGhtcjoge1xuICAgICAgb3ZlcmxheTogdHJ1ZSxcbiAgICB9LFxuICAgIHByb3h5OiB7XG4gICAgICAnL2FwaSc6IHtcbiAgICAgICAgdGFyZ2V0OiAnaHR0cDovL2xvY2FsaG9zdDo1MDAxJyxcbiAgICAgICAgY2hhbmdlT3JpZ2luOiB0cnVlLFxuICAgICAgICBzZWN1cmU6IGZhbHNlLFxuICAgICAgICByZXdyaXRlOiAocGF0aCkgPT4gcGF0aC5yZXBsYWNlKC9eXFwvYXBpLywgJy9hcGknKSAgLy8gT3B0aW9uYWw6IGtlZXBzICcvYXBpJyBwcmVmaXhcbiAgICAgIH1cbiAgICB9LFxuICB9LFxufSlcbiJdLAogICJtYXBwaW5ncyI6ICI7QUFBb2QsU0FBUyxvQkFBb0I7QUFDamYsT0FBTyxXQUFXO0FBQ2xCLE9BQU8saUJBQWlCO0FBR3hCLElBQU8sc0JBQVEsYUFBYTtBQUFBLEVBQzFCLFNBQVMsQ0FBQyxNQUFNLEdBQUcsWUFBWSxDQUFDO0FBQUEsRUFDaEMsTUFBTTtBQUFBLEVBQ04sUUFBUTtBQUFBLElBQ04sT0FBTztBQUFBLE1BQ0wsWUFBWTtBQUFBLElBQ2Q7QUFBQSxJQUNBLEtBQUs7QUFBQSxNQUNILFNBQVM7QUFBQSxJQUNYO0FBQUEsSUFDQSxPQUFPO0FBQUEsTUFDTCxRQUFRO0FBQUEsUUFDTixRQUFRO0FBQUEsUUFDUixjQUFjO0FBQUEsUUFDZCxRQUFRO0FBQUEsUUFDUixTQUFTLENBQUMsU0FBUyxLQUFLLFFBQVEsVUFBVSxNQUFNO0FBQUE7QUFBQSxNQUNsRDtBQUFBLElBQ0Y7QUFBQSxFQUNGO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
