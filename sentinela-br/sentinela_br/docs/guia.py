from pdfbase import *

PAINEL = "https://claude.ai/artifact/74Ar4fMp9UmHrTkf3Koh4e"
APP = "https://claude.ai/artifact/3DuUMqVfPqXQMu1MqA1Dfm"
st = [P("pAInel Sentinela BR", "t"), P("Guia da apresentação, simulação do app no computador e roadmap · Ministério dos Transportes · Equipe 4 · Innovathon 2026", "st")]
st.append(caixa(f"<b>Links.</b> Painel: <link href='{PAINEL}' color='#0e7490'>{PAINEL}</link><br/>App do motorista (emulador de celular): <link href='{APP}' color='#0e7490'>{APP}</link><br/>"
                "<b>Sem internet:</b> os arquivos pAInel_Sentinela_BR.html e Sentinela_BR_App_Rota_Segura.html abrem com duplo clique no Chrome ou no Edge e funcionam offline. "
                "Os links abrem com a conta do Claude que publicou; para outra pessoa abrir, use o botão Compartilhar."))

st.append(P("1. Antes de entrar na sala (15 minutos)", "h1"))
st.append(tabela(["Item", "Como fazer", "Ok"], [
    ["Notebook carregado e na tomada", "Desative o modo de economia de energia e a suspensão de tela.", "☐"],
    ["Arquivos no notebook", "Copie para a área de trabalho: pAInel_Sentinela_BR.html, Sentinela_BR_App_Rota_Segura.html e os dois vídeos (painel e app). Leve cópia em pen drive.", "☐"],
    ["Duas janelas", "Janela 1: painel. Janela 2: app do motorista (o celular aparece na tela do computador). Não precisa de celular nem de espelhamento.", "☐"],
    ["Som", "Ligue o som do notebook. No app, a voz dos alertas usa a voz em português do Windows (no Edge, a voz Francisca soa mais natural).", "☐"],
    ["Plano B", "Se algo falhar, rode os vídeos: painel (2 min 59 s) e app (1 min 53 s).", "☐"]], [4.2, 11.0, 1.8]))

st.append(P("2. Ligar no projetor (Data Show)", "h1"))
st += B(["Conecte o cabo HDMI e pressione <b>Windows + P</b>. Escolha <b>Duplicar</b>, para ver no notebook o mesmo que a banca vê.",
         "Resolução recomendada: 1920 × 1080. Se o projetor for antigo, 1280 × 720 também funciona: o celular do app se ajusta sozinho à altura da tela.",
         "No navegador, pressione <b>F11</b> para tela cheia. Ajuste o zoom com <b>Ctrl + (mais)</b> ou <b>Ctrl − (menos)</b> até o texto ficar legível do fundo da sala.",
         "Para alternar entre painel e app durante a fala, use <b>Alt + Tab</b>."])

st.append(P("3. Roteiro de 7 minutos", "h1"))
st.append(tabela(["Tempo", "Tela", "O que mostrar e dizer"], [
    ["0:00", "Painel · A tese", "Abra na tela <b>A tese</b> e leia a frase: \"Metade das mortes está em 20% dos trechos. Sabemos quais são, o que fazer e quem faz.\" Aponte os três blocos (1.769 trechos; vidas salvas por ano com o orçamento; DNIT e 38 concessionárias), a curva e o mapa. Feche com o teste: escolhidos só com 2021–2023, os mesmos 20% concentraram 38% das mortes de 2024–2026."],
    ["1:00", "Visão IA", "\"O pAInel Sentinela BR é um BAI: Business Artificial Intelligence.\" Leia 2 ou 3 itens de \"O que fazer agora\". Mostre a projeção até 2030 e o gráfico do Pnatrans: o Brasil está longe da meta. Passe o mouse no selo de atualização: aparecem todas as fontes."],
    ["1:45", "Mapa, responsáveis e pavimento", "No mapa, clique em <b>Cor: responsável</b> (azul DNIT, magenta concessionária, base ANTT por km) e em <b>Cor: pavimento (ICM)</b>. Mostre o quadro do pavimento: pavimento ruim não explica as mortes. Em \"Quem cuida de cada rodovia\", clique em uma concessionária: o painel inteiro filtra."],
    ["2:30", "Ranking de trechos", "Os 30 piores trechos. Clique no primeiro: mortes por ano, como se morre, motivo da PRF, ação recomendada, custo, vidas salvas e dono."],
    ["3:30", "Plano de ação", "Mova o orçamento (por exemplo, R$ 1 bilhão). Mostre vidas salvas por ano, divisão por responsável e a lista de ações."],
    ["4:15", "Clima e desastres", "Calendário do risco climático e quem age em cada evento. Mostre os desastres oficiais (Defesa Civil) e o risco de inundação em 2050 (AdaptaBrasil): 81 trechos com três evidências são a prioridade máxima de adaptação."],
    ["5:00", "App do motorista", "Alt + Tab para a janela do app e faça a simulação do item 4."],
    ["6:30", "Fontes e método", "Tudo vem de base oficial; custos e vidas são estimativas com fonte. Atualização automática às 8h, 14h e 18h."]], [1.4, 3.2, 12.4]))

