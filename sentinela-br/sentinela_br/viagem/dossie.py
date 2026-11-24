import os as _os
_BASE = _os.environ.get("SENTINELA_BASE", "/home/claude")
"""Dossiê por trecho: cada acidente fatal com seus motivos (PRF), agrupamento dos motivos,
recomendações com evidência e órgão responsável, e avisos nacionais pelo histórico.
Acrescenta ao dados/sentinela_dados.json as chaves "fatais", "dossie", "regras", "grupos" e "avisos"."""
import json, pickle, re
import numpy as np, pandas as pd

D = json.load(open("dados/sentinela_dados.json"))
T = D["trechos"]; UFS = D["meta"]["ufs"]
idx = {(T["br"][i], UFS[T["uf"][i]], T["km"][i]): i for i in range(len(T["br"]))}
rede = pickle.load(open("rede.pkl", "rb"))
t = pd.read_pickle(f"{_BASE}/real/prf_2021_2026.pkl")
t = t[(t.mortos > 0) & t.id.isin(rede["t_limpo_ids"])].copy()
t["bin"] = (np.floor(t.km) // 5 * 5).astype(int)
t["ti"] = [idx.get((int(b), u, int(k)), -1) if pd.notna(b) else -1 for b, u, k in zip(t.br, t.uf, t.bin)]
t = t[t.ti >= 0].copy()
print("acidentes fatais ligados a trechos:", len(t), "mortes:", int(t.mortos.sum()))

# ---------- grupos de motivos (causa apontada pela PRF)
GRUPOS = [
 ("clima", "Natureza e clima", "chuva, água ou óleo na pista, neblina, detritos e queda de barreira"),
 ("via", "Via e sinalização", "iluminação, sinalização, buracos, acostamento, curvas, defensas e travessias"),
 ("conduta", "Imprudência e erro do condutor", "contramão, ultrapassagem, velocidade, falta de atenção, manobras proibidas"),
 ("incapaz", "Sono, álcool ou mal súbito", "condutor dormindo, alcoolizado, sob efeito de drogas ou com mal súbito"),
 ("pedestre", "Pedestres", "pedestre na pista ou atravessando fora da faixa"),
 ("veiculo", "Falha do veículo", "pneus, freios, falhas mecânicas e carga"),
 ("animais", "Animais na pista", "animais soltos na rodovia"),
 ("outros", "Outras causas", "demais registros"),
]
G = {g[0]: k for k, g in enumerate(GRUPOS)}
REGRA_GRUPO = [
 ("clima", r"Chuva|Pista Escorregadia|Acumulo de água|Neblina|Fumaça|areia ou detritos|Fenômenos da natureza|Obstrução na via|Objeto estático|Acumulo de óleo|drenagem"),
 ("via", r"Iluminação|Sinalização|sinalização|esburacada|Curva acentuada|falhas na via|Afundamento|Acostamento em desnível|Falta de acostamento|elemento de contenção|Obras na pista|Desvio temporário|Declive acentuado|Restrição de visibilidade|Pista em desnível|largura insuficiente|Redutor de velocidade|Semáforo com defeito|sem a presença de local apropriado"),
 ("incapaz", r"Dormindo|álcool pelo condutor|psicoativas pelo condutor|Mal súbito|Transtornos Mentais"),
 ("pedestre", r"Pedestre|pedestre"),
 ("veiculo", r"mecânicas|pneu|freio|Carga excessiva|suspensão|Faróis desregulados|Modificação proibida"),
 ("animais", r"Animais"),
 ("conduta", r"contramão|reação|Velocidade|Acessar a via|Ultrapassagem|mudança de faixa|distância|entre as faixas|Conversão proibida|Acesso irregular|preferência|cruzamento|Acostamento|acostamento|Retorno proibido|Estacionar|Frear bruscamente|semáforo|racha|celular|farol|calçada"),
]
def grupo(c):
    c = str(c or "")
    if "Suicídio" in c: return "outros"
    for g, rx in REGRA_GRUPO:
        if re.search(rx, c): return g
    return "outros"
t["g"] = t.causa_acidente.map(grupo)

# ---------- recomendações: regra, condição sobre os acidentes fatais do trecho, medida, órgãos
ORG = {"gestor": "Gestor da via (DNIT ou concessionária)", "prf": "PRF", "defesa": "Defesa Civil",
       "prefeitura": "Prefeitura", "detran": "DETRAN", "antt": "ANTT", "mt": "Ministério dos Transportes"}
C = t.causas_todas.fillna(""); TP = t.tipos_todos.fillna(""); TV = t.tracado_via.fillna("")
def has(s, rx): return s.str.contains(rx, regex=True)
noite = t.fase_dia.isin(["Plena Noite", "Anoitecer", "Amanhecer"])
chuva_cond = t.condicao_metereologica.isin(["Chuva", "Garoa/Chuvisco"]) | has(C, "Chuva|Pista Escorregadia")
REGRAS = [
 ("frontal", "Separação física entre os sentidos (barreira ou defensa central) e faixas adicionais de ultrapassagem; duplicação onde o volume justificar", ["gestor", "mt"],
  has(TP, "Colisão frontal|lateral sentido oposto") | has(C, "contramão|Ultrapassagem Indevida"), "colisões frontais ou laterais em sentido oposto, por contramão ou ultrapassagem indevida"),
 ("frontal_fisc", "Fiscalização de ultrapassagem proibida e sonorizadores no eixo da pista", ["prf", "gestor"],
  has(C, "Ultrapassagem Indevida|contramão"), "ultrapassagem indevida ou contramão apontadas pela PRF"),
 ("pedestre", "Passarela ou travessia semaforizada, calçadas e paradas de ônibus seguras", ["gestor", "prefeitura"],
  has(TP, "Atropelamento de Pedestre"), "atropelamentos de pedestres"),
 ("pedestre_luz", "Iluminação do trecho e das travessias", ["gestor", "prefeitura"],
  has(TP, "Atropelamento de Pedestre") & noite, "atropelamentos à noite ou ao amanhecer/anoitecer"),
 ("velocidade", "Controle eletrônico de velocidade e redução do limite onde necessário", ["gestor", "prf"],
  has(C, "Velocidade Incompatível|Reação tardia|Ausência de reação|distância do veículo"), "velocidade incompatível ou falta de tempo de reação"),
 ("intersecao", "Readequação de acessos e interseções (rotatória, faixa de aceleração, viaduto) e fechamento de acessos irregulares", ["gestor", "prf"],
  has(TP, "Colisão transversal") | has(C, "Acessar a via sem observar|Acesso irregular|Conversão proibida|preferência no cruzamento|Retorno proibido"), "colisões em cruzamentos, acessos e conversões"),
 ("sono", "Pontos de parada e descanso, sonorizadores nas bordas e fiscalização do tempo de direção", ["mt", "gestor", "prf"],
  has(C, "Condutor Dormindo"), "condutores dormindo ao volante"),
 ("alcool", "Operações de fiscalização de alcoolemia nos dias e horários de maior risco", ["prf", "detran"],
  has(C, "álcool pelo condutor|psicoativas pelo condutor"), "condutores alcoolizados ou sob efeito de drogas"),
 ("curva", "Sinalização de curva, defensas metálicas, área de escape e revisão do traçado", ["gestor"],
  (TV.str.contains("Curva|Declive")) & has(TP, "Saída de leito|Tombamento|Capotamento|Colisão com objeto|Colisão frontal"), "saídas de pista, tombamentos ou colisões em curvas e declives"),
 ("via", "Manutenção do pavimento, do acostamento e da sinalização; defensas onde faltam", ["gestor"],
  has(C, "esburacada|Afundamento|Acostamento em desnível|Falta de acostamento|falhas na via|Ausência de sinalização|Sinalização mal posicionada|Sinalização encoberta|elemento de contenção|Iluminação deficiente|Deficiência do Sistema"), "falhas de pavimento, acostamento, sinalização, iluminação ou contenção apontadas pela PRF"),
 ("chuva", "Recuperação da aderência do pavimento e da drenagem; alerta e operação especial em dias de chuva", ["gestor", "prf", "defesa"],
  chuva_cond | has(C, "Acumulo de água|drenagem"), "acidentes com chuva, pista molhada ou água acumulada"),
 ("encosta", "Contenção de encostas, limpeza da pista e protocolo de interdição preventiva em chuva forte", ["gestor", "defesa"],
  has(C, "areia ou detritos|Fenômenos da natureza|Obstrução na via|Objeto estático"), "objetos, detritos ou material de encosta na pista"),
 ("neblina", "Painéis de alerta e sinalização refletiva para neblina; operação comboio em visibilidade baixa", ["gestor", "prf"],
  t.condicao_metereologica.eq("Nevoeiro/Neblina") | has(C, "Neblina|Fumaça"), "acidentes com neblina ou fumaça"),
 ("animais", "Cercamento com passagens de fauna e recolhimento de animais soltos", ["gestor", "prf", "prefeitura"],
  has(C, "Animais") | has(TP, "Atropelamento de Animal"), "animais na pista"),
 ("veiculo", "Fiscalização de condições do veículo, pesagem e carga", ["prf", "antt"],
  has(C, "mecânicas|pneu|freio|Carga excessiva|suspensão"), "falhas de pneu, freio, mecânicas ou excesso de carga"),
 ("moto", "Fiscalização e campanha dirigidas a motociclistas", ["prf", "detran"],
  t.moto.fillna(False).astype(bool) | has(TP, "Queda de ocupante"), "acidentes fatais com motocicleta"),
]
for rid, *_ , mask, _ in [(r[0], r[1], r[2], r[3], r[4]) for r in REGRAS]:
    t["r_" + rid] = mask.values

# ---------- tabelas de códigos
def cod(col):
    vals = sorted(t[col].fillna("Não informado").astype(str).unique())
    m = {v: k for k, v in enumerate(vals)}
    return vals, [m[v] for v in t[col].fillna("Não informado").astype(str)]
causas_l, cp = cod("causa_acidente")
causas_l = [("Outras causas" if "Suicídio" in c else c) for c in causas_l]
tipos_l, tp = cod("tipo_acidente")
met_l, cm = cod("condicao_metereologica")
fase_l, fd = cod("fase_dia")
trac_l, tv = cod("tracado_via")
todas = sorted({c for s in t.causas_todas.fillna("") for c in s.split("|") if c and "Suicídio" not in c})
ix_todas = {c: k for k, c in enumerate(todas)}
t = t.sort_values(["ti", "data"]).reset_index(drop=True)
causas_l, cp = cod("causa_acidente"); causas_l = [("Outras causas" if "Suicídio" in c else c) for c in causas_l]
_, tp = cod("tipo_acidente"); _, cm = cod("condicao_metereologica"); _, fd = cod("fase_dia"); _, tv = cod("tracado_via")
fatais = {
  "ti": t.ti.astype(int).tolist(), "d": t.data.dt.strftime("%Y%m%d").astype(int).tolist(),
  "h": pd.to_numeric(t.horario.str[:2], errors="coerce").fillna(-1).astype(int).tolist(),
  "m": t.mortos.astype(int).tolist(), "fg": t.feridos_graves.fillna(0).astype(int).tolist(),
  "cp": cp, "ca": [[ix_todas[c] for c in s.split("|") if c in ix_todas][:5] for s in t.causas_todas.fillna("")],
  "tp": tp, "cm": cm, "fd": fd, "tv": tv, "g": [G[x] for x in t.g],
}
cods = {"causas": causas_l, "todas": todas, "tipos": tipos_l, "tempo": met_l, "fase": fase_l, "tracado": trac_l}

# ---------- dossiê por trecho
dos = {}
regs = [(r[0], r[1], r[2], r[4]) for r in REGRAS]
for ti, g in t.groupby("ti"):
    M = int(g.mortos.sum())
    gm = [0] * len(GRUPOS)
    for k, v in g.groupby("g").mortos.sum().items(): gm[G[k]] = int(v)
    recs = []
    for rid, med, orgs, txt in regs:
        sub = g[g["r_" + rid]]
        mm = int(sub.mortos.sum())
        if mm >= 2 or (mm >= 1 and mm / M >= .34):
            recs.append([rid, mm, len(sub)])
    recs.sort(key=lambda r: -r[1])
    noite_pct = float(g.mortos[g.fase_dia.isin(["Plena Noite", "Anoitecer", "Amanhecer"])].sum() / M)
    chuva_pct = float(g.mortos[g.condicao_metereologica.isin(["Chuva", "Garoa/Chuvisco"]) | g.causas_todas.fillna("").str.contains("Chuva|Pista Escorregadia")].sum() / M)
    meses = g.groupby(g.data.dt.month).mortos.sum()
    dos[int(ti)] = {"g": gm, "r": recs[:6], "noite": round(noite_pct, 2), "chuva": round(chuva_pct, 2),
                    "mes": [int(meses.get(m, 0)) for m in range(1, 13)]}
print("trechos com dossiê:", len(dos))

# ---------- avisos nacionais (histórico real, sem simulação)
ult = t.data.max()
cron = set(i for i in range(len(T["br"])) if T["cronico"][i] or T["nivel"][i] >= 2)
def mes_set(m): return {m, m % 12 + 1}
hoje = pd.Timestamp("2026-11-23")
mes_ref = mes_set(hoje.month)  # este mês e o próximo
t["clima_any"] = t.condicao_metereologica.isin(["Chuva", "Garoa/Chuvisco", "Nevoeiro/Neblina"]) | t.causas_todas.fillna("").str.contains("Chuva|Pista Escorregadia|Acumulo de água|Neblina|areia ou detritos|Fenômenos da natureza|Obstrução na via")
av = []
# 1. época de chuva: mortes ligadas a clima neste mês e no próximo, em anos anteriores
s = t[t.clima_any & t.data.dt.month.isin(mes_ref)].groupby("ti").agg(m=("mortos", "sum"), anos=("ano", "nunique"))
for ti, r in s[(s.m >= 2)].iterrows():
    av.append({"ti": int(ti), "tipo": "chuva", "m": int(r.m), "anos": int(r.anos)})
# 2. fim de ano e férias: trechos críticos com mais mortes em dezembro/janeiro
s = t[t.data.dt.month.isin({12, 1}) & t.ti.isin(cron)].groupby("ti").agg(m=("mortos", "sum"), anos=("ano", "nunique"))
for ti, r in s[(s.m >= 3) & (s.anos >= 2)].iterrows():
    av.append({"ti": int(ti), "tipo": "ferias", "m": int(r.m), "anos": int(r.anos)})
# 3. morte recente em trecho crônico: últimos 90 dias da base
rec = t[(t.data > ult - pd.Timedelta(days=90)) & t.ti.isin(cron)].groupby("ti").agg(m=("mortos", "sum"), ult=("data", "max"))
for ti, r in rec.iterrows():
    av.append({"ti": int(ti), "tipo": "recente", "m": int(r.m), "ult": r.ult.strftime("%Y%m%d")})
print("avisos:", pd.Series([a["tipo"] for a in av]).value_counts().to_dict())

D["fatais"] = fatais; D["cods"] = cods; D["dossie"] = dos
D["grupos"] = [{"id": g[0], "nome": g[1], "desc": g[2]} for g in GRUPOS]
D["regras"] = {r[0]: {"medida": r[1], "orgaos": [ORG[o] for o in r[2]], "porque": r[4]} for r in REGRAS}
D["avisos"] = {"lista": av, "referencia": "dezembro e janeiro" if False else f"{hoje.month:02d}", "base_ate": ult.strftime("%Y-%m-%d"),
               "meses": sorted(mes_ref)}
json.dump(D, open("dados/sentinela_dados.json", "w"), ensure_ascii=False, separators=(",", ":"))
import os; print("tamanho", round(os.path.getsize("dados/sentinela_dados.json") / 1e6, 2), "MB")
# amostra
i = idx[(40, "MG", 520)]; print(T["mortos"][i], dos[i])
