import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

const backendPort = process.env.VITE_BACKEND_PORT || process.env.BACKEND_PORT || '8005';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3001,
    proxy: {
      '/api': {
        target: `http://localhost:${backendPort}`,
        changeOrigin: true,
      },
      '/health': {
        target: `http://localhost:${backendPort}`,
        changeOrigin: true,
      }
    },
  },
});
