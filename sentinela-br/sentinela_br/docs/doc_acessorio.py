from pdfbase import *

st = []
st += [P("pAInel Sentinela BR", "t"), P("Documento acessório · Acórdão 1799/2026-TCU-Plenário, benchmark internacional e glossário de fontes · Ministério dos Transportes · Equipe 4 · Innovathon · Brasília, 24/11/2026", "st")]
st.append(caixa("<b>Para que serve este documento.</b> O pAInel trata do problema: onde, por que e quando se morre nas rodovias, e o que fazer. "
                 "Este acessório reúne, em separado, o que a banca pode querer citar: o resumo do Acórdão do TCU sobre o Pnatrans, o que outros países usam para reduzir mortes e de onde vem cada dado."))

# ---------------- 1. Acórdão
st.append(P("1. Resumo do Acórdão 1799/2026-TCU-Plenário", "h1"))
st.append(tabela(["Item", "Conteúdo"], [
    ["Processo", "TC 021.469/2025-3"], ["Relator", "Ministro Antonio Anastasia"], ["Sessão", "8/7/2026 (Plenário); notícia publicada em 15/7/2026"],
    ["Objeto", "Avaliar a formulação, a implementação e o alcance das metas do Plano Nacional de Redução de Mortes e Lesões no Trânsito (Pnatrans)"],
    ["Foco", "Secretaria Nacional de Trânsito (Senatran), responsável por coordenar, supervisionar e monitorar o plano"],
    ["Base legal", "Lei 13.614/2018 (institui o Pnatrans)"],
    ["Meta do plano", "Reduzir em pelo menos 50% o índice de mortes no trânsito por 100 mil habitantes até 2030, em comparação com 2020"],
    ["Potencial citado", "Até 86 mil vidas salvas entre 2021 e 2030 e economia de R$ 260 bilhões para a sociedade"]], [3.5, 13.5]))
st.append(P("Principais achados", "h2"))
st += B(["Coordenação frágil entre União, estados, DF e municípios; a Senatran não tem instrumentos para exigir implementação, envio de dados e reporte.",
         "Baixa adesão: só 60 dos 5.570 municípios registravam ações do Pnatrans; em 2025, só 8 dos 27 Cetran enviaram os relatórios.",
         "Não há processo estruturado de gestão de riscos no plano.",
         "A Câmara Temática não tem regras mínimas de funcionamento.",
         "Dados com limitações de qualidade, cobertura e padronização.",
         "Capacidade institucional limitada da Senatran (pessoal, planejamento, tecnologia).",
         "Indicadores medem atividades e produtos, e não a contribuição para reduzir mortes.",
         "Faltam critérios para priorizar fatores de risco e usuários vulneráveis.",
         "Recursos de segurança viária difíceis de rastrear no orçamento."])
st.append(P("Quem deve cumprir e o quê", "h2"))
st.append(tabela(["Destinatário", "Tipo", "O que fazer", "Prazo"], [
    ["Senatran", "Determinação", "Instituir processo estruturado de gestão de riscos para o Pnatrans", "Até 360 dias"],
    ["Senatran", "Determinação", "Padronizar nacionalmente os dados sobre sinistros de trânsito", "Não informado na notícia"],
    ["Senatran", "Determinação", "Levantar os programas e recursos orçamentários ligados à segurança viária", "Não informado na notícia"],
    ["Órgãos do Pnatrans", "Recomendação", "Aprimorar coordenação, monitoramento, indicadores e desenho do plano, com critérios para priorizar usuários e fatores de risco", "–"],
    ["Ministério dos Transportes com o Ministério do Planejamento e Orçamento", "Recomendação", "Identificar as programações orçamentárias ligadas ao Pnatrans", "–"]], [3.6, 2.6, 8.0, 2.8]))
