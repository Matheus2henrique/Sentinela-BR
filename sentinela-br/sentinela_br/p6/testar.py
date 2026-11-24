import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1600, 'height': 1000})
        erros = []; pg.on('pageerror', lambda e: erros.append(str(e))); pg.on('console', lambda m: m.type == 'error' and erros.append(m.text))
        await pg.goto('file:///home/claude/sentinela_br/p6/saida/index.html'); await pg.wait_for_timeout(2500)
        await pg.screenshot(path='/tmp/p6_alerta.png')
        await pg.evaluate("document.getElementById('alerta').hidden=true")
        await pg.screenshot(path='/tmp/p6_visao.png', full_page=True)
        for v in ['ranking', 'plano', 'clima', 'app', 'fontes']:
            await pg.evaluate(f"__sentinela.irPara('{v}')"); await pg.wait_for_timeout(700); await pg.screenshot(path=f'/tmp/p6_{v}.png', full_page=True)
        await pg.select_option('#f-uf', 'MG'); await pg.wait_for_timeout(500)
        await pg.evaluate("__sentinela.irPara('ranking')"); await pg.wait_for_timeout(500)
        await pg.click('#top30 .tc'); await pg.wait_for_timeout(600); await pg.screenshot(path='/tmp/p6_gaveta.png')
        print(await pg.evaluate("document.getElementById('resumoF').textContent"))
        await pg.click('#limpar'); await pg.wait_for_timeout(500); print(await pg.evaluate("document.getElementById('resumoF').textContent"))
        print('ERROS:', erros[:8]); await b.close()
asyncio.run(main())
