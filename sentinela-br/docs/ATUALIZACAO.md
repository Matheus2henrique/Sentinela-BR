# pAInel Sentinela BR · atualização automática

Ministério dos Transportes · Equipe 4 · Innovathon 2026

## O que faz
- **8h, 14h e 18h (Brasília):** `atualizar.py` baixa as bases oficiais, recalcula trechos, risco, plano e clima e gera `p6/saida/index.html` com a nova data e hora no selo de atualização.
- **De hora em hora:** `monitor_alertas.py` consulta os avisos ativos do INMET, cruza com os trechos de risco e grava `p6/alertas_inmet.json`. O painel abre um pop-up com o órgão líder e os órgãos que agem juntos:
  - chuva forte e deslizamento: líder Defesa Civil, com PRF, gestor da via e Cemaden/SGB;
  - vendaval e granizo: líder Defesa Civil, com PRF e gestor da via;
  - neblina: líder PRF, com gestor da via;
  - baixa umidade e queimadas: líder Corpo de Bombeiros e Ibama/Prevfogo, com PRF, gestor e Defesa Civil.
- Opcional: `ALERTA_WEBHOOK` envia o mesmo alerta ao Teams, Slack ou e-mail.

## Como ligar (escolha um)
1. **GitHub Actions:** copie `real/` e `sentinela_br/` para um repositório, mantenha `.github/workflows/atualizar_painel.yml` e ative o GitHub Pages. O painel fica publicado no endereço do Pages.
2. **Servidor do Ministério:** `docker build -t sentinela .` na pasta que contém `real/` e `sentinela_br/`, depois `docker run -d sentinela`. O agendamento está em `crontab.txt`.

## Fontes que a rotina baixa
| Base | Situação |
|---|---|
| PRF – sinistros (página de dados abertos, Google Drive) | ativa |
| SIM/DataSUS (opendatasus) | idem |
| ANTT – trechos concedidos | idem |

Sem acesso a uma base, a rotina registra no log e mantém a última versão: o painel nunca fica sem dados.
