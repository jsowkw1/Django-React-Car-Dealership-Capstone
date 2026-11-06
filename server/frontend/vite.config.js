import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// The production build is served by Django: index.html is rendered as a
// template and assets are collected as static files under /static/.
export default defineConfig(({ command }) => ({
  base: command === 'build' ? '/static/' : '/',
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/djangoapp': 'http://localhost:8000',
      '/admin': 'http://localhost:8000',
    },
  },
}));
