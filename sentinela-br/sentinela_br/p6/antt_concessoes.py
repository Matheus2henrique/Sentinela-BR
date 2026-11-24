"""Trechos concedidos de rodovias federais — ANTT, dados abertos, arquivo informacoes-sobre-os-trechos-concedidos8_2026.csv
https://dados.antt.gov.br/dataset/trecho-concedido (somente tipo_de_rodovia = Federal; sentidos agregados).
Códigos de UF usados pela ANTT: 55 RO, 59 PA, 61 TO, 70 BA, 71 MG, 72 ES, 73 RJ, 74 SP, 75 PR, 76 SC, 77 RS, 78 MS, 79 MT, 80 GO, 81 DF."""
FONTE = "ANTT – Informações sobre os trechos concedidos (arquivo 8/2026)"
URL = "https://dados.antt.gov.br/dataset/8900b6f4-1da4-4e55-9823-de5d11ad4672/resource/916c7db5-4327-43a2-874c-f3ad293548cb/download/informacoes-sobre-os-trechos-concedidos8_2026.csv"
NOMES = {"AUTOPISTA FLUMINENSE": "Autopista Fluminense", "AUTOPISTA LITORAL SUL": "Autopista Litoral Sul", "AUTOPISTA PLANALTO SUL": "Autopista Planalto Sul",
 "AUTOPISTA REGIS BITTENCOURT": "Autopista Régis Bittencourt", "CONCEBRA": "Concebra", "CONCER": "Concer", "ECOSUL": "Ecosul", "ECOVIAS CAPIXABA": "Ecovias Capixaba",
 "ECOVIAS DAS GERAIS": "Ecovias das Gerais", "ECOVIAS DO ARAGUAIA": "Ecovias do Araguaia", "ECOVIAS DO CERRADO": "Ecovias do Cerrado", "ECOVIAS MINAS GOIÁS": "Ecovias Minas Goiás",
 "ECOVIAS PONTE": "Ecovias Ponte", "ECOVIAS RIO MINAS": "Ecovias Rio Minas", "ELOVIAS": "Elovias", "EPR IGUAÇU": "EPR Iguaçu", "EPR PARANÁ": "EPR Paraná",
 "EPR VIA MINEIRA": "EPR Via Mineira", "LITORAL PIONEIRO": "EPR Litoral Pioneiro", "MOTIVA MINAS SP": "Motiva Minas SP (Fernão Dias)", "MOTIVA PARANÁ": "Motiva Paraná",
 "NOVA 364": "Nova 364", "NOVA 381": "Nova 381", "NOVA ROTA DO OESTE": "Nova Rota do Oeste", "PANTANAL": "Motiva Pantanal", "RIOSP": "RioSP",
 "RODOVIA DO AÇO": "Rodovia do Aço", "ROTA VERDE GOIÁS": "Rota Verde Goiás", "TRANSBRASILIANA": "Transbrasiliana", "VIA ARAUCÁRIA": "Via Araucária",
 "VIA BRASIL": "Via Brasil", "VIA CAMPO": "Via Campo", "VIA COSTEIRA": "Via Costeira", "VIA CRISTAIS": "Via Cristais", "VIA SUL": "Via Sul",
 "WAY 153": "Way 153", "WAY 262": "Way 262", "WAY 364": "Way 364"}
