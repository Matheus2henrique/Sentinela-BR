import json, sys
from pdfbase import *
from reportlab.platypus import Image as RLImage, PageBreak, KeepTogether, Table, TableStyle, Paragraph
sys.path.insert(0, '/home/claude/sentinela_br/docs'); from glossario import G
J = '/home/claude/tut/jpg/'
PAINEL = "https://claude.ai/artifact/74Ar4fMp9UmHrTkf3Koh4e"; APP = "https://claude.ai/artifact/3DuUMqVfPqXQMu1MqA1Dfm"
def img(n, w=17.0):
    from PIL import Image as PI
    W, H = PI.open(J + n + '.jpg').size; return RLImage(J + n + '.jpg', width=w * cm, height=w * cm * H / W)
PEND = []
def _pend():
    global PEND; x = PEND; PEND = []; return x
def fig(n, legenda, w=17.0): return KeepTogether(_pend() + [img(n, w), P(legenda, 'n')])
def par(n1, n2, l1, l2, w=5.4):
    t = Table([[img(n1, w), img(n2, w)], [P(l1, 'n'), P(l2, 'n')]], colWidths=[8.5 * cm, 8.5 * cm])
    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'TOP')])); return KeepTogether(_pend() + [t])
def passo(n, t, txt):
    global PEND; PEND = [P(f'{n}. {t}', 'h2')] + ([P(x) for x in txt] if isinstance(txt, list) else [P(txt)]); return []
CAPA = lambda tit, sub: [P('pAInel Sentinela BR', 't'), P(f'{tit} · Ministério dos Transportes · Equipe 4 · Innovathon 2026', 'st'), P(sub)]

# ================= A. Glossário das fontes + tutorial de decisão =================
st = CAPA('Glossário das fontes, links de acesso e tutorial para decisão', 'Documento para as autoridades que usam o painel: como ler cada tela para decidir, o significado de cada termo e de onde vem cada número.')
st.append(caixa("<b>Sem dados fictícios.</b> Todos os números do painel vêm de bases oficiais (PRF, DNIT, ANTT, Defesa Civil, AdaptaBrasil/MCTI, SIM/Ministério da Saúde, IBGE, Senatran) ou de publicações técnicas reconhecidas (FHWA, Trafikverket). "
                "Custos e vidas salvas são <b>estimativas</b> com método e fonte declarados, para priorizar, não orçamento de obra. "
                f"Painel: <link href='{PAINEL}' color='#0e7490'>{PAINEL}</link>."))
st.append(P('Parte 1. Tutorial para decisão', 'h1'))
st.append(P('O painel responde a cinco perguntas de quem decide. Cada uma tem um lugar na tela e uma decisão associada.'))
st.append(tabela(['Pergunta', 'Onde olhar', 'Decisão'], [
 ['Estamos no caminho da meta do Pnatrans?', 'Visão IA: projeção até 2030 e gráfico do Pnatrans', 'Tamanho do esforço e do orçamento'],
 ['Onde agir primeiro?', 'A tese (curva de concentração e mapa) e Ranking de trechos', 'Lista de trechos prioritários'],
 ['O que fazer em cada trecho?', 'Detalhe do trecho (clique no ranking ou no mapa)', 'Medida, custo, vidas salvas e responsável'],
 ['Quanto investir e com qual retorno?', 'Plano de ação', 'Orçamento e carteira de obras'],
 ['Quem precisa agir?', 'Mapa por responsável, quadro DNIT × concessionárias, Clima', 'Cobrança ao DNIT, às concessionárias (via ANTT), à PRF e à Defesa Civil']], [5.0, 6.0, 6.0]))
