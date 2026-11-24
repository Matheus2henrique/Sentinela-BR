import base64, pathlib, json
import os
G = pathlib.Path(os.environ.get('SENTINELA_NODE_MODULES', '/home/claude/apresentacao/geo/node_modules'))
tpl = pathlib.Path('app_template.html').read_text()
fonts = ''
for fam, pkg, w in [('Overpass','overpass',400),('Overpass','overpass',600),('Overpass','overpass',800),('JetBrains Mono','jetbrains-mono',400),('JetBrains Mono','jetbrains-mono',700)]:
    f = G/f'@fontsource/{pkg}/files/{pkg}-latin-{w}-normal.woff2'
    if f.exists(): fonts += f"@font-face{{font-family:'{fam}';font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{base64.b64encode(f.read_bytes()).decode()}) format('woff2')}}\n"
D = json.load(open('dados_app2.json'))
D['alerta'] = {int(k): v for k, v in D['alerta'].items()}
D['muns'] = json.load(open('municipios_app.json')); D.pop('cidades', None)
dados = json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
html = tpl.replace('__FONTS__', fonts).replace('__LEAFLET_CSS__', (G/'leaflet/dist/leaflet.css').read_text()).replace('__LEAFLET_JS__', (G/'leaflet/dist/leaflet.js').read_text().replace('</script', '<\\/script')).replace('__DATA__', dados)
pathlib.Path('saida').mkdir(exist_ok=True); pathlib.Path('saida/index.html').write_text(html); print('ok', len(html)//1024, 'KB')
