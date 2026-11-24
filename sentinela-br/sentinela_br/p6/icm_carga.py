"""Carga dos arquivos oficiais do ICM (DNIT – Condições do Pavimento) recebidos:
 2021: icm_dezembro_csv.csv · 2022: icm_12_2022.csv · 2023: icm-dados-aberto-12_2023.xlsx (aba ICM - PAV)
 2024: icm-dados-abertos-12_2024.xlsx (aba ICM - Levantamentos PAV) · 2025: levantamentos_pavimentada_2025_12.csv
 2026: levantamentos_pavimentada_2026_10.csv.  ICM = 0,7·IP + 0,3·IC (DNIT). Por km e ano vale o pior sentido
 (mesma lógica do ICM_Unificado dos arquivos de 2025 e 2026). Somente pista pavimentada."""
import csv, glob, io, os, re, collections, json, openpyxl
def num(x):
    if x is None: return None
    if isinstance(x, (int, float)): return float(x)
    x = str(x).strip().strip('"')
    if not x: return None
    x = x.replace(',', '.') if x.count(',') == 1 and '.' not in x else x.replace('.', '').replace(',', '.') if ',' in x else x
    try: return float(x)
    except ValueError: return None
def br(x): m = re.search(r'(\d+)', str(x)); return int(m.group(1)) if m else 0
REG = collections.defaultdict(dict)   # (ano) -> {(br, uf, km_int): icm (pior sentido)}
LL = {}                               # (br, uf, km_int) -> (lat, lon) quando o arquivo traz
def guarda(ano, b, uf, ki, kf, v, la=None, lo=None):
    if v is None or not (0 <= v <= 100) or ki is None or not b: return
    a, z = sorted((ki, kf if kf is not None else ki + 1))
    for k in range(int(a), max(int(a) + 1, int(z + 0.999) if z > a else int(a) + 1)):
        key = (b, uf, k); REG[ano][key] = max(v, REG[ano].get(key, -1))
        if la is not None and lo is not None and key not in LL: LL[key] = (la, lo)
def csv_antigo(arq, ano):   # 2021 e 2022: UF;Rodovia;km inicial;km final;Extensão;Data;Latitude;Longitude;[Obs;]ICC;ICP;ICM
    txt = open(arq, encoding='utf-8-sig').read(); linhas = txt.splitlines(); h = next(i for i, l in enumerate(linhas) if l.startswith('UF;'))
    rd = csv.reader(io.StringIO('\n'.join(linhas[h:])), delimiter=';'); cab = next(rd); ix = {c.strip(): i for i, c in enumerate(cab)}
    n = 0
    for r in rd:
        if len(r) < len(cab) or not r[0].strip(): continue
        guarda(ano, br(r[ix['Rodovia']]), r[ix['UF']].strip(), num(r[ix['km inicial']]), num(r[ix['km final']]), num(r[ix['ICM']]), num(r[ix['Latitude']]), num(r[ix['Longitude']])); n += 1
    return n
def xlsx(arq, ano, aba):    # 2023 e 2024: colunas fixas; ICM na 31ª coluna, lat/lon na 26ª/27ª
    ws = openpyxl.load_workbook(arq, read_only=True)[aba]; n = 0
    for k, r in enumerate(ws.iter_rows(values_only=True)):
        if k < 3 or not r[0]: continue
        guarda(ano, br(r[1]), str(r[0]).strip(), num(r[3]), num(r[4]), num(r[30]), num(r[25]), num(r[26])); n += 1
    return n
def csv_novo(arq, ano):     # 2025 e 2026: levantamentos_pavimentada (Rodovia, Km_Inicial, Km_Final, ICM por sentido)
    rd = csv.DictReader(open(arq, encoding='utf-8-sig'), delimiter=';'); n = 0
    for r in rd:
        if (r.get('Superfície') or r.get('Superficie') or 'Pavimentada') != 'Pavimentada': continue
        guarda(ano, br(r['Rodovia']), r['UF'].strip(), num(r['Km_Inicial']), num(r['Km_Final']), num(r['ICM'])); n += 1
    return n
def tipo(arq):
    """Reconhece o layout pelo conteúdo (vale para os nomes que o DNIT usar nas próximas publicações)."""
    if arq.lower().endswith('.xlsx'):
        wb = openpyxl.load_workbook(arq, read_only=True)
        aba = next((w for w in wb.sheetnames if 'PAV' in w.upper() and 'NPAV' not in w.upper()), None)
        return (xlsx, (aba,)) if aba else (None, ())
    ini = open(arq, encoding='utf-8-sig', errors='replace').read(4000)
    if 'id_malha' in ini and 'Km_Inicial' in ini: return csv_novo, ()
    if 'km inicial' in ini and 'ICM' in ini: return csv_antigo, ()
    return None, ()
