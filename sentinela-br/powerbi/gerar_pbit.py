"""Gera Sentinela_BR.pbit (modelo do Power BI) a partir do kit de CSV (pasta powerbi/)."""
import csv, json, uuid, zipfile, re, io, os, sys
K = '/home/claude/pbi2'; OUT = '/home/claude/entregas/Sentinela_BR.pbit'
G = lambda: str(uuid.uuid4())
def u16(o): return (o if isinstance(o, str) else json.dumps(o, ensure_ascii=False)).encode('utf-16-le')
num_re = re.compile(r'^-?\d+(,\d+)?$')
TXT_FORCE = {'id_trecho': 'int64', 'ano': 'int64', 'km_inicio': 'int64', 'km_fim': 'int64', 'icm_ano': 'int64', 'anos_com_morte': 'int64', 'anos_com_desastre_2016_2025': 'int64'}
NONE_SUM = {'id_trecho', 'ano', 'km_inicio', 'km_fim', 'latitude', 'longitude', 'icm_ano', 'icm_ultimo', 'icm_2021', 'icm_2022', 'icm_2023', 'icm_2024', 'icm_2025', 'icm_2026', 'inundacao_2050_indice', 'eficacia', 'rs_por_vida_ano', 'taxa_100mil', 'meta_2030', 'tendencia', 'pct_noite', 'pct_urbano', 'anos_com_morte', 'anos_com_desastre_2016_2025', 'mortes_prf_por_100mil', 'mortes_prf_por_10mil_veiculos'}
def tipos(arq):
    rd = csv.reader(open(os.path.join(K, arq), encoding='utf-8-sig'), delimiter=';'); cab = next(rd); vals = [[] for _ in cab]
    for k, r in enumerate(rd):
        for j, v in enumerate(r): vals[j].append(v)
    out = []
    for c, vs in zip(cab, vals):
        nv = [v for v in vs if v != '']
        if c in TXT_FORCE: t = TXT_FORCE[c]
        elif nv and all(num_re.match(v) for v in nv): t = 'double' if any(',' in v for v in nv) else 'int64'
        else: t = 'string'
        out.append((c, t))
    return out
MT = {'string': 'type text', 'int64': 'Int64.Type', 'double': 'type number'}
def m_csv(arq, cols):
    nums = [c for c, t in cols if t != 'string']
    tl = ', '.join(f'{{"{c}", {MT[t]}}}' for c, t in cols)
    lines = ['let',
             f'    Fonte = Csv.Document(File.Contents(Text.TrimEnd(PastaDados, "\\") & "\\{arq}"), [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),',
             '    Cabecalho = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),']
    if nums: lines.append(f'    Vazios = Table.ReplaceValue(Cabecalho, "", null, Replacer.ReplaceValue, {{{", ".join(chr(34) + c + chr(34) for c in nums)}}}),')
    else: lines.append('    Vazios = Cabecalho,')
    lines += [f'    Tipos = Table.TransformColumnTypes(Vazios, {{{tl}}}, "pt-BR")', 'in', '    Tipos']
    return lines
TAB = {}
def tabela(nome, cols, m, extra=None):
    t = {'name': nome, 'lineageTag': G(), 'columns': [], 'partitions': [{'name': f'{nome}-{G()}', 'mode': 'import', 'source': {'type': 'm', 'expression': m}}],
         'annotations': [{'name': 'PBI_ResultType', 'value': 'Table'}]}
    for c, ty in cols:
        col = {'name': c, 'dataType': ty, 'sourceColumn': c, 'lineageTag': G(), 'summarizeBy': ('none' if ty == 'string' or c in NONE_SUM else 'sum'), 'annotations': [{'name': 'SummarizationSetBy', 'value': 'Automatic'}]}
        if ty == 'double': col['formatString'] = '#,0.00'
        if ty == 'int64' and col['summarizeBy'] == 'sum': col['formatString'] = '#,0'
        if c == 'latitude': col['dataCategory'] = 'Latitude'
        if c == 'longitude': col['dataCategory'] = 'Longitude'
        t['columns'].append(col)
    if extra: t.update(extra)
    TAB[nome] = t; return t
