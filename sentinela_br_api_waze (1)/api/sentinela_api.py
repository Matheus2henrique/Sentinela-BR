"""Sentinela BR - API de riscos nas rodovias federais.

Serve os trechos criticos (PRF 2021-2026), o calculo de riscos de uma viagem,
as demandas por orgao e um feed no formato Waze CIFS (Closure and Incident Feed
Specification) para plugar os pontos de atencao no Waze.

Rodar:  uvicorn sentinela_api:app --host 0.0.0.0 --port 8000
Docs:   http://localhost:8000/docs
"""
from __future__ import annotations

import heapq
import json
import os
import time
import unicodedata
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

DADOS = Path(os.environ.get("SENTINELA_DADOS", Path(__file__).parent / "dados" / "sentinela_dados.json"))
D = json.loads(DADOS.read_text(encoding="utf-8"))
T = D["trechos"]
N = len(T["br"])
CATS = D["meta"]["categorias"]
UFS = D["meta"]["ufs"]
MUN = D["meta"]["municipios"]
BRT = timezone(timedelta(hours=-3))
NIVEL = ["baixo", "atenção", "alto", "muito alto"]
PER = ["madrugada (0h-6h)", "manhã (6h-12h)", "tarde (12h-18h)", "noite (18h-24h)"]
DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
PISTA = ["simples", "dupla", "múltipla"]

# Subtipos HAZARD do CIFS para cada fator de risco
WAZE_SUBTIPO = {
    "alagamento": "HAZARD_WEATHER_FLOOD",
    "chuva": "HAZARD_WEATHER_HEAVY_RAIN",
    "neblina": "HAZARD_WEATHER_FOG",
    "encosta": "HAZARD_ON_ROAD_OBJECT",
    "via": "HAZARD_ON_ROAD_POT_HOLE",
    "animais": "HAZARD_ON_SHOULDER_ANIMALS",
}
WAZE_PRIORIDADE = ["alagamento", "encosta", "neblina", "animais", "via", "chuva"]
CURTO = {  # nomes curtos para a descricao (< 40 caracteres)
    "chuva": "chuva", "alagamento": "alagamento", "encosta": "queda de barreira", "via": "pista ruim",
    "curva": "curvas", "neblina": "neblina", "animais": "animais", "pedestres": "pedestres",
    "frontal": "colisão frontal", "sono": "sono", "motos": "motos", "alcool": "álcool",
    "velocidade": "velocidade", "traseira": "engavetamento",
}
MEDIDAS = {
    "frontal": [("Separação física central ou faixa adicional de ultrapassagem", "gestor"), ("Fiscalização de ultrapassagem proibida", "prf")],
    "pedestres": [("Passarela ou travessia segura", "gestor"), ("Iluminação e calçadas no trecho urbano", "prefeitura")],
    "chuva": [("Restauração da aderência do pavimento", "gestor"), ("Operação de chuva com redução de velocidade", "prf"), ("Alerta de chuva aos motoristas", "defesa_civil")],
    "alagamento": [("Melhoria da drenagem superficial", "gestor"), ("Monitoramento e alerta de alagamento", "defesa_civil")],
    "encosta": [("Contenção de encostas e limpeza da pista", "gestor"), ("Protocolo de interdição preventiva por chuva", "defesa_civil")],
    "via": [("Restauração do pavimento e do acostamento", "gestor"), ("Revisão da sinalização e iluminação", "gestor")],
    "curva": [("Sinalização de curva e defensas", "gestor"), ("Fiscalização de velocidade", "prf")],
    "neblina": [("Sinalização e painéis de alerta de neblina", "gestor")],
    "animais": [("Cercamento com passagem de fauna", "gestor")],
    "sono": [("Sonorizadores de bordo e ponto de parada e descanso", "gestor"), ("Fiscalização do tempo de direção", "prf")],
    "motos": [("Fiscalização dirigida a motociclistas", "prf"), ("Campanha para motociclistas", "detran")],
    "alcool": [("Operações de alcoolemia", "prf"), ("Campanha sobre álcool e direção", "detran")],
    "velocidade": [("Fiscalização eletrônica de velocidade", "gestor"), ("Fiscalização de velocidade", "prf")],
    "traseira": [("Gestão de velocidade e aviso de fila", "gestor")],
}
ORGAOS = {"gestor": "Gestor da via (DNIT ou concessionária)", "prf": "Polícia Rodoviária Federal",
          "defesa_civil": "Defesa Civil", "prefeitura": "Prefeitura", "detran": "DETRAN"}


