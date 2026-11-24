# Sentinela BR · Rota Segura (app do motorista)

Protótipo que leva a inteligência do painel ao motorista: carro, moto, ônibus e caminhão. Roda no navegador, sem instalar (`dist/app_rota_segura.html`). No computador, aparece como uma tela de celular, para demonstração no projetor.

## Como usar

1. **Saindo de** e **Destino** começam vazios. Toque no campo: abre a lista dos 5.571 municípios do IBGE, com as capitais no topo. Digite parte do nome (sem precisar de acento) e escolha.
2. Escolha o veículo e toque em **Ver rotas**.
3. Compare a **Mais segura** (verde, recomendada) com a **Mais rápida** (azul). Cada uma mostra km, tempo sem paradas, trechos críticos e mortes registradas desde 2021.
4. Toque em **Iniciar**. Dois quilômetros antes de cada trecho perigoso, aparece o cartão com rodovia, km, cidade, motivo registrado pela PRF e o cuidado necessário; a voz lê o aviso.
5. **Simulação 1×** acelera para 3× e 8×; **Voz** liga e desliga o som; **Encerrar** termina a viagem.
6. Na chegada: pontos de condução segura e o que podem render. **Meus pontos** mostra o saldo; **Como funciona**, o caminho para virar realidade.

## Como vira realidade

| Etapa | O que é | Quem |
|---|---|---|
| 1. Alertas no Waze | O Ministério, com o DNIT, publica os trechos críticos no feed do Waze for Cities, programa gratuito para órgãos públicos. Uma pessoa física não cria essa camada; o órgão parceiro, sim. | MT, DNIT, PRF |
| 2. Módulo no app CNH do Brasil | Função "Viagem segura" no app oficial, com pontos ligados ao RNPC | Senatran, Serpro |
| 3. Piloto | Este protótipo, no navegador do celular, com caminhoneiros e motoristas de ônibus em corredores críticos | MT, PRF, concessionárias |

## Incentivos (moeda de troca)

| Incentivo | Situação |
|---|---|
| Registro Nacional Positivo de Condutores (RNPC), no app CNH do Brasil | Existe |
| Desconto no IPVA para bom motorista (ex.: RS, até 15%) | Existe em alguns estados |
| Desconto no pedágio federal para quem acumula pontos | Proposta (regulação da ANTT) |
| Benefícios para caminhoneiros e empresas de ônibus | Proposta |
| Parceiros na estrada (postos, pontos de parada e descanso) | Proposta |

## Limites do protótipo

- O movimento do veículo é simulado; trechos, motivos e números são reais (PRF 2021–2026).
- A malha vem das coordenadas da PRF. Em poucos trechos sem registro (partes da BR-319 e da BR-174), a ligação usa a distância em linha reta mais 25%.
- Municípios sem ligação por rodovia federal (por exemplo, Macapá e Oiapoque) recebem aviso, e a rota vai até o ponto mais próximo da malha.
- A voz usa a voz em português do sistema operacional.