st.append(P("Como o pAInel Sentinela BR ajuda a cumprir", "h2"))
st.append(tabela(["Exigência", "Contribuição do pAInel"], [
    ["Gestão de riscos", "Cada trecho de 5 km com mortes vira um risco com probabilidade, impacto, causa, medida e órgão responsável."],
    ["Padronização de dados", "Chave única de localização (rodovia, km, coordenada) para cruzar PRF, RENAEST, SIM/DataSUS, ANTT e DNIT."],
    ["Indicadores de resultado", "Mortes por ano em cada trecho tratado, antes e depois da medida; taxa por 100 mil habitantes e por 10 mil veículos."],
    ["Priorização", "Pareto 80/20: poucos trechos e poucas medidas concentram a maior parte das mortes."]], [4.2, 12.8]))
st.append(P("Fonte: notícia oficial do TCU (portal.tcu.gov.br, 15/7/2026). Para citações formais, consultar o inteiro teor do Acórdão.", "n"))

# ---------------- 2. Benchmark
st.append(PageBreak())
st.append(P("2. Benchmark internacional: o que os países usam para reduzir mortes", "h1"))
st.append(caixa("<b>Resposta direta:</b> nenhum país reduziu mortes com um dashboard sozinho. Os que avançaram combinam quatro peças: "
                 "(1) base de dados única e padronizada; (2) mapa de risco por trecho; (3) plano de investimento com custo e vidas salvas por medida; "
                 "(4) indicadores de resultado acompanhados com regularidade. O painel é a vitrine dessas peças."))
st.append(Spacer(1, 6))
st.append(tabela(["País ou programa", "O que usam", "É um dashboard?", "Resultado ou evidência", "O que serve ao Brasil"], [
    ["Suécia · Visão Zero (Trafikverket)", "Estrada 2+1 com barreira central em rodovias de pista simples", "Não. Política de engenharia com avaliação antes e depois",
     "Avaliação de 2009: mortes caíram 77% nas vias convertidas", "Colisão frontal é a 1ª causa de morte nas BRs (31% das mortes, PRF)"],
    ["EUA · FHWA", "Catálogo de 28 medidas comprovadas, com fatores de redução (CMF Clearinghouse)", "Não. Catálogo técnico de eficácia",
     "Barreira central: −97% de colisões que cruzam o canteiro; rotatória: −78% a −82% de colisões graves", "Base para estimar vidas salvas por medida"],
    ["iRAP · ViDA (mais de 100 países)", "Classificação por estrelas da via, estimativa de mortes e lesões graves e plano de investimento por segmento de 100 m", "Sim, plataforma online gratuita com análise econômica",
     "Estudo da Johns Hopkins: cerca de 700 mil mortes e lesões graves evitadas em projetos com o método", "Melhor encaixe para orçamento e vidas salvas por trecho"],
    ["Nova Zelândia · MegaMaps (NZTA)", "Mapa geoespacial com limites de velocidade, risco de colisão, risco da infraestrutura, velocidade média e volume", "Sim, ferramenta geoespacial para os gestores das vias",
     "Base do programa de velocidade e infraestrutura; meta de −40% em mortes e lesões graves até 2030", "Modelo para velocidade segura por trecho"],
    ["França · controle automatizado", "Radares automáticos com processamento centralizado das multas, desde 2003", "Não. Sistema de fiscalização",
     "Avaliação de 2013: 75% da queda da mortalidade entre 2003 e 2010 atribuída ao controle de velocidade", "Fiscalização eletrônica nos trechos críticos"],
    ["Reino Unido · STATS19 (DfT)", "Padrão nacional único de registro policial, dados abertos, painel interativo e indicadores de desempenho", "Sim, painel e ferramentas de mapa e download",
     "Fonte oficial dos indicadores da estratégia nacional", "Padrão único de dado (determinação do TCU)"],
    ["União Europeia · Observatório (CARE e KPIs)", "Base harmonizada dos países e 8 indicadores-chave de desempenho", "Sim, observatório com dados e indicadores",
     "Projeto Trendline com 25 Estados-membros coletando os KPIs", "Indicadores de resultado, não de atividade"],
    ["Índia · iRAD/eDAR", "Base única integrando polícia, saúde, transporte e órgãos rodoviários; app com GPS e fotos; alerta ao engenheiro da via", "Sim, app de registro e painel de análise",
     "Em operação nos 36 estados e territórios; apoio do Banco Mundial", "Modelo para um RENAEST integrado com saúde e DNIT/ANTT"],
    ["Colômbia · Observatório Nacional (ANSV)", "SINIDATA e Tablero BI, com análise por corredor (ANI e INVIAS)", "Sim, painel BI e plataforma de dados",
     "Publica dados quase em tempo real e corredores críticos", "Referência regional próxima da realidade brasileira"]], [3.0, 3.6, 2.6, 4.0, 3.8]))
