# Fontes de dados e glossário

Só constam as bases conectadas ao painel. Nenhum dado do painel é fictício ou sintético.

- **Integrada:** já alimenta o painel.
- **Referência:** documento de contexto, não alimenta números.

"Conferido em 23/11/2026" indica que o endereço foi aberto e conferido durante a construção.

## 1. Bases que alimentam o painel

| Fonte | Órgão | Conteúdo | Situação | Link |
|---|---|---|---|---|
| Sinistros de trânsito nas rodovias federais (por ocorrência e por pessoa) | Polícia Rodoviária Federal (PRF) | Data, hora, BR, km, coordenada, causa, tipo, clima, vítimas. Jan/2021 a out/2026 | Integrada | [acessar](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf) |
| Condições do Pavimento – ICM (Índice de Condição da Manutenção) | DNIT – dados abertos | ICM por km da malha pavimentada sob administração do DNIT. Arquivos: icm_dezembro_csv (dez/2021), icm_12_2022, icm-dados-aberto-12_2023, icm-dados-abertos-12_2024, levantamentos_pavimentada_2025_12 e levantamentos_pavimentada_2026_10 | Integrada · arquivos oficiais carregados em 24/11/2026 | [acessar](https://servicos.dnit.gov.br/dadosabertos/dataset/condicoes-do-pavimento) |
| Trechos concedidos (km inicial e final), arquivo 8/2026 | ANTT – dados abertos | Responsável de cada trecho: concessionária ou DNIT | Integrada · Conferido em 23/11/2026 | [acessar](https://dados.antt.gov.br/dataset/trecho-concedido) |
| Atlas Digital de Desastres no Brasil (base S2iD 1991–2025, v1.1 de 06/08/2026) | MIDR – Defesa Civil | Desastres registrados e reconhecidos por município. No painel: chuva, inundação, enxurrada, alagamento, deslizamento, erosão, vento, granizo, tornado e incêndio florestal, 2016–2025 | Integrada · arquivo oficial carregado em 24/11/2026 | [acessar](https://atlasdigital.mdr.gov.br) |
| AdaptaBrasil – Desastres geo-hidrológicos: inundações, enxurradas e alagamentos (indicador 60041, risco de impacto) | MCTI / INPE | Risco de impacto por município com a chuva intensa projetada; exportação 2050, cenário pessimista (5.569 municípios classificados) | Integrada · arquivo oficial carregado em 24/11/2026 | [acessar](https://adaptabrasil.mcti.gov.br) |
| Metadados do indicador 60041 | INPE – catálogo de dados | Definição do indicador: ameaça climática, geomorfologia, uso do solo, vulnerabilidade e exposição | Referência | [acessar](https://data.inpe.br/geonetwork/srv/api/records/adaptabrasil60041) |
| Mortalidade (SIM) – dados abertos | Ministério da Saúde | Declarações de óbito (Mortalidade Geral 1979–2026 prévia). Óbitos de trânsito, CID-10 V01–V89: 37.150 em 2024; 36.955 em 2025 (preliminar) | Integrada · série nacional 2010–2025 (2025 preliminar, arquivo Mortalidade Geral 2025 processado em 24/11/2026) | [acessar](https://dadosabertos.saude.gov.br/dataset/sim) |
| Série de óbitos e taxa 2010–2023 | Ministério da Saúde (apresentação à Câmara, 2025) | Óbitos e taxa por 100 mil habitantes | Integrada · Conferido em 23/11/2026 | [acessar](https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/cvt/apresentacoes-em-eventos/eventos-2025/arquivos-de-eventos-2025/ap-25-08-26-marli-mesquita-minsaude) |
| Óbitos de 2024 (37.150) usados pela auditoria do TCU | SIM/MS, divulgado pelo Portal do Trânsito | Total nacional de 2024 | Integrada · Conferido em 23/11/2026 | [acessar](https://www.portaldotransito.com.br/?p=58404) |
| Estimativas de população 2024 e 2025 | IBGE | População por UF e município (1º/7). 2025: 213.421.037 habitantes | Integrada · Conferido em 23/11/2026 | [acessar](https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2024/estimativa_dou_2024.pdf) |
| Frota de veículos (dez/2024) | Senatran, publicada no Anuário Estatístico do IBGE | Frota com placa por UF e tipo | Integrada · Conferido em 23/11/2026 | [acessar](https://anuario.ibge.gov.br/images/aeb/2024/s5/2_pdf/s5t2102.pdf) |
| Frota de veículos – página oficial | Senatran / Ministério dos Transportes | Frota mensal por UF, município e tipo | Integrada | [acessar](https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-Senatran/frota-de-veiculos-2024) |
| Municípios brasileiros com código e coordenadas do IBGE | Compilação pública dos códigos do IBGE (repositório aberto) | Nome, UF, código e coordenadas dos 5.571 municípios (inclui Distrito Federal e Fernando de Noronha) (app do motorista: origem e destino) | Integrada · Conferido em 23/11/2026 | [acessar](https://github.com/kelvins/municipios-brasileiros) |

## 2. Custos de referência e eficácia das medidas

| Fonte | Órgão | Conteúdo | Situação | Link |
|---|---|---|---|---|
| Custos Médios Gerenciais (CMG) | DNIT | Tabelas trimestrais; a mais recente é de julho de 2026 | Integrada · Conferido em 23/11/2026 | [acessar](https://www.gov.br/dnit/pt-br/assuntos/planejamento-e-pesquisa/custos-referenciais/custo-medio-gerencial) |
| CMG de março de 2015 (terceira faixa: R$ 1,80 a 2,10 milhões por km) | DNIT | Base do custo da faixa adicional 2+1 (a atualizar pelo CMG vigente) | Integrada · Conferido em 23/11/2026 | [acessar](https://www.gov.br/dnit/pt-br/assuntos/planejamento-e-pesquisa/custos-e-pagamentos/custos-e-pagamentos-dnit/custo-medio-gerencial/CustosMdiosGer.MARO15.pdf) |
| SICRO abr/2026 – barreira New Jersey (R$ 326,31/m) | DNIT (consulta pela plataforma Orçamentor) | Composição 3713822 | Integrada · Conferido em 23/11/2026 | [acessar](https://www.orcamentor.com/sicro/composicoes/?page=30) |
| SICRO abr/2026 – defensa maleável simples (R$ 851,99/m) | DNIT (consulta pela plataforma Orçamentor) | Composição 3713600 | Integrada · Conferido em 23/11/2026 | [acessar](https://orcamentor.com/sicro/composicoes/3713600/) |
| Fiscalização eletrônica de velocidade (R$ 4 mil por faixa/mês) | DNIT – PNCV (divulgado pelo Setcesp, 2016) | Custo mensal por faixa monitorada | Integrada · Conferido em 23/11/2026 | [acessar](https://setcesp.org.br/noticias/fiscalizacao-eletronica-esta-garantida-nas-rodovias-federais/) |
| Passarela na BR-020 (≈ R$ 4,8 milhões) | DER-DF (Jornal de Brasília, nov/2026) | Referência de custo de travessia segura | Integrada · Conferido em 23/11/2026 | [acessar](https://jornaldebrasilia.com.br/brasilia/publicado-aviso-de-licitacao-para-construir-passarela-na-br-020/) |
| Viaduto da BR-470/SC (R$ 17,5 milhões) | DNIT (2025) | Teto de custo de interseção em desnível | Integrada · Conferido em 23/11/2026 | [acessar](https://www.gov.br/dnit/pt-br/assuntos/noticias/dnit-entrega-terceiro-viaduto-da-br-470-sc-em-2025-no-vale-do-itajai) |
| Proven Safety Countermeasures | FHWA (EUA) | Eficácia de barreira central, rotatória, sonorizadores, travessias, radares | Integrada · Conferido em 23/11/2026 | [acessar](https://highways.dot.gov/safety/proven-safety-countermeasures) |
| Barreiras centrais e vias 2+1 | Trafikverket (Suécia) | Redução de mortes com separação de sentidos | Integrada · Conferido em 23/11/2026 | [acessar](https://bransch.trafikverket.se/en/startpage/operations/Operations-road/vision-zero-academy/Key-interventions-based-on-Vision-Zero/median-barriers/) |

## 3. Referências de contexto

| Fonte | Órgão | Conteúdo | Situação | Link |
|---|---|---|---|---|
| Pnatrans – revisão e meta | Ministério dos Transportes | Meta de reduzir à metade o índice de mortes até 2030 | Referência · Conferido em 23/11/2026 | [acessar](https://www.gov.br/participamaisbrasil/revisao-pnatrans) |
| Acórdão 1799/2026-TCU-Plenário (notícia) | TCU | Auditoria do Pnatrans | Referência · Conferido em 23/11/2026 | [acessar](https://portal.tcu.gov.br/imprensa/noticias/tribunal-avalia-plano-nacional-para-reduzir-mortes-e-lesoes-no-transito) |
| Waze for Cities | Waze / Google | Canal oficial para órgãos públicos enviarem alertas e interdições | Referência · Conferido em 23/11/2026 | [acessar](https://www.waze.com/pt-BR/wazeforcities/) |
| Feed de dados de parceiros do Waze | Google | Formato e passos para publicar alertas | Referência · Conferido em 23/11/2026 | [acessar](https://developers.google.com/waze/data-feed/overview?hl=pt-br) |
| Registro Nacional Positivo de Condutores (RNPC) | Senatran (reportagem CNN Brasil) | Cadastro do bom condutor no app CNH do Brasil | Referência · Conferido em 23/11/2026 | [acessar](https://www.cnnbrasil.com.br/auto/como-funciona-e-quais-beneficios-do-cadastro-de-bom-motorista/) |
| Desconto do Bom Motorista no IPVA (RS) | Governo do Rio Grande do Sul | Até 15% de desconto para quem não tem multa | Referência · Conferido em 23/11/2026 | [acessar](https://estado.rs.gov.br/descontos-dos-programas-bom-cidadao-e-bom-motorista-chegam-a-r-288-milhoes) |

## Glossário

| Termo | Significado |
|---|---|
| BAI (Business Artificial Intelligence) | Painel que entrega a projeção e a ação recomendada, com fonte, em vez de só mostrar dados para o gestor interpretar. |
| Trecho de 5 km | Unidade de análise: rodovia, UF e intervalo de 5 km (km 0–5, 5–10...). O painel mostra os trechos com pelo menos uma morte desde 2021. |
| Mortes esperadas (próximos 12 meses) | Estimativa de risco do trecho: frequência de sinistros fatais com correção estatística (Bayes empírico) × gravidade suavizada. Evita que um único acidente grave distorça o ranking. |
| Bayes empírico | Método que aproxima trechos com pouca evidência da média do corredor (mesma BR e UF) e mantém o valor próprio dos trechos com histórico consistente. |
| Nível de risco | Crítico: 2 ou mais mortes esperadas por ano; Alto: 1 a 2; Médio: 0,4 a 1; Baixo: abaixo de 0,4. |
| Em alta | Trecho com média de mortes em 2024–2025 maior que a média de 2021–2023. |
| Pareto (80/20) | Poucos trechos concentram a maior parte das mortes: 20% dos trechos somam 50% das mortes. |
| Mecanismo (como se morre) | Agrupamento dos tipos de sinistro da PRF: colisão frontal, saída de pista e capotamento, atropelamento, colisão traseira, colisão em cruzamento e outros. |
| Vidas salvas por ano | Mortes esperadas no trecho × parcela do mecanismo tratado × eficácia da medida (estudos da FHWA e da Trafikverket). Estimativa para priorizar. |
| Custo por vida salva | Custo da medida dividido pelas vidas salvas por ano. Base do critério "máximo de vidas por real". |
| ICM (Índice de Condição da Manutenção) | Indicador do DNIT por km: 0,7 × IP (pavimento: panelas, remendos, trincas) + 0,3 × IC (conservação: roçada, drenagem, sinalização). Bom abaixo de 30; Regular 30 a 50; Ruim 50 a 70; Péssimo a partir de 70. |
| DNIT (administração direta) | Departamento Nacional de Infraestrutura de Transportes: responsável pelas rodovias federais não concedidas. |
| Concessionária federal (fiscalização ANTT) | Empresa que opera trecho de rodovia federal por contrato; a Agência Nacional de Transportes Terrestres fiscaliza o contrato. |
| Pnatrans | Plano Nacional de Redução de Mortes e Lesões no Trânsito. Meta: reduzir à metade o índice de mortes por 100 mil habitantes até 2030 (de 15,6 em 2020 para 7,8). |
| SIM | Sistema de Informações sobre Mortalidade do Ministério da Saúde; óbitos por lesão de trânsito (CID-10 V01 a V89). É o indicador oficial do Pnatrans. |
| RENAEST | Registro Nacional de Sinistros e Estatísticas de Trânsito (Senatran): sinistros de todas as vias, não só das federais. |
| PNCV | Programa Nacional de Controle Eletrônico de Velocidade do DNIT (radares). |
| SICRO | Sistema de Custos Referenciais de Obras do DNIT: preço de referência de cada serviço (por exemplo, metro de barreira ou de defensa). |
| CMG | Custo Médio Gerencial do DNIT: custo médio por km de tipos de obra (por exemplo, terceira faixa). |
| Faixa adicional 2+1 | Pista com faixa extra que alterna o sentido a cada poucos km, com barreira central: permite ultrapassar sem invadir a contramão. |
| Barreira New Jersey | Barreira de concreto que separa os sentidos e impede a colisão frontal. |
| Defensa metálica e sonorizador | Guarda-corpo lateral e faixas que vibram ao pisar na borda; reduzem saída de pista e capotamento. |
| Risco climático recorrente | Trecho com ao menos 8 sinistros com chuva, neblina, fumaça, vento ou deslizamento, concentrados na mesma janela de 3 meses em pelo menos 4 de 5 anos, com frequência 1,3 vez maior que no resto do ano. |
| Desastre recorrente (Defesa Civil) | Município com desastre que afeta rodovias (chuva, inundação, deslizamento, vento, incêndio) registrado no Atlas Digital de Desastres/S2iD em pelo menos 6 dos 10 anos de 2016 a 2025. |
| Dupla evidência | Trecho com risco climático recorrente nos sinistros da PRF e desastre recorrente no município segundo a Defesa Civil: prioridade para drenagem, contenção de encosta e interdição preventiva. |
| Risco futuro de inundação (AdaptaBrasil) | Indicador 60041 do AdaptaBrasil (MCTI/INPE): risco de impacto de inundações, enxurradas e alagamentos no município, de Muito baixo a Muito alto, com a chuva intensa projetada. No painel: 2050, cenário pessimista. |
| Três evidências (prioridade máxima de adaptação) | Trecho com risco climático recorrente na PRF, desastre recorrente no município (Defesa Civil) e risco alto ou muito alto de inundação em 2050 (AdaptaBrasil). |
| Órgão líder do evento climático | Defesa Civil (chuva, deslizamento, vento); PRF (neblina); Corpo de Bombeiros e Ibama/Prevfogo (fumaça de queimadas), sempre com o gestor da via. |
| RNPC | Registro Nacional Positivo de Condutores: cadastro de bons motoristas no app CNH do Brasil. |
| Waze for Cities | Programa gratuito do Waze para órgãos públicos publicarem alertas e interdições no aplicativo. |
| Atualização automática | Rotina que baixa as bases e recalcula o painel às 8h, 14h e 18h (Brasília) e consulta os avisos do INMET de hora em hora. |
