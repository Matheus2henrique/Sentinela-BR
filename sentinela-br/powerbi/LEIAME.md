# pAInel Sentinela BR · base para Power BI
Ministério dos Transportes · Equipe 4 · Innovathon 2026

## Jeito mais rápido: o modelo pronto (Sentinela_BR.pbit)
1. Descompacte este kit numa pasta, por exemplo `C:\Sentinela_BR\powerbi`.
2. Abra `Sentinela_BR.pbit` no Power BI Desktop. Ele pede o parâmetro **PastaDados**: informe a pasta do passo 1 e clique em **Carregar**.
3. O modelo já vem com as tabelas, as relações, as medidas (inclusive o selo "Atualizado em" e a lista de fontes) e cinco páginas: Visão, Ranking e ações, Pnatrans, Clima e pavimento, Fontes.
4. Salve como `.pbix`. Para publicar, use o botão Publicar e agende a atualização às 8h, 14h e 18h.

Se a sua versão do Power BI recusar o modelo, monte pelo passo a passo abaixo: as tabelas e medidas são as mesmas.

## Tabelas (CSV, separador ";", decimal ",", UTF-8)
| Arquivo | Conteúdo | Chave |
|---|---|---|
| dim_trecho.csv | 8.847 trechos de 5 km com morte: rodovia, UF, km, município, responsável, risco, motivo, clima | id_trecho |
| fato_mortes_ano.csv | mortes por trecho e ano (2021–2026; 2026 até outubro) | id_trecho |
| fato_mortes_tipo.csv | mortes por trecho e tipo de sinistro | id_trecho |
| fato_acao_ia.csv | ações possíveis por trecho com custo, eficácia, vidas salvas e dono | id_trecho |
| fato_pnatrans.csv | SIM: óbitos e taxa por 100 mil (2010–2025; 2025 preliminar) e meta 2030 | ano |
| dim_uf.csv | população, frota e mortes PRF 2024 por UF | uf |

Relacione `dim_trecho[id_trecho]` 1:N com as três tabelas fato de trecho.

## Selo de atualização com dica das fontes
1. **Obter dados > Consulta nula**, cole `atualizacao_e_fontes.pq` e dê o nome `Atualizacao`.
2. Crie as medidas de `medidas_dax.txt`.
3. **Inserir > Botão > Em branco**. Em **Ícone**, use `icone_atualizacao.svg` (Personalizado). Em **Texto do botão > fx**, escolha a medida `Atualizado em` (mostra dd/mm/aaaa e hh:mm).
4. Em **Ação > Dica de ferramenta > fx**, escolha a medida `Fontes do painel`. Ao passar o mouse, aparecem todas as fontes.
5. No Serviço do Power BI, agende a atualização às 08:00, 14:00 e 18:00 (fuso de Brasília). Cada atualização regrava a data e a hora do selo.

## Botão de limpar filtros
**Inserir > Botão > Redefinir**: em **Ação**, tipo **Indicador**, apontando para um indicador "Sem filtros" criado com todos os filtros limpos. Use **Sincronizar segmentações** (Exibir > Sincronizar segmentações) para que os filtros valham em todas as páginas.

## Origem e método
Mesmas fontes e método do painel HTML (aba Fontes e método). Custos e vidas salvas são estimativas com fonte citada.
