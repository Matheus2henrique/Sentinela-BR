import { TomTomMap } from '@tomtom-org/maps-sdk/map';
import { LngLatBounds } from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const MODOS = { carro: 'car', moto: 'motorcycle', onibus: 'bus', caminhao: 'truck' };

async function calcular(apiKey, coordenadas, veiculo, { evitar, direcao, sinal } = {}) {
  const percurso = coordenadas.map(([lon, lat]) => `${lat.toFixed(6)},${lon.toFixed(6)}`).join(':');
  const url = new URL(`https://api.tomtom.com/routing/1/calculateRoute/${percurso}/json`);
  url.search = new URLSearchParams({
    key: apiKey, maxAlternatives: '2', travelMode: MODOS[veiculo], traffic: 'false',
    instructionsType: 'text', language: 'pt-BR'
  });
  if (direcao !== undefined) url.searchParams.set('vehicleHeading', direcao);

  const timeout = AbortSignal.timeout(15000);
  const opcoes = { signal: sinal ? AbortSignal.any([sinal, timeout]) : timeout };
  if (evitar) {
    const [oeste, sul, leste, norte] = evitar;
    opcoes.method = 'POST';
    opcoes.headers = { 'Content-Type': 'application/json' };
    opcoes.body = JSON.stringify({
      avoidAreas: { rectangles: [{
        southWestCorner: { latitude: sul, longitude: oeste },
        northEastCorner: { latitude: norte, longitude: leste }
      }] }
    });
  }
  const resposta = await fetch(url, opcoes);
  if (!resposta.ok) {
    const erro = new Error('Solicitação de rota recusada pelo TomTom.');
    erro.status = resposta.status;
    throw erro;
  }
  const { routes = [] } = await resposta.json();
  return routes.map(rota => ({
    coordenadas: rota.legs.flatMap((leg, i) => leg.points.slice(i ? 1 : 0)
      .map(p => [p.longitude, p.latitude])),
    km: rota.summary.lengthInMeters / 1000,
    segundos: rota.summary.travelTimeInSeconds,
    instrucoes: (rota.guidance?.instructions ?? []).map(i => ({
      km: i.routeOffsetInMeters / 1000,
      via: i.roadNumbers?.join(' · ') || i.street || '',
      mensagem: i.message
    }))
  })).filter(r => r.coordenadas.length > 1 && r.km > 0 && Number.isFinite(r.segundos));
}

const colecao = features => ({ type: 'FeatureCollection', features });
const linha = ({ coordenadas, ...estilo }) => ({
  type: 'Feature', geometry: { type: 'LineString', coordinates: coordenadas }, properties: estilo
});
const ponto = ({ coordenada, ...estilo }) => ({
  type: 'Feature', geometry: { type: 'Point', coordinates: coordenada }, properties: estilo
});

function esperarMapa(mapa) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => concluir(new Error('Tempo de carregamento do mapa excedido.')), 15000);
    const pronto = () => concluir();
    const falha = ({ error }) => {
      if (!mapa.getStyle()?.layers?.length || [401, 403].includes(error?.status)) {
        concluir(new Error('O TomTom não conseguiu carregar o mapa.'));
      }
    };
    function concluir(erro) {
      clearTimeout(timeout);
      mapa.off('load', pronto);
      mapa.off('error', falha);
      if (erro) reject(erro);
      else resolve();
    }
    mapa.on('load', pronto);
    mapa.on('error', falha);
    if (mapa.loaded()) pronto();
  });
}

function criarCamadas(mapa) {
  for (const id of ['sentinela-rotas', 'sentinela-alertas', 'sentinela-desvio', 'sentinela-carro']) {
    mapa.addSource(id, { type: 'geojson', data: colecao([]) });
  }
  mapa.addLayer({
    id: 'sentinela-rotas', type: 'line', source: 'sentinela-rotas',
    layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: { 'line-color': ['get', 'cor'], 'line-width': ['get', 'largura'], 'line-opacity': ['get', 'opacidade'] }
  });
  mapa.addLayer({
    id: 'sentinela-desvio', type: 'line', source: 'sentinela-desvio',
    paint: { 'line-color': '#67e8f9', 'line-width': 5, 'line-dasharray': [2, 1.5] }
  });
  mapa.addLayer({
    id: 'sentinela-alertas', type: 'circle', source: 'sentinela-alertas',
    paint: {
      'circle-color': ['get', 'cor'], 'circle-radius': ['get', 'raio'],
      'circle-stroke-color': '#fff', 'circle-stroke-width': ['get', 'borda']
    }
  });
  mapa.addLayer({
    id: 'sentinela-carro', type: 'circle', source: 'sentinela-carro',
    paint: { 'circle-color': '#22d3ee', 'circle-radius': 10, 'circle-stroke-color': '#fff', 'circle-stroke-width': 3 }
  });
}