st.append(P('Roteiro de leitura em seis passos', 'h2'))
st += B(['<b>Confira a atualização.</b> O selo no canto superior direito mostra data e hora (8h, 14h e 18h). Passe o mouse: aparecem todas as fontes.',
         '<b>Escolha o recorte.</b> Estado, rodovia, responsável, tipo de morte, risco, pavimento e <b>Atenção especial</b>. Os filtros valem para todas as telas; <b>Limpar filtros</b> volta ao Brasil.',
         '<b>Leia "O que fazer agora".</b> Projeção, causa que mais mata, três prioridades, ganho rápido, tendência, quem age, pavimento e clima.',
         '<b>Abra os piores trechos.</b> No Ranking, clique no trecho: motivo da PRF, medida recomendada, custo, vidas salvas por ano e responsável.',
         '<b>Defina o orçamento.</b> No Plano de ação, mova a barra: o painel escolhe onde investir para salvar mais vidas e separa por responsável.',
         '<b>Acione os responsáveis.</b> DNIT, concessionária (via ANTT), PRF e Defesa Civil, conforme o mapa, o plano e a aba Clima.'])
st.append(fig('p01_topo', 'Visão IA: os quatro números do topo, "O que fazer agora" e a projeção.'))
st.append(P('Leituras que mudam decisões (dados atuais)', 'h2'))
st.append(tabela(['Achado', 'Implicação para a decisão'], [
 ['50% das mortes estão em 20% dos trechos (1.769)', 'Concentrar o orçamento nesses trechos rende mais vidas por real.'],
 ['Colisão frontal é a causa que mais mata (35%)', 'Separar sentidos (barreira central, faixa 2+1) é a medida de maior efeito.'],
 ['Radares nos 100 trechos mais críticos: R$ 38,4 mi até 2030, cerca de 72 vidas por ano', 'Ganho rápido, executável no curto prazo pelo PNCV.'],
 ['Com R$ 1 bilhão, o plano recomendado salva cerca de 593 vidas por ano', 'Ordem de grandeza do retorno para negociar orçamento.'],
 ['DNIT: 58% das mortes; 38 concessionárias federais: 42%', 'Metade da agenda passa pela fiscalização dos contratos na ANTT.'],
 ['77% das mortes da malha DNIT estão em pavimento bom; 5% em ruim ou péssimo', 'Recapear não basta: o risco está em velocidade, traçado e travessias.'],
 ['1.323 trechos com mais mortes em 2024–2025 que em 2021–2023', 'Lista de alerta para fiscalização da PRF.'],
 ['15% das mortes ocorrem com chuva, neblina, fumaça, vento ou deslizamento', 'Protocolo sazonal com Defesa Civil, PRF e gestor da via.'],
 ['244 trechos com dupla evidência: sinistros climáticos (PRF) e desastre recorrente no município (Defesa Civil), 1.941 mortes', 'Prioridade para drenagem, contenção de encosta e interdição preventiva.'],
 ['42% das mortes estão em municípios com risco alto ou muito alto de inundação em 2050 (AdaptaBrasil); 81 trechos têm as três evidências (691 mortes)', 'Prioridade máxima de adaptação: drenagem dimensionada para a chuva projetada, greide, interdição preventiva.']], [8.0, 9.0]))
st.append(PageBreak())
st.append(P('Parte 2. Glossário', 'h1'))
st.append(tabela(['Termo', 'Significado'], [[a, b] for a, b in G], [4.6, 12.4]))
st.append(PageBreak())
st.append(P('Parte 3. Fontes de dados e links de acesso', 'h1'))
st.append(P('Só aparecem as bases conectadas ao painel. <b>Integrada</b>: já alimenta o painel. <b>Referência</b>: documento de contexto. "Conferido em 23/11/2026": endereço aberto e conferido durante a construção.', 'n'))
def lk(u): return Paragraph(f"<link href='{u}' color='#0e7490'>{u}</link>", S['c'])
for s in json.load(open('/home/claude/sentinela_br/docs/fontes.json')):
    st.append(P(s['secao'], 'h2'))
    d = [[Paragraph(c, S['cb']) for c in ['Fonte', 'Órgão', 'Conteúdo e período', 'Situação', 'Link de acesso']]] + [[Paragraph(x['fonte'], S['c']), Paragraph(x['orgao'], S['c']), Paragraph(x['conteudo'], S['c']), Paragraph(x['situacao'], S['c']), lk(x['link'])] for x in s['itens']]
    t = Table(d, colWidths=[w * cm for w in (3.3, 2.2, 4.0, 2.4, 5.1)], repeatRows=1)
    t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#9aa5ab')), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eef6f8')), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4)]))
    st.append(t)
