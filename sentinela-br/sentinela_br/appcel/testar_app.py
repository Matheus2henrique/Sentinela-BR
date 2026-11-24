import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1600, 'height': 1000})
        er = []; pg.on('pageerror', lambda e: er.append(str(e))); pg.on('console', lambda m: m.type == 'error' and er.append(m.text))
        await pg.goto('file:///home/claude/sentinela_br/appcel/saida/index.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='/tmp/a1.png')
        await pg.fill('#orig', 'Brasília - DF'); await pg.fill('#dest', 'Boa Vista - RR'); await pg.click('#ver'); await pg.wait_for_timeout(1200); await pg.screenshot(path='/tmp/a2.png')
        print(await pg.evaluate("(()=>{const R=__app.R();return [R.rap.km,R.seg.km,R.rap.crit,R.seg.crit,R.igual]})()"))
        await pg.click('#iniciar'); await pg.wait_for_timeout(9000); await pg.screenshot(path='/tmp/a3.png')
        await pg.wait_for_function("document.getElementById('alerta').classList.contains('on')", timeout=60000); await pg.wait_for_timeout(500); await pg.screenshot(path='/tmp/a4.png')
        await pg.click('#c-fim'); await pg.wait_for_timeout(800); await pg.screenshot(path='/tmp/a5.png')
        await pg.click('.nav button[data-ir=s-info]') if await pg.is_visible('#s-fim .nav') else None
        await pg.evaluate("__app.ir('s-info')"); await pg.wait_for_timeout(400); await pg.screenshot(path='/tmp/a6.png')
        await pg.evaluate("__app.ir('s-inicio')"); await pg.fill('#dest', 'São Paulo - SP'); await pg.click('#ver'); await pg.wait_for_timeout(1200); await pg.screenshot(path='/tmp/a7.png')
        print('ERROS', er[:5]); await b.close()
asyncio.run(main())