def sem_acento(s: str) -> str:
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower().strip()


def alertas(i: int) -> list[str]:
    a = [c["id"] for k, c in enumerate(CATS) if T["alertas"][i] >> k & 1]
    ordem = {c["id"]: T["catM"][i][k] for k, c in enumerate(CATS)}
    return sorted(a, key=lambda x: -ordem[x])


def nome(i: int) -> str:
    return f"BR-{T['br'][i]:03d}/{UFS[T['uf'][i]]} km {T['km'][i]}-{T['km'][i] + 5}"


def trecho_id(i: int) -> str:
    return f"BR{T['br'][i]:03d}-{UFS[T['uf'][i]]}-{T['km'][i]:04d}"


IDX = {trecho_id(i): i for i in range(N)}
VIZ = {(T["br"][i], T["uf"][i], T["km"][i]): i for i in range(N)}


def orgaos(i: int) -> dict:
    r: dict[str, list[str]] = {}
    for a in alertas(i)[:3]:
        for medida, org in MEDIDAS.get(a, []):
            r.setdefault(ORGAOS[org], [])
            if medida not in r[ORGAOS[org]]:
                r[ORGAOS[org]].append(medida)
    return r or {ORGAOS["gestor"]: ["Inspeção de segurança viária do trecho"],
                 ORGAOS["prf"]: ["Fiscalização nos dias e horários de maior risco"]}


def info(i: int, completo: bool = True) -> dict:
    d = {
        "id": trecho_id(i), "trecho": nome(i), "br": T["br"][i], "uf": UFS[T["uf"][i]],
        "km_inicial": T["km"][i], "km_final": T["km"][i] + 5, "municipio": MUN[T["mun"][i]],
        "lat": T["lat"][i], "lon": T["lon"][i], "nivel_risco": NIVEL[T["nivel"][i]],
        "nivel": T["nivel"][i], "cronico": bool(T["cronico"][i]),
        "mortes_desde_2021": T["mortos"][i], "acidentes": T["n"][i], "acidentes_fatais": T["fatais"][i],
        "fatores": [next(c["nome"] for c in CATS if c["id"] == a) for a in alertas(i)],
        "fatores_ids": alertas(i),
    }
    if completo:
        d.update({
            "mortes_por_ano": dict(zip(["2021", "2022", "2023", "2024", "2025", "2026"], T["mAno"][i])),
            "anos_com_acidente_fatal": T["anosFatal"][i],
            "fatais_por_ano_ajustado": T["eb"][i] / 100,
            "periodo_mais_perigoso": PER[T["per"][i]] if T["per"][i] >= 0 else None,
            "dia_mais_perigoso": DIAS[T["dia"][i]] if T["dia"][i] >= 0 else None,
            "meses_com_mais_acidentes_de_chuva": T["mesesChuva"][i],
            "tipo_pista": PISTA[T["pista"][i]], "urbano_pct": T["urb"][i],
            "mortes_por_fator": {c["id"]: T["catM"][i][k] for k, c in enumerate(CATS) if T["catM"][i][k]},
            "orgaos_e_medidas": orgaos(i),
        })
    return d


# ---------------- rota ----------------
ADJ: list[list[tuple[int, float]]] = [[] for _ in range(N)]
for a, b, w in zip(D["grafo"]["a"], D["grafo"]["b"], D["grafo"]["w"]):
    ADJ[a].append((b, w))
    ADJ[b].append((a, w))