st.append(P("O que se encaixa melhor para o Brasil", "h2"))
st += B(["<b>Dado único (Índia e Reino Unido):</b> RENAEST como base nacional, integrada a PRF, SIM/SIH (saúde), DNIT e ANTT pela mesma chave de localização. Responde à determinação de padronizar dados.",
         "<b>Risco e investimento por trecho (iRAP e Nova Zelândia):</b> cada trecho com sua medida, custo e vidas salvas estimadas. Responde à determinação de gestão de riscos.",
         "<b>Medidas comprovadas (Suécia, EUA e França):</b> separar sentidos, proteger a saída de pista, travessias seguras e fiscalização eletrônica de velocidade.",
         "<b>Indicadores de resultado (União Europeia):</b> mortes por trecho tratado, antes e depois, além da taxa oficial do Pnatrans.",
         "<b>Alerta ao motorista:</b> o DNIT já usa o Waze for Cities para avisar sobre escolas à beira das BRs, cruzando dados com a PRF. O mesmo canal leva os alertas do Sentinela."])

st.append(P("3. Medidas com eficácia comprovada", "h1"))
st.append(tabela(["Medida", "Efeito publicado", "Fonte", "Problema que ataca nas BRs (mortes 2021–out/2026, PRF)"], [
    ["Barreira central / estrada 2+1", "−97% de colisões que cruzam o canteiro (EUA); −77% de mortes (Suécia)", "FHWA; Trafikverket", "Colisão frontal e lateral em sentido oposto: 35%"],
    ["Sonorizadores no eixo e na borda", "−44% de colisões frontais graves; −36% de saídas de pista graves", "FHWA", "Frontal e saída de pista"],
    ["Rotatória no lugar de cruzamento", "−78% a −82% de colisões com feridos ou mortos", "FHWA", "Colisão transversal: 7,9%"],
    ["Canteiro e ilha de refúgio para pedestre", "−46% de atropelamentos em faixas marcadas", "FHWA", "Atropelamento: 15,5%"],
    ["Sinalização de curva (chevrons)", "−16% de colisões com vítimas fora de interseções", "FHWA", "Saída de pista: 11,9%"],
    ["Fiscalização eletrônica de velocidade", "75% da queda de mortalidade na França (2003–2010) atribuída ao controle de velocidade", "Governo francês (avaliação de 2013)", "Velocidade, traseiras e todas as colisões graves"],
    ["Auditoria de segurança viária", "Até −60% de colisões nos locais auditados", "FHWA", "Todos os tipos"]], [3.8, 5.0, 2.8, 5.4]))
st.append(P("Os percentuais das BRs são da base aberta da PRF (tipo do sinistro com morte). Os efeitos vêm de estudos de outros países e servem de premissa até a avaliação brasileira, trecho a trecho.", "n"))