function desenharRotulosExportados(ctx, canvas, rotulos) {
  if (!rotulos.length) return;
  const area = canvas.getBoundingClientRect();
  const proporcao = canvas.width / area.width, escala = canvas.width / canvas.clientWidth;
  for (const botao of rotulos) {
    const rect = botao.getBoundingClientRect(), ancora = botao.parentElement.getBoundingClientRect();
    const estilo = getComputedStyle(botao);
    const x = (rect.left - area.left) * proporcao, y = (rect.top - area.top) * proporcao;
    const largura = rect.width * proporcao, altura = rect.height * proporcao;
    ctx.strokeStyle = estilo.borderTopColor;
    ctx.lineWidth = escala;
    ctx.beginPath();
    ctx.moveTo((ancora.left - area.left) * proporcao, (ancora.top - area.top) * proporcao);
    ctx.lineTo(x + largura / 2, y + altura / 2);
    ctx.stroke();
    ctx.beginPath();
    ctx.roundRect(x, y, largura, altura, 9 * escala);
    ctx.fillStyle = estilo.backgroundColor;
    ctx.fill();
    ctx.lineWidth = parseFloat(estilo.borderTopWidth) * escala;
    ctx.stroke();
    ctx.fillStyle = estilo.color;
    ctx.textBaseline = 'middle';
    ctx.font = `800 ${14 * escala}px sans-serif`;
    ctx.fillText(botao.querySelector('.rota-tempo').textContent, x + 9 * escala, y + 15 * escala);
    ctx.fillStyle = '#c3d3e9';
    ctx.font = `${12 * escala}px sans-serif`;
    ctx.fillText(botao.querySelector('.rota-km').textContent, x + 9 * escala, y + 30 * escala);
  }
}

async function exportar(mapa, rotulos) {
  await new Promise((resolve, reject) => {
    const pronto = () => { clearTimeout(timeout); resolve(); };
    const timeout = setTimeout(() => {
      mapa.off('render', pronto);
      reject(new Error('O mapa não respondeu à solicitação de exportação.'));
    }, 4000);
    mapa.once('render', pronto);
    mapa.triggerRepaint();
  });
  const origem = mapa.getCanvas(), imagem = document.createElement('canvas');
  imagem.width = origem.width;
  const escala = origem.width / origem.clientWidth;
  const rodape = Math.ceil(24 * escala);
  imagem.height = origem.height + rodape;
  const ctx = imagem.getContext('2d');
  ctx.drawImage(origem, 0, 0);
  desenharRotulosExportados(ctx, origem, rotulos);
  ctx.fillStyle = '#0a101c';
  ctx.fillRect(0, origem.height, imagem.width, rodape);
  ctx.fillStyle = '#e8f1ff';
  ctx.font = `${11 * escala}px sans-serif`;
  ctx.textBaseline = 'middle';
  ctx.fillText('© TomTom · © OpenStreetMap contributors · PRF', 8 * escala, origem.height + rodape / 2);
  const arquivo = await new Promise(resolve => imagem.toBlob(resolve, 'image/png'));
  if (!arquivo) throw new Error('O mapa não pôde ser exportado.');
  const url = URL.createObjectURL(arquivo);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'sentinela-br-mapa.png';
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}

async function conectar(container, apiKey, { aoMover, aoEncerrarMovimento, aoSelecionar }) {
  const sdk = new TomTomMap({
    apiKey, style: 'streetDark', language: 'pt-BR',
    attribution: { position: 'top-left', padding: { horizontal: 12, vertical: 122 } },
    mapLibre: {
      container, center: [-52, -14], zoom: 4, dragRotate: false, pitchWithRotate: false,
      canvasContextAttributes: { preserveDrawingBuffer: true }
    }
  });
  const mapa = sdk.mapLibreMap;
  try {
    await esperarMapa(mapa);
    criarCamadas(mapa);
  } catch (erro) {
    mapa.remove();
    throw erro;
  }
  const atualizar = (id, features) => mapa.getSource(id).setData(colecao(features));
  const carro = coordenada => atualizar('sentinela-carro', coordenada ? [ponto({ coordenada })] : []);
  mapa.on('move', aoMover);
  mapa.on('moveend', aoEncerrarMovimento);
  mapa.on('click', ({ point }) => {
    const camadas = { layers: ['sentinela-rotas'] };
    const comRota = feature => Number.isInteger(feature.properties.rota);
    const { x, y } = point;
    const linha = mapa.queryRenderedFeatures(point, camadas).find(comRota) ??
      mapa.queryRenderedFeatures([[x - 7, y - 7], [x + 7, y + 7]], camadas).find(comRota);
    if (linha) aoSelecionar(linha.properties.rota);
  });
  return {
    calcular: (coordenadas, veiculo, opcoes) => calcular(apiKey, coordenadas, veiculo, opcoes),
    desenhar(linhas, pontos, posicao) {
      atualizar('sentinela-rotas', linhas.map(linha));
      atualizar('sentinela-alertas', pontos.map(ponto));
      atualizar('sentinela-desvio', []);
      carro(posicao);
    },
    prever: coordenadas => atualizar('sentinela-desvio', coordenadas ? [linha({ coordenadas })] : []),
    enquadrar(coordenadas, topo, base, maxZoom = 13) {
      const limites = new LngLatBounds();
      coordenadas.forEach(coordenada => limites.extend(coordenada));
      mapa.fitBounds(limites, { padding: { top: topo, bottom: base, left: 20, right: 20 }, maxZoom, animate: false });
    },
    centrar: (centro, zoom) => mapa.jumpTo({ center: centro, zoom }),
    mover(posicao) { carro(posicao); mapa.jumpTo({ center: posicao }); },
    redimensionar: () => mapa.resize(),
    projetar: coordenada => mapa.project(coordenada),
    localizar({ x, y }) {
      const { lng, lat } = mapa.unproject([x, y]);
      return [lng, lat];
    },
    zoom: () => mapa.getZoom(),
    exportar: (rotulos = []) => exportar(mapa, rotulos)
  };
}

async function chaveLocal() {
  try {
    const resposta = await fetch('./tomtom-config', { cache: 'no-store' });
    if (resposta.ok && resposta.headers.get('Content-Type')?.includes('application/json')) {
      return (await resposta.json()).apiKey || '';
    }
  } catch {}
  return '';
}

window.configurarTomTom({ conectar, chaveLocal });
