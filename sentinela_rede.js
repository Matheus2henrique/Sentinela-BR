import { isIPv4 } from 'node:net';
import { networkInterfaces } from 'node:os';
import { preview } from 'vite';

const porta = 4174;
const pagina = '/Sentinela_BR_App_Rota_Segura.html';
const ipInformado = process.argv[2];
const adaptadores = Object.entries(networkInterfaces()).flatMap(([nome, enderecos]) =>
  enderecos.filter(({ family, internal }) => family === 'IPv4' && !internal)
    .map(({ address, netmask }) => ({ nome, address, netmask }))
);
const candidatos = adaptadores.filter(({ nome, address }) => ipInformado ?
  address === ipInformado : /wi[-\s]?fi|wlan|wireless|sem fio/i.test(nome));

if (candidatos.length !== 1) {
  console.error('Informe o IPv4 do adaptador da rede local com npm run rede -- SEU_IP.');
  for (const { nome, address } of adaptadores) console.error(`${nome} · ${address}`);
  process.exit(1);
}

const [{ address: host, netmask }] = candidatos;
const numeroIPv4 = ip => ip.split('.').reduce((numero, parte) => (numero << 8) | Number(parte), 0);
const mascara = numeroIPv4(netmask);
const subrede = numeroIPv4(host) & mascara;

await preview({
  preview: { host, port: porta, strictPort: true },
  plugins: [{
    name: 'sentinela-rede-local',
    enforce: 'pre',
    configurePreviewServer({ middlewares }) {
      middlewares.use((req, res, next) => {
        const remoto = req.socket.remoteAddress?.replace(/^::ffff:/, '') ?? '';
        if (!isIPv4(remoto) || (numeroIPv4(remoto) & mascara) !== subrede) {
          res.statusCode = 403;
          res.end('Acesso restrito à rede local do Sentinela BR.');
          return;
        }
        if (req.url === '/' && ['GET', 'HEAD'].includes(req.method)) {
          res.writeHead(302, { Location: pagina }).end();
          return;
        }
        next();
      });
    }
  }]
});

console.log(`Abra http://${host}:${porta} em outro dispositivo conectado ao mesmo Wi-Fi.`);