# ---------------- 4. Glossário de fontes
st.append(PageBreak())
st.append(P("4. Glossário das fontes", "h1"))
st.append(P("<b>No painel</b>: já integrada. <b>A integrar</b>: base oficial e aberta, pronta para entrar assim que o download for liberado no ambiente de processamento. <b>Referência</b>: usada para método, eficácia ou contexto."))
F = [
 ["PRF – sinistros por ocorrência", "Polícia Rodoviária Federal", "Cada sinistro nas BRs: data, hora, local (BR, km, coordenada), causas, tipo, clima e vítimas", "2021–out/2026", "No painel", "gov.br/prf › Dados abertos"],
 ["SIM – Sistema de Informações sobre Mortalidade", "Ministério da Saúde (DataSUS)", "Óbitos por lesão de trânsito (CID-10 V01–V89). Base do indicador oficial do Pnatrans", "Série 2010–2024 no painel; microdados a integrar", "No painel / A integrar", "opendatasus.saude.gov.br"],
 ["SIH – internações", "Ministério da Saúde (DataSUS)", "Internações e custos hospitalares por lesão de trânsito", "2021–2025", "A integrar", "datasus.saude.gov.br"],
 ["RENAEST", "Senatran", "Registro nacional de sinistros de todas as vias (federais, estaduais e municipais): sinistros, localidade, veículos e vítimas", "2021–2026", "A integrar", "dados.transportes.gov.br › RENAEST"],
 ["Estimativas de população", "IBGE", "População por município e UF (1º/7/2024)", "2024", "No painel", "ftp.ibge.gov.br › Estimativas_2024"],
 ["Frota de veículos", "Senatran", "Frota com placa por UF, município e tipo", "dez/2024", "No painel", "gov.br/transportes › Frota de veículos"],
 ["Trechos concedidos", "ANTT", "Concessionária, rodovia, UF e km inicial e final de cada trecho concedido", "Atual", "A integrar", "dados.antt.gov.br › trecho-concedido"],
 ["SNV – Sistema Nacional de Viação", "DNIT", "Malha federal oficial: trechos, extensão, pista simples ou dupla, pavimento", "Versão vigente", "A integrar", "gov.br/dnit › PNV e SNV"],
 ["PNCT – contagem de tráfego (VMDa)", "DNIT", "Volume médio diário de veículos por posto", "2021–2025", "A integrar", "servicos.dnit.gov.br › dadospnct"],
 ["Estações e histórico climático (BDMEP)", "INMET", "Chuva, temperatura e vento por estação, hora a hora", "2021–2026", "A integrar", "bdmep.inmet.gov.br"],
 ["Alertas meteorológicos e API", "INMET", "Avisos de chuva forte, ventania e outros em tempo real", "Tempo real", "A integrar (servidor)", "alertas2.inmet.gov.br; apitempo.inmet.gov.br"],
 ["S2iD e Atlas Digital de Desastres", "MIDR – Defesa Civil", "Desastres registrados por município (deslizamentos, inundações, enxurradas)", "1991–2025", "A integrar", "s2id.mi.gov.br; atlasdigital.mdr.gov.br"],
 ["AdaptaVias", "Ministério dos Transportes", "Índice de Risco Climático das rodovias federais (deslizamento, erosão, inundação), cenários atuais e futuros", "Estudo publicado", "A integrar", "gov.br/transportes › Projeto AdaptaVias"],
 ["AdaptaBrasil", "MCTI", "Plataforma pública que recebe os resultados do AdaptaVias", "Atual", "A integrar", "adaptabrasil.mcti.gov.br"],
 ["Monitoramento de áreas de risco", "Cemaden", "Municípios monitorados e alertas de risco geo-hidrológico", "Atual", "A integrar", "gov.br/cemaden"],
 ["Pnatrans", "Senatran / Contran", "Metas, pilares e plano de ações (Lei 13.614/2018)", "2021–2030", "Referência", "gov.br/transportes › Pnatrans"],
 ["Acórdão 1799/2026-TCU-Plenário", "TCU", "Auditoria do Pnatrans", "2026", "Referência", "portal.tcu.gov.br"],
 ["Medidas comprovadas e CMF Clearinghouse", "FHWA (EUA)", "Eficácia das medidas de engenharia", "Atual", "Referência", "highways.dot.gov › proven-safety-countermeasures"],
 ["ViDA / Star Rating", "iRAP", "Método de risco da via e plano de investimento", "Atual", "Referência", "irap.org › ViDA"],
 ["Visão Zero e estrada 2+1", "Trafikverket (Suécia)", "Avaliação de barreira central e 2+1", "1998–2019", "Referência", "bransch.trafikverket.se"],
 ["MegaMaps", "NZTA (Nova Zelândia)", "Mapa de risco e velocidade segura", "Atual", "Referência", "nzta.govt.nz › MegaMaps"],
 ["STATS19", "DfT (Reino Unido)", "Padrão nacional de dados e painel", "Atual", "Referência", "gov.uk › road safety data"],
 ["Observatório Europeu e KPIs", "Comissão Europeia", "Indicadores-chave de segurança viária", "2021–2030", "Referência", "road-safety.transport.ec.europa.eu"],
 ["iRAD / eDAR", "MoRTH (Índia)", "Base integrada polícia, saúde, transporte e rodovias", "Atual", "Referência", "irad.parivahan.gov.in"],
 ["Observatório Nacional de Segurança Viária", "ANSV (Colômbia)", "Painel BI e SINIDATA", "Atual", "Referência", "ansv.gov.co › observatorio"],
 ["Waze for Cities", "Waze / Google", "Canal oficial para órgãos públicos enviarem alertas e interdições", "Atual", "Referência", "waze.com/pt-BR/wazeforcities"],
 ["RNPC – Registro Nacional Positivo de Condutores", "Senatran", "Cadastro do bom condutor (Lei 14.071/2020), base para benefícios no app CNH do Brasil", "Desde 2022", "Referência", "Portal de Serviços da Senatran; app CNH do Brasil"],
]
st.append(tabela(["Fonte", "Órgão", "O que traz", "Período", "Situação", "Onde obter"], F, [3.2, 2.4, 4.6, 2.0, 1.9, 2.9]))
st.append(P("Glossário de termos", "h2"))
st.append(tabela(["Termo", "Significado"], [
    ["Pnatrans", "Plano Nacional de Redução de Mortes e Lesões no Trânsito. Meta: metade da taxa de mortes por 100 mil habitantes até 2030, sobre 2020."],
    ["Taxa por 100 mil habitantes", "Óbitos do SIM no ano ÷ população do IBGE × 100.000. Indicador oficial do Pnatrans."],
    ["Taxa por 10 mil veículos", "Óbitos ÷ frota × 10.000. Segundo indicador previsto no Pnatrans."],
    ["CID-10 V01–V89", "Códigos de causa de morte por acidente de transporte terrestre usados pelo SIM."],
    ["Trecho de 5 km", "Unidade de análise do pAInel: rodovia, UF e quilômetro, em blocos de 5 km."],
    ["Pareto 80/20", "Poucas causas ou locais concentram a maior parte do problema; tratá-los primeiro gera mais vidas salvas por real investido."],
    ["Sistema Seguro", "Abordagem adotada pelo Pnatrans: a via deve perdoar o erro humano para que ele não seja fatal."],
    ["Fator de redução (CMF)", "Percentual de colisões evitadas por uma medida, medido em estudos antes e depois."],
    ["Estrada 2+1", "Pista com três faixas alternando a de ultrapassagem e barreira entre os sentidos."],
    ["VMDa", "Volume médio diário anual de veículos num trecho."],
    ["Índice de Risco Climático", "Indicador do AdaptaVias que combina ameaça climática, exposição e vulnerabilidade da rodovia."],
    ["RNPC", "Registro Nacional Positivo de Condutores: quem não comete infração há 12 meses pode receber benefícios."]], [4.0, 13.0]))
gerar("/home/claude/sentinela_br/docs/Sentinela_BR_Documento_Acessorio.pdf", "Documento acessório", st)
print("ok")