# apêndice ICM e concessões
I = json.load(open('/home/claude/sentinela_br/p6/icm.json'))
st.append(P('Arquivos do ICM (DNIT) carregados', 'h2'))
st.append(tabela(['Ano', 'Arquivo oficial', 'Linhas lidas', 'Km avaliados'], [[a, f, f'{l:,}'.replace(',', '.'), f'{k:,}'.replace(',', '.')] for a, f, l, k in I['arquivos']], [1.6, 9.4, 3.0, 3.0]))
tx = [f"{v:.1f}".replace('.', ',') for v in I['cruz']['taxa']]
st.append(P(f"Regra: {I['regra']}. Cruzamento no mesmo ano (mortes por 100 km por ano): Bom {tx[0]}; Regular {tx[1]}; Ruim {tx[2]}; Péssimo {tx[3]}.", 'n'))
sys.path.insert(0, '/home/claude/sentinela_br/p6'); from antt_concessoes import TRECHOS
Dj = json.load(open('/home/claude/sentinela_br/p6/dados.json')); ct = {c['nome']: c for c in Dj['ctab']}
st.append(PageBreak()); st.append(P('Parte 4. Quem cuida de cada rodovia federal: concessionárias (ANTT) e DNIT', 'h1'))
st.append(P('Fonte: ANTT, <i>Informações sobre os trechos concedidos</i>, arquivo 8/2026 (rodovias federais; BR, UF, km inicial e final). Fora dos intervalos abaixo, o responsável é o DNIT (administração direta). Mortes: PRF, jan/2021 a out/2026.', 'n'))
lin = []
for n in sorted(ct, key=lambda n: -ct[n]['m']):
    c = ct[n]
    if c['trechos']: lin.append([n, '; '.join(f"BR-{t['br']:03d}/{t['uf']} km {t['a']:.1f}–{t['z']:.1f}".replace('.', ',') for t in c['trechos']), f"{c['km']:,}".replace(',', '.'), f"{c['m']:,}".replace(',', '.')])
st.append(tabela(['Concessionária', 'Rodovias e km concedidos', 'Km', 'Mortes 2021–2026'], lin, [3.4, 9.6, 1.3, 2.7]))
gerar('/home/claude/entregas/Sentinela_BR_Glossario_Fontes_e_Tutorial_Decisao.pdf', 'Glossário das fontes e tutorial para decisão', st)
print('A ok')

# ================= B. Tutorial do BAI =================
st = CAPA('Tutorial do BAI (painel de decisão)', 'Passo a passo de cada tela do pAInel Sentinela BR, com as imagens do painel em funcionamento. Dados reais: PRF jan/2021 a out/2026, DNIT, ANTT, SIM/MS, IBGE e Senatran.')
st.append(caixa(f"<b>Como abrir.</b> Pelo link <link href='{PAINEL}' color='#0e7490'>{PAINEL}</link> ou pelo arquivo <b>pAInel_Sentinela_BR.html</b>, que abre com duplo clique no Chrome ou no Edge, sem internet. "
                "No projetor: <b>Windows + P</b> → Duplicar; <b>F11</b> para tela cheia; <b>Ctrl +</b> ou <b>Ctrl −</b> para ajustar o tamanho."))