ARQS = ['dim_trecho.csv', 'dim_uf.csv', 'fato_mortes_ano.csv', 'fato_mortes_tipo.csv', 'fato_acao_ia.csv', 'fato_pnatrans.csv']
for a in ARQS:
    cols = tipos(a); tabela(a[:-4], cols, m_csv(a, cols))
# Atualizacao (selo)
tabela('Atualizacao', [('DataHora', 'dateTime')], ['let', '    Agora = DateTimeZone.SwitchZone(DateTimeZone.UtcNow(), -3),', '    Fonte = #table(type table [DataHora = datetime], {{DateTimeZone.RemoveZone(Agora)}})', 'in', '    Fonte'])
TAB['Atualizacao']['columns'][0]['formatString'] = 'dd/MM/yyyy HH:mm'
# Fontes (do fontes.json do painel)
F = json.load(open('/home/claude/sentinela_br/docs/fontes.json'))
lin = []
for s in F:
    for x in s['itens']:
        e = lambda v: v.replace('"', '""')
        lin.append(f'{{"{e(s["secao"].split(". ", 1)[-1])}", "{e(x["fonte"])}", "{e(x["orgao"])}", "{e(x["conteudo"])}", "{e(x["situacao"])}", "{e(x["link"])}"}}')
tabela('Fontes', [(c, 'string') for c in ['Grupo', 'Fonte', 'Orgao', 'Conteudo', 'Situacao', 'Link']],
       ['let', '    Fonte = #table(type table [Grupo = text, Fonte = text, Orgao = text, Conteudo = text, Situacao = text, Link = text], {'] + ['        ' + l + (',' if k < len(lin) - 1 else '') for k, l in enumerate(lin)] + ['    })', 'in', '    Fonte'])
TAB['Fontes']['columns'][5]['dataCategory'] = 'WebUrl'
# Medidas
fontes_txt = open(os.path.join(K, 'medidas_dax.txt'), encoding='utf-8').read()
fdax = fontes_txt.split('Fontes do painel =', 1)[1].split('// 3)', 1)[0].strip()
MED = [
 ('Mortes', 'SUM ( fato_mortes_ano[mortes] )', '#,0'),
 ('Mortes esperadas 12m', 'SUM ( dim_trecho[mortes_esperadas_12m] )', '#,0'),
 ('Trechos', 'COUNTROWS ( dim_trecho )', '#,0'),
 ('Trechos críticos', 'CALCULATE ( COUNTROWS ( dim_trecho ), dim_trecho[nivel_risco] = "Crítico" )', '#,0'),
 ('Vidas salvas/ano (ação principal)', 'SUMX ( VALUES ( dim_trecho[id_trecho] ), CALCULATE ( MAX ( fato_acao_ia[vidas_ano] ) ) )', '#,0.0'),
 ('Custo da ação principal', 'SUMX ( VALUES ( dim_trecho[id_trecho] ), VAR v = CALCULATE ( MAX ( fato_acao_ia[vidas_ano] ) ) RETURN CALCULATE ( MIN ( fato_acao_ia[custo_rs] ), fato_acao_ia[vidas_ano] = v ) )', '"R$" #,0'),
 ('Vidas salvas/ano (todas as ações)', 'SUM ( fato_acao_ia[vidas_ano] )', '#,0.0'),
 ('Custo das ações', 'SUM ( fato_acao_ia[custo_rs] )', '"R$" #,0'),
 ('Óbitos SIM', 'SUM ( fato_pnatrans[obitos_sim] )', '#,0'),
 ('Taxa por 100 mil', 'AVERAGE ( fato_pnatrans[taxa_100mil] )', '0.0'),
 ('Meta Pnatrans 2030', 'AVERAGE ( fato_pnatrans[meta_2030] )', '0.0'),
 ('% mortes em concessões', 'DIVIDE ( CALCULATE ( [Mortes], dim_trecho[responsavel] <> "DNIT" ), [Mortes] )', '0%'),
 ('Atualizado em', 'VAR t = MAX ( Atualizacao[DataHora] ) RETURN "⟳ Atualizado em " & FORMAT ( t, "dd/MM/yyyy" ) & " às " & FORMAT ( t, "HH:mm" )', None),
 ('Fontes do painel', fdax, None)]
