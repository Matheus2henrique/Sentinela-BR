"""AdaptaBrasil (MCTI/INPE) – indicador 60041: risco de impacto de inundações, enxurradas e alagamentos (desastres geo-hidrológicos),
por município, com ameaça climática projetada (chuva intensa em 1 e 5 dias). Arquivo exportado: 2050, cenário pessimista.
Cruza com o município de cada trecho de 5 km."""
import csv, glob, json, os, sys, unicodedata, collections
AQUI = os.path.dirname(os.path.abspath(__file__))
CL = ['Muito baixo', 'Baixo', 'Médio', 'Alto', 'Muito alto']
sa = lambda s: unicodedata.normalize('NFD', str(s)).encode('ascii', 'ignore').decode().lower().replace("'", '').replace('-', ' ').strip()
def consolidar(arq, dados=os.path.join(AQUI, 'dados.json'), saida=os.path.join(AQUI, 'adapta.json')):
    M = {}; meta = {}
    for r in csv.DictReader(open(arq, encoding='utf-8-sig'), delimiter=';'):
        nome, uf = r['nome'].rsplit('/', 1)
        if r['classe'] in CL: M[(sa(nome), uf.strip())] = (CL.index(r['classe']), float(r['valor']))
        meta['ano'] = r['ano']
    D = json.load(open(dados)); T = D['tr']; n = len(T['br'])
    c = [-1] * n; v = [None] * n
    for i in range(n):
        x = M.get((sa(T['mun'][i]), T['uf'][i]))
        if x: c[i], v[i] = x
    nac = collections.Counter(k for k, _ in M.values())
    cen = 'pessimista' if 'pess' in os.path.basename(arq) else 'otimista' if 'otim' in os.path.basename(arq) else ''
    out = {'fonte': 'AdaptaBrasil (MCTI) – Desastres geo-hidrológicos: inundações, enxurradas e alagamentos (indicador 60041, risco de impacto)',
           'link': 'https://adaptabrasil.mcti.gov.br', 'meta': 'https://data.inpe.br/geonetwork/srv/api/records/adaptabrasil60041',
           'ano': meta.get('ano'), 'cenario': cen, 'classes': CL, 'municipios': [nac.get(k, 0) for k in range(5)], 'c': c, 'v': v}
    json.dump(out, open(saida, 'w'), ensure_ascii=False, separators=(',', ':'))
    ok = sum(1 for x in c if x >= 0); hi = [i for i in range(n) if c[i] >= 3]
    print(f'municípios com classe: {len(M)}; trechos com classe: {ok} de {n}; alto/muito alto: {len(hi)} trechos, {sum(T["m"][i] for i in hi)} mortes')
    return out
if __name__ == '__main__': consolidar(sys.argv[1])