def carregar(pasta):
    arqs = sorted(glob.glob(os.path.join(pasta, '**', '*.csv'), recursive=True) + glob.glob(os.path.join(pasta, '**', '*.xlsx'), recursive=True))
    por_ano = {}
    for arq in arqs:
        m = re.findall(r'(20\d\d)', os.path.basename(arq)); f, extra = tipo(arq)
        if not f: continue
        ano = int(m[-1]) if m else 2021   # o arquivo "icm_dezembro_csv" do DNIT é o levantamento de dez/2021
        if ano not in por_ano or os.path.getmtime(arq) > os.path.getmtime(por_ano[ano][1]): por_ano[ano] = (f, arq, extra)
    info = []
    for ano in sorted(por_ano):
        f, arq, extra = por_ano[ano]; n = f(arq, ano, *extra)
        nome = os.path.basename(arq); nome = nome.split('-', 1)[1] if re.match(r'^[0-9a-f]{8}-', nome) else nome
        info.append((ano, nome, n, len(REG[ano]))); print(f'{ano}: {nome} · {n} linhas · {len(REG[ano])} km avaliados')
    return info
def classe(v): return 0 if v < 30 else 1 if v < 50 else 2 if v < 70 else 3
def consolidar(pasta, dados=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dados.json'), saida=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icm.json')):
    info = carregar(pasta); D = json.load(open(dados)); T = D['tr']; n = len(T['br'])
    import antt_concessoes as AC; conc_km = lambda b, u, k: AC.responsavel(b, u, k, k + 1) is not None
    idx = {(b, u, k): i for i, (b, u, k) in enumerate(zip(T['br'], T['uf'], T['km']))}
    anos = sorted(REG); serie = [None] * n; icm = [-1.0] * n; ano_i = [0] * n; kmc = {}
    for a in anos:
        acc = collections.defaultdict(list); km = [0, 0, 0, 0]
        for (b, u, k), v in REG[a].items():
            if conc_km(b, u, k): continue   # km concedido: o ICM do DNIT não se aplica (cuidado pela concessionária)
            km[classe(v)] += 1; i = idx.get((b, u, k // 5 * 5))
            if i is not None and T['conc'][i] < 0: acc[i].append(v)
        kmc[str(a)] = km
        for i, vs in acc.items():
            m = round(sum(vs) / len(vs), 1); serie[i] = serie[i] or {}; serie[i][str(a)] = m
    for i in range(n):
        if serie[i]: a = max(serie[i], key=int); icm[i] = serie[i][a]; ano_i[i] = int(a)
    # cruzamento no mesmo ano: mortes do ano (PRF) no trecho × classe do ICM daquele ano; denominador = km avaliados no ano
    mo = [0, 0, 0, 0]
    for i in range(n):
        for k, a in enumerate(range(2021, 2027)):
            v = (serie[i] or {}).get(str(a))
            if v is not None: mo[classe(v)] += T['ano'][i][k]
    kma = [sum(kmc[a][c] for a in kmc) for c in range(4)]
    cruz = {'mortes': mo, 'km_ano': kma, 'taxa': [round(mo[c] / kma[c] * 100, 2) if kma[c] else 0 for c in range(4)]}
    print('cruzamento no mesmo ano:', cruz)
    out = {'cruz': cruz, 'fonte': 'DNIT – Condições do Pavimento (ICM), dados abertos', 'link': 'https://servicos.dnit.gov.br/dadosabertos/dataset/condicoes-do-pavimento',
           'ate': max(anos), 'anos': anos, 'arquivos': [[a, f, l, k] for a, f, l, k in info], 'icm': icm, 'ano': ano_i, 'serie': serie, 'km_classe': kmc,
           'classes': ['Bom', 'Regular', 'Ruim', 'Péssimo'], 'regra': 'ICM = 0,7·IP + 0,3·IC; por km vale o pior sentido; trecho de 5 km = média dos km avaliados'}
    json.dump(out, open(saida, 'w'), ensure_ascii=False, separators=(',', ':'))
    com = [i for i in range(n) if icm[i] >= 0]; dn = [i for i in range(n) if T['conc'][i] < 0]
    print(f'trechos com ICM: {len(com)} de {n} ({len([i for i in com if T["conc"][i] < 0])} de {len(dn)} trechos DNIT); mortes cobertas: {sum(T["m"][i] for i in com)} de {sum(T["m"][i] for i in dn)} em trechos DNIT')
    return out
if __name__ == '__main__':
    import sys; consolidar(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/icm_in')