med = tabela('Medidas', [('Coluna', 'string')], ['let', '    Fonte = #table(type table [Coluna = text], {})', 'in', '    Fonte'])
med['columns'][0]['isHidden'] = True
med['measures'] = [dict({'name': n, 'expression': e, 'lineageTag': G()}, **({'formatString': f} if f else {})) for n, e, f in MED]
REL = [('fato_mortes_ano', 'id_trecho', 'dim_trecho', 'id_trecho'), ('fato_mortes_tipo', 'id_trecho', 'dim_trecho', 'id_trecho'),
       ('fato_acao_ia', 'id_trecho', 'dim_trecho', 'id_trecho'), ('dim_trecho', 'uf', 'dim_uf', 'uf')]
ordem = ['PastaDados'] + list(TAB)
model = {'name': 'SemanticModel', 'compatibilityLevel': 1550, 'model': {
  'culture': 'pt-BR', 'dataAccessOptions': {'legacyRedirects': True, 'returnErrorValuesAsNull': True}, 'defaultPowerBIDataSourceVersion': 'powerBI_V3', 'sourceQueryCulture': 'pt-BR',
  'tables': list(TAB.values()),
  'relationships': [{'name': G(), 'fromTable': a, 'fromColumn': b, 'toTable': c, 'toColumn': d} for a, b, c, d in REL],
  'expressions': [{'name': 'PastaDados', 'kind': 'm', 'expression': '"C:\\Sentinela_BR\\powerbi" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]', 'lineageTag': G(),
                   'description': 'Pasta onde estão os CSV do kit (dim_trecho.csv, fato_*.csv, dim_uf.csv).', 'annotations': [{'name': 'PBI_ResultType', 'value': 'Text'}, {'name': 'PBI_NavigationStepName', 'value': 'Navegação'}]}],
  'annotations': [{'name': 'PBI_QueryOrder', 'value': json.dumps(ordem, ensure_ascii=False)}, {'name': '__PBI_TimeIntelligenceEnabled', 'value': '0'}, {'name': 'PBIDesktopVersion', 'value': '2.128.751.0 (24.04)'}]}}
# ---------- relatório ----------
def ref(tb, c, medida=False):
    k = 'Measure' if medida else 'Column'; return {k: {'Expression': {'SourceRef': {'Entity': tb}}, 'Property': c}}
def proto(campos):
    ents = []; sel = []
    for tb, c, m in campos:
        if tb not in ents: ents.append(tb)
    al = {tb: f't{k}' for k, tb in enumerate(ents)}
    for tb, c, m in campos:
        sel.append({('Measure' if m else 'Column'): {'Expression': {'SourceRef': {'Source': al[tb]}}, 'Property': c}, 'Name': f'{tb}.{c}', 'NativeReferenceName': c})
    return {'Version': 2, 'From': [{'Name': al[tb], 'Entity': tb, 'Type': 0} for tb in ents], 'Select': sel}
def lit(v): return {'expr': {'Literal': {'Value': v}}}
def vis(x, y, w, h, tipo, proj, titulo=None, z=0, objs=None, ordem=None):
    campos = []; P = {}
    for papel, lst in proj.items():
        P[papel] = []
        for tb, c, m in lst:
            campos.append((tb, c, m)); P[papel].append({'queryRef': f'{tb}.{c}', **({'active': True} if papel == 'Category' else {})})
    pq = proto(list(dict.fromkeys(campos)))
    if ordem:
        tb, c, m, d = ordem; al = next(f['Name'] for f in pq['From'] if f['Entity'] == tb)
        pq['OrderBy'] = [{'Direction': d, 'Expression': {('Measure' if m else 'Column'): {'Expression': {'SourceRef': {'Source': al}}, 'Property': c}}}]
    sv = {'visualType': tipo, 'projections': P, 'prototypeQuery': pq, 'drillFilterOtherVisuals': True}
    vo = {}
    if titulo: vo['title'] = [{'properties': {'show': lit('true'), 'text': lit("'" + titulo.replace("'", "''") + "'")}}]
    if vo: sv['vcObjects'] = vo
    if objs: sv['objects'] = objs
    nome = uuid.uuid4().hex[:20]
    cfg = {'name': nome, 'layouts': [{'id': 0, 'position': {'x': x, 'y': y, 'z': z, 'width': w, 'height': h}}], 'singleVisual': sv}
    return {'x': x, 'y': y, 'z': z, 'width': w, 'height': h, 'config': json.dumps(cfg, ensure_ascii=False), 'filters': '[]'}
