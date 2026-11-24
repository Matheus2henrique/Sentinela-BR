import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1600, 'height': 1000})
        erros = []; pg.on('pageerror', lambda e: erros.append(str(e))); pg.on('console', lambda m: m.type == 'error' and erros.append(m.text))
        await pg.goto('file:///home/claude/sentinela_br/p6/saida/index.html'); await pg.wait_for_timeout(2500)
        await pg.evaluate("document.getElementById('alerta').hidden=true")
        await pg.click('.seg button[data-m=dono]'); await pg.wait_for_timeout(800)
        m = await pg.query_selector('#mapa'); await m.scroll_into_view_if_needed(); await pg.wait_for_timeout(400)
        await pg.screenshot(path='/tmp/d_mapa.png')
        t = await pg.query_selector('#o-kpi'); await t.scroll_into_view_if_needed(); await pg.wait_for_timeout(300); await pg.screenshot(path='/tmp/d_tab.png')
        await pg.click('#o-corpo tr[data-g^="c:"]'); await pg.wait_for_timeout(800)
        print(await pg.evaluate("document.getElementById('resumoF').textContent"), await pg.evaluate("document.getElementById('f-gestor').selectedOptions[0].textContent"))
        await m.scroll_into_view_if_needed(); await pg.screenshot(path='/tmp/d_filtro.png')
        await pg.evaluate("__sentinela.irPara('ranking')"); await pg.wait_for_timeout(500)
        await pg.click('#top30 .tc'); await pg.wait_for_timeout(600); await pg.screenshot(path='/tmp/d_gaveta.png')
        print(await pg.evaluate("document.querySelector('#g-corpo .sub').textContent"))
        print('ERROS:', erros[:8]); await b.close()
asyncio.run(main())
