"""Todos os municípios do IBGE (5.570) com coordenadas -> ponto mais próximo da malha federal da PRF (componente principal)."""
import csv, json, collections, numpy as np
D = json.load(open('dados_app2.json')); N = len(D['lat'])
adj = collections.defaultdict(list)
for a, b in zip(D['grafo']['a'], D['grafo']['b']): adj[a].append(b); adj[b].append(a)
comp = [-1] * N; c = 0
for s in range(N):
    if comp[s] >= 0: continue
    st = [s]; comp[s] = c
    while st:
        u = st.pop()
        for v in adj[u]:
            if comp[v] < 0: comp[v] = c; st.append(v)
    c += 1
big = collections.Counter(comp).most_common(1)[0][0]
ok = np.array([i for i in range(N) if comp[i] == big and D['br'][i] > 0])
la, lo = np.array(D['lat'])[ok], np.array(D['lon'])[ok]
UF = {r['codigo_uf']: r['uf'] for r in csv.DictReader(open('/tmp/mun_ibge/estados.csv', encoding='utf-8-sig'))}
M = []
OLD = {(c[0], c[1]): c[2] for c in D['cidades'] if comp[c[2]] == big}
for r in csv.DictReader(open('/tmp/mun_ibge/municipios.csv', encoding='utf-8')):
    y, x = float(r['latitude']), float(r['longitude'])
    d = np.hypot((la - y) * 111.2, (lo - x) * 111.2 * np.cos(np.radians(y))); k = int(d.argmin()); no, dist = int(ok[k]), float(d[k])
    o = OLD.get((r['nome'], UF[r['codigo_uf']]))
    if o is not None:  # município com registros da PRF: usa o ponto da própria cidade na malha
        no = o; dist = float(np.hypot((D['lat'][o] - y) * 111.2, (D['lon'][o] - x) * 111.2 * np.cos(np.radians(y))))
    M.append([r['nome'], UF[r['codigo_uf']], no, round(dist), int(r['capital']), round(y, 4), round(x, 4)])
M.sort(key=lambda m: (m[0].lower(), m[1]))
print(len(M), 'municípios; distância mediana até a malha:', int(np.median([m[3] for m in M])), 'km; >100 km:', sum(m[3] > 100 for m in M))
json.dump(M, open('municipios_app.json', 'w'), ensure_ascii=False, separators=(',', ':'))
