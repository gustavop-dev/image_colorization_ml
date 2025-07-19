import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  // Configure base path for assets to be served from /static/frontend/
  base: '/static/frontend/',
  
  build: {
    // Output directory for generated files (relative to vite.config.js)
    // Files will be placed in the backend static directory structure
    outDir: '../backend/static/frontend',
    rollupOptions: {
      output: {
        // Custom file naming patterns for different asset types
        assetFileNames: (assetInfo) => {
          if (/\.(png|jpg|jpeg|gif|svg|webp|bmp)$/.test(assetInfo.name)) {
            return 'img/[name][extname]';
          }
          if (/\.css$/.test(assetInfo.name)) {
            return 'css/[name][extname]';
          }
          return 'assets/[name][extname]';
        },
        // Main entry point will be named index.js for easy reference
        entryFileNames: 'js/index.js',
        // Code splitting chunks follow standard naming convention
        chunkFileNames: 'js/[name].js',
      },
    },
    // Clean output directory before each build to ensure fresh deployment
    emptyOutDir: true,
  },
  
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  
  plugins: [
    vue(),
    tailwindcss(),
  ],
  
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