CIDADES = {sem_acento(f"{c[0]} - {c[1]}"): c for c in D["cidades"]}


def achar_cidade(txt: str):
    k = sem_acento(txt).replace(",", " - ").replace("/", " - ")
    k = " - ".join(p.strip() for p in k.split("-") if p.strip())
    if k in CIDADES:
        return CIDADES[k]
    so = [c for c in D["cidades"] if sem_acento(c[0]) == k.split(" - ")[0]]
    return max(so, key=lambda c: c[3]) if so else None


def dijkstra(s: int, t: int):
    dist = {s: 0.0}
    prev = {}
    h = [(0.0, s)]
    while h:
        d, u = heapq.heappop(h)
        if u == t:
            break
        if d > dist.get(u, 1e18):
            continue
        for v, w in ADJ[u]:
            nd = d + w
            if nd < dist.get(v, 1e18):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(h, (nd, v))
    if t not in dist:
        return None
    path = [t]
    while path[-1] != s:
        path.append(prev[path[-1]])
    path.reverse()
    return path, [dist[p] for p in path], dist[t]


app = FastAPI(title="Sentinela BR API", version="1.0",
              description="Riscos nas rodovias federais com dados abertos da PRF (2021-2026) e feed Waze CIFS.")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])


@app.get("/")
def raiz():
    return {"servico": "Sentinela BR", "fonte": D["meta"]["fonte"], "gerado": D["meta"]["gerado"], "trechos": N,
            "rotas": ["/v1/trechos", "/v1/trechos/{id}", "/v1/ranking", "/v1/rota", "/v1/encaminhamentos",
                      "/v1/waze/cifs.json", "/v1/waze/cifs.xml", "/v1/clima", "/v1/estatisticas", "/docs"]}


@app.get("/v1/estatisticas")
def estatisticas():
    return D["nacional"]


@app.get("/v1/trechos")
def trechos(uf: str | None = None, br: int | None = None, nivel_min: int = Query(1, ge=0, le=3),
            fator: str | None = Query(None, description="id do fator, ex.: chuva, alagamento, encosta, pedestres"),
            formato: str = Query("geojson", pattern="^(geojson|json)$")):
    ufi = UFS.index(uf.upper()) if uf else None
    feats = []
    for i in range(N):
        if T["nivel"][i] < nivel_min and not (nivel_min <= 1 and T["cronico"][i]):
            continue
        if ufi is not None and T["uf"][i] != ufi:
            continue
        if br is not None and T["br"][i] != br:
            continue
        if fator and fator not in alertas(i):
            continue
        feats.append(i)
    if formato == "json":
        return [info(i, False) for i in feats]
    return {"type": "FeatureCollection", "features": [
        {"type": "Feature", "id": trecho_id(i), "geometry": {"type": "Point", "coordinates": [T["lon"][i], T["lat"][i]]},
         "properties": info(i, False)} for i in feats]}


@app.get("/v1/trechos/{tid}")
def trecho(tid: str):
    if tid not in IDX:
        raise HTTPException(404, "Trecho não encontrado. Formato do id: BR116-SP-0225")
    return info(IDX[tid])


@app.get("/v1/ranking")
def ranking(uf: str | None = None, br: int | None = None, limite: int = Query(20, ge=1, le=200)):
    ufi = UFS.index(uf.upper()) if uf else None
    ids = [i for i in range(N) if (ufi is None or T["uf"][i] == ufi) and (br is None or T["br"][i] == br)]
    ids.sort(key=lambda i: -T["eb"][i])
    return [info(i) for i in ids[:limite]]


