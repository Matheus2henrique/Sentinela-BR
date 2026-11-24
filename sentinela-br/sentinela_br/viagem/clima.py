import os as _os
_BASE = _os.environ.get("SENTINELA_BASE", "/home/claude")
"""Eventos climáticos e desastres recorrentes por trecho (PRF, todos os sinistros 2021-out/2026)
+ dados oficiais do Pnatrans (SIM/MS, IBGE, Senatran). Acrescenta D['clima'] e D['pnatrans']."""
import json, re
import numpy as np, pandas as pd

D = json.load(open("dados/sentinela_dados.json"))
T = D["trechos"]; UFS = D["meta"]["ufs"]
idx = {(T["br"][i], UFS[T["uf"][i]], T["km"][i]): i for i in range(len(T["br"]))}
t = pd.read_pickle(f"{_BASE}/real/prf_2021_2026.pkl")
t = t[t.br.notna() & t.km.notna()].copy()
C = t.causas_todas.fillna(""); W = t.condicao_metereologica.fillna("")

CATS = [
 ("encosta", "Deslizamento e detritos", "queda de barreira, areia ou detritos na pista, fenômenos naturais",
  "Contenção de encosta, drenagem e monitoramento geotécnico; interdição preventiva com alerta de chuva forte",
  ["Gestor da via (DNIT ou concessionária)", "Defesa Civil", "PRF"]),
 ("fumaca", "Fumaça de queimadas", "fumaça na pista, típica da estação seca",
  "Prevenção e combate a incêndios na faixa de domínio; operação PRF de controle de tráfego com fumaça",
  ["Ibama/Prevfogo e Corpo de Bombeiros", "Gestor da via (DNIT ou concessionária)", "PRF"]),
 ("neblina", "Neblina", "nevoeiro ou neblina com baixa visibilidade",
  "Tachas refletivas, faixas de alto desempenho e painel de mensagem com sensor de visibilidade; comboio da PRF",
  ["Gestor da via (DNIT ou concessionária)", "PRF"]),
 ("chuva", "Chuva e pista molhada", "chuva, água acumulada, pista escorregadia, drenagem deficiente",
  "Drenagem e recuperação da aderência do pavimento; redução de velocidade e aviso ao motorista em dia de chuva",
  ["Gestor da via (DNIT ou concessionária)", "PRF", "Defesa Civil"]),
 ("vento", "Vento forte e granizo", "rajadas de vento ou granizo",
  "Aviso ao motorista com alerta do INMET; atenção a veículos altos e motos",
  ["PRF", "Gestor da via (DNIT ou concessionária)"]),
]
K = {c[0]: k for k, c in enumerate(CATS)}
cat = pd.Series(-1, index=t.index)
regras = [
 ("vento", C.str.contains("^$") & False | W.isin(["Vento", "Granizo"])),
 ("chuva", C.str.contains("Chuva|Pista Escorregadia|Acumulo de água|drenagem") | W.isin(["Chuva", "Garoa/Chuvisco"])),
 ("neblina", C.str.contains("Neblina") | W.isin(["Nevoeiro/Neblina"])),
 ("fumaca", C.str.contains("Fumaça")),
 ("encosta", C.str.contains("areia ou detritos|Fenômenos da natureza")),
]
for nome, m in regras:  # ordem crescente de prioridade
    cat[m] = K[nome]