st += passo(1, 'Alerta climático ao abrir', 'Se houver trechos entrando na época de risco climático recorrente, o painel abre um aviso com a lista, o órgão líder (Defesa Civil, PRF ou Bombeiros) e os órgãos de apoio. Clique em <b>Fechar</b>; o sino no topo reabre o aviso.')
st.append(fig('p00_alerta', 'Pop-up de alerta climático: trecho, evento, mortes desde 2021 e quem age.'))
st += passo(2, 'Menu lateral e selo de atualização', 'O menu à esquerda, com ícones, leva às seis telas: A tese, Visão IA, Ranking de trechos, Plano de ação, Clima e desastres, e Fontes e método. A seta no rodapé do menu recolhe a barra para mostrar só os ícones; em telas menores ela já abre recolhida. O selo mostra data e hora da última atualização (dd/mm/aaaa hh:mm); passe o mouse para ver a lista de fontes. A atualização automática roda às 8h, 14h e 18h.')
st.append(fig('p02_fontes_dica', 'Dica do selo de atualização com todas as fontes do painel.'))
st += passo(3, 'A tese: a tela de abertura', ['O painel abre nesta tela. Ela resume a tese em uma frase: <b>metade das mortes está em 20% dos trechos, e sabemos quais são, o que fazer e quem faz</b>.',
  '<b>1 · Quais são:</b> quantos trechos, quantos km, as rodovias com mais mortes. <b>2 · O que fazer:</b> vidas salvas por ano com o orçamento do Plano aplicado só nesses trechos, e a medida para cada tipo de morte. <b>3 · Quem faz:</b> DNIT e concessionárias (base ANTT), com PRF e Defesa Civil.',
  'A curva mostra a concentração; a linha tracejada é o teste fora da amostra: escolhidos só com 2021–2023, os 20% concentraram 38% das mortes de 2024–2026, quase o dobro do acaso. O mapa marca esses trechos em vermelho; clique para o detalhe. A tela acompanha os filtros: com Minas Gerais, por exemplo, mostra os 20% de Minas.'])
st.append(fig('p24_tese', 'A tese em uma tela: concentração das mortes, os três blocos de decisão, a curva e o mapa.'))
st += passo(4, 'Filtros globais e Limpar filtros', 'Estado, rodovia, responsável (DNIT, concessionárias ou uma concessionária específica), tipo de morte, nível de risco, pavimento (ICM) e <b>Atenção especial</b>, que mostra só os trechos que pedem cuidado: mortes subindo, acidente com chuva que se repete (PRF), cidade com desastre frequente (Defesa Civil) ou cidade com risco de enchente em 2050 (AdaptaBrasil); além da busca por município, BR ou km. O filtro vale para todas as telas ao mesmo tempo. O contador mostra quantos trechos e filtros estão ativos.')
st.append(fig('p12_filtro_mg', 'Exemplo: filtro Minas Gerais. Números, recomendações, gráficos e mapa mudam juntos.'))
st.append(PageBreak())
st += passo(5, 'Visão IA: números e "O que fazer agora"', ['Os quatro números do topo: mortes no recorte, mortes esperadas nos próximos 12 meses, vidas salvas por ano com o plano recomendado e concentração (Pareto).',
     '"O que fazer agora" é a leitura automática da série: projeção, causa que mais mata, três prioridades, ganho rápido, tendência, quem age, pavimento e clima. O botão <b>Gerar parecer executivo</b> escreve um parecer para subsecretários (situação, onde agir, custo e vidas, quem age, próximo passo) com os filtros aplicados. No link publicado, o texto é redigido por IA generativa só com os dados do painel; no arquivo offline, o painel monta o parecer pelas próprias regras. Há também parecer do plano e de cada trecho.'])
