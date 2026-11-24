"""pAInel Sentinela BR · atualização automática (Ministério dos Transportes · Equipe 4)

Roda às 8h, 14h e 18h (horário de Brasília). Em cada execução:
  1. baixa as bases oficiais abertas (PRF; e, quando o acesso estiver liberado, RENAEST, SIM/DataSUS, ANTT, DNIT);
  2. consolida a PRF 2021–ano corrente por ocorrência;
  3. recalcula malha, trechos de 5 km, risco esperado, dossiê, clima e o arquivo do painel;
  4. consulta os alertas oficiais do INMET e grava os que tocam trechos críticos (pop-up do painel);
  5. gera saida/index.html com a nova data e hora de atualização.

Estrutura de pastas esperada (igual à do desenvolvimento): BASE/real e BASE/sentinela_br.
No contêiner e no GitHub Actions, BASE = /home/claude (ver Dockerfile e workflow).
"""
import datetime, json, os, re, subprocess, sys, zipfile, io, pathlib, zoneinfo
import urllib.request

BASE = pathlib.Path(os.environ.get("SENTINELA_BASE", "/home/claude"))
REAL, SBR = BASE / "real", BASE / "sentinela_br"
TZ = zoneinfo.ZoneInfo("America/Sao_Paulo")
LOG = SBR / "atualizacao" / "log_atualizacao.txt"
UA = {"User-Agent": "SentinelaBR/1.0 (Ministerio dos Transportes)"}

def log(msg):
    linha = f"{datetime.datetime.now(TZ):%d/%m/%Y %H:%M} {msg}"
    print(linha); LOG.parent.mkdir(parents=True, exist_ok=True); LOG.open("a").write(linha + "\n")

def baixar(url, destino, timeout=300):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r, open(destino, "wb") as f:
        while (bloco := r.read(1 << 20)): f.write(bloco)
    return destino

# ---------- 1. PRF: links publicados na página de dados abertos ----------
PAGINA_PRF = "https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf"
def baixar_prf():
    html = urllib.request.urlopen(urllib.request.Request(PAGINA_PRF, headers=UA), timeout=60).read().decode("utf-8", "ignore")
    ano = datetime.date.today().year
    for y in range(2021, ano + 1):
        # 2021 até o ano anterior: base por pessoa com todas as causas e tipos; ano corrente: base por ocorrência
        padrao = rf'href="([^"]+)"[^>]*>[^<]*(?:Agrupados por pessoa - Todas as causas e tipos de acidentes)?[^<]*{y}' if y < ano else rf'href="([^"]+)"[^>]*>[^<]*Agrupados por ocorr[eê]ncia[^<]*{y}'
        m = re.search(padrao, html, re.I)
        if not m: log(f"PRF {y}: link não encontrado na página (verificar layout)"); continue
        url = m.group(1)
        if "drive.google.com" in url:  # os arquivos da PRF ficam no Google Drive
            fid = re.search(r"/d/([\w-]+)|id=([\w-]+)", url); fid = fid.group(1) or fid.group(2)
            subprocess.run([sys.executable, "-m", "gdown", "--fuzzy", url, "-O", str(REAL / f"prf_{y}.zip")], check=False)
        else:
            baixar(url, REAL / f"prf_{y}.zip")
        destino = REAL / (f"zip{y}" if y < ano else "prf")
        try:
            with zipfile.ZipFile(REAL / f"prf_{y}.zip") as z: z.extractall(destino)
            if y == ano:
                for p in destino.glob(f"datatran{y}*.csv"): p.rename(destino / f"datatran{y}.csv")
            log(f"PRF {y}: atualizado")
        except Exception as e:
            log(f"PRF {y}: falha ao extrair ({e})")

# ---------- 2. Bases complementares (entram assim que o acesso estiver liberado) ----------
COMPLEMENTARES = {
    "renaest": "https://dados.transportes.gov.br/api/3/action/package_show?id=renaest",
    "antt_trechos": "https://dados.antt.gov.br/api/3/action/package_show?id=trecho-concedido",
    "sim": "https://opendatasus.saude.gov.br/api/3/action/package_show?id=sim",
}
def baixar_complementares():
    pasta = REAL / "complementares"; pasta.mkdir(exist_ok=True)
    for nome, api in COMPLEMENTARES.items():
        try:
            meta = json.load(urllib.request.urlopen(urllib.request.Request(api, headers=UA), timeout=60))
            recursos = sorted(meta["result"]["resources"], key=lambda r: r.get("last_modified") or r.get("created") or "", reverse=True)
            for r in recursos[:3]:  # os mais recentes; a carga completa fica a cargo do script de cada base
                baixar(r["url"], pasta / f"{nome}_{r['id']}{pathlib.Path(r['url']).suffix}")
            log(f"{nome}: {len(recursos[:3])} arquivo(s) baixado(s)")
        except Exception as e:
            log(f"{nome}: indisponível nesta execução ({e.__class__.__name__})")

# ---------- 3. Recalcular o painel ----------
ETAPAS = [(REAL, "consolidar_todos.py"), (SBR / "viagem", "malha_real.py"), (SBR / "viagem", "perfis.py"),
          (SBR / "viagem", "estatisticas_extra.py"), (SBR / "viagem", "dossie.py"), (SBR / "viagem", "clima.py"),
          (SBR / "p6", "preparar.py")]
def recalcular():
    for pasta, script in ETAPAS:
        r = subprocess.run([sys.executable, script], cwd=pasta, capture_output=True, text=True)
        log(f"{script}: {'ok' if r.returncode == 0 else 'ERRO ' + r.stderr[-400:]}")
        if r.returncode: raise SystemExit(1)

def main():
    log("início da atualização")
    try: baixar_prf()
    except Exception as e: log(f"PRF: sem acesso nesta execução ({e.__class__.__name__}); usando a última base")
    baixar_complementares()
    recalcular()
    r = subprocess.run([sys.executable, "icm_dnit.py", "baixar"], cwd=SBR / "p6", capture_output=True, text=True)
    log("ICM DNIT: " + (r.stdout.strip().splitlines() or ["sem saída"])[-1] if r.returncode == 0 else f"ICM DNIT: indisponível nesta execução; mantido o último icm.json")
    subprocess.run([sys.executable, "monitor_alertas.py", "--sem-montar"], cwd=SBR / "atualizacao", check=False)
    r = subprocess.run([sys.executable, "montar.py"], cwd=SBR / "p6", capture_output=True, text=True); log("montar.py: " + r.stdout.strip())
    log("fim da atualização")

if __name__ == "__main__":
    main()
