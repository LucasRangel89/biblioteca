from caminhos import PAINEL_URL, TMP
from relogio import fixa
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
URL = PAINEL_URL
def tabelas(w, visoes, nome, tema='light', linhas=7, alto=560):
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': w, 'height': 900}, color_scheme=tema, locale='pt-BR', timezone_id='America/Sao_Paulo')
        pg = ctx.new_page(); fixa(pg); pg.goto(URL); pg.wait_for_timeout(900)
        pg.evaluate("() => document.querySelector('#aviso .pri')?.click()"); pg.wait_for_timeout(200)
        ims = []
        for v in visoes:
            pg.evaluate(f"() => (document.querySelector('#nav-m [data-ir={v}]') && getComputedStyle(document.querySelector('#nav-m')).display !== 'none' ? document.querySelector('#nav-m [data-ir={v}]') : document.querySelector('#nav [data-ir={v}]')).click()"); pg.wait_for_timeout(800)
            box = pg.evaluate(f"() => {{ const r = document.querySelector('#p-tab-{v}').getBoundingClientRect(); return [r.left + scrollX, r.top + scrollY, r.width, r.height]; }}")
            pg.screenshot(path=f'{TMP}/shots/_full.png', full_page=True)
            im = Image.open(f'{TMP}/shots/_full.png').convert('RGB')
            ims.append(im.crop((max(0, int(box[0]) - 6), int(box[1]) - 6, int(box[0] + box[2]) + 6, int(box[1]) + alto)))
        b.close()
    H = sum(i.height for i in ims) + 10 * (len(ims) - 1); W = max(i.width for i in ims)
    out = Image.new('RGB', (W, H), (110, 110, 110)); y = 0
    for i in ims: out.paste(i, (0, y)); y += i.height + 10
    out.save(f'{TMP}/shots/{nome}.png'); print(nome, out.size)
if __name__ == '__main__':
    w = int(sys.argv[1]); tabelas(w, sys.argv[3].split(','), sys.argv[2], alto=int(sys.argv[4]) if len(sys.argv) > 4 else 560)
