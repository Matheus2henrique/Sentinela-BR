import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';

const app = fileURLToPath(new URL('./Sentinela_BR_App_Rota_Segura.html', import.meta.url));

function servirChaveTomTom({ middlewares }) {
  middlewares.use('/tomtom-config', (request, response, next) => {
    if (request.method !== 'GET') return next();
    response.setHeader('Content-Type', 'application/json');
    response.setHeader('Cache-Control', 'no-store');
    response.end(JSON.stringify({ apiKey: process.env.TOMTOM_API_KEY?.trim() || '' }));
  });
}

export default defineConfig({
  base: './',
  server: { host: '127.0.0.1', cors: false },
  preview: { host: '127.0.0.1', cors: false },
  build: { rollupOptions: { input: app } },
  plugins: [{
    name: 'sentinela-tomtom-config',
    configureServer: servirChaveTomTom,
    configurePreviewServer: servirChaveTomTom
  }]
});
