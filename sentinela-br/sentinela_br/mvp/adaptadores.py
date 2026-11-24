"""Adaptadores: leem cada base no layout em que ela é publicada e devolvem um formato
canônico. É a ÚNICA camada que precisa mudar quando um órgão alterar o layout.

Cada leitor:
  1. encontra os arquivos pelo padrão de nome (aceita os reais e os _SINTETICO);
  2. tenta as codificações usuais (latin-1 / utf-8) e o separador ';';
  3. valida as colunas obrigatórias e registra divergências em `RELATORIO`.
"""
import glob
import io
import os
import re

import numpy as np
import pandas as pd

RELATORIO = []  # mensagens de validação de esquema


def _log(fonte, msg):
    RELATORIO.append(f"[{fonte}] {msg}")


def _ler_csv(caminho, **kw):
    for enc in ("utf-8-sig", "latin-1"):
        try:
            return pd.read_csv(caminho, sep=";", encoding=enc, low_memory=False, **kw)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"não foi possível ler {caminho}")


def _num(s):
    """Converte '123,4' / '1.234,5' / '123.4' / -9999 em float."""
    if s.dtype.kind in "if":
        return s.astype(float)
    t = s.astype(str).str.strip()
    virg = t.str.contains(",", regex=False)
    t = t.where(~virg, t.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    return pd.to_numeric(t, errors="coerce")


def _validar(df, obrigatorias, fonte, arquivo):
    faltam = [c for c in obrigatorias if c not in df.columns]
    if faltam:
        _log(fonte, f"{os.path.basename(arquivo)}: colunas ausentes {faltam}")
    else:
        _log(fonte, f"{os.path.basename(arquivo)}: OK ({len(df)} linhas)")
    return not faltam


# ----------------------------------------------------------------------------- PRF
PRF_OBRIG = ["id", "data_inversa", "horario", "uf", "br", "km", "municipio", "causa_acidente", "tipo_acidente",
             "classificacao_acidente", "fase_dia", "condicao_metereologica", "tipo_pista", "tracado_via",
             "uso_solo", "mortos", "feridos_graves", "feridos_leves", "veiculos", "latitude", "longitude"]


def ler_prf(pasta):
    arqs = sorted(glob.glob(os.path.join(pasta, "prf", "datatran*.csv")))
    if not arqs:
        raise FileNotFoundError("nenhum arquivo datatran*.csv em prf/")
    partes = []
    for a in arqs:
        df = _ler_csv(a, dtype=str)
        df.columns = [c.strip().lower() for c in df.columns]
        if _validar(df, PRF_OBRIG, "PRF", a):
            partes.append(df)
    df = pd.concat(partes, ignore_index=True)
    # datas: anos antigos vêm como dd/mm/aaaa
    df["data"] = pd.to_datetime(df.data_inversa, format="%Y-%m-%d", errors="coerce")
    alt = pd.to_datetime(df.data_inversa, format="%d/%m/%Y", errors="coerce")
    df["data"] = df.data.fillna(alt)
    df["hora"] = pd.to_numeric(df.horario.str[:2], errors="coerce")
    df["br"] = pd.to_numeric(df.br, errors="coerce")
    for c in ["km", "latitude", "longitude"]:
        df[c] = _num(df[c])
    for c in ["mortos", "feridos_graves", "feridos_leves", "veiculos", "pessoas"]:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    for c in ["causa_acidente", "tipo_acidente", "classificacao_acidente", "fase_dia",
              "condicao_metereologica", "tipo_pista", "tracado_via", "uso_solo", "uf", "municipio"]:
        df[c] = df[c].astype(str).str.strip()
    # traçado pode vir com múltiplos valores separados por ';' em anos recentes: fica o primeiro
    df["tracado_via"] = df.tracado_via.str.split(";").str[0]
    n0 = len(df)
    df = df.dropna(subset=["data", "br", "km"]).drop_duplicates("id")
    if len(df) < n0:
        _log("PRF", f"{n0 - len(df)} registros descartados (sem data/br/km ou id duplicado)")
    df["fatal"] = df.classificacao_acidente.str.contains("Fatais", case=False)
    df["com_vitima"] = ~df.classificacao_acidente.str.contains("Sem V", case=False)
    df["ksi"] = df.fatal | (df.feridos_graves > 0)  # mortos ou feridos graves
    df["km_int"] = np.floor(df.km).astype(int)
    return df


# ----------------------------------------------------------------------------- ANTT
def ler_antt(pasta):
    arqs = sorted(glob.glob(os.path.join(pasta, "antt", "*.csv")))
    partes = []
    for a in arqs:
        df = _ler_csv(a, dtype=str)
        df.columns = [c.strip().lower() for c in df.columns]
        if not _validar(df, ["data", "km", "trecho", "mortos"], "ANTT", a):
            continue
        df["data"] = pd.to_datetime(df.data, dayfirst=True, errors="coerce")
        df["km"] = _num(df.km)
        tr = df.trecho.str.extract(r"BR-?(\d+)\D+([A-Z]{2})")
        df["br"] = pd.to_numeric(tr[0], errors="coerce")
        df["uf"] = tr[1]
        df["mortos"] = pd.to_numeric(df.mortos, errors="coerce").fillna(0)
        df["arquivo"] = os.path.basename(a)
        partes.append(df[["data", "br", "uf", "km", "mortos", "tipo_de_ocorrencia", "arquivo"]])
    return pd.concat(partes, ignore_index=True) if partes else pd.DataFrame()


# ----------------------------------------------------------------------------- INMET
def ler_inmet(pasta):
    """Retorna (estacoes, chuva_diaria[codigo, data, mm])."""
    arqs = sorted(glob.glob(os.path.join(pasta, "inmet", "*.CSV")) + glob.glob(os.path.join(pasta, "inmet", "*.csv")))
    est, diarias = {}, []
    for a in arqs:
        with open(a, encoding="latin-1") as f:
            linhas = f.read().splitlines()
        meta = {}
        for l in linhas[:8]:
            k, _, v = l.partition(";")
            meta[k.strip().rstrip(":").upper()] = v.strip()
        cod = meta.get("CODIGO (WMO)")
        lat, lon = float(meta["LATITUDE"].replace(",", ".")), float(meta["LONGITUDE"].replace(",", "."))
        est[cod] = dict(codigo=cod, nome=meta.get("ESTACAO", meta.get("ESTAÇÃO")), uf=meta.get("UF"),
                        lat=lat, lon=lon, fonte="INMET")
        df = pd.read_csv(io.StringIO("\n".join(linhas[8:])), sep=";", dtype=str)
        df.columns = [c.strip() for c in df.columns]
        col_data = [c for c in df.columns if c.upper().startswith("DATA")][0]
        col_chuva = [c for c in df.columns if "PRECIPITA" in c.upper()]
        if not col_chuva:
            _log("INMET", f"{os.path.basename(a)}: coluna de precipitação não encontrada")
            continue
        mm = _num(df[col_chuva[0]])
        mm = mm.where(mm >= 0)  # -9999 = falha
        d = pd.to_datetime(df[col_data].str.replace("-", "/"), format="%Y/%m/%d", errors="coerce")
        g = pd.DataFrame({"data": d, "mm": mm}).groupby("data").agg(mm=("mm", "sum"), n=("mm", "count"))
        g.loc[g.n < 20, "mm"] = np.nan  # dia com muitas horas faltando
        g = g.reset_index()
        g["codigo"] = cod
        diarias.append(g[["codigo", "data", "mm"]])
        _log("INMET", f"{os.path.basename(a)}: OK ({len(df)} horas)")
    return pd.DataFrame(est.values()), pd.concat(diarias, ignore_index=True)


# ----------------------------------------------------------------------------- CEMADEN
def ler_cemaden(pasta):
    arqs = sorted(glob.glob(os.path.join(pasta, "cemaden", "*.csv")))
    if not arqs:
        return pd.DataFrame(), pd.DataFrame()
    partes = []
    for a in arqs:
        df = _ler_csv(a, dtype=str)
        df.columns = [c.strip() for c in df.columns]
        if _validar(df, ["codEstacao", "latitude", "longitude", "datahora", "valorMedida"], "CEMADEN", a):
            partes.append(df)
    df = pd.concat(partes, ignore_index=True)
    df["mm"] = _num(df.valorMedida)
    df["data"] = pd.to_datetime(df.datahora.str[:10], errors="coerce")
    est = df.groupby("codEstacao").agg(nome=("nomeEstacao", "first"), uf=("uf", "first"),
                                       lat=("latitude", "first"), lon=("longitude", "first")).reset_index()
    est["lat"], est["lon"] = _num(est.lat), _num(est.lon)
    est = est.rename(columns={"codEstacao": "codigo"}).assign(fonte="CEMADEN")
    g = df.groupby(["codEstacao", "data"]).agg(mm=("mm", "sum"), n=("mm", "count")).reset_index()
    g.loc[g.n < 18, "mm"] = np.nan
    return est, g.rename(columns={"codEstacao": "codigo"})[["codigo", "data", "mm"]]


# ----------------------------------------------------------------------------- DNIT
def ler_snv(pasta):
    a = glob.glob(os.path.join(pasta, "dnit", "snv*.csv"))[0]
    df = _ler_csv(a, dtype=str)
    _validar(df, ["vl_br", "sg_uf", "vl_codigo", "vl_km_inic", "vl_km_fina"], "SNV", a)
    for c in ["vl_km_inic", "vl_km_fina", "lat_ini", "lon_ini", "lat_fim", "lon_fim"]:
        df[c] = _num(df[c])
    df["br"] = pd.to_numeric(df.vl_br)
    df["concedido"] = df.get("ds_adminis", pd.Series("", index=df.index)).str.contains("Conce", case=False, na=False)
    return df


def segmentos_1km(snv):
    """Quebra cada trecho do SNV em unidades de análise de 1 km, interpolando coordenadas.
    Com o shapefile real, troque a interpolação linear por `linha.interpolate()` (GeoPandas)."""
    linhas = []
    for r in snv.itertuples():
        k0, k1 = int(np.floor(r.vl_km_inic)), int(np.ceil(r.vl_km_fina))
        for k in range(k0, k1):
            f = lambda km: (km - r.vl_km_inic) / max(r.vl_km_fina - r.vl_km_inic, 1e-9)
            fa, fb = max(0, f(k)), min(1, f(k + 1))
            linhas.append(dict(br=r.br, uf=r.sg_uf, km=k, cod_snv=r.vl_codigo, concedido=r.concedido,
                               superficie=r.ds_superfi,
                               lat_a=r.lat_ini + (r.lat_fim - r.lat_ini) * fa, lon_a=r.lon_ini + (r.lon_fim - r.lon_ini) * fa,
                               lat_b=r.lat_ini + (r.lat_fim - r.lat_ini) * fb, lon_b=r.lon_ini + (r.lon_fim - r.lon_ini) * fb))
    s = pd.DataFrame(linhas).drop_duplicates(["br", "uf", "km"])
    s["lat"], s["lon"] = (s.lat_a + s.lat_b) / 2, (s.lon_a + s.lon_b) / 2
    s["seg_id"] = s.br.astype(int).astype(str).str.zfill(3) + "-" + s.uf + "-" + s.km.astype(str).str.zfill(4)
    return s.reset_index(drop=True)


def ler_vmda(pasta):
    a = glob.glob(os.path.join(pasta, "dnit", "vmda*.csv"))[0]
    df = _ler_csv(a, dtype=str)
    _validar(df, ["ano", "br", "uf", "km_inicial", "km_final", "vmda"], "VMDa", a)
    for c in ["km_inicial", "km_final"]:
        df[c] = _num(df[c])
    df["br"] = pd.to_numeric(df.br)
    df["ano"] = pd.to_numeric(df.ano)
    df["vmda"] = _num(df.vmda)
    return df


def ler_intervencoes(pasta):
    a = glob.glob(os.path.join(pasta, "dnit", "intervencoes*.csv"))
    if not a:
        return pd.DataFrame()
    df = _ler_csv(a[0], dtype=str)
    df["br"] = pd.to_numeric(df.br)
    df["km_inicial"], df["km_final"] = _num(df.km_inicial), _num(df.km_final)
    df["data_inicio"] = pd.to_datetime(df.data_inicio)
    df["data_conclusao"] = pd.to_datetime(df.data_conclusao)
    return df


def ler_interdicoes(pasta):
    a = glob.glob(os.path.join(pasta, "dnit", "ocorrencias_interdicao*.csv"))
    if not a:
        _log("INTERDICOES", "arquivo ausente: módulo de deslizamentos desativado")
        return pd.DataFrame()
    df = _ler_csv(a[0], dtype=str)
    df["br"] = pd.to_numeric(df.br)
    df["km"] = _num(df.km_inicial)
    df["data"] = pd.to_datetime(df.data_hora_inicio).dt.normalize()
    _log("INTERDICOES", f"OK ({len(df)} ocorrências)")
    return df


def ler_setores_risco(pasta):
    a = glob.glob(os.path.join(pasta, "sgb", "*.csv"))
    if not a:
        return pd.DataFrame()
    df = _ler_csv(a[0], dtype=str)
    df["lat"], df["lon"] = _num(df.LATITUDE), _num(df.LONGITUDE)
    return df


def ler_previsao(pasta):
    a = glob.glob(os.path.join(pasta, "previsao", "*.csv"))
    if not a:
        return pd.DataFrame()
    df = _ler_csv(a[0], dtype=str)
    df["prev24"] = _num(df.chuva_prevista_24h_mm)
    df["obs48"] = _num(df.chuva_observada_48h_anteriores_mm)
    return df