@app.get("/v1/rota")
def rota(origem: str = Query(..., examples=["Brasilia - DF"]), destino: str = Query(..., examples=["Rio de Janeiro - RJ"]),
         saida: str = Query("07:00", pattern=r"^\d{2}:\d{2}$"), data: str | None = Query(None, examples=["2026-12-20"]),
         veiculo: str = Query("carro", pattern="^(carro|moto|caminhao|onibus)$")):
    o, d = achar_cidade(origem), achar_cidade(destino)
    if not o or not d:
        raise HTTPException(404, "Cidade não encontrada. Use 'Cidade - UF'.")
    r = dijkstra(o[2], d[2])
    if not r:
        raise HTTPException(404, "Sem ligação por rodovias federais entre as cidades.")
    path, acum, km = r
    vel = {"carro": 72, "moto": 68, "caminhao": 60, "onibus": 65}[veiculo]
    hh, mm = map(int, saida.split(":"))
    mes = int(data[5:7]) if data else None
    per = lambda h: 0 if h < 6 else 1 if h < 12 else 2 if h < 18 else 3
    pontos = []
    for i, dist in zip(path, acum):
        if not (T["nivel"][i] >= 1 or T["cronico"][i] or T["alertas"][i] & 6):
            continue
        hora = (hh + mm / 60 + dist / vel) % 24
        p = info(i)
        p.update({"km_da_viagem": round(dist), "passagem_prevista": f"{int(hora):02d}:{int(hora % 1 * 60):02d}",
                  "passa_no_horario_mais_perigoso": T["per"][i] >= 0 and T["per"][i] == per(hora),
                  "mes_com_mais_acidentes_de_chuva": bool(mes and mes in T["mesesChuva"][i] and T["alertas"][i] & 7),
                  "_score": T["eb"][i] + (40 if T["cronico"][i] else 0)})
        pontos.append(p)
    top = sorted(pontos, key=lambda p: -p["_score"])[:15]
    top.sort(key=lambda p: p["km_da_viagem"])
    for p in top:
        p.pop("_score")
    return {"origem": f"{o[0]} - {o[1]}", "destino": f"{d[0]} - {d[1]}", "distancia_km": round(km),
            "horas_dirigindo": round(km / vel, 1), "mortes_no_caminho_desde_2021": sum(T["mortos"][i] for i in path),
            "trechos_risco_alto": sum(1 for i in path if T["nivel"][i] >= 2 or T["cronico"][i]),
            "mortes_por_fator": {c["id"]: sum(T["catM"][i][k] for i in path) for k, c in enumerate(CATS)},
            "pontos_de_atencao": top,
            "geometria": {"type": "LineString", "coordinates": [[T["lon"][i], T["lat"][i]] for i in path]},
            "aviso": "Rota aproximada, só por rodovias federais. Confira a previsão do tempo (INMET) e os alertas da Defesa Civil antes de sair."}


@app.get("/v1/encaminhamentos")
def encaminhamentos(uf: str = Query(..., examples=["MG"]), limite: int = Query(15, ge=1, le=100)):
    ufi = UFS.index(uf.upper())
    ids = sorted((i for i in range(N) if T["uf"][i] == ufi and (T["nivel"][i] >= 2 or T["cronico"][i])), key=lambda i: -T["eb"][i])[:limite]
    por: dict[str, list] = {}
    for i in ids:
        for org, medidas in orgaos(i).items():
            por.setdefault(org, []).append({"trecho": nome(i), "id": trecho_id(i), "municipio": MUN[T["mun"][i]],
                                            "mortes_desde_2021": T["mortos"][i], "medidas": medidas})
    return {"uf": uf.upper(), "gerado": datetime.now(BRT).isoformat(timespec="seconds"), "orgaos": por,
            "observacao": "O gestor de cada trecho (DNIT ou concessionária) deve ser confirmado na malha oficial do DNIT (SNV)."}