# (concessionária, ano do PNV/SNV, BR, UF, km inicial, km final)
TRECHOS = [
 ("AUTOPISTA FLUMINENSE", 2019, 101, "RJ", 0.0, 322.1),
 ("AUTOPISTA LITORAL SUL", 2009, 101, "SC", 0.0, 244.68), ("AUTOPISTA LITORAL SUL", 2009, 116, "PR", 71.1, 115.2), ("AUTOPISTA LITORAL SUL", 2009, 376, "PR", 614.4, 682.123),
 ("AUTOPISTA PLANALTO SUL", 2017, 116, "PR", 115.0, 211.8), ("AUTOPISTA PLANALTO SUL", 2017, 116, "SC", 0.0, 310.24),
 ("AUTOPISTA REGIS BITTENCOURT", 2017, 116, "SP", 268.9, 569.1), ("AUTOPISTA REGIS BITTENCOURT", 2017, 116, "PR", 0.0, 71.1),
 ("CONCEBRA", 2017, 153, "GO", 490.0, 703.9), ("CONCEBRA", 2017, 60, "GO", 0.0, 139.0), ("CONCEBRA", 2017, 60, "DF", 0.0, 31.9),
 ("CONCER", 2016, 40, "MG", 773.5, 828.7), ("CONCER", 2016, 40, "RJ", 0.0, 125.2),
 ("ECOSUL", 1996, 116, "RS", 400.5, 661.0), ("ECOSUL", 1996, 392, "RS", 0.0, 68.4), ("ECOSUL", 1996, 392, "RS", 71.3, 199.7),
 ("ECOVIAS CAPIXABA", 2020, 101, "BA", 939.2, 956.73), ("ECOVIAS CAPIXABA", 2020, 101, "ES", 0.0, 247.799), ("ECOVIAS CAPIXABA", 2020, 101, "ES", 278.301, 374.4), ("ECOVIAS CAPIXABA", 2020, 101, "ES", 379.3, 461.09),
 ("ECOVIAS DAS GERAIS", 2021, 116, "MG", 0.0, 408.499), ("ECOVIAS DAS GERAIS", 2021, 251, "MG", 193.7, 520.1),
 ("ECOVIAS DO ARAGUAIA", 2021, 153, "TO", 622.7, 801.87), ("ECOVIAS DO ARAGUAIA", 2021, 153, "GO", 0.0, 442.9), ("ECOVIAS DO ARAGUAIA", 2021, 414, "GO", 300.0, 442.92), ("ECOVIAS DO ARAGUAIA", 2021, 80, "GO", 94.3, 181.05),
 ("ECOVIAS DO CERRADO", 2020, 364, "GO", 0.0, 192.2), ("ECOVIAS DO CERRADO", 2020, 365, "MG", 626.0, 870.11),
 ("ECOVIAS MINAS GOIÁS", 2017, 50, "MG", 0.0, 65.7), ("ECOVIAS MINAS GOIÁS", 2017, 50, "MG", 77.0, 207.3), ("ECOVIAS MINAS GOIÁS", 2017, 50, "GO", 95.0, 314.2),
 ("ECOVIAS PONTE", 2017, 101, "RJ", 322.067, 333.623),
 ("ECOVIAS RIO MINAS", 2021, 116, "MG", 408.5, 587.574), ("ECOVIAS RIO MINAS", 2021, 116, "MG", 588.7, 818.1), ("ECOVIAS RIO MINAS", 2021, 116, "RJ", 2.1, 148.65), ("ECOVIAS RIO MINAS", 2021, 116, "RJ", 168.72, 214.8),
 ("ECOVIAS RIO MINAS", 2021, 465, "RJ", 0.0, 23.2), ("ECOVIAS RIO MINAS", 2021, 493, "RJ", 0.0, 25.4), ("ECOVIAS RIO MINAS", 2021, 493, "RJ", 48.1, 122.7),
 ("ELOVIAS", 2020, 40, "MG", 776.1, 831.4), ("ELOVIAS", 2020, 40, "RJ", 0.0, 125.2), ("ELOVIAS", 2020, 495, "RJ", 34.4, 34.5),
 ("EPR IGUAÇU", 2019, 163, "PR", 123.7, 197.424), ("EPR IGUAÇU", 2019, 277, "PR", 303.801, 732.224), ("EPR IGUAÇU", 2019, 469, "PR", 1.8, 2.487),
 ("EPR PARANÁ", 2025, 272, "PR", 524.7, 570.0), ("EPR PARANÁ", 2025, 369, "PR", 88.2, 182.7), ("EPR PARANÁ", 2025, 376, "PR", 31.5, 202.3),
 ("EPR VIA MINEIRA", 2012, 40, "MG", 543.5, 776.1),
 ("LITORAL PIONEIRO", 2019, 153, "PR", 0.0, 51.806), ("LITORAL PIONEIRO", 2019, 277, "PR", 0.0, 83.844), ("LITORAL PIONEIRO", 2019, 369, "PR", 1.0, 51.744), ("LITORAL PIONEIRO", 2019, 369, "PR", 60.9, 88.409),
 ("MOTIVA MINAS SP", 2007, 381, "MG", 477.2, 949.9), ("MOTIVA MINAS SP", 2007, 381, "SP", 0.0, 90.4),
 ("MOTIVA PARANÁ", 2023, 369, "PR", 182.7, 200.8), ("MOTIVA PARANÁ", 2023, 373, "PR", 171.9, 183.4), ("MOTIVA PARANÁ", 2023, 376, "PR", 8.6, 10.0), ("MOTIVA PARANÁ", 2023, 376, "PR", 202.3, 470.7), ("MOTIVA PARANÁ", 2023, 376, "PR", 482.2, 549.3),
 ("NOVA 364", 2021, 364, "RO", 27.6, 337.3), ("NOVA 364", 2021, 364, "RO", 350.2, 713.6),
 ("NOVA 381", 2022, 381, "MG", 146.9, 450.4),
 ("NOVA ROTA DO OESTE", 2016, 163, "MT", 0.0, 119.9), ("NOVA ROTA DO OESTE", 2016, 163, "MT", 507.1, 855.0), ("NOVA ROTA DO OESTE", 2016, 364, "MT", 201.0, 402.4), ("NOVA ROTA DO OESTE", 2016, 364, "MT", 434.6, 588.2), ("NOVA ROTA DO OESTE", 2016, 70, "MT", 495.9, 524.0),
 ("PANTANAL", 2014, 163, "MS", 0.0, 845.9),
 ("RIOSP", 2000, 101, "RJ", 380.8, 598.6), ("RIOSP", 2000, 101, "SP", 0.0, 52.59), ("RIOSP", 2000, 116, "RJ", 169.0, 339.482), ("RIOSP", 2000, 116, "SP", 0.0, 231.947),
 ("RODOVIA DO AÇO", 2016, 393, "RJ", 101.9, 286.4),
 ("ROTA VERDE GOIÁS", 2025, 452, "GO", 0.0, 196.6), ("ROTA VERDE GOIÁS", 2025, 60, "GO", 164.0, 393.6),
 ("TRANSBRASILIANA", 2015, 153, "SP", 0.0, 230.2), ("TRANSBRASILIANA", 2015, 153, "SP", 255.0, 347.7),
 ("VIA ARAUCÁRIA", 2019, 277, "PR", 107.3, 303.8), ("VIA ARAUCÁRIA", 2019, 373, "PR", 183.4, 282.7), ("VIA ARAUCÁRIA", 2019, 376, "PR", 591.6, 606.2), ("VIA ARAUCÁRIA", 2019, 476, "PR", 143.7, 197.7),
 ("VIA BRASIL", 2021, 163, "PA", 0.0, 674.4), ("VIA BRASIL", 2021, 163, "MT", 854.2, 1115.35), ("VIA BRASIL", 2021, 230, "PA", 1096.0, 1129.0),
 ("VIA CAMPO", 2025, 163, "PR", 197.6, 343.9), ("VIA CAMPO", 2025, 163, "PR", 349.5, 354.2), ("VIA CAMPO", 2025, 369, "PR", 334.8, 509.9), ("VIA CAMPO", 2025, 467, "PR", 102.0, 118.0),
 ("VIA COSTEIRA", 2020, 101, "SC", 245.0, 464.285),
 ("VIA CRISTAIS", 2010, 40, "MG", 0.0, 533.2), ("VIA CRISTAIS", 2010, 40, "GO", 95.7, 157.3),
 ("VIA SUL", 2019, 101, "RS", 0.0, 88.5), ("VIA SUL", 2019, 290, "RS", 0.0, 98.1), ("VIA SUL", 2019, 386, "RS", 179.96, 446.0), ("VIA SUL", 2019, 448, "RS", 0.5, 22.1),
 ("WAY 153", 2025, 153, "MG", 0.0, 247.0), ("WAY 153", 2025, 153, "GO", 529.87, 702.73), ("WAY 153", 2025, 262, "MG", 796.31, 902.7),
 ("WAY 262", 2023, 262, "MG", 347.9, 787.9),
 ("WAY 364", 2022, 364, "MT", 0.0, 201.0), ("WAY 364", 2022, 364, "GO", 192.7, 387.5), ("WAY 364", 2022, 60, "GO", 393.6, 470.0)]

