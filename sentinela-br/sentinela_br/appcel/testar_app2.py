import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for vw, vh in [(1920, 1080), (1366, 768)]:
            pg = await b.new_page(viewport={'width': vw, 'height': vh}); er = []
            pg.on('pageerror', lambda e: er.append(str(e))); pg.on('console', lambda m: m.type == 'error' and er.append(m.text))
            await pg.goto('file:///home/claude/sentinela_br/appcel/saida/index.html'); await pg.wait_for_timeout(1200)
            print(vw, 'origem vazia:', repr(await pg.input_value('#orig')))
            await pg.click('#orig'); await pg.wait_for_timeout(500)
            n = await pg.evaluate("document.querySelectorAll('#l-orig .it').length"); print('itens ao clicar:', n)
            await pg.screenshot(path=f'/tmp/m_{vw}_1.png')
            await pg.type('#orig', 'sao jose', delay=30); await pg.wait_for_timeout(300)
            print('filtro "sao jose":', await pg.evaluate("document.querySelectorAll('#l-orig .it').length"))
            await pg.screenshot(path=f'/tmp/m_{vw}_2.png')
            await pg.click('#l-orig .it[data-k]'); print('origem:', await pg.input_value('#orig'))
            await pg.click('#dest'); await pg.type('#dest', 'oiapoque', delay=30); await pg.keyboard.press('Enter'); print('destino:', await pg.input_value('#dest'))
            await pg.click('#ver'); await pg.wait_for_timeout(1500); await pg.screenshot(path=f'/tmp/m_{vw}_3.png')
            print('erro:', await pg.text_content('#erro'), '| rota:', await pg.evaluate("(()=>{const R=__app.R();return R?[Math.round(R.rap.km),Math.round(R.seg.km)]:null})()"))
            print('ERROS', er[:5]); await pg.close()
        # teste em massa de pares aleatórios
        pg = await b.new_page(); await pg.goto('file:///home/claude/sentinela_br/appcel/saida/index.html'); await pg.wait_for_timeout(1000)
        r = await pg.evaluate("""(()=>{let ok=0,falha=0,ex=[];for(let k=0;k<60;k++){const a=Math.floor(Math.random()*5571),c=Math.floor(Math.random()*5571);const A=D_m(a),C=D_m(c);if(A.i===C.i)continue;try{const R=__app.rotas(A.i,C.i);if(R)ok++;else{falha++;ex.push(A.nome+'-'+C.nome)}}catch(e){falha++;ex.push(String(e))}}return [ok,falha,ex.slice(0,5)]})()""".replace('D_m', '(k=>MUNS[k])')) if False else None
        await b.close()
asyncio.run(main())