st.append(fig('p03_insights', '"O que fazer agora": leitura automática, sempre com o recorte dos filtros.', 13))
st.append(par('p04_proj', 'p05_pnatrans', 'Projeção nos trechos: real, se nada mudar e com o plano.', 'Pnatrans: taxa por 100 mil habitantes (SIM, 2025 preliminar: 17,3), tendência e meta de 7,8 em 2030.', 8.2))
st += passo(6, 'Mapa em três cores', 'Os botões acima do mapa trocam a cor dos pontos. <b>Risco</b>: mortes esperadas nos próximos 12 meses. <b>Responsável</b>: azul para DNIT, magenta para concessionária federal (base da ANTT por km). <b>Pavimento</b>: ICM do DNIT nas faixas oficiais. <b>Inundação 2050</b>: risco do município no AdaptaBrasil (cenário pessimista). Passe o mouse para ver o resumo; clique para abrir o detalhe.')
st.append(par('p06_mapa_risco', 'p07_mapa_dono', 'Cor por risco.', 'Cor por responsável: DNIT × concessionárias.', 8.2))
st.append(par('p08_mapa_icm', 'p22_mapa_adapta', 'Cor por pavimento (ICM); cinza = trecho concedido ou sem levantamento.', 'Cor por risco de inundação em 2050 (AdaptaBrasil, cenário pessimista).', 8.2))
st.append(PageBreak())
st += passo(7, 'Pareto, pavimento e responsáveis', 'Ainda na Visão IA: por que se morre (mecanismos e a medida que funciona para cada um), o quadro do pavimento (ICM × mortes) e o quadro "Quem cuida de cada rodovia", com uma linha por responsável e os km concedidos. Clique numa linha para filtrar o painel inteiro por aquela concessionária.')
st.append(fig('p09_pareto', 'Por que se morre: quatro mecanismos somam 85% das mortes.', 11))
st.append(fig('p10_icm', 'Pavimento × mortes: no mesmo ano do levantamento, trechos ruins não têm mais mortes por km que os bons.'))
st.append(fig('p11_donos', 'DNIT × concessionárias: mortes, trechos e km concedidos de cada contrato (ANTT).', 14))
st.append(PageBreak())
st += passo(8, 'Ranking de trechos', 'Os 30 piores trechos em cartões e, abaixo, todos os 8.847 trechos com morte (role a lista). Cada linha traz risco, mortes, mortes esperadas, motivo principal registrado pela PRF, ação recomendada e responsável.')
st.append(fig('p13_ranking', 'Top 30: mortes, esperadas por ano, anos com morte, motivo e ação com custo e vidas salvas.'))
st.append(fig('p14_todos', 'Todos os trechos com morte, ordenados pelo risco.'))
st += passo(9, 'Detalhe do trecho', 'Clique em qualquer trecho (ranking ou mapa). O painel mostra mortes por ano, como se morre, motivos da PRF, ações recomendadas com custo e vidas salvas, responsável, pavimento (ICM com a série 2021–2026) e risco climático, com o órgão líder.')
st.append(fig('p15_gaveta', 'Detalhe do trecho: tudo o que é preciso para decidir e cobrar o responsável.'))
st.append(PageBreak())
st += passo(10, 'Plano de ação', ['Mova a barra de orçamento. O critério padrão é o <b>máximo de vidas por real</b>; o alternativo, <b>trechos mais críticos primeiro</b> (pacote de obras por trecho).',
     'O painel mostra o investimento, as vidas salvas por ano e de 2027 a 2030, a parcela das mortes esperadas que o plano evita, a divisão por responsável e por medida, e a lista de ações (botão <b>Baixar plano (CSV)</b>).'])
