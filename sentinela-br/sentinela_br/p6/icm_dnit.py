"""ICM – Índice de Condição da Manutenção (DNIT, dados abertos "Condições do Pavimento").
1) baixar(): lista e baixa todos os CSV do conjunto pela API CKAN do DNIT (série histórica);
2) consolidar(pasta): lê os CSV (qualquer mês/ano), reconhece as colunas pelo nome, cruza com os trechos de 5 km
   (BR + UF + km; ou latitude/longitude quando o km não vier) e grava icm.json para o painel.
Faixas oficiais do DNIT: ICM < 30 Bom; 30–50 Regular; 50–70 Ruim; > 70 Péssimo.
Uso: python icm_dnit.py baixar   |   python icm_dnit.py consolidar <pasta_com_csv>"""
import csv, io, json, os, re, sys, glob, unicodedata, urllib.request, math, collections
API = os.environ.get("DNIT_CKAN", "https://servicos.dnit.gov.br/dadosabertos/api/3/action/package_show?id=condicoes-do-pavimento")
PAGINA = "https://servicos.dnit.gov.br/dadosabertos/dataset/condicoes-do-pavimento"
AQUI = os.path.dirname(os.path.abspath(__file__))
CLASSES = ["Bom", "Regular", "Ruim", "Péssimo"]
def classe(v): return 0 if v < 30 else 1 if v < 50 else 2 if v < 70 else 3
def sa(s): return unicodedata.normalize("NFD", str(s)).encode("ascii", "ignore").decode().lower().strip()
def num(x):
    x = str(x).strip().replace(" ", "")
    if not x: return None
    if "," in x and "." in x: x = x.replace(".", "").replace(",", ".")
    else: x = x.replace(",", ".")
    try: return float(x)
    except ValueError: return None

def baixar(destino=os.path.join(AQUI, "icm_csv")):
    os.makedirs(destino, exist_ok=True)
    pkg = json.load(urllib.request.urlopen(API, timeout=60))["result"]
    n = 0
    for r in pkg["resources"]:
        if (r.get("format") or "").lower() not in ("csv", "xlsx"): continue
        nome = re.sub(r"[^\w.-]+", "_", (r.get("name") or r["id"]))[:90] + "." + (r.get("format") or "csv").lower()
        alvo = os.path.join(destino, nome)
        if os.path.exists(alvo): continue
        urllib.request.urlretrieve(r["url"], alvo); n += 1
    print("CSV novos do ICM:", n); return destino

COL = {"br": [r"^br$", r"^rodovia$", r"^vl_br$", r"^br_"], "uf": [r"^uf$", r"^sg_uf$", r"^estado$"],
       "kmi": [r"km.*ini", r"^km_?i$", r"^vl_km_inicial$"], "kmf": [r"km.*fi", r"^km_?f$", r"^vl_km_final$"], "km": [r"^km$"],
       "icm": [r"^icm$", r"^vl_icm$", r"^icm_?(valor|total)?$"], "data": [r"data", r"^mes", r"periodo", r"levantamento"],
       "ano": [r"^ano$"], "lat": [r"^lat", r"latitude"], "lon": [r"^lon", r"longitude", r"^lng"]}
def mapear(cab):
    m = {}
    c2 = [sa(c) for c in cab]
    for k, pads in COL.items():
        for p in pads:
            hit = [i for i, c in enumerate(c2) if re.search(p, c) and not (k == "icm" and "np" in c)]
            if hit: m[k] = hit[0]; break
    return m
