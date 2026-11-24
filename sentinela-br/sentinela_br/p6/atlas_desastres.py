"""Atlas Digital de Desastres no Brasil (MIDR/Defesa Civil, base S2iD consolidada 1991–2025, v1.1 de 06/08/2026).
Cruza os desastres que afetam rodovias (chuva, inundação, enxurrada, alagamento, deslizamento, erosão, vento, granizo,
tornado, incêndio florestal) com o município de cada trecho de 5 km. Estiagem, seca, ondas de calor/frio e doenças ficam fora."""
import json, os, sys, unicodedata, collections, openpyxl, pickle
AQUI = os.path.dirname(os.path.abspath(__file__))
CAT = {'Chuvas Intensas': 0, 'Enxurradas': 0, 'Inundações': 0, 'Alagamentos': 0, 'Movimento de Massa': 1, 'Erosão': 1,
       'Vendavais e Ciclones': 2, 'Granizo': 2, 'Tornado': 2, 'Incêndio Florestal': 3}
NOMES = ['Chuva, inundação e enxurrada', 'Deslizamento e erosão', 'Vento, granizo e tornado', 'Incêndio florestal']
sa = lambda s: unicodedata.normalize('NFD', str(s)).encode('ascii', 'ignore').decode().lower().replace("'", '').replace('-', ' ').strip()
def ler(arq):
    cache = arq + '.pkl'
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(arq): return pickle.load(open(cache, 'rb'))
    ws = openpyxl.load_workbook(arq, read_only=True)['Atlas Valores Originais']; out = []
    for k, r in enumerate(ws.iter_rows(values_only=True)):
        if k == 0: assert r[1] == 'Nome_Municipio' and r[8] == 'descricao_tipologia', r[:10]; continue
        if r[8] in CAT and r[5]: out.append((sa(r[1]), r[2], r[5].year, r[5].month, CAT[r[8]], r[12], int(r[14] or 0)))
    pickle.dump(out, open(cache, 'wb')); return out
def consolidar(arq, dados=os.path.join(AQUI, 'dados.json'), saida=os.path.join(AQUI, 'atlas.json')):
    R = ler(arq); D = json.load(open(dados)); T = D['tr']; n = len(T['br'])
    mun = collections.defaultdict(lambda: [0, 0, 0, 0]); anos = collections.defaultdict(set); recon = collections.Counter()
    mes = [[0] * 12 for _ in range(4)]; nac = [0, 0, 0, 0]; mortos = 0
    for m, uf, a, ms, c, st, mo in R:
        if 2016 <= a <= 2025: anos[(m, uf)].add(a)
        if 2021 <= a <= 2025:
            mun[(m, uf)][c] += 1; nac[c] += 1; mes[c][ms - 1] += 1; mortos += mo
            if st == 'Reconhecido': recon[(m, uf)] += 1
    dz = [None] * n; za = [0] * n; zr = [0] * n; ok = 0
    for i in range(n):
        k = (sa(T['mun'][i]), T['uf'][i])
        if k in mun: dz[i] = mun[k]; za[i] = len(anos[k]); zr[i] = recon[k]; ok += 1
        elif k in anos: za[i] = len(anos[k])
    out = {'fonte': 'Atlas Digital de Desastres no Brasil (MIDR/Defesa Civil, base S2iD 1991–2025)', 'link': 'https://atlasdigital.mdr.gov.br',
           'arquivo': os.path.basename(arq).split('-', 1)[-1] if os.path.basename(arq)[8:9] == '-' else os.path.basename(arq),
           'periodo': '2021–2025', 'cats': NOMES, 'nac': nac, 'mes': mes, 'mortos': mortos, 'municipios': len(mun),
           'dz': dz, 'za': za, 'zr': zr}
    json.dump(out, open(saida, 'w'), ensure_ascii=False, separators=(',', ':'))
    com = [i for i in range(n) if dz[i]]
    print(f'registros que afetam rodovias: {len(R)}; 2021–2025: {sum(nac)} em {len(mun)} municípios; mortes nos desastres: {mortos}')
    print(f'trechos em município com desastre 2021–2025: {len(com)} de {n}; mortes PRF nesses trechos: {sum(T["m"][i] for i in com)}')
    return out
if __name__ == '__main__': consolidar(sys.argv[1])
