import os as _os
_BASE = _os.environ.get("SENTINELA_BASE", "/home/claude")
"""Perfil de risco por trecho de 5 km (PRF 2021-out/2026), grafo simplificado para rotas e estatísticas nacionais.
Gera dados/sentinela_dados.json, consumido pelo painel e pela API."""
import json, pickle, numpy as np, pandas as pd
from scipy.spatial import cKDTree
R = 6371.0
rede = pickle.load(open("rede.pkl", "rb"))
nos, arestas, cidades = rede["nos"], rede["arestas"], rede["cidades"]
t = pd.read_pickle(f"{_BASE}/real/prf_2021_2026.pkl")
t["limpo"] = t.id.isin(rede["t_limpo_ids"])
t["bin"] = (np.floor(t.km) // 5 * 5).astype(int)
t["fatal"] = t.classificacao_acidente.str.contains("Fatais", na=False)
t["grave"] = t.fatal | (t.feridos_graves > 0)
t["hora"] = pd.to_numeric(t.horario.str[:2], errors="coerce")
C = t.causas_todas.fillna(""); T = t.tipos_todos.fillna(""); M = t.condicao_metereologica.fillna("")
def tem(s, termos): return s.str.contains("|".join(termos), regex=True)
CAT = {
 "chuva": ("Chuva e pista molhada", M.isin(["Chuva", "Garoa/Chuvisco"]) | tem(C, ["Chuva", "Pista Escorregadia"])),
 "alagamento": ("Alagamento e água na pista", tem(C, ["Acumulo de água", "drenagem ineficiente"])),
 "encosta": ("Objetos, detritos ou queda de barreira", tem(C, ["Fenômenos da natureza", "Objeto estático", "Obstrução na via", "areia ou detritos"])),
 "via": ("Via ruim: buracos, acostamento, sinalização", tem(C, ["Pista esburacada", "Afundamento", "Demais falhas na via", "Falta de acostamento",
          "Acostamento em desnível", "Pista em desnível", "Ausência de sinalização", "Sinalização mal posicionada", "Sinalização encoberta",
          "Iluminação deficiente", "Deficiência do Sistema", "Falta de elemento de contenção", "largura insuficiente", "Obras na pista", "Desvio temporário", "Acumulo de óleo"])),
 "curva": ("Curvas e serra", t.tracado_via.isin(["Curva", "Declive"]) | tem(C, ["Curva acentuada", "Declive acentuado", "Restrição de visibilidade"])),
 "neblina": ("Neblina ou fumaça", M.eq("Nevoeiro/Neblina") | tem(C, ["Neblina", "Fumaça"])),
 "animais": ("Animais na pista", tem(C, ["Animais na Pista"]) | tem(T, ["Atropelamento de Animal"])),
 "pedestres": ("Pedestres na pista", tem(T, ["Atropelamento de Pedestre"])),
 "frontal": ("Ultrapassagem e colisão frontal", tem(T, ["Colisão frontal", "Colisão lateral sentido oposto"]) | tem(C, ["Ultrapassagem Indevida", "Transitar na contramão"])),
 "sono": ("Sono e fadiga", tem(C, ["Condutor Dormindo"])),
 "motos": ("Motociclistas", t.moto.fillna(False).astype(bool) | tem(T, ["Queda de ocupante"]) | tem(C, ["motocicleta"])),
 "alcool": ("Álcool", tem(C, ["Ingestão de álcool pelo condutor", "psicoativas pelo condutor"])),
 "velocidade": ("Velocidade incompatível", tem(C, ["Velocidade Incompatível"])),
 "traseira": ("Engavetamento e colisão traseira", tem(T, ["Colisão traseira", "Engavetamento"])),
}
for k, (_, s) in CAT.items():
    t["c_" + k] = s.values
anos = [2021, 2022, 2023, 2024, 2025, 2026]
n_anos = 5 + 10 / 12
# ---------- agregação por trecho (só registros com coordenada coerente)
tt = t
t = tt[tt.limpo].copy()
g = t.groupby(["br", "uf", "bin"])
b = g.agg(n=("id", "size"), mortos=("mortos", "sum"), fatais=("fatal", "sum"), graves=("grave", "sum"),
          urbano=("uso_solo", lambda s: (s == "Sim").mean()), pista=("tipo_pista", lambda s: s.mode().iat[0] if len(s.mode()) else ""),
          mun=("municipio", lambda s: s.mode().iat[0])).reset_index()
fa = t[t.fatal].groupby(["br", "uf", "bin", "ano"]).size().unstack(fill_value=0).reindex(columns=anos, fill_value=0)
mo = t.groupby(["br", "uf", "bin", "ano"]).mortos.sum().unstack(fill_value=0).reindex(columns=anos, fill_value=0)
b = b.merge(fa.add_prefix("f").reset_index(), on=["br", "uf", "bin"], how="left").merge(mo.add_prefix("m").reset_index(), on=["br", "uf", "bin"], how="left").fillna(0)
b["anos_fatal"] = (b[[f"f{a}" for a in anos]] > 0).sum(axis=1)
# EB: acidentes fatais por ano, encolhidos para a média do corredor
b["fat_ano"] = b.fatais / n_anos
out = []
for (br, uf), gg in b.groupby(["br", "uf"]):
    m = gg.fatais.mean(); v = gg.fatais.var(ddof=0) if len(gg) > 1 else m
    alpha = max((v - m) / m ** 2, 0.05) if m > 0 else 1.0
    w = 1 / (1 + alpha * m)
    out.append(pd.Series(w * m + (1 - w) * gg.fatais, index=gg.index))
b["eb"] = pd.concat(out) / n_anos
q = b.eb.quantile([0.85, 0.95, 0.99])
b["nivel"] = np.select([b.eb >= q[0.99], b.eb >= q[0.95], b.eb >= q[0.85]], [3, 2, 1], 0)
b["cronico"] = (b.anos_fatal >= 4) & (b.fatais >= 5)
# categorias: contagem, mortes, alerta
nac = {k: t["c_" + k].mean() for k in CAT}
for k in CAT:
    a = t[t["c_" + k]].groupby(["br", "uf", "bin"]).agg(**{f"{k}_n": ("id", "size"), f"{k}_m": ("mortos", "sum")}).reset_index()
    b = b.merge(a, on=["br", "uf", "bin"], how="left")
    b[[f"{k}_n", f"{k}_m"]] = b[[f"{k}_n", f"{k}_m"]].fillna(0)
    minimo = 2 if k in ("alagamento", "encosta", "neblina") else 4
    b[f"{k}_alerta"] = ((b[f"{k}_n"] >= minimo) & (b[f"{k}_n"] / b.n >= 1.5 * nac[k])) | (b[f"{k}_m"] >= 3)
# horário e dia de maior risco (acidentes com vítima grave)
gv = t[t.grave]
per = pd.cut(gv.hora, [-1, 5, 11, 17, 23], labels=["madrugada", "manhã", "tarde", "noite"])
hp = gv.assign(per=per).groupby(["br", "uf", "bin"]).per.agg(lambda s: s.mode().iat[0] if len(s.mode()) else "")
dias = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
dp = gv.assign(dw=gv.data.dt.dayofweek).groupby(["br", "uf", "bin"]).dw.agg(lambda s: dias[int(s.mode().iat[0])] if len(s.mode()) else "")
b = b.join(hp.rename("periodo"), on=["br", "uf", "bin"]).join(dp.rename("dia"), on=["br", "uf", "bin"])
# meses de chuva com mais acidentes
cm = t[t.c_chuva].groupby(["br", "uf", "bin"]).data.agg(lambda s: list(s.dt.month.value_counts().head(3).index))
b = b.join(cm.rename("meses_chuva"), on=["br", "uf", "bin"])
# posição do trecho: mediana dos nós do grafo
nos["bin"] = nos.km_int // 5 * 5
pos = nos.groupby(["br", "uf", "bin"]).agg(lat=("lat", "median"), lon=("lon", "median")).reset_index()
b = b.merge(pos, on=["br", "uf", "bin"], how="inner")
b = b.sort_values(["br", "uf", "bin"]).reset_index(drop=True)
b["i"] = np.arange(len(b))
print("trechos", len(b), "| níveis:", b.nivel.value_counts().to_dict(), "| crônicos:", int(b.cronico.sum()))
# ---------- grafo simplificado (nó = trecho de 5 km)
key = {(r.br, r.uf, r.bin): r.i for r in b.itertuples()}
nos["ti"] = [key.get((x, y, z), -1) for x, y, z in zip(nos.br, nos.uf, nos.bin)]
ti = nos.ti.values
ea, eb_ = ti[arestas.a.values], ti[arestas.b.values]
ok = (ea >= 0) & (eb_ >= 0) & (ea != eb_)
E = pd.DataFrame({"a": np.minimum(ea[ok], eb_[ok]), "b": np.maximum(ea[ok], eb_[ok]), "tipo": arestas.tipo.values[ok]})
la, lo = b.lat.values, b.lon.values
def hav(a1, o1, a2, o2):
    a1, o1, a2, o2 = map(np.radians, (a1, o1, a2, o2))
    return 2 * R * np.arcsin(np.sqrt(np.sin((a2 - a1) / 2) ** 2 + np.cos(a1) * np.cos(a2) * np.sin((o2 - o1) / 2) ** 2))
E = E.drop_duplicates(["a", "b"])
mesmo = (b.br.values[E.a] == b.br.values[E.b]) & (b.uf.values[E.a] == b.uf.values[E.b])
dkm = np.abs(b.bin.values[E.a] - b.bin.values[E.b]).astype(float)
dd = hav(la[E.a], lo[E.a], la[E.b], lo[E.b])
E["w"] = np.where(mesmo & (dkm <= 1.6 * dd + 6), np.maximum(dkm, dd), dd * 1.3 + 0.5).round(1)
print("arestas do grafo simplificado", len(E))
# ---------- cidades
cid = cidades.copy()
cid["ti"] = [ti[n] for n in cid.nid]
cid = cid[cid.ti >= 0]
def tit(m):
    menores = {"de", "da", "do", "das", "dos", "e"}
    return " ".join(w if w in menores else w.capitalize() for w in str(m).lower().split())
# nomes com acento: usa o nome mais frequente com acento? A PRF grava sem acento; mantém título simples
cid = cid.sort_values("n", ascending=False)
# ---------- corredores e nacionais (base completa)
t = tt
cor = t.groupby(["br", "uf"]).agg(mortos=("mortos", "sum"), n=("id", "size")).reset_index()
cm_ = t.groupby(["br", "uf", "ano"]).mortos.sum().unstack(fill_value=0).reindex(columns=anos, fill_value=0)
cor = cor.join(cm_.add_prefix("m"), on=["br", "uf"]).sort_values("mortos", ascending=False)
nacional = {
  "periodo": "jan/2021 a out/2026",
  "mortes_ano": {str(a): int(t[t.ano == a].mortos.sum()) for a in anos},
  "acidentes_ano": {str(a): int((t.ano == a).sum()) for a in anos},
  "mortes_total": int(t.mortos.sum()), "acidentes_total": int(len(t)),
  "mortes_por_categoria": {k: int(t.loc[t["c_" + k], "mortos"].sum()) for k in CAT},
  "mortes_por_hora": [int(t.loc[t.hora == h, "mortos"].sum()) for h in range(24)],
  "mortes_por_mes": [int(t.loc[t.data.dt.month == m, "mortos"].sum()) for m in range(1, 13)],
  "pista_simples_pct": float(t.loc[t.tipo_pista == "Simples", "mortos"].sum() / t.mortos.sum()),
  "mortes_moto_pct_2021_2025": float(t.loc[t.ano <= 2025, "mortos_moto"].sum() / t.loc[t.ano <= 2025, "mortos"].sum()),
  "mortes_pedestre_pct_2021_2025": float(t.loc[t.ano <= 2025, "mortos_pedestre"].sum() / t.loc[t.ano <= 2025, "mortos"].sum()),
  "noite_pct": float(t.loc[t.fase_dia == "Plena Noite", "mortos"].sum() / t.mortos.sum()),
}
print(json.dumps(nacional, ensure_ascii=False)[:600])
pickle.dump({"b": b, "E": E, "cid": cid, "cor": cor, "nac": nacional, "CAT": {k: v[0] for k, v in CAT.items()}}, open("perfis.pkl", "wb"))
