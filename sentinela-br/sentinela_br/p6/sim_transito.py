"""SIM/DataSUS – Mortalidade Geral (JSON do Open Data SUS): óbitos por lesão de trânsito (causa básica CID-10 V01–V89)."""
import re, sys, zipfile, collections, json
arq = sys.argv[1]
rx = re.compile(r'\{[^{}]*?"DTOBITO":"(\d*)"[^{}]*?"CODMUNOCOR":"(\d*)"[^{}]*?"CAUSABAS":"([A-Z0-9]*)"')
tot = 0; vt = collections.Counter(); uf = collections.Counter(); mes = collections.Counter(); grupo = collections.Counter(); resto = ''
UF = {'11':'RO','12':'AC','13':'AM','14':'RR','15':'PA','16':'AP','17':'TO','21':'MA','22':'PI','23':'CE','24':'RN','25':'PB','26':'PE','27':'AL','28':'SE','29':'BA','31':'MG','32':'ES','33':'RJ','35':'SP','41':'PR','42':'SC','43':'RS','50':'MS','51':'MT','52':'GO','53':'DF'}
G = lambda c: 'Pedestre' if c < 'V10' else 'Ciclista' if c < 'V20' else 'Motociclista' if c < 'V30' else 'Triciclo' if c < 'V40' else 'Automóvel' if c < 'V50' else 'Caminhonete' if c < 'V60' else 'Veículo pesado' if c < 'V70' else 'Ônibus' if c < 'V80' else 'Outros'
with zipfile.ZipFile(arq) as z, z.open(z.namelist()[0]) as f:
    while True:
        b = f.read(1 << 24)
        if not b: break
        s = resto + b.decode('utf-8', 'replace'); ult = s.rfind('},{')
        bloco, resto = (s[:ult + 1], s[ult + 2:]) if ult >= 0 else ('', s)
        tot += bloco.count('"contador"')
        for dt, mun, cb in rx.findall(bloco):
            if cb[:1] == 'V' and cb[1:3].isdigit() and 1 <= int(cb[1:3]) <= 89:
                vt['total'] += 1; uf[UF.get(mun[:2], '??')] += 1; mes[dt[2:4]] += 1; grupo[G(cb[:3])] += 1
tot += resto.count('"contador"')
out = {'ano': 2025, 'registros': tot, 'transito': vt['total'], 'uf_ocorrencia': dict(uf), 'mes': dict(sorted(mes.items())), 'vitima': dict(grupo)}
json.dump(out, open('sim_2025_transito.json', 'w'), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False)[:900])
