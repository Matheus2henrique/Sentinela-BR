"""Consolida as bases da PRF por pessoa/causa (2021-2025) por ocorrência e une a 2026 (por ocorrência)."""
import os, sys, pandas as pd, numpy as np
sys.path.insert(0, os.path.join(os.environ.get('SENTINELA_BASE', '/home/claude'), 'sentinela_br/mvp'))
import adaptadores as ad
cols = ["id","pesid","data_inversa","horario","uf","br","km","municipio","causa_principal","causa_acidente","ordem_tipo_acidente",
        "tipo_acidente","classificacao_acidente","fase_dia","condicao_metereologica","tipo_pista","tracado_via","uso_solo",
        "tipo_veiculo","tipo_envolvido","mortos","feridos_graves","latitude","longitude"]
partes = []
for y in [2021, 2022, 2023, 2024, 2025]:
    d = pd.read_csv(f"zip{y}/acidentes{y}_todas_causas_tipos.csv", sep=";", encoding="latin-1", usecols=cols, dtype=str)
    for c in ["mortos", "feridos_graves"]:
        d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0)
    pes = d.drop_duplicates(["id", "pesid"])
    m = pes.groupby("id").agg(mortos=("mortos", "sum"), feridos_graves=("feridos_graves", "sum"),
                              moto=("tipo_veiculo", lambda s: s.isin(["Motocicleta", "Motoneta", "Ciclomotor"]).any()),
                              mortos_moto=("mortos", "size")).reset_index()
    # mortos em moto e pedestres mortos (por pessoa)
    pm = pes[pes.mortos > 0]
    mm = pm[pm.tipo_veiculo.isin(["Motocicleta", "Motoneta", "Ciclomotor"]) & pm.tipo_envolvido.isin(["Condutor", "Passageiro"])].groupby("id").size()
    mp = pm[pm.tipo_envolvido.eq("Pedestre")].groupby("id").size()
    causas = d.groupby("id").causa_acidente.agg(lambda s: "|".join(sorted(set(s.dropna()))))
    tipos = d.groupby("id").tipo_acidente.agg(lambda s: "|".join(sorted(set(s.dropna()))))
    d["prio"] = d.causa_principal.eq("Sim").astype(int) * 2 + d.ordem_tipo_acidente.eq("1").astype(int)
    acc = d.sort_values("prio", ascending=False).drop_duplicates("id").drop(
        columns=["mortos", "feridos_graves", "pesid", "tipo_veiculo", "tipo_envolvido", "prio", "causa_principal", "ordem_tipo_acidente"])
    acc = acc.merge(m[["id", "mortos", "feridos_graves", "moto"]], on="id")
    acc["causas_todas"] = acc.id.map(causas); acc["tipos_todos"] = acc.id.map(tipos)
    acc["mortos_moto"] = acc.id.map(mm).fillna(0); acc["mortos_pedestre"] = acc.id.map(mp).fillna(0)
    acc["ano"] = y
    print(y, len(acc), "acidentes", int(acc.mortos.sum()), "mortes")
    partes.append(acc)
# 2026 (por ocorrência, só causa principal)
p26 = pd.read_csv("prf/datatran2026.csv", sep=";", encoding="latin-1", dtype=str)
for c in ["mortos", "feridos_graves"]:
    p26[c] = pd.to_numeric(p26[c], errors="coerce").fillna(0)
p26["causas_todas"] = p26.causa_acidente; p26["tipos_todos"] = p26.tipo_acidente
p26["moto"] = np.nan; p26["mortos_moto"] = np.nan; p26["mortos_pedestre"] = np.nan; p26["ano"] = 2026
p26 = p26[[c for c in partes[0].columns if c in p26.columns]]
print(2026, len(p26), "acidentes", int(p26.mortos.sum()), "mortes")
t = pd.concat(partes + [p26], ignore_index=True)
t["km"] = ad._num(t.km.astype(str)); t["latitude"] = ad._num(t.latitude.astype(str)); t["longitude"] = ad._num(t.longitude.astype(str))
t["br"] = pd.to_numeric(t.br, errors="coerce")
t["data"] = pd.to_datetime(t.data_inversa, errors="coerce")
t = t.dropna(subset=["br", "km"])
t["br"] = t.br.astype(int)
t.to_pickle("prf_2021_2026.pkl")
print("total", len(t), int(t.mortos.sum()))
print(t.groupby("ano").agg(acid=("id", "size"), mortos=("mortos", "sum")))
