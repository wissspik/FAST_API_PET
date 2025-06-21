import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: { 
    port: 3000,
    proxy: {
      '/entrance': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      },
      '/registration': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      },
      '/protected': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
}); 