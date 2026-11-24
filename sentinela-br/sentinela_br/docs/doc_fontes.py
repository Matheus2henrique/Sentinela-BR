from pdfbase import *
from reportlab.platypus import Paragraph

def lk(u):
    return Paragraph(f"<link href='{u}' color='#0e7490'>{u}</link>", S["c"])
def tab(linhas, larg=(3.3, 2.2, 4.0, 2.4, 5.1)):
    cab = ["Fonte", "Órgão", "Conteúdo e período", "Situação", "Link de acesso"]
    dados = [[Paragraph(c, S["cb"]) for c in cab]] + [[Paragraph(a, S["c"]), Paragraph(b, S["c"]), Paragraph(c, S["c"]), Paragraph(d, S["c"]), lk(e)] for a, b, c, d, e in linhas]
    t = Table(dados, colWidths=[w * cm for w in larg], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa5ab")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef6f8")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t

C = "Conferido em 23/11/2026"
st = [P("pAInel Sentinela BR", "t"), P("Fontes de dados e links de acesso · Ministério dos Transportes · Equipe 4 · Innovathon 2026", "st")]
st.append(caixa("Todas as fontes abaixo são oficiais ou publicações técnicas reconhecidas. <b>Integrada</b>: já alimenta o painel. "
                "<b>A integrar</b>: base oficial e aberta que entra na atualização automática (8h, 14h e 18h) assim que o acesso for liberado no ambiente de processamento. "
                f"Na coluna Situação, \"{C.lower()}\" indica que o endereço foi aberto e conferido durante a construção do painel."))

st.append(P("1. Bases que alimentam o painel", "h1"))
st.append(tab([
 ["Sinistros de trânsito nas rodovias federais (por ocorrência e por pessoa)", "Polícia Rodoviária Federal (PRF)", "Data, hora, BR, km, coordenada, causa, tipo, clima, vítimas. Jan/2021 a out/2026", "Integrada", "https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf"],
 ["Mortalidade (SIM) – dados abertos", "Ministério da Saúde", "Óbitos por lesão de trânsito, CID-10 V01–V89; microdados por município", f"Integrada (série nacional) · {C}", "https://www.gov.br/saude/pt-br/acesso-a-informacao/sic/dados-em-transparencia-ativa/svsa/mortalidade"],
 ["Série de óbitos e taxa 2010–2023", "Ministério da Saúde (apresentação à Câmara, 2025)", "Óbitos e taxa por 100 mil habitantes", f"Integrada · {C}", "https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/cvt/apresentacoes-em-eventos/eventos-2025/arquivos-de-eventos-2025/ap-25-08-26-marli-mesquita-minsaude"],
 ["Óbitos de 2024 (37.150) usados pela auditoria do TCU", "SIM/MS, divulgado pelo Portal do Trânsito", "Total nacional de 2024", f"Integrada · {C}", "https://www.portaldotransito.com.br/?p=58404"],
 ["Estimativas de população 2024", "IBGE", "População por UF e município (1º/7/2024)", f"Integrada · {C}", "https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2024/estimativa_dou_2024.pdf"],
 ["Frota de veículos (dez/2024)", "Senatran, publicada no Anuário Estatístico do IBGE", "Frota com placa por UF e tipo", f"Integrada · {C}", "https://anuario.ibge.gov.br/images/aeb/2024/s5/2_pdf/s5t2102.pdf"],
 ["Frota de veículos – página oficial", "Senatran / Ministério dos Transportes", "Frota mensal por UF, município e tipo", "Integrada", "https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-Senatran/frota-de-veiculos-2024"],
 ["Municípios com código IBGE", "Compilação pública dos códigos do IBGE", "Nome, UF e código de cada município", f"Integrada · {C}", "https://github.com/kelvins/municipios-brasileiros"]]))