UFCOD = {"55": "RO", "59": "PA", "61": "TO", "70": "BA", "71": "MG", "72": "ES", "73": "RJ", "74": "SP", "75": "PR", "76": "SC", "77": "RS", "78": "MS", "79": "MT", "80": "GO", "81": "DF"}
def atualizar_da_antt(url=URL, timeout=60):
    """Na rotina automática (8h, 14h, 18h): baixa o CSV vigente da ANTT e substitui a tabela embutida.
    Sem acesso à internet, mantém a tabela acima (arquivo 8/2026)."""
    global TRECHOS
    import csv, io, os, urllib.request
    try:
        raw = urllib.request.urlopen(os.environ.get("ANTT_TRECHOS_URL", url), timeout=timeout).read().decode("utf-8-sig", "replace")
        novos = {}
        for r in csv.DictReader(io.StringIO(raw), delimiter=";"):
            if (r.get("tipo_de_rodovia") or "").strip().lower() != "federal": continue
            uf = UFCOD.get((r.get("uf") or "").strip(), (r.get("uf") or "").strip().upper())
            br = int("".join(ch for ch in r["rodovia"] if ch.isdigit()))
            a, z = sorted((float(r["km_m_inicial"].replace(",", ".")), float(r["km_m_final"].replace(",", "."))))
            c = r["concessionaria"].strip().upper(); NOMES.setdefault(c, c.title())
            novos[(c, br, uf, a, z)] = (c, int(r.get("ano_do_pnv_snv") or 0), br, uf, a, z)
        if len(novos) > 50: TRECHOS = list(novos.values()); return True
    except Exception as e:
        print("ANTT indisponível, usando tabela embutida (8/2026):", e)
    return False

def responsavel(br, uf, km_ini, km_fim):
    """Concessionária com maior sobreposição (≥ metade do trecho); empate ou sobreposição de contratos: o de PNV mais recente."""
    melhor, sob = None, 0
    for c, ano, b, u, a, z in TRECHOS:
        if b != br or u != uf: continue
        o = min(km_fim, z) - max(km_ini, a)
        if o <= 0: continue
        if o > sob + 1e-6 or (abs(o - sob) < 1e-6 and melhor and ano > melhor[1]): melhor, sob = (c, ano), o
    return NOMES[melhor[0]] if melhor and sob >= (km_fim - km_ini) / 2 else None
