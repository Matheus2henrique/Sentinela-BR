# Sentinela BR – API e feed para o Waze

API com os trechos críticos das rodovias federais (sinistros da PRF de jan/2021 a out/2026), o cálculo de riscos de uma viagem, as demandas por órgão e um **feed no formato Waze CIFS** com os pontos de atenção.

## Rodar

```bash
pip install -r requirements.txt
uvicorn sentinela_api:app --host 0.0.0.0 --port 8000
# documentação interativa: http://localhost:8000/docs
```

Também é possível usar Docker: `docker build -t sentinela-api . && docker run -p 8000:8000 sentinela-api`

## Rotas

| Rota | O que devolve |
|---|---|
| `GET /v1/rota?origem=Brasilia - DF&destino=Rio de Janeiro - RJ&saida=07:00&data=2026-12-20&veiculo=carro` | Distância, tempo, mortes no caminho, até 15 pontos de atenção em ordem (com horário previsto de passagem, se passa no horário mais perigoso e se é mês de chuva), geometria da rota |
| `GET /v1/trechos?uf=SP&br=116&nivel_min=2&fator=alagamento` | Trechos de risco em GeoJSON (`formato=json` para lista simples) |
| `GET /v1/trechos/BR116-SP-0225` | Ficha completa de um trecho: mortes por ano, fatores, horários, órgãos e medidas |
| `GET /v1/ranking?uf=MG&limite=20` | Trechos mais perigosos, ordenados pelo risco ajustado |
| `GET /v1/encaminhamentos?uf=PE` | Demandas agrupadas por órgão (gestor da via, PRF, Defesa Civil, prefeitura, DETRAN) |
| `GET /v1/waze/cifs.json?uf=MG&nivel_min=2&dias=7` | Feed Waze CIFS em JSON |
| `GET /v1/waze/cifs.xml` | O mesmo feed em XML |
| `GET /v1/clima?lat=-15.8&lon=-47.9` | Chuva prevista nas próximas 24 h (Open-Meteo), para cruzar com os trechos de risco de chuva |
| `GET /v1/estatisticas` | Totais nacionais |

Fatores (`fator=`): chuva, alagamento, encosta (objetos, detritos ou queda de barreira), via, curva, neblina, animais, pedestres, frontal, sono, motos, alcool, velocidade, traseira.

## Como plugar no Waze

O Waze recebe dados de parceiros pelo programa **Waze for Cities** e pelo **Partner Hub**. O formato aceito para incidentes é o **CIFS** (Closure and Incident Feed Specification): uma URL pública que o Waze lê periodicamente.

1. Publique a API (ou só os arquivos de `saida/`, gerados por `python exportar_estatico.py`) num endereço HTTPS público.
2. Cadastre o órgão no Waze for Cities e, no Partner Hub, registre a URL do feed: `https://SEU-DOMINIO/v1/waze/cifs.xml` (ou `.json`).
3. Gere o feed de novo todo dia (os incidentes têm `endtime` de 7 dias por padrão, até 14).

Cada trecho vira um incidente `HAZARD` com:

- `id` estável (`sentinela-BR116-SP-0225`), para o Waze atualizar o mesmo ponto em vez de duplicar;
- `subtype` conforme o fator principal: alagamento → `HAZARD_WEATHER_FLOOD`, chuva → `HAZARD_WEATHER_HEAVY_RAIN`, neblina → `HAZARD_WEATHER_FOG`, queda de barreira → `HAZARD_ON_ROAD_OBJECT`, pista ruim → `HAZARD_ON_ROAD_POT_HOLE`, animais → `HAZARD_ON_SHOULDER_ANIMALS`, demais → `HAZARD_ON_ROAD`;
- `polyline` com dois pontos ao longo da rodovia (início e fim do trecho), `direction` = `BOTH_DIRECTIONS`, `street` = `BR-116`;
- `description` curta (menos de 40 caracteres, como pede a especificação), por exemplo "Atenção: pedestres, 49 mortes".

Por padrão o feed traz só os trechos de risco alto e muito alto (`nivel_min=2`, cerca de 1.200 no país), para não poluir o mapa do motorista.

**Evolução natural:** ligar o feed à previsão do tempo, publicando o alerta de alagamento ou queda de barreira só quando houver chuva forte prevista para aquele trecho (rota `/v1/clima`), e incluir interdições informadas pela PRF e pela Defesa Civil como `ROAD_CLOSED`.

## Limites

- Rotas e distâncias são aproximadas e consideram só rodovias federais.
- O gestor de cada trecho (DNIT ou concessionária) precisa ser confirmado com a malha oficial do DNIT (SNV).
- O risco é histórico (2021 a 2026). Previsão do tempo ao vivo depende de acesso à internet a partir do servidor.