def texto(x, y, w, h, linhas, z=0):
    pars = [{'textRuns': [{'value': t, 'textStyle': st}]} for t, st in linhas]
    cfg = {'name': uuid.uuid4().hex[:20], 'layouts': [{'id': 0, 'position': {'x': x, 'y': y, 'z': z, 'width': w, 'height': h}}],
           'singleVisual': {'visualType': 'textbox', 'drillFilterOtherVisuals': True, 'objects': {'general': [{'properties': {'paragraphs': pars}}]}}}
    return {'x': x, 'y': y, 'z': z, 'width': w, 'height': h, 'config': json.dumps(cfg, ensure_ascii=False), 'filters': '[]'}
M = lambda c: ('Medidas', c, True); D_ = lambda c: ('dim_trecho', c, False)
TIT = lambda t: texto(16, 8, 900, 52, [('pAInel Sentinela BR · ' + t, {'fontWeight': 'bold', 'fontSize': '20pt'}), ('Ministério dos Transportes · Equipe 4 · Innovathon 2026', {'fontSize': '10pt', 'color': '#605E5C'})])
SELO = lambda: vis(940, 10, 324, 56, 'card', {'Values': [M('Atualizado em')]}, None, 5, {'labels': [{'properties': {'fontSize': lit('11D')}}], 'categoryLabels': [{'properties': {'show': lit('false')}}]})
def fatias(y=70):
    return [vis(16 + k * 252, y, 240, 56, 'slicer', {'Values': [D_(c)]}, t, 2, {'data': [{'properties': {'mode': lit("'Dropdown'")}}]})
            for k, (c, t) in enumerate([('uf', 'Estado'), ('rodovia', 'Rodovia'), ('responsavel', 'Responsável'), ('nivel_risco', 'Nível de risco'), ('concessionaria', 'Concessionária')])]
pag = []
v1 = [TIT('Visão'), SELO()] + fatias() + [
  vis(16, 136, 302, 110, 'card', {'Values': [M('Mortes')]}, 'Mortes jan/2021 a out/2026 (PRF)'),
  vis(330, 136, 302, 110, 'card', {'Values': [M('Mortes esperadas 12m')]}, 'Mortes esperadas nos próximos 12 meses'),
  vis(644, 136, 302, 110, 'card', {'Values': [M('Trechos críticos')]}, 'Trechos críticos'),
  vis(958, 136, 306, 110, 'card', {'Values': [M('Vidas salvas/ano (ação principal)')]}, 'Vidas salvas/ano com a ação principal (estimativa)'),
  vis(16, 258, 420, 220, 'lineChart', {'Category': [('fato_mortes_ano', 'ano', False)], 'Y': [M('Mortes')]}, 'Mortes por ano (2026 até outubro)'),
  vis(448, 258, 400, 220, 'clusteredBarChart', {'Category': [('fato_mortes_tipo', 'tipo_sinistro', False)], 'Y': [M('Mortes')]}, 'Como se morre', ordem=('Medidas', 'Mortes', True, 2)),
  vis(860, 258, 404, 220, 'clusteredBarChart', {'Category': [D_('responsavel')], 'Y': [M('Mortes esperadas 12m')]}, 'Mortes esperadas por responsável', ordem=('Medidas', 'Mortes esperadas 12m', True, 2)),
  vis(16, 490, 1248, 220, 'tableEx', {'Values': [D_('rodovia'), D_('uf'), D_('km_inicio'), D_('municipio'), D_('nivel_risco'), D_('mortes_esperadas_12m'), D_('mortes_2021_out2026'), D_('motivo_principal_prf'), D_('responsavel'), D_('concessionaria')]},
      'Trechos com maior risco', ordem=('dim_trecho', 'mortes_esperadas_12m', False, 2))]