def ler(arq):
    raw = open(arq, "rb").read()
    for enc in ("utf-8-sig", "latin-1"):
        try: txt = raw.decode(enc); break
        except UnicodeDecodeError: continue
    sep = ";" if txt[:2000].count(";") > txt[:2000].count(",") else ","
    rd = csv.reader(io.StringIO(txt), delimiter=sep); cab = next(rd); m = mapear(cab)
    falta = [k for k in ("icm",) if k not in m]
    if falta or not (("br" in m and "uf" in m and ("kmi" in m or "km" in m)) or ("lat" in m and "lon" in m)):
        print("  ignorado (colunas não reconhecidas):", os.path.basename(arq), cab[:12]); return []
    ano_arq = re.search(r"(20\d\d)", os.path.basename(arq))
    out = []
    for row in rd:
        try:
            v = num(row[m["icm"]])
            if v is None or v < 0 or v > 100: continue
            br = int(re.sub(r"\D", "", row[m["br"]]) or 0) if "br" in m else 0
            uf = row[m["uf"]].strip().upper()[:2] if "uf" in m else ""
            ki = num(row[m["kmi"]]) if "kmi" in m else num(row[m["km"]]) if "km" in m else None
            kf = num(row[m["kmf"]]) if "kmf" in m else (ki + 1 if ki is not None else None)
            la = num(row[m["lat"]]) if "lat" in m else None; lo = num(row[m["lon"]]) if "lon" in m else None
            dt = row[m["data"]].strip() if "data" in m else ""
            ano = int(row[m["ano"]]) if "ano" in m and row[m["ano"]].strip().isdigit() else int(re.search(r"(20\d\d)", dt).group(1)) if re.search(r"(20\d\d)", dt) else int(ano_arq.group(1)) if ano_arq else 0
            out.append((br, uf, ki, kf, la, lo, v, ano, dt))
        except (IndexError, ValueError): continue
    print(f"  {os.path.basename(arq)}: {len(out)} registros")
    return out

def consolidar(pasta, trechos_json=os.path.join(AQUI, "dados.json"), saida=os.path.join(AQUI, "icm.json")):
    D = json.load(open(trechos_json)); T = D["tr"]
    chave = {(b, u, k): i for i, (b, u, k) in enumerate(zip(T["br"], T["uf"], T["km"]))}
    grade = collections.defaultdict(list)  # para cruzar por latitude/longitude
    for i, (la, lo) in enumerate(zip(T["lat"], T["lon"])): grade[(round(la * 10), round(lo * 10))].append(i)
    def perto(la, lo):
        best, bd = None, 3.0  # até 3 km
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for i in grade.get((round(la * 10) + dx, round(lo * 10) + dy), []):
                    d = math.hypot((T["lat"][i] - la) * 111, (T["lon"][i] - lo) * 111 * math.cos(math.radians(la)))
                    if d < bd: best, bd = i, d
        return best
    regs = []
    for arq in sorted(glob.glob(os.path.join(pasta, "**", "*.csv"), recursive=True)): regs += ler(arq)
    if not regs: print("Nenhum registro de ICM reconhecido."); return None
    ult = max(r[7] for r in regs)
    km_cls = collections.defaultdict(lambda: [0.0] * 4)  # km avaliados por classe e ano (malha DNIT)
    por_tr = collections.defaultdict(lambda: collections.defaultdict(list))  # trecho -> ano -> valores
    for br, uf, ki, kf, la, lo, v, ano, dt in regs:
        ext = max(0.1, (kf - ki)) if ki is not None and kf is not None else 1.0
        km_cls[ano][classe(v)] += ext
        alvo = []
        if br and uf and ki is not None:
            for b5 in range(int(ki // 5 * 5), int(max(ki, (kf or ki) - 1e-6) // 5 * 5) + 5, 5):
                if (br, uf, b5) in chave: alvo.append(chave[(br, uf, b5)])
        if not alvo and la is not None and lo is not None:
            j = perto(la, lo)
            if j is not None: alvo.append(j)
        for j in alvo: por_tr[j][ano].append(v)
    n = len(T["br"]); icm = [-1.0] * n; icm_ano = [0] * n; serie = [None] * n
    for j, anos in por_tr.items():
        a = max(anos); icm[j] = round(sum(anos[a]) / len(anos[a]), 1); icm_ano[j] = a
        serie[j] = {str(k): round(sum(v) / len(v), 1) for k, v in sorted(anos.items())}
    nac = {str(a): [round(x) for x in v] for a, v in sorted(km_cls.items()) if a}
    out = {"fonte": "DNIT – Condições do Pavimento (ICM), dados abertos", "link": PAGINA, "ate": ult, "registros": len(regs),
           "icm": icm, "ano": icm_ano, "serie": serie, "km_classe": nac, "classes": CLASSES}
    json.dump(out, open(saida, "w"), ensure_ascii=False, separators=(",", ":"))
    com = sum(1 for x in icm if x >= 0)
    print(f"ICM: {len(regs)} registros, trechos com ICM: {com} de {n}, último ano: {ult}")
    return out

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "baixar":
        import icm_carga; icm_carga.consolidar(baixar())
    elif len(sys.argv) > 2 and sys.argv[1] == "consolidar": consolidar(sys.argv[2])
    else: print(__doc__)
