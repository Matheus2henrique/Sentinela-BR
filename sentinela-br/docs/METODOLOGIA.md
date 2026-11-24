# Metodologia

Todos os números do painel vêm de bases oficiais. Onde há estimativa (risco futuro, custo, vidas salvas), o método e a fonte estão descritos aqui e na aba **Fontes e método** do painel.

## 1. Unidade de análise: trecho de 5 km

Cada sinistro da PRF (jan/2021 a out/2026) é posicionado pela rodovia (BR), pela UF e pelo km, e agrupado em trechos de 5 km (`km 0–5`, `5–10`...). Só entram registros com coordenada coerente com a rodovia declarada. O painel mostra os **8.847 trechos com pelo menos uma morte**, que somam 33.797 mortes.

## 2. Risco: mortes esperadas nos próximos 12 meses

Um único acidente grave (um ônibus, por exemplo) não pode transformar um trecho em "crítico". Por isso o risco é estimado em duas partes.

1. **Frequência de sinistros fatais, com Bayes empírico.** Para cada rodovia em cada UF, a média e a variância de sinistros fatais por trecho definem o peso `w = 1 / (1 + α·média)`, com `α = max((variância − média)/média², 0,05)`. A frequência do trecho é `w·média do corredor + (1 − w)·observado`, dividida pelos 5,83 anos observados. Trechos com pouca evidência ficam perto da média do corredor; trechos com histórico consistente ficam com o próprio valor.
2. **Gravidade suavizada.** Mortes por sinistro fatal: `(mortes + 3 × média nacional) / (sinistros fatais + 3)`.

**Mortes esperadas por ano** = frequência (1) × gravidade (2).

| Nível | Mortes esperadas por ano |
|---|---|
| Crítico | 2 ou mais |
| Alto | de 1 a 2 |
| Médio | de 0,4 a 1 |
| Baixo | abaixo de 0,4 |

**Em alta:** média de mortes de 2024–2025 maior que a média de 2021–2023.

## 3. Como se morre (mecanismo)

Os tipos de sinistro da PRF são agrupados em seis mecanismos: colisão frontal, saída de pista e capotamento, atropelamento, colisão traseira, colisão em cruzamento e outros. O mecanismo define a medida que funciona (Pareto: quatro mecanismos somam 85% das mortes).

## 4. Plano de ação: custo e vidas salvas

| Medida | Quando se aplica | Custo de referência | Eficácia (redução de mortes) |
|---|---|---|---|
| Fiscalização eletrônica de velocidade | Qualquer trecho com morte | R$ 4 mil por faixa/mês × 2 faixas × 48 meses = R$ 384 mil (DNIT, PNCV) | 20% (FHWA, piso da faixa de 20% a 54%) |
| Barreira central de concreto | Pista dupla com colisão frontal | 5.000 m × R$ 326,31/m (SICRO abr/2026, composição 3713822) | 77% (Trafikverket) |
| Faixa adicional 2+1 com barreira | Pista simples com colisão frontal | 5 km × R$ 1,95 mi/km (CMG mar/2015, terceira faixa) + barreira | 77% (Trafikverket) |
| Defensa metálica e sonorizadores de borda | Saída de pista ou capotamento | 2.000 m × R$ 851,99/m (SICRO abr/2026, composição 3713600) | 36% (FHWA) |
| Travessia segura | Atropelamento | ≈ R$ 4,8 mi por passarela (DER-DF, BR-020) | 46% (FHWA) |
| Rotatória ou interseção em desnível | Colisão em cruzamento | Teto de R$ 17,5 mi (viaduto da BR-470/SC, DNIT) | 78% (FHWA) |

**Vidas salvas por ano** de uma medida = mortes esperadas no trecho × parcela das mortes do mecanismo que ela trata × eficácia.

O plano tem dois critérios, à escolha do gestor:

- **Máximo de vidas por real** (padrão): ordena todas as ações possíveis pelo custo por vida salva e escolhe até esgotar o orçamento.
- **Trechos mais críticos primeiro:** percorre os trechos do maior para o menor risco e aplica o pacote de obras de cada um (ações com até R$ 20 mi por vida salva ao ano).

Custos e vidas salvas são estimativas para priorizar, não orçamento de obra.

## 5. Projeção e meta do Pnatrans

- **2026:** mortes até outubro divididas pela parcela histórica de jan–out no ano (82,4%).
- **2027–2030:** tendência linear das mortes anuais 2021–2026 nos trechos filtrados.
- **Indicador nacional:** taxa do SIM/MS por 100 mil habitantes (IBGE), com tendência e meta do Pnatrans para 2030 (7,8, metade da taxa de 2020).

## 6. Responsável por trecho: DNIT ou concessionária

A base da ANTT *Informações sobre os trechos concedidos* (arquivo 8/2026) traz BR, UF, km inicial e km final de cada contrato federal. Um trecho de 5 km recebe a concessionária cujo intervalo cobre pelo menos metade dele; quando dois contratos se sobrepõem (Concer e Elovias na BR-040; Concebra e Way 153 na BR-153/GO), vale o mais recente. Fora dos intervalos, o responsável é o **DNIT (administração direta)**. Rodovias federais delegadas a estados não constam da base da ANTT.