causa_clim = C.str.contains("Chuva|Pista Escorregadia|Acumulo de água|drenagem|Neblina|Fumaça|areia ou detritos|Fenômenos da natureza")
t["cat"] = cat; t["cc"] = causa_clim
c = t[t.cat >= 0].copy()
c["mes"] = c.data.dt.month - 1
c["bin"] = (np.floor(c.km) // 5 * 5).astype(int)
c["br"] = c.br.astype(int)
print("sinistros com evento climático:", len(c), "mortes:", int(c.mortos.sum()), "de", int(t.mortos.sum()))

REG = {"N": "AC AM AP PA RO RR TO", "NE": "AL BA CE MA PB PE PI RN SE", "CO": "DF GO MS MT", "SE": "ES MG RJ SP", "S": "PR RS SC"}
UFREG = {u: r for r, s in REG.items() for u in s.split()}
full = c[c.ano <= 2025]
nac = {
 "mes_cat": [[int(((full.cat == k) & (full.mes == m)).sum()) for m in range(12)] for k in range(len(CATS))],
 "mes_cat_m": [[int(full[(full.cat == k) & (full.mes == m)].mortos.sum()) for m in range(12)] for k in range(len(CATS))],
 "reg_mes": {r: [int(full[(full.uf.map(UFREG) == r) & (full.mes == m)].mortos.sum()) for m in range(12)] for r in REG},
 "ano": {str(a): [int(c[(c.ano == a)].mortos.sum()), int((c.ano == a).sum())] for a in range(2021, 2027)},
 "total": [int(len(c)), int(c.mortos.sum()), int(c.feridos_graves.sum()), int(c.cc.sum())],
 "mortes_tot": int(t.mortos.sum()),
}

t["mes"] = t.data.dt.month - 1; t["bin"] = (np.floor(t.km) // 5 * 5).astype(int); t["br"] = t.br.astype(int)
TOT = {k: np.bincount(g.mes, minlength=12) for k, g in t.groupby(["br", "uf", "bin"])}
rows = []
for (br, uf, b), g in c.groupby(["br", "uf", "bin"]):
    if len(g) < 6: continue
    mes = np.bincount(g.mes, minlength=12)
    tri = [mes[m] + mes[(m + 1) % 12] + mes[(m + 2) % 12] for m in range(12)]
    j = int(np.argmax(tri)); jan = {j, (j + 1) % 12, (j + 2) % 12}
    gj = g[g.mes.isin(jan) & (g.ano <= 2025)]
    rec = int(gj.ano.nunique())  # anos completos (2021-2025) com evento na mesma janela
    conc = tri[j] / len(g); tot = TOT[(br, uf, b)]
    lift = conc / max(1e-9, sum(tot[m] for m in jan) / tot.sum())
    cats = np.bincount(g.cat, minlength=len(CATS)).tolist()
    m, fg = int(g.mortos.sum()), int(g.feridos_graves.sum())
    rows.append(dict(ti=idx.get((br, uf, b), -1), br=br, uf=uf, km=b, lat=round(float(g.latitude.median()), 4), lon=round(float(g.longitude.median()), 4),
                     mun=g.municipio.mode().iat[0].title(), n=len(g), m=m, fg=fg, cc=int(g.cc.sum()), cats=cats, mes=mes.tolist(),
                     anos=[int((g.ano == a).sum()) for a in range(2021, 2027)], j=j, rec=rec, conc=round(conc, 2), lift=round(lift, 2),
                     score=round(m * 10 + fg * 3 + len(g), 1)))
R = pd.DataFrame(rows)
R["saz"] = ((R.rec >= 4) & (R.lift >= 1.3) & (R.n >= 8)).astype(int)
R = R.sort_values("score", ascending=False)
print("trechos com >=6 eventos:", len(R), "sazonais recorrentes:", int(R.saz.sum()), "mortes nos sazonais:", int(R[R.saz == 1].m.sum()))
cols = ["ti", "br", "uf", "km", "lat", "lon", "mun", "n", "m", "fg", "cc", "cats", "mes", "anos", "j", "rec", "conc", "lift", "saz", "score"]
D["clima"] = {"cats": [dict(id=a, nome=b, desc=d, acao=e, orgaos=f) for a, b, d, e, f in CATS],
              "nac": nac, "reg": {r: s.split() for r, s in REG.items()},
              "tr": {k: R[k].tolist() for k in cols}, "base_ate": str(t.data.max().date())}

# ---------- Pnatrans: dados oficiais verificados
POP = dict(RO=1746227, AC=880631, AM=4281209, RR=716793, PA=8664306, AP=802837, TO=1577342, MA=7010960, PI=3375646, CE=9233656, RN=3446071,
           PB=4145040, PE=9539029, AL=3220104, SE=2291077, BA=14850513, MG=21322691, ES=4102129, RJ=17219679, SP=45973194, PR=11824665,
           SC=8058441, RS=11229915, MS=2901895, MT=3836399, GO=7350483, DF=2982818)
FROTA = dict(AC=367440, AP=258190, AM=1202431, PA=2810011, RO=1243638, RR=289075, TO=923976, AL=1166897, BA=5389511, CE=3905225, MA=2248041,
             PB=1681969, PE=3730069, PI=1527217, RN=1629028, SE=1005290, ES=2494996, MG=13975854, RJ=7973983, SP=34332819, PR=9179769,
             RS=8311600, SC=6442054, DF=2159414, GO=4926608, MT=2831640, MS=1967775)
assert sum(POP.values()) == 212583750 and sum(FROTA.values()) == 123974520
SIM = {2010: 42844, 2011: 43256, 2012: 44812, 2013: 42266, 2014: 43780, 2015: 38651, 2016: 37345, 2017: 35375, 2018: 32655,
       2019: 31945, 2020: 32716, 2021: 33813, 2022: 33894, 2023: 34881, 2024: 37150}
TAXA = {2010: 22.0, 2011: 22.1, 2012: 22.7, 2013: 21.2, 2014: 21.8, 2015: 19.1, 2016: 18.3, 2017: 17.2, 2018: 15.8, 2019: 15.4,
        2020: 15.6, 2021: 16.1, 2022: 16.1, 2023: 16.5}
TAXA[2024] = round(SIM[2024] / sum(POP.values()) * 1e5, 1)
prf24 = {u: D["extra"]["ufs"][u]["m"][3] for u in POP}
D["pnatrans"] = {"sim": SIM, "taxa": TAXA, "meta2030": round(TAXA[2020] / 2, 1), "pop": POP, "frota": FROTA,
                 "prf24": prf24, "prf24_tot": int(D["nacional"]["mortes_ano"]["2024"]),
                 "fontes": {"sim": "SIM/Ministério da Saúde, CID-10 V01–V89 (2010–2023: apresentação MS à Câmara, 2025; 2024: extração usada na auditoria do TCU)",
                            "pop": "IBGE, Estimativas da População, 1º/7/2024 (DOU)", "frota": "Senatran, frota com placa, dez/2024 (IBGE, Anuário Estatístico)"}}
print("taxa 2024:", TAXA[2024], "meta:", D["pnatrans"]["meta2030"], "PRF 2024:", D["pnatrans"]["prf24_tot"], "=", round(D["pnatrans"]["prf24_tot"] / SIM[2024] * 100, 1), "% do SIM")
json.dump(D, open("dados/sentinela_dados.json", "w"), ensure_ascii=False, separators=(",", ":"))