pag.append(('Visão', v1))
v2 = [TIT('Ranking e ações'), SELO()] + fatias() + [
  vis(16, 136, 1248, 290, 'tableEx', {'Values': [D_('rodovia'), D_('uf'), D_('km_inicio'), D_('km_fim'), D_('municipio'), D_('nivel_risco'), D_('mortes_esperadas_12m'), D_('mortes_2021_out2026'), D_('tipo_principal'), D_('motivo_principal_prf'), D_('responsavel'), D_('concessionaria'), D_('icm_classe'), D_('inundacao_2050_classe')]},
      'Todos os trechos com morte', ordem=('dim_trecho', 'mortes_esperadas_12m', False, 2)),
  vis(16, 438, 1248, 272, 'tableEx', {'Values': [D_('rodovia'), D_('uf'), D_('km_inicio'), ('fato_acao_ia', 'medida', False), ('fato_acao_ia', 'dono', False), ('fato_acao_ia', 'custo_rs', False), ('fato_acao_ia', 'vidas_ano', False), ('fato_acao_ia', 'rs_por_vida_ano', False), ('fato_acao_ia', 'fonte_custo', False), ('fato_acao_ia', 'fonte_eficacia', False)]},
      'Ações por trecho: custo, vidas salvas e dono (estimativas)', ordem=('fato_acao_ia', 'vidas_ano', False, 2))]
pag.append(('Ranking e ações', v2))
v3 = [TIT('Pnatrans'), SELO(),
  vis(16, 80, 300, 110, 'card', {'Values': [M('Óbitos SIM')]}, 'Óbitos no trânsito (SIM), anos selecionados'),
  vis(328, 80, 300, 110, 'card', {'Values': [M('Meta Pnatrans 2030')]}, 'Meta Pnatrans 2030 (por 100 mil)'),
  vis(16, 202, 1248, 420, 'lineChart', {'Category': [('fato_pnatrans', 'ano', False)], 'Y': [M('Taxa por 100 mil'), M('Meta Pnatrans 2030')]}, 'Mortes por 100 mil habitantes (SIM/MS e IBGE; 2025 preliminar) e meta de 2030'),
  texto(16, 632, 1248, 60, [('Fonte: Ministério da Saúde, SIM (CID-10 V01–V89); IBGE. Meta do Pnatrans: metade da taxa de 2020 até 2030.', {'fontSize': '10pt'})])]
pag.append(('Pnatrans', v3))
v4 = [TIT('Clima, desastres e pavimento'), SELO()] + fatias() + [
  vis(16, 136, 410, 270, 'clusteredBarChart', {'Category': [D_('clima_evento')], 'Y': [M('Mortes')]}, 'Mortes em trechos com risco climático recorrente (PRF)', ordem=('Medidas', 'Mortes', True, 2)),
  vis(436, 136, 410, 270, 'clusteredBarChart', {'Category': [D_('inundacao_2050_classe')], 'Y': [M('Mortes')]}, 'Mortes por risco de inundação do município em 2050 (AdaptaBrasil)'),
  vis(856, 136, 408, 270, 'clusteredBarChart', {'Category': [D_('icm_classe')], 'Y': [M('Mortes')]}, 'Mortes por condição do pavimento (ICM DNIT)'),
  vis(16, 418, 1248, 292, 'tableEx', {'Values': [D_('rodovia'), D_('uf'), D_('km_inicio'), D_('municipio'), D_('clima_evento'), D_('clima_janela'), D_('desastre_recorrente'), D_('anos_com_desastre_2016_2025'), D_('inundacao_2050_classe'), D_('mortes_2021_out2026'), D_('responsavel')]},
      'Trechos com evento climático (PRF), desastre (Defesa Civil) e risco 2050', ordem=('dim_trecho', 'mortes_2021_out2026', False, 2))]
