"""Liga componentes isolados da malha PRF ao longo da mesma BR (ex.: BR-319 AM e BR-174 AM/RR),
para permitir rotas como Brasília -> Boa Vista. Arestas novas: distância em linha reta x 1,25, marcadas como 'sem registro PRF'."""
import json, math, collections
D = json.load(open('dados_app.json')); N = len(D['lat']); U = D['ufs']
la, lo, br = D['lat'], D['lon'], D['br']
def hv(a, b):
    p1, p2 = math.radians(la[a]), math.radians(la[b]); dp = p2 - p1; dl = math.radians(lo[b] - lo[a])
    return 6371 * 2 * math.asin(math.sqrt(math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2))
G = D['grafo']; A, B, W = list(G['a']), list(G['b']), list(G['w']); novo = [0]*len(A)
def comps():
    adj = collections.defaultdict(list)
    for a, b in zip(A, B): adj[a].append(b); adj[b].append(a)
    c = [-1]*N; k = 0
    for s in range(N):
        if c[s] >= 0: continue
        st = [s]; c[s] = k
        while st:
            u = st.pop()
            for v in adj[u]:
                if c[v] < 0: c[v] = k; st.append(v)
        k += 1
    return c
for rodada in range(10):
    c = comps(); sz = collections.Counter(c); big = sz.most_common(1)[0][0]; feitos = 0
    for k in sorted(sz, key=lambda k: sz[k]):
        if k == big: continue
        nos = [i for i in range(N) if c[i] == k and br[i] > 0]
        if not nos: continue
        melhor = None
        for i in nos:
            for j in range(N):
                if c[j] == k or br[j] != br[i]: continue
                d = hv(i, j)
                if d < 420 and (melhor is None or d < melhor[0]): melhor = (d, i, j)
        if melhor:
            d, i, j = melhor; A.append(i); B.append(j); W.append(round(d * 1.25, 1)); novo.append(1); feitos += 1
    if not feitos: break
c = comps(); sz = collections.Counter(c); big = sz.most_common(1)[0][0]
print('arestas novas', sum(novo), 'nós na malha principal', sz[big], 'de', N)
G.update(a=A, b=B, w=W, novo=novo)
# cidades que faltavam (capitais do Norte), no nó mais próximo da malha principal
def perto(lat, lon, uf):
    cand = [i for i in range(N) if c[i] == big and U[D['uf'][i]] == uf]
    return min(cand, key=lambda i: (la[i]-lat)**2 + (lo[i]-lon)**2) if cand else None
nomes = {(x[0], x[1]) for x in D['cidades']}
for nm, uf, lat, lon, pop in [('Boa Vista', 'RR', 2.8235, -60.6758, 436), ('Manaus', 'AM', -3.119, -60.0217, 2063), ('Macapá', 'AP', 0.0349, -51.0694, 442), ('Rio Branco', 'AC', -9.9754, -67.8249, 364), ('Belém', 'PA', -1.4558, -48.4902, 1303)]:
    if (nm, uf) in nomes: continue
    i = perto(lat, lon, uf)
    if i is not None: D['cidades'].append([nm, uf, i, pop]); print('cidade', nm, uf, '->', i, D['br'][i], round(math.dist((la[i], lo[i]), (lat, lon)), 2))
json.dump(D, open('dados_app2.json', 'w'), ensure_ascii=False, separators=(',', ':'))
