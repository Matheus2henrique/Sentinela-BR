import base64, pathlib, json, datetime, zoneinfo
import os
G = pathlib.Path(os.environ.get('SENTINELA_NODE_MODULES', '/home/claude/apresentacao/geo/node_modules'))
tpl = pathlib.Path('painel_template.html').read_text()
fonts = ''
for fam, pkg, w in [('Overpass','overpass',400),('Overpass','overpass',600),('Overpass','overpass',800),('JetBrains Mono','jetbrains-mono',400),('JetBrains Mono','jetbrains-mono',700)]:
    f = G/f'@fontsource/{pkg}/files/{pkg}-latin-{w}-normal.woff2'
    if not f.exists(): continue
    b = base64.b64encode(f.read_bytes()).decode()
    fonts += f"@font-face{{font-family:'{fam}';font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{b}) format('woff2')}}\n"
D = json.load(open('dados.json'))
D['gerado'] = datetime.datetime.now(zoneinfo.ZoneInfo('America/Sao_Paulo')).isoformat(timespec='minutes')
cfg = pathlib.Path('config.json'); D.update(json.loads(cfg.read_text()) if cfg.exists() else {})
sm = pathlib.Path('sim_2025_transito.json')
if sm.exists():  # SIM/DataSUS 2025 (preliminar) e IBGE 2025 (213.421.037 habitantes)
    S = json.loads(sm.read_text()); D['pn']['sim']['2025'] = S['transito']; D['pn']['taxa']['2025'] = round(S['transito'] / 213421037 * 1e5, 1); D['pn']['prelim'] = [2025]
ad = pathlib.Path('adapta.json'); D['adapta'] = json.loads(ad.read_text()) if ad.exists() else None
at = pathlib.Path('atlas.json'); D['atlas'] = json.loads(at.read_text()) if at.exists() else None
icm = pathlib.Path('icm.json'); D['icm'] = json.loads(icm.read_text()) if icm.exists() else None
alerts = pathlib.Path('alertas_inmet.json'); D['alertas'] = json.loads(alerts.read_text()) if alerts.exists() else []
dados = json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
html = tpl.replace('__FONTS__', fonts).replace('__LEAFLET_CSS__', (G/'leaflet/dist/leaflet.css').read_text()).replace('__LEAFLET_JS__', (G/'leaflet/dist/leaflet.js').read_text().replace('</script', '<\\/script')).replace('__DATA__', dados)
pathlib.Path('saida').mkdir(exist_ok=True); pathlib.Path('saida/index.html').write_text(html)
print('ok', len(html)//1024, 'KB', D['gerado'])
