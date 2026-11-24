import os as _os
_BASE = _os.environ.get("SENTINELA_BASE", "/home/claude")
"""Reconstrói a geometria das rodovias federais a partir das coordenadas dos registros da PRF (2021-2026)
e monta um grafo geométrico para rotas. Saída: rede.pkl."""
import numpy as np, pandas as pd, pickle
from scipy.spatial import cKDTree
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
R = 6371.0
def hav(a1, o1, a2, o2):
    a1, o1, a2, o2 = map(np.radians, (a1, o1, a2, o2))
    return 2 * R * np.arcsin(np.sqrt(np.sin((a2 - a1) / 2) ** 2 + np.cos(a1) * np.cos(a2) * np.sin((o2 - o1) / 2) ** 2))

t = pd.read_pickle(f"{_BASE}/real/prf_2021_2026.pkl")
t = t[t.latitude.between(-34.5, 5.6) & t.longitude.between(-74.5, -28.5)].copy()
t["km_int"] = np.floor(t.km).astype(int)
# limpeza por registro: descarta coordenadas longe da mediana local do corredor
lim = []
for (br, uf), g in t.groupby(["br", "uf"]):
    g = g.sort_values("km")
    if len(g) >= 5:
        ml = g.latitude.rolling(31, center=True, min_periods=1).median(); mo = g.longitude.rolling(31, center=True, min_periods=1).median()
        g = g[hav(g.latitude, g.longitude, ml, mo) <= 8]
    lim.append(g)
t = pd.concat(lim)
p = t.groupby(["br", "uf", "km_int"]).agg(lat=("latitude", "median"), lon=("longitude", "median"), n=("id", "size")).reset_index()
p["nid"] = np.arange(len(p))
print("pontos", len(p))
X = np.c_[p.lat.values * 111.0, p.lon.values * 111.0 * np.cos(np.radians(p.lat.values))]
tree = cKDTree(X)
cor = (p.br.astype(str) + "-" + p.uf).values
E = {}
def add(i, j, w, tipo):
    k = (min(i, j), max(i, j))
    if k not in E or w < E[k][0]:
        E[k] = (w, tipo)
# 1) sequência do km quando coerente
for (br, uf), g in p.groupby(["br", "uf"]):
    g = g.sort_values("km_int"); a = g.iloc[:-1]; b = g.iloc[1:]
    gap = b.km_int.values - a.km_int.values
    d = np.hypot(*(X[a.nid.values] - X[b.nid.values]).T)
    for i, j, dd, gg in zip(a.nid.values, b.nid.values, d, gap):
        if gg <= 60 and dd <= 1.5 * gg + 10:
            add(i, j, max(float(gg), dd), 0)
# 2) vizinhos geométricos (mesmo corredor ou cruzamentos)
dist, idx = tree.query(X, k=8, distance_upper_bound=5.0)
for i in range(len(p)):
    for dd, j in zip(dist[i, 1:], idx[i, 1:]):
        if np.isfinite(dd):
            if cor[i] == cor[j]:
                gk = abs(int(p.km_int.values[i]) - int(p.km_int.values[j]))
                add(i, j, max(float(gk), dd) if gk <= 1.5 * dd + 3 else dd * 1.3, 1)
            else:
                add(i, j, dd * 1.25 + 0.2, 1)
# 2b) pontas de corredor (fim de BR ou de segmento) ligam às rodovias mais próximas (até 15 km; mesma BR em outra UF até 40 km)
pontas = []
for (br, uf), g in p.groupby(["br", "uf"]):
    g = g.sort_values("km_int"); km = g.km_int.values; ids = g.nid.values
    quebra = np.nonzero(np.diff(km) > 25)[0]
    ini = np.r_[0, quebra + 1]; fim = np.r_[quebra, len(km) - 1]
    pontas += list(ids[ini]) + list(ids[fim])
for i in set(pontas):
    for dd, j in zip(*tree.query(X[i], k=60, distance_upper_bound=40.0)):
        if not np.isfinite(dd) or cor[j] == cor[i]:
            continue
        mesma_br = p.br.values[j] == p.br.values[i]
        if dd <= 15 or (mesma_br and dd <= 40):
            add(i, j, dd * 1.35 + 1.0, 3)
def comps():
    k = np.array(list(E.keys()))
    M = sp.coo_matrix((np.ones(len(k)), (k[:, 0], k[:, 1])), shape=(len(p), len(p)))
    return connected_components(M, directed=False)
nc, lab = comps(); print("componentes antes das pontes", nc, "maior", np.bincount(lab).max())
# 3) pontes (Boruvka): cada componente com 3+ pontos liga ao componente vizinho mais próximo (até 80 km)
for it in range(20):
    nc, lab = comps(); cnt = np.bincount(lab)
    grandes = np.nonzero(cnt >= 3)[0]
    if len(grandes) <= 1:
        break
    novas = 0
    for c in grandes:
        mem = np.nonzero(lab == c)[0]; out = np.nonzero((lab != c) & (cnt[lab] >= 3))[0]
        if len(out) == 0:
            continue
        to = cKDTree(X[out]); d, j = to.query(X[mem]); k = d.argmin()
        if d[k] <= 80:
            add(mem[k], out[j[k]], d[k] * 1.4 + 2, 2); novas += 1
    print("iteração", it, "componentes", nc, "pontes", novas)
    if novas == 0:
        break
nc, lab = comps(); cnt = np.bincount(lab); big = cnt.argmax()
print("componentes", nc, "maior", cnt.max(), f"({cnt.max()/len(p):.1%})")
p["principal"] = lab == big
e = pd.DataFrame([(a, b, w, tp) for (a, b), (w, tp) in E.items()], columns=["a", "b", "w", "tipo"])
# cidades
c = t.groupby(["municipio", "uf"]).agg(lat=("latitude", "median"), lon=("longitude", "median"), n=("id", "size")).reset_index()
c = c[c.n >= 10].reset_index(drop=True)
pm = p[p.principal]
tc = cKDTree(X[pm.nid.values])
Xc = np.c_[c.lat.values * 111.0, c.lon.values * 111.0 * np.cos(np.radians(c.lat.values))]
dd, ii = tc.query(Xc)
c["nid"] = pm.nid.values[ii]; c["dist_km"] = dd
c = c[c.dist_km <= 12].reset_index(drop=True)
print("cidades", len(c), "arestas", len(e))
pickle.dump({"nos": p, "arestas": e, "cidades": c, "t_limpo_ids": set(t.id)}, open("rede.pkl", "wb"))