st.append(P("2. Bases a integrar na atualização automática", "h1"))
st.append(tab([
 ["RENAEST – Registro Nacional de Sinistros e Estatísticas de Trânsito", "Senatran", "Sinistros, localidade, veículos e vítimas de todas as vias; arquivos desde 2021", f"A integrar · {C}", "https://dados.transportes.gov.br/dataset/42e2320b-ea67-4fdc-896f-71363e043fc6"],
 ["RENAEST – página institucional", "Ministério dos Transportes", "Apresentação e painel público", f"A integrar · {C}", "https://www.gov.br/transportes/pt-br/assuntos/transito/arquivos-senatran/docs/renaest"],
 ["Trechos concedidos (km inicial e final), arquivo 8/2026", "ANTT – dados abertos", "Responsável de cada trecho: concessionária ou DNIT", f"Integrada · {C}", "https://dados.antt.gov.br/dataset/trecho-concedido"],
 ["Boletim anual de sinistros em rodovias concedidas 2025", "ANTT", "Sinistros e vítimas por concessionária", f"A integrar · {C}", "https://www.gov.br/antt/pt-br/assuntos/rodovias/informacoes-gerais/boletim-anual-de-acidentes/boletim-anual-de-sinistros-de-transito-em-rodovias-2025"],
 ["Sistema Nacional de Viação (SNV)", "DNIT", "Malha federal oficial; permite rotas em todo o país, inclusive Roraima e Amazonas", "A integrar", "https://www.gov.br/dnit/pt-br/assuntos/atlas-e-mapas/pnv-e-snv"],
 ["Plano Nacional de Contagem de Tráfego (PNCT)", "DNIT", "Volume médio diário de veículos por posto", "A integrar", "https://servicos.dnit.gov.br/dadospnct/"],
 ["Avisos meteorológicos", "INMET", "Alertas de chuva forte, vendaval, granizo e baixa umidade, em tempo real", "A integrar", "https://alertas2.inmet.gov.br/"],
 ["Banco de dados meteorológicos (BDMEP)", "INMET", "Chuva, temperatura e vento por estação", "A integrar", "https://bdmep.inmet.gov.br/"],
 ["Atlas Digital de Desastres no Brasil", "MIDR – Defesa Civil", "Desastres por município, 1991 em diante", f"A integrar · {C}", "https://atlasdigital.mdr.gov.br"],
 ["S2iD – Sistema Integrado de Informações sobre Desastres", "MIDR – Defesa Civil", "Registros de desastres e reconhecimentos federais", "A integrar", "https://s2id.mi.gov.br/"],
 ["Projeto AdaptaVias", "Ministério dos Transportes", "Índice de Risco Climático das rodovias federais (deslizamento, erosão, inundação)", f"A integrar · {C}", "https://www.gov.br/transportes/pt-br/assuntos/sustentabilidade/projeto-adaptavias"],
 ["AdaptaBrasil", "MCTI", "Plataforma pública que recebe os resultados do AdaptaVias", "A integrar", "https://adaptabrasil.mcti.gov.br/"]]))

st.append(P("3. Custos de referência e eficácia das medidas", "h1"))
st.append(tab([
 ["Custos Médios Gerenciais (CMG)", "DNIT", "Tabelas trimestrais; a mais recente é de julho de 2026", f"Integrada · {C}", "https://www.gov.br/dnit/pt-br/assuntos/planejamento-e-pesquisa/custos-referenciais/custo-medio-gerencial"],
 ["CMG de março de 2015 (terceira faixa: R$ 1,80 a 2,10 milhões por km)", "DNIT", "Base do custo da faixa adicional 2+1 (a atualizar pelo CMG vigente)", f"Integrada · {C}", "https://www.gov.br/dnit/pt-br/assuntos/planejamento-e-pesquisa/custos-e-pagamentos/custos-e-pagamentos-dnit/custo-medio-gerencial/CustosMdiosGer.MARO15.pdf"],
 ["SICRO abr/2026 – barreira New Jersey (R$ 326,31/m)", "DNIT (consulta pela plataforma Orçamentor)", "Composição 3713822", f"Integrada · {C}", "https://www.orcamentor.com/sicro/composicoes/?page=30"],
 ["SICRO abr/2026 – defensa maleável simples (R$ 851,99/m)", "DNIT (consulta pela plataforma Orçamentor)", "Composição 3713600", f"Integrada · {C}", "https://orcamentor.com/sicro/composicoes/3713600/"],
 ["Fiscalização eletrônica de velocidade (R$ 4 mil por faixa/mês)", "DNIT – PNCV (divulgado pelo Setcesp, 2016)", "Custo mensal por faixa monitorada", f"Integrada · {C}", "https://setcesp.org.br/noticias/fiscalizacao-eletronica-esta-garantida-nas-rodovias-federais/"],
 ["Passarela na BR-020 (≈ R$ 4,8 milhões)", "DER-DF (Jornal de Brasília, nov/2026)", "Referência de custo de travessia segura", f"Integrada · {C}", "https://jornaldebrasilia.com.br/brasilia/publicado-aviso-de-licitacao-para-construir-passarela-na-br-020/"],
 ["Viaduto da BR-470/SC (R$ 17,5 milhões)", "DNIT (2025)", "Teto de custo de interseção em desnível", f"Integrada · {C}", "https://www.gov.br/dnit/pt-br/assuntos/noticias/dnit-entrega-terceiro-viaduto-da-br-470-sc-em-2025-no-vale-do-itajai"],
 ["Proven Safety Countermeasures", "FHWA (EUA)", "Eficácia de barreira central, rotatória, sonorizadores, travessias, radares", f"Integrada · {C}", "https://highways.dot.gov/safety/proven-safety-countermeasures"],
 ["Barreiras centrais e vias 2+1", "Trafikverket (Suécia)", "Redução de mortes com separação de sentidos", f"Integrada · {C}", "https://bransch.trafikverket.se/en/startpage/operations/Operations-road/vision-zero-academy/Key-interventions-based-on-Vision-Zero/median-barriers/"]]))

st.append(P("4. Referências de contexto", "h1"))
st.append(tab([
 ["Pnatrans – revisão e meta", "Ministério dos Transportes", "Meta de reduzir à metade o índice de mortes até 2030", f"Referência · {C}", "https://www.gov.br/participamaisbrasil/revisao-pnatrans"],
 ["Acórdão 1799/2026-TCU-Plenário (notícia)", "TCU", "Auditoria do Pnatrans", f"Referência · {C}", "https://portal.tcu.gov.br/imprensa/noticias/tribunal-avalia-plano-nacional-para-reduzir-mortes-e-lesoes-no-transito"],
 ["Waze for Cities", "Waze / Google", "Canal oficial para órgãos públicos enviarem alertas e interdições", f"Referência · {C}", "https://www.waze.com/pt-BR/wazeforcities/"],
 ["Feed de dados de parceiros do Waze", "Google", "Formato e passos para publicar alertas", f"Referência · {C}", "https://developers.google.com/waze/data-feed/overview?hl=pt-br"],
 ["Registro Nacional Positivo de Condutores (RNPC)", "Senatran (reportagem CNN Brasil)", "Cadastro do bom condutor no app CNH do Brasil", f"Referência · {C}", "https://www.cnnbrasil.com.br/auto/como-funciona-e-quais-beneficios-do-cadastro-de-bom-motorista/"],
 ["Desconto do Bom Motorista no IPVA (RS)", "Governo do Rio Grande do Sul", "Até 15% de desconto para quem não tem multa", f"Referência · {C}", "https://estado.rs.gov.br/descontos-dos-programas-bom-cidadao-e-bom-motorista-chegam-a-r-288-milhoes"]]))
st.append(P("Os links que levam a planilhas e arquivos grandes (RENAEST, SIM, ANTT, DNIT) são baixados pela rotina automática do painel; o pacote de atualização registra em log cada base baixada e cada falha de acesso.", "n"))

# 5. Rodovias federais concedidas x DNIT (base ANTT)
import sys, json; sys.path.insert(0, "/home/claude/sentinela_br/p6")
from antt_concessoes import TRECHOS, NOMES
from reportlab.platypus import PageBreak
from reportlab.lib.units import cm
Dj = json.load(open("/home/claude/sentinela_br/p6/dados.json")); ct = {c["nome"]: c for c in Dj["ctab"]}
tr = Dj["tr"]; mD = sum(m for m, c in zip(tr["m"], tr["conc"]) if c < 0); mC = sum(m for m, c in zip(tr["m"], tr["conc"]) if c >= 0)
st.append(PageBreak())
st.append(P("5. Quem cuida de cada rodovia federal: concessionárias e DNIT", "h1"))
st.append(P(f"Fonte: ANTT, base de dados abertos <i>Informações sobre os trechos concedidos</i>, arquivo 8/2026 (rodovias federais; BR, UF, km inicial e final). Cada trecho de 5 km do painel recebe um único responsável: a concessionária cujo intervalo cobre o trecho; quando dois contratos se sobrepõem, vale o mais recente. Todo o restante da malha federal é de responsabilidade do DNIT (administração direta). A ANTT fiscaliza os contratos de concessão. Mortes: PRF, jan/2021 a out/2026.", "n"))
st.append(P(f"<b>DNIT:</b> {mD:,} mortes ({mD/(mD+mC):.0%}) · <b>Concessionárias:</b> {mC:,} mortes ({mC/(mD+mC):.0%}).".replace(",", "."), "n"))
lin = []
for n in sorted(ct, key=lambda n: -ct[n]["m"]):
    c = ct[n]
    if not c["trechos"]: continue
    fx = "; ".join(f"BR-{t['br']:03d}/{t['uf']} km {t['a']:.1f}–{t['z']:.1f}".replace(".", ",") for t in c["trechos"])
    lin.append([n, fx, f"{c['km']:,}".replace(",", "."), f"{c['m']:,}".replace(",", ".")])
st.append(tabela(["Concessionária", "Rodovias e km concedidos (ANTT)", "Km", "Mortes 2021–2026 (PRF)"], lin, [3.4, 9.6, 1.3, 2.7]))
st.append(P("Observações: a Concer (BR-040 RJ/MG) e a Elovias têm intervalos coincidentes na BR-040 RJ/MG; onde coincidem, prevalece a Elovias, contrato mais recente. O mesmo vale para Concebra e Way 153 na BR-153/GO. Rodovias federais delegadas a estados (por exemplo, concessões estaduais em MS e MG) não constam da base da ANTT. Trechos com quilometragem fora dos intervalos acima estão sob o DNIT.", "n"))
gerar("/home/claude/sentinela_br/docs/Sentinela_BR_Fontes_e_Links.pdf", "Fontes e links de acesso", st)
print("ok")
