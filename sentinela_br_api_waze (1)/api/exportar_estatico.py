"""Gera os arquivos estáticos do feed (para hospedar em qualquer servidor ou bucket, sem rodar a API)."""
import json
from pathlib import Path
from fastapi.testclient import TestClient
from sentinela_api import app, UFS

c = TestClient(app)
out = Path("saida"); out.mkdir(exist_ok=True)
(out / "waze_cifs_brasil.json").write_text(c.get("/v1/waze/cifs.json?dias=14").text, encoding="utf-8")
(out / "waze_cifs_brasil.xml").write_text(c.get("/v1/waze/cifs.xml?dias=14").text, encoding="utf-8")
(out / "trechos_criticos.geojson").write_text(c.get("/v1/trechos?nivel_min=1").text, encoding="utf-8")
for uf in UFS:
    (out / f"encaminhamentos_{uf}.json").write_text(c.get(f"/v1/encaminhamentos?uf={uf}").text, encoding="utf-8")
print("ok:", sorted(p.name for p in out.iterdir())[:5], "...")