# ---------------- Waze CIFS ----------------
def incidentes_waze(uf: str | None, nivel_min: int, dias: int) -> list[dict]:
    agora = datetime.now(BRT).replace(microsecond=0)
    fim = agora + timedelta(days=dias)
    ufi = UFS.index(uf.upper()) if uf else None
    out = []
    for i in range(N):
        if T["br"][i] == 0 or (ufi is not None and T["uf"][i] != ufi):
            continue
        if not (T["nivel"][i] >= nivel_min or (nivel_min >= 2 and T["cronico"][i] and T["nivel"][i] >= 1)):
            continue
        al = alertas(i)
        fat = next((a for a in WAZE_PRIORIDADE if a in al), al[0] if al else None)
        sub = WAZE_SUBTIPO.get(fat, "HAZARD_ON_ROAD")
        j = VIZ.get((T["br"][i], T["uf"][i], T["km"][i] + 5)) or VIZ.get((T["br"][i], T["uf"][i], T["km"][i] - 5))
        p1 = (T["lat"][i], T["lon"][i])
        p2 = (T["lat"][j], T["lon"][j]) if j is not None else (p1[0] + 0.002, p1[1] + 0.002)
        principal = CURTO[fat] if fat else "trecho crítico"
        desc = f"Atenção: {principal}, {T['mortos'][i]} mortes"
        if len(desc) >= 40:
            desc = f"Trecho crítico: {T['mortos'][i]} mortes"
        out.append({
            "id": f"sentinela-{trecho_id(i)}", "type": "HAZARD", "subtype": sub,
            "polyline": f"{p1[0]:.5f} {p1[1]:.5f} {p2[0]:.5f} {p2[1]:.5f}",
            "direction": "BOTH_DIRECTIONS", "street": f"BR-{T['br'][i]:03d}",
            "starttime": agora.isoformat(), "endtime": fim.isoformat(),
            "description": desc, "reference": nome(i),
        })
    return out


@app.get("/v1/waze/cifs.json")
def waze_json(uf: str | None = None, nivel_min: int = Query(2, ge=1, le=3), dias: int = Query(7, ge=1, le=14)):
    return {"incidents": incidentes_waze(uf, nivel_min, dias)}


@app.get("/v1/waze/cifs.xml")
def waze_xml(uf: str | None = None, nivel_min: int = Query(2, ge=1, le=3), dias: int = Query(7, ge=1, le=14)):
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>', "<incidents>"]
    for x in incidentes_waze(uf, nivel_min, dias):
        linhas.append(f'  <incident id="{escape(x["id"])}">')
        for k in ["type", "subtype", "polyline", "direction", "street", "starttime", "endtime", "description"]:
            linhas.append(f"    <{k}>{escape(str(x[k]))}</{k}>")
        linhas.append("  </incident>")
    linhas.append("</incidents>")
    return Response("\n".join(linhas), media_type="application/xml")


# ---------------- clima ao vivo (opcional) ----------------
_cache: dict = {}


@app.get("/v1/clima")
def clima(lat: float, lon: float):
    """Previsão de chuva das próximas 24 h (Open-Meteo), para cruzar com os trechos de risco."""
    k = (round(lat, 2), round(lon, 2))
    if k in _cache and time.time() - _cache[k][0] < 1800:
        return _cache[k][1]
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={k[0]}&longitude={k[1]}"
           "&hourly=precipitation,precipitation_probability&forecast_hours=24&timezone=America%2FSao_Paulo")
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            j = json.load(r)
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"erro": "Previsão indisponível no momento", "detalhe": str(e)[:120]}, status_code=503)
    h = j.get("hourly", {})
    chuva = h.get("precipitation", []) or [0]
    resp = {"lat": k[0], "lon": k[1], "chuva_24h_mm": round(sum(chuva), 1), "chuva_max_hora_mm": max(chuva),
            "prob_max_pct": max(h.get("precipitation_probability", []) or [0]),
            "alerta": "chuva forte" if max(chuva) >= 10 else "chuva" if sum(chuva) >= 5 else "sem chuva relevante",
            "fonte": "Open-Meteo"}
    _cache[k] = (time.time(), resp)
    return resp