st.append(fig('p16_plano', 'Plano de ação com R$ 1 bilhão: cerca de 593 vidas salvas por ano (estimativa).'))
st.append(fig('p17_plano_dono', 'Divisão por responsável e por medida; lista das ações selecionadas.'))
st.append(PageBreak())
st += passo(11, 'Clima e desastres', 'Mortes em sinistros com evento climático, calendário do risco por mês, quem age em cada tipo de evento (líder e apoio), a lista de trechos com risco climático recorrente e os desastres oficiais da Defesa Civil nos municípios das rodovias (Atlas Digital de Desastres/S2iD). O quadro <b>Risco futuro</b> mostra o risco de inundação em 2050 (AdaptaBrasil) e os trechos com três evidências, com as ações de adaptação e quem age. No filtro <b>Atenção especial</b>, as opções "Cidade com desastre frequente" e "Cidade com risco de enchente em 2050" levam esses recortes para todas as telas.')
st.append(fig('p18_clima', 'Calendário do risco climático e órgãos responsáveis por evento.'))
st.append(fig('p19_clima_donos', 'Quem age em cada evento e trechos com risco recorrente.'))
st.append(fig('p21_desastres', 'Desastres oficiais nos municípios das rodovias e trechos com dupla evidência (PRF e Defesa Civil).'))
st.append(fig('p23_adapta', 'Risco futuro de inundação (2050) e prioridade máxima de adaptação: três evidências no mesmo trecho.'))
st += passo(12, 'Fontes e método', 'Tabela das fontes conectadas, com link, custos e eficácia de cada medida, e o método completo (risco, plano, responsáveis, pavimento, clima).')
st.append(fig('p20_fontes', 'Fontes e método.'))
st.append(P('Boas práticas na apresentação', 'h2'))
st += B(['Comece pelo Brasil inteiro, depois filtre um estado para mostrar que tudo muda junto.', 'Abra um trecho do Top 30 e leia em voz alta: motivo, ação, custo, vidas e responsável.', 'No Plano, mostre R$ 1 bilhão e a divisão DNIT × concessionárias.', 'Feche com Fontes e método: nenhum número sem origem.'])
gerar('/home/claude/entregas/Sentinela_BR_Tutorial_BAI.pdf', 'Tutorial do BAI', st)
print('B ok')

# ================= C. Tutorial do app =================
st = CAPA('Tutorial do app do motorista · Rota Segura', 'Como usar o protótipo do aplicativo, separado do painel, e como ele vira realidade.')
st.append(caixa(f"<b>Como abrir.</b> Arquivo <b>Sentinela_BR_App_Rota_Segura.html</b> (duplo clique no Chrome ou no Edge, funciona sem internet) ou o link <link href='{APP}' color='#0e7490'>{APP}</link>. "
                "No computador, o app aparece como uma tela de celular: é a forma de mostrar no projetor sem espelhar um aparelho. No celular, o mesmo link ocupa a tela inteira. Teste o som antes: a voz dos alertas usa a voz em português do sistema."))