pag.append(('Clima e pavimento', v4))
v5 = [TIT('Fontes'), SELO(), vis(16, 80, 1248, 560, 'tableEx', {'Values': [('Fontes', c, False) for c in ['Grupo', 'Fonte', 'Orgao', 'Conteudo', 'Situacao', 'Link']]}, 'Fontes de dados conectadas e links de acesso'),
  texto(16, 650, 1248, 60, [('Custos e vidas salvas são estimativas para priorizar (DNIT SICRO/CMG/PNCV; FHWA; Trafikverket). Atualização às 8h, 14h e 18h.', {'fontSize': '10pt'})])]
pag.append(('Fontes', v5))
secoes = []
for k, (nome, vs) in enumerate(pag):
    for z, v in enumerate(vs):
        c = json.loads(v['config']); c['layouts'][0]['position']['z'] = z * 1000; v['z'] = z * 1000; v['config'] = json.dumps(c, ensure_ascii=False)
    secoes.append({'id': k, 'name': f'ReportSection{uuid.uuid4().hex[:20]}', 'displayName': nome, 'filters': '[]', 'ordinal': k, 'visualContainers': vs, 'config': '{}', 'displayOption': 1, 'width': 1280, 'height': 720})
layout = {'id': 0, 'sections': secoes, 'config': json.dumps({'version': '5.37', 'themeCollection': {}, 'activeSectionIndex': 0, 'defaultDrillFilterOtherVisuals': True,
           'settings': {'useNewFilterPaneExperience': True, 'allowChangeFilterTypes': True, 'useStylableVisualContainerHeader': True, 'exportDataMode': 1}}), 'layoutOptimization': 0}
# ---------- validação interna ----------
cols = {(t['name'], c['name']) for t in model['model']['tables'] for c in t['columns']} | {(t['name'], m['name']) for t in model['model']['tables'] for m in t.get('measures', [])}
for s in secoes:
    for v in s['visualContainers']:
        c = json.loads(v['config']); sv = c['singleVisual']
        for sel in sv.get('prototypeQuery', {}).get('Select', []):
            tb, cc = sel['Name'].split('.', 1); assert (tb, cc) in cols, sel['Name']
for a, b, c, d in REL: assert (a, b) in cols and (c, d) in cols
print('tabelas', len(TAB), 'medidas', len(MED), 'páginas', len(secoes), 'visuais', sum(len(s['visualContainers']) for s in secoes))
CT = '<?xml version="1.0" encoding="utf-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="json" ContentType="" /><Override PartName="/Version" ContentType="" /><Override PartName="/DataModelSchema" ContentType="" /><Override PartName="/DiagramLayout" ContentType="" /><Override PartName="/Report/Layout" ContentType="" /><Override PartName="/Settings" ContentType="" /><Override PartName="/Metadata" ContentType="" /></Types>'
diag = {'version': '1.1.0', 'diagrams': [{'ordinal': 0, 'scrollPosition': {'x': 0, 'y': 0}, 'nodes': [], 'name': 'Todas as tabelas', 'zoomValue': 100, 'pinKeyFieldsToTop': False, 'showExtraHeaderInfo': False, 'hideKeyFieldsWhenCollapsed': False, 'tablesLocked': False}], 'selectedDiagram': 'Todas as tabelas', 'defaultDiagram': 'Todas as tabelas'}
settings = {'Version': 4, 'ReportSettings': {}, 'QueriesSettings': {'TypeDetectionEnabled': True, 'RelationshipImportEnabled': True, 'Version': '2.128.751.0'}}
meta = {'Version': 5, 'AutoCreatedRelationships': [], 'FileDescription': 'pAInel Sentinela BR · Ministério dos Transportes · Equipe 4 · Innovathon 2026. Informe a pasta dos CSV do kit ao abrir.', 'CreatedFrom': 'Desktop', 'CreatedFromRelease': '2024.04'}
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '\ufeff' + CT)
    z.writestr('Version', u16('1.28'))
    z.writestr('DataModelSchema', u16(model))
    z.writestr('DiagramLayout', u16(diag))
    z.writestr('Report/Layout', u16(layout))
    z.writestr('Settings', u16(settings))
    z.writestr('Metadata', u16(meta))
print('ok', OUT, os.path.getsize(OUT))
