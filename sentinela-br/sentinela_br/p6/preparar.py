"""Dados do pAInel Sentinela BR (BAI): PRF 2021-out/2026 por trecho de 5 km, mecanismo da morte, motivo,
responsável por trecho (base ANTT de trechos concedidos, 8/2026), risco esperado (Bayes empírico), clima sazonal,
série nacional SIM/IBGE/Senatran. Tudo calculado aqui a partir de bases oficiais."""
import json, numpy as np, pandas as pd

import os
BASE = os.environ.get("SENTINELA_BASE", "/home/claude")
V = f"{BASE}/sentinela_br/viagem/dados/sentinela_dados.json"
D = json.load(open(V)); T = D["trechos"]; UFS = D["meta"]["ufs"]; MUN = D["meta"]["municipios"]
idx = {(T["br"][i], UFS[T["uf"][i]], T["km"][i]): i for i in range(len(T["br"]))}
t = pd.read_pickle(f"{BASE}/real/prf_2021_2026.pkl")
t = t[t.br.notna() & t.km.notna()].copy()
t["br"] = t.br.astype(int); t["bin"] = (np.floor(t.km) // 5 * 5).astype(int); t["mes"] = t.data.dt.month
f = t[t.mortos > 0].copy()

# mecanismo do sinistro fatal -> grupo de medida (Sistema Seguro)
MEC = [("frontal", ["Colisão frontal", "Colisão lateral sentido oposto"]),
       ("saida", ["Saída de leito carroçável", "Tombamento", "Capotamento", "Colisão com objeto"]),
       ("pedestre", ["Atropelamento de Pedestre"]),
       ("traseira", ["Colisão traseira", "Engavetamento"]),
       ("intersecao", ["Colisão transversal"]),
       ("outros", [])]
T2M = {tp: k for k, (_, l) in enumerate(MEC) for tp in l}
f["mec"] = f.tipo_acidente.map(lambda x: T2M.get(x, 5))

# responsável por trecho: base oficial da ANTT de trechos concedidos (km inicial e final por BR e UF); fora dela, DNIT
import antt_concessoes as AC
AC.atualizar_da_antt()
from antt_concessoes import responsavel, NOMES, FONTE as FONTE_ANTT, URL as URL_ANTT
TRECHOS = AC.TRECHOS
CN = sorted({NOMES[c[0]] for c in TRECHOS}); CK = {n: k for k, n in enumerate(CN)}
def dono(br, uf, km):
    n = responsavel(br, uf, km, km + 5)
    return CK[n] if n else -1
CAUSAS = f.causa_acidente.fillna("Não informada").value_counts().index.tolist(); CI = {c: k for k, c in enumerate(CAUSAS)}
Cl = D["clima"]; ct = pd.DataFrame(Cl["tr"]); ck = {(r.br, r.uf, r.km): r for r in ct[ct.saz == 1].itertuples()}
ANOS_OBS = 5 + 10 / 12  # jan/2021 a out/2026
SEV_MED = float(f.mortos.sum() / f.id.nunique()); print("mortes por sinistro fatal:", round(SEV_MED, 3))
rows = []
for (br, uf, b), g in f.groupby(["br", "uf", "bin"]):
    i = idx.get((br, uf, b), -1)
    m = int(g.mortos.sum())
    nf = int(g.id.nunique()); sev = (m + 3 * SEV_MED) / (nf + 3)  # gravidade suavizada: evita que um único ônibus vire "risco crônico"
    esp = (T["eb"][i] / 100 * sev) if i >= 0 else nf / ANOS_OBS * sev
    cs = g.groupby(g.causa_acidente.fillna("Não informada")).mortos.sum().sort_values(ascending=False)
    pista = g.tipo_pista.fillna("").value_counts(); dupla = int(pista.get("Dupla", 0) + pista.get("Múltipla", 0) > pista.get("Simples", 0))
    ano = [int(g[g.ano == a].mortos.sum()) for a in range(2021, 2027)]
    c = ck.get((br, uf, b))
    rows.append(dict(br=br, uf=uf, km=b, lat=round(float(g.latitude.median()), 4), lon=round(float(g.longitude.median()), 4),
        mun=MUN[T["mun"][i]] if i >= 0 else g.municipio.mode().iat[0].title(), m=m, fg=int(g.feridos_graves.sum()), ano=ano,
        med=[int(g[g.mec == k].mortos.sum()) for k in range(6)], cau=[[CI[x], int(v)] for x, v in cs.head(3).items()],
        noite=round(float(g[g.fase_dia.isin(["Plena Noite", "Anoitecer", "Amanhecer"])].mortos.sum() / m), 2),
        urb=round(float(g[g.uso_solo.astype(str).str.startswith("Sim")].mortos.sum() / m), 2), dupla=dupla,
        moto=int(g.mortos_moto.sum()), esp=round(float(esp), 2), anosM=int(sum(1 for x in ano if x > 0)),
        tend=round((ano[3] + ano[4]) / 2 - (ano[0] + ano[1] + ano[2]) / 3, 2),
        conc=dono(br, uf, b), cj=int(c.j) if c else -1, cc=[int(x) for x in c.cats] if c else []))
R = pd.DataFrame(rows).sort_values(["esp", "m"], ascending=False).reset_index(drop=True)
print("trechos com morte:", len(R), "mortes:", R.m.sum(), "esperadas 12m:", round(R.esp.sum()))
print("trechos concedidos:", int((R.conc >= 0).sum()), "mortes em concessões:", int(R[R.conc >= 0].m.sum()), "DNIT:", int(R[R.conc < 0].m.sum()))
# tabela de concessões (ANTT) com mortes PRF nos trechos de cada uma
CTAB = []
for n in CN:
    rr = [dict(br=b, uf=u, a=a, z=z) for c, ano, b, u, a, z in TRECHOS if NOMES[c] == n]
    sub = R[R.conc == CK[n]]
    CTAB.append(dict(nome=n, trechos=rr, km=round(sum(x["z"] - x["a"] for x in rr)), m=int(sub.m.sum()), esp=round(float(sub.esp.sum()), 1), n=int(len(sub))))

# série nacional PRF e projeção 2026
mm = f.groupby(["ano", "mes"]).mortos.sum().unstack(fill_value=0)
share_jan_out = float((mm.loc[2021:2025, 1:10].sum(axis=1) / mm.loc[2021:2025].sum(axis=1)).mean())
prf_ano = {int(a): int(v) for a, v in f.groupby("ano").mortos.sum().items()}
proj26 = round(prf_ano[2026] / share_jan_out)
print("fração jan-out:", round(share_jan_out, 3), "projeção 2026:", proj26)

P = D["pnatrans"]
OUT = {"gerado": "2026-11-23T23:59:00-03:00", "base_ate": "31/10/2026",
 "causas": CAUSAS, "conc": CN, "ctab": CTAB, "fonteConc": [FONTE_ANTT, URL_ANTT], "mec": [m[0] for m in MEC], "mecTipos": [m[1] for m in MEC],
 "tr": {k: R[k].tolist() for k in ["br", "uf", "km", "lat", "lon", "mun", "m", "fg", "ano", "med", "cau", "noite", "urb", "dupla", "moto", "esp", "anosM", "tend", "conc", "cj", "cc"]},
 "nac": {"prf_ano": prf_ano, "proj26": proj26, "fracJanOut": round(share_jan_out, 4),
         "prf_mes": {int(a): [int(x) for x in mm.loc[a].reindex(range(1, 13), fill_value=0)] for a in mm.index}},
 "pn": {k: P[k] for k in ["sim", "taxa", "meta2030", "pop", "frota", "prf24"]},
 "clima": {"cats": [c["nome"] for c in Cl["cats"]], "acao": [c["acao"] for c in Cl["cats"]], "orgaos": [", ".join(c["orgaos"]) for c in Cl["cats"]],
           "mes_cat_m": Cl["nac"]["mes_cat_m"], "mes_cat": Cl["nac"]["mes_cat"], "total": Cl["nac"]["total"], "mortes_tot": Cl["nac"]["mortes_tot"],
           "n_saz": int((ct.saz == 1).sum()), "m_saz": int(ct[ct.saz == 1].m.sum())},
 "contorno": D["contorno"], "linhas": D["linhas"]}
s = json.dumps(OUT, ensure_ascii=False, separators=(",", ":"))
open(f"{BASE}/sentinela_br/p6/dados.json", "w").write(s)
print(len(s) // 1024, "KB")