st.append(P("4. Simulação do app no computador, passo a passo", "h1"))
st += B(["A tela mostra um celular, como se estivesse espelhado. Tudo é clicado com o mouse.",
         "Toque em <b>Saindo de</b> e escolha a cidade na lista dos 5.571 municípios (por exemplo, Curitiba - PR); faça o mesmo em <b>Destino</b> (Porto Alegre - RS). Escolha o veículo: carro, moto, ônibus ou caminhão.",
         "Toque em <b>Ver rotas</b>. O app mostra a rota <b>Mais segura</b> (verde, recomendada) e a <b>Mais rápida</b> (azul), com km, tempo, trechos críticos, mortes registradas e por qual BR cada uma passa; embaixo, onde o caminho muda. Bom exemplo: Curitiba → Porto Alegre, a rota segura pela BR-376/BR-101 evita 6 trechos críticos e 151 mortes com 29 km a mais. Quando não há caminho mais seguro (Belo Horizonte → Vitória), o app mostra uma rota só e explica.",
         "Toque em <b>Iniciar</b>. O carro anda no mapa. Dois quilômetros antes de cada trecho perigoso, aparece o cartão laranja ou vermelho com rodovia, km, cidade, motivo registrado pela PRF, número de mortes e o cuidado necessário; a voz lê o aviso.",
         "O botão <b>Simulação 1×</b> acelera para 3× e 8×. <b>Voz</b> liga e desliga o som. <b>Encerrar</b> termina a viagem.",
         "Na chegada, aparecem os pontos de condução segura e o que eles podem render (RNPC e IPVA, que existem; pedágio e frotas, como proposta). A aba <b>Como funciona</b> mostra os três caminhos para virar realidade."])
st.append(caixa("<b>Importante para a banca.</b> O movimento do carro é simulado; os trechos, os motivos e os números são reais (PRF 2021–2026). "
                "A malha de rotas foi reconstruída com as coordenadas da PRF; nos poucos trechos sem registro da PRF (por exemplo, partes da BR-319 e da BR-174), a ligação usa a distância em linha reta acrescida de 25%. A malha oficial do DNIT (SNV) substitui essa aproximação no roadmap."))

