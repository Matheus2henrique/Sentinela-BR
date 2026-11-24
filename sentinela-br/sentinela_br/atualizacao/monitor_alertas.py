"""Monitor de risco climático do pAInel Sentinela BR.

Consulta os avisos meteorológicos ativos do INMET, cruza os municípios de cada aviso com os trechos
de risco do painel e grava p6/alertas_inmet.json. O painel abre um pop-up com esses alertas, com o órgão líder
e os órgãos que agem juntos em cada tipo de evento. Roda junto com a atualização (8h, 14h, 18h) e,
de hora em hora, sozinho (ver crontab.txt e o workflow).

Opcional: defina ALERTA_WEBHOOK (Teams, Slack ou e-mail via serviço) para avisar as equipes.
"""
import csv, io, json, os, pathlib, subprocess, sys, unicodedata, urllib.request

BASE = pathlib.Path(os.environ.get("SENTINELA_BASE", "/home/claude"))
P6 = BASE / "sentinela_br" / "p6"
# Endpoint usado pelo portal alertas2.inmet.gov.br (confirmar com o INMET na formalização da parceria)
INMET = os.environ.get("INMET_AVISOS_URL", "https://apiprevmet3.inmet.gov.br/avisos/ativos")
MUNICIPIOS = "https://raw.githubusercontent.com/kelvins/municipios-brasileiros/main/csv/municipios.csv"
UFCOD = {11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO", 21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL", 28: "SE", 29: "BA",
         31: "MG", 32: "ES", 33: "RJ", 35: "SP", 41: "PR", 42: "SC", 43: "RS", 50: "MS", 51: "MT", 52: "GO", 53: "DF"}
# quem age em cada tipo de evento: líder e órgãos que atuam juntos
DONOS = [(("desliz", "movimento de massa", "chuvas intensas", "acumulado de chuva", "tempestade"), "Defesa Civil", ["PRF", "Gestor da via (DNIT ou concessionária)", "Cemaden e Serviço Geológico do Brasil"]),
         (("vendaval", "ventos costeiros", "granizo"), "Defesa Civil", ["PRF", "Gestor da via (DNIT ou concessionária)"]),
         (("nevoeiro", "neblina"), "PRF", ["Gestor da via (DNIT ou concessionária)"]),
         (("baixa umidade", "incêndio", "queimada", "fumaça"), "Corpo de Bombeiros e Ibama/Prevfogo", ["PRF", "Gestor da via (DNIT ou concessionária)", "Defesa Civil"]),
         (("",), "Defesa Civil", ["PRF", "Gestor da via (DNIT ou concessionária)"])]
sem_acento = lambda s: unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower().strip()

def obter(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "SentinelaBR/1.0"}), timeout=60).read()

def main():
    D = json.load(open(P6 / "dados.json")); T = D["tr"]
    mun_ibge = {}
    for r in csv.DictReader(io.StringIO(obter(MUNICIPIOS).decode("utf-8"))):
        mun_ibge[r["codigo_ibge"]] = (sem_acento(r["nome"]), UFCOD.get(int(r["codigo_uf"]), ""))
    idx = {}
    for i in range(len(T["br"])):
        if T["esp"][i] >= 0.4 or T["cj"][i] >= 0: idx.setdefault((sem_acento(T["mun"][i]), T["uf"][i]), []).append(i)
    avisos = json.loads(obter(INMET))
    lista = avisos if isinstance(avisos, list) else sum((v for v in avisos.values() if isinstance(v, list)), [])
    saida = []
    for a in lista:
        evento = a.get("descricao") or a.get("evento") or "Aviso meteorológico"
        sev = a.get("severidade") or a.get("nivel") or ""
        geos = [g.strip() for g in str(a.get("geocodes") or a.get("municipios") or "").split(",") if g.strip()]
        trechos = sorted({i for g in geos for i in idx.get(mun_ibge.get(g, ("", "")), [])}, key=lambda i: -T["esp"][i])
        if not trechos: continue
        ev = sem_acento(evento)
        lider, com = next((l, c) for chaves, l, c in DONOS if any(k in ev for k in chaves))
        nomes = "; ".join(f"BR-{T['br'][i]:03d}/{T['uf'][i]} km {T['km'][i]} ({T['mun'][i]})" for i in trechos[:6])
        saida.append({"titulo": f"{evento} {('· ' + sev) if sev else ''} · {len(trechos)} trechos de risco",
                      "texto": f"Líder: {lider}. Agem juntos: {', '.join(com)}. Vigência: {a.get('inicio', '')} a {a.get('fim', '')}. Trechos: {nomes}.",
                      "lider": lider, "orgaos": com, "trechos": trechos[:50]})
    (P6 / "alertas_inmet.json").write_text(json.dumps(saida, ensure_ascii=False))
    print(f"{len(saida)} alertas do INMET tocam trechos de risco")
    hook = os.environ.get("ALERTA_WEBHOOK")
    if hook and saida:
        corpo = json.dumps({"text": "pAInel Sentinela BR · alertas climáticos\n" + "\n".join(f"- {s['titulo']}: {s['texto']}" for s in saida[:10])}).encode()
        urllib.request.urlopen(urllib.request.Request(hook, data=corpo, headers={"Content-Type": "application/json"}), timeout=30)
    if "--sem-montar" not in sys.argv:
        subprocess.run([sys.executable, "montar.py"], cwd=P6, check=False)

if __name__ == "__main__":
    try: main()
    except Exception as e:  # sem acesso ao INMET: o painel mantém o alerta sazonal pelo histórico da PRF
        print("monitor: INMET indisponível nesta execução:", e.__class__.__name__); (P6 / "alertas_inmet.json").write_text("[]")
