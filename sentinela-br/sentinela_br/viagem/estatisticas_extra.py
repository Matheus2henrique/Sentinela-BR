import os as _os
_BASE = _os.environ.get("SENTINELA_BASE", "/home/claude")
"""Agregados por UF, BR, BR/UF e município (base completa da PRF), para o assistente responder sem servidor."""
import json, re, pandas as pd, numpy as np
exec(open("perfis.py").read().split("for k, (_, s) in CAT.items():")[0].split("rede = pickle.load")[0])  # imports
t = pd.read_pickle(f"{_BASE}/real/prf_2021_2026.pkl")
t["hora"] = pd.to_numeric(t.horario.str[:2], errors="coerce")
src = open("perfis.py").read()
bloco = src[src.index("C = t.causas_todas"):src.index("for k, (_, s) in CAT.items():")]
exec(bloco)
for k, (_, s) in CAT.items(): t["c_" + k] = s.values
D = json.load(open("dados/sentinela_dados.json"))
ids = [c["id"] for c in D["meta"]["categorias"]]
anos = [2021, 2022, 2023, 2024, 2025, 2026]
t["fatal"] = t.classificacao_acidente.str.contains("Fatais", na=False)
def serie(g, col, f=sum):
    s = g.groupby("ano")[col].sum() if col != "n" else g.groupby("ano").size()
    return [int(s.get(a, 0)) for a in anos]
def causas(g, n=6):
    s = g[g.mortos > 0].groupby("causa_acidente").mortos.sum().sort_values(ascending=False).head(n)
    return [[k, int(v)] for k, v in s.items()]
def bloco_stats(g, completo=True):
    d = {"m": serie(g, "mortos"), "a": serie(g, "n"), "fg": serie(g, "feridos_graves")}
    if completo:
        d["cat"] = [int(g.loc[g["c_" + k], "mortos"].sum()) for k in ids]
        d["catAno"] = [[int(g.loc[g["c_" + k] & (g.ano == a), "mortos"].sum()) for a in anos] for k in ids]
        d["causas"] = causas(g)
        h = g.groupby("hora").mortos.sum(); d["hora"] = [int(h.get(x, 0)) for x in range(24)]
        g5 = g[g.ano <= 2025]; tot = max(1, g5.mortos.sum())
        d["moto"] = round(float(g5.mortos_moto.sum() / tot), 3); d["ped"] = round(float(g5.mortos_pedestre.sum() / tot), 3)
        d["simples"] = round(float(g.loc[g.tipo_pista.eq("Simples"), "mortos"].sum() / max(1, g.mortos.sum())), 3)
    return d
out = {"ufs": {}, "brs": {}, "bruf": {}, "muns": {}, "nac_causas": causas(t, 10),
       "nac_catAno": [[int(t.loc[t["c_" + k] & (t.ano == a), "mortos"].sum()) for a in anos] for k in ids],
       "nac_fg": serie(t, "feridos_graves")}
for uf, g in t.groupby("uf"): out["ufs"][uf] = bloco_stats(g)
for br, g in t.groupby("br"):
    if pd.isna(br) or int(br) == 0: continue
    d = bloco_stats(g, False); d["causas"] = causas(g, 4); out["brs"][str(int(br))] = d
for (br, uf), g in t.groupby(["br", "uf"]):
    if pd.isna(br) or int(br) == 0: continue
    s = serie(g, "mortos")
    if sum(s): out["bruf"][f"{int(br)}|{uf}"] = {"m": s, "a": serie(g, "n"), "causas": causas(g, 4)}
for (mu, uf), g in t.groupby(["municipio", "uf"]):
    s = serie(g, "mortos")
    if sum(s) >= 1: out["muns"][f"{mu}|{uf}"] = {"m": s, "a": serie(g, "n"), "causas": causas(g, 3)}
D["extra"] = out
json.dump(D, open("dados/sentinela_dados.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(len(out["ufs"]), len(out["brs"]), len(out["bruf"]), len(out["muns"]))
print("DF", out["ufs"]["DF"]["m"], out["ufs"]["DF"]["causas"][:3])
print(sum(out["ufs"][u]["m"][1] for u in out["ufs"]), D["nacional"]["mortes_ano"]["2022"])
import os; print(os.path.getsize("dados/sentinela_dados.json") / 1e6, "MB")