st.append(fig('a00_pc', 'O app no computador: tela de celular pronta para o projetor.', 15))
st += passo(1, 'Escolher origem e destino', 'Os campos <b>Saindo de</b> e <b>Destino</b> começam vazios. Toque no campo: abre a lista dos 5.571 municípios do IBGE, com as 27 capitais no topo. Digite parte do nome (sem precisar de acento) e toque na cidade, ou aperte Enter para a primeira da lista. O "×" limpa o campo. Os botões de exemplo preenchem o destino com um toque.')
st.append(par('a02_lista', 'a03_busca', 'Lista completa ao tocar no campo.', 'Busca enquanto digita: nome exato e capitais primeiro.'))
st += passo(2, 'Veículo e rotas', 'Escolha carro, moto, ônibus ou caminhão e toque em <b>Ver rotas</b>. O app compara a rota <b>Mais segura</b> (verde, recomendada) com a <b>Mais rápida</b> (azul): km, tempo sem paradas, trechos críticos e mortes registradas desde 2021. A diferença aparece embaixo: trechos críticos e mortes evitados, km a mais e <b>onde o caminho muda</b> (entre quais cidades e por qual BR); no mapa, as partes diferentes ficam destacadas. A rota segura só é sugerida quando é outro caminho de fato, evita ao menos 2 trechos críticos ou 10% das mortes registradas e tem desvio de até 15%. Quando não há alternativa (por exemplo, Belo Horizonte → Vitória), o app mostra uma só rota e avisa que os trechos críticos terão alerta de voz.')
st.append(par('a04_preenchido', 'a05_rotas', 'Curitiba - PR → Porto Alegre - RS, carro.', 'Rota segura pela BR-376/BR-101: evita 6 trechos críticos e 151 mortes com 29 km a mais.'))
st.append(par('a06_rapida', 'a14_unica', 'Tocando na rota mais rápida (BR-116), o mapa destaca o caminho dela.', 'Belo Horizonte → Vitória: não há caminho mais seguro; o app mostra uma rota só.'))
st += passo(3, 'Navegação e alertas de voz', 'Toque em <b>Iniciar</b>. O mapa acompanha o veículo; no topo, a rodovia atual e a próxima troca de via; embaixo, velocidade, km restantes, chegada e próximo alerta. Dois quilômetros antes de cada trecho perigoso, aparece o cartão com rodovia, km, cidade, motivo registrado pela PRF, mortes no ponto e o cuidado necessário, e a voz lê o aviso. <b>Simulação 1×</b> acelera para 3× e 8×; <b>Voz</b> liga e desliga; <b>Encerrar</b> termina.')
st.append(par('a07_nav', 'a08_alerta', 'Navegação: via atual, km restantes e próximo alerta.', 'Alerta: motivo da PRF, mortes no ponto e o que fazer.'))
st += passo(4, 'Chegada, pontos e moeda de troca', 'Na chegada: km percorridos, alertas recebidos, trechos críticos evitados e pontos de condução segura (10 a cada 100 km, 20 por alerta, 50 pela rota segura). Abaixo, o que os pontos podem render, marcado como <b>existe</b> (RNPC; desconto de IPVA em alguns estados) ou <b>proposta</b> (pedágio federal, caminhoneiros e ônibus, parceiros).')
st.append(par('a09_chegada', 'a10_beneficios', 'Resumo da viagem e pontos.', 'Benefícios: o que existe e o que é proposta.'))
st += passo(5, 'Meus pontos e Como funciona', 'Na barra inferior: <b>Meus pontos</b> mostra o saldo e as regras; <b>Como funciona</b> mostra os três caminhos para virar realidade.')
st.append(par('a11_pontos', 'a12_como', 'Saldo e regras dos pontos.', 'Waze for Cities, CNH do Brasil e piloto.'))
st += passo(6, 'Cidades fora da malha federal', 'Quando a cidade fica longe de rodovia federal (por exemplo, Oiapoque e Macapá), o app avisa a distância e leva a rota até o ponto mais próximo da malha.')
st.append(fig('a13_longe', 'Aviso para destino sem ligação por rodovia federal.', 5.4))
st.append(P('Como vira realidade', 'h1'))
st.append(tabela(['Etapa', 'O que é', 'Quem'], [
 ['1. Alertas no Waze', 'O Ministério, com o DNIT, publica os trechos críticos no feed oficial do Waze for Cities, programa gratuito para órgãos públicos. Uma pessoa física não cria essa camada; o órgão parceiro, sim.', 'MT, DNIT, PRF'],
 ['2. Módulo no app CNH do Brasil', 'Função "Viagem segura" no app oficial, com pontos ligados ao Registro Nacional Positivo de Condutores (RNPC).', 'Senatran, Serpro'],
 ['3. Piloto', 'Este protótipo, no navegador do celular e sem instalar, com caminhoneiros e motoristas de ônibus em corredores críticos.', 'MT, PRF, concessionárias']], [3.8, 9.8, 3.4]))
st.append(P('Limites do protótipo', 'h2'))
st += B(['O movimento do veículo é simulado; trechos, motivos e números são reais (PRF jan/2021 a out/2026).', 'A malha de rotas vem das coordenadas da PRF. Em poucos trechos sem registro (partes da BR-319 e da BR-174), a ligação usa a distância em linha reta mais 25%. A malha oficial do DNIT (SNV) substitui essa aproximação.', 'Benefícios marcados como proposta dependem de regulamentação.'])
gerar('/home/claude/entregas/Sentinela_BR_Tutorial_App.pdf', 'Tutorial do app do motorista', st)
print('C ok')