## 7. Condição do pavimento (ICM do DNIT)

- **Arquivos:** levantamentos de dez/2021, dez/2022, dez/2023, dez/2024, 2025 (acumulado até dez) e out/2026, só pista pavimentada.
- **Índice:** ICM = 0,7 × IP (pavimento) + 0,3 × IC (conservação).
- **Agregação:** em cada km vale o pior sentido, mesma lógica do `ICM_Unificado` dos arquivos de 2025 e 2026. No trecho de 5 km, vale a média dos km avaliados.
- **Faixas oficiais:** Bom abaixo de 30; Regular de 30 a 50; Ruim de 50 a 70; Péssimo a partir de 70.
- **Abrangência:** o ICM vale só para km sob administração do DNIT; km concedidos ficam fora.
- **Cruzamento no mesmo ano:** mortes do ano no trecho (PRF) × classe do ICM do mesmo ano. O denominador são os km avaliados em cada classe.

Resultado: 5,7 mortes por 100 km por ano em pavimento bom; 6,3 em regular; 5,7 em ruim; 2,3 em péssimo. Pavimento ruim não explica a maior parte das mortes. Recuperar pavimento é necessário, mas não reduz mortes sozinho; o ganho vem de velocidade, separação de fluxos e travessias.

## 8. Risco climático recorrente

Um trecho tem risco climático recorrente quando atende às três condições:

- ao menos 8 sinistros com chuva, neblina, fumaça, vento ou deslizamento;
- concentração na mesma janela de 3 meses em pelo menos 4 dos 5 anos completos;
- frequência na janela ao menos 1,3 vez a do resto do ano.

O pop-up do painel lista os trechos que entram na janela no mês corrente. Cada tipo de evento tem um órgão líder e órgãos de apoio (Defesa Civil, PRF, gestor da via, Corpo de Bombeiros, Ibama/Prevfogo, Cemaden/SGB).

## 9. Desastres oficiais (Defesa Civil)

Atlas Digital de Desastres no Brasil (MIDR, base S2iD consolidada 1991–2025, v1.1 de 06/08/2026). Entram os desastres que afetam rodovias: chuvas intensas, enxurradas, inundações, alagamentos, movimento de massa, erosão, vendavais, granizo, tornado e incêndio florestal. Estiagem, seca, ondas de calor e frio e doenças ficam fora. Cada trecho recebe os desastres do seu município. **Desastre recorrente:** município com desastre em pelo menos 6 dos 10 anos de 2016 a 2025 (1.739 trechos). **Dupla evidência:** trecho com risco climático recorrente na PRF e desastre recorrente no município (244 trechos, 1.941 mortes).

## 10. Risco futuro de inundação (AdaptaBrasil)

Indicador 60041 do AdaptaBrasil (MCTI/INPE): risco de impacto de inundações, enxurradas e alagamentos por município, combinando ameaça climática (chuva intensa em 1 e 5 dias), geomorfologia, uso do solo, vulnerabilidade e exposição. Arquivo exportado: 2050, cenário pessimista, 5.569 municípios classificados (Muito baixo a Muito alto). Cada trecho recebe a classe do seu município: 3.650 trechos (42% das mortes) estão em municípios com risco alto ou muito alto. **Três evidências:** risco climático recorrente na PRF, desastre recorrente na Defesa Civil e risco alto ou muito alto em 2050 (81 trechos, 691 mortes). As ações de adaptação (drenagem, greide, interdição preventiva, rota alternativa) aparecem sem custo e vidas estimados, porque não há referência publicada de efeito sobre mortes.

## 10a. Indicador nacional (SIM)

Óbitos por lesão de trânsito com causa básica CID-10 V01–V89, do arquivo Mortalidade Geral do Open Data SUS (dadosabertos.saude.gov.br/dataset/sim). 2025 (preliminar): 36.955 óbitos em 1.534.588 declarações; taxa de 17,3 por 100 mil com a população do IBGE de 2025 (213.421.037). O script `sim_transito.py` refaz a contagem a partir do arquivo oficial.

## 11. App do motorista: rota mais segura

- **Malha:** reconstruída com os pontos da PRF e ligada ao longo da mesma BR.
- **Peso de cada trecho:** km × (1 + α × risco), com α testado em 0,4, 1, 2 e 4.
- **Rota recomendada:** a de menor risco total com até 15% a mais de distância. Ela só aparece como alternativa quando evita ao menos 2 trechos críticos ou 10% das mortes registradas; senão, o app mostra uma rota só e avisa que não há caminho mais seguro.
- **Onde muda:** pontos da rota segura a mais de cerca de 4 km da rota rápida formam os trechos diferentes, destacados no mapa e descritos por cidade e BR.
- **Alertas:** de voz, 2 km antes de cada trecho alto ou crítico, com o motivo mais frequente registrado pela PRF.
- **Origem e destino:** os 5.571 municípios do IBGE, cada um ligado ao ponto mais próximo da malha federal. Quando a distância passa de 120 km, o app avisa que não há ligação por rodovia federal.