st.append(P("5. Como vira produto de verdade: roadmap", "h1"))
st.append(tabela(["Prazo", "Entrega", "Quem"], [
    ["30 dias", "Liberar o acesso às bases (RENAEST, SIM, DNIT, INMET, S2iD, AdaptaVias) e ligar a atualização automática às 8h, 14h e 18h no servidor do Ministério ou da Serpro.", "MT (SGETI), Senatran, Serpro"],
    ["60 dias", "Ligar o download automático do ICM do DNIT (já integrado com os arquivos de 2021 a out/2026) e integrar a malha oficial do DNIT (SNV). Alertas do INMET em tempo real, com aviso à Defesa Civil, à PRF e ao gestor da via.", "MT, DNIT, INMET, Defesa Civil"],
    ["90 dias", "Feed oficial no Waze for Cities com os trechos perigosos e os motivos. O Waze mostra o alerta; a rota mais segura fica no app do governo.", "DNIT, PRF, Waze"],
    ["120 dias", "Módulo Viagem Segura no app CNH do Brasil, com a rota mais segura, os avisos por voz e a pontuação de direção segura ligada ao RNPC.", "Senatran, Serpro"],
    ["180 dias", "Incentivos: desconto no IPVA nos estados que aderirem, parceiros do RNPC, proposta de desconto em pedágio na regulação da ANTT e programa para frotas de ônibus e caminhões.", "Senatran, estados, ANTT, mercado"],
    ["Contínuo", "Medir: mortes por ano em cada trecho tratado, antes e depois, e a taxa oficial do Pnatrans.", "MT e Senatran"]], [2.0, 11.0, 4.0]))

st.append(P("6. Por que o motorista vai usar: incentivos", "h1"))
st.append(tabela(["Incentivo", "Situação", "Como funciona"], [
    ["RNPC na CNH do Brasil", "Existe hoje", "O Registro Nacional Positivo de Condutores (Lei 14.071/2020) já está no app CNH do Brasil e dá acesso a benefícios de órgãos e empresas parceiras."],
    ["Desconto no IPVA", "Existe em alguns estados", "Rio Grande do Sul, Pará e Amazonas já premiam o bom condutor (no RS, até 15%). Proposta: somar a pontuação de uso do app."],
    ["Renovação da CNH", "Existe em alguns DETRAN", "Desconto na renovação para bons condutores. Proposta: incluir o uso do app como critério."],
    ["Pedágio", "Proposta", "Tarifa reduzida para quem acumula pontos, a ser estudada pela ANTT nas concessões."],
    ["Caminhoneiros e ônibus", "Proposta", "Pontos de parada e descanso na rota; empresas de transporte e embarcadores valorizam frotas com uso comprovado do app."]], [3.6, 3.2, 10.2]))

st.append(P("7. Perguntas prováveis da banca", "h1"))
st.append(tabela(["Pergunta", "Resposta curta"], [
    ["Os dados são reais?", "Sim. Mortes e trechos vêm da PRF; o indicador do Pnatrans, do SIM e do IBGE; a frota, da Senatran. Custos e vidas salvas são estimativas com fonte citada (DNIT, FHWA, Suécia)."],
    ["Por que confiar na previsão?", "O risco de cada trecho usa toda a série 2021–2026 com correção estatística (Bayes empírico), para não exagerar trechos com um único acidente grave."],
    ["Quem é o responsável por cada trecho?", "A base oficial da ANTT de trechos concedidos (BR, UF, km inicial e final) define a concessionária de cada trecho; fora desses intervalos, DNIT. Concessões: 42% das mortes; DNIT: 58%."],
    ["E a condição do pavimento?", "O ICM do DNIT (2021 a out/2026) está integrado: 77% das mortes da malha DNIT estão em pavimento bom e 5% em ruim ou péssimo. No mesmo ano do levantamento, trechos ruins não têm mais mortes por km. Recapear é necessário, mas não basta."],
    ["Quanto custa e quantas vidas salva?", "No plano recomendado, com R$ 1 bilhão, cerca de 600 vidas por ano pelo critério de custo-efetividade (estimativa)."],
    ["Por que não só um dashboard?", "Nenhum país reduziu mortes só com painel. O Sentinela junta dado único, risco por trecho, plano com custo e vidas e indicador de resultado (ver o documento acessório)."],
    ["Como isso ajuda no Acórdão do TCU?", "Atende à gestão de riscos, à padronização de dados e aos indicadores de resultado. O resumo está no documento acessório."]], [5.0, 12.0]))
gerar("/home/claude/sentinela_br/docs/Sentinela_BR_Guia_Apresentacao_e_App.pdf", "Guia da apresentação e do app", st)
print("ok")
