from caminhos import PAINEL_URL, TMP
from relogio import fixa
import sys, json
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
def run(steps, w=1440, h=900, tema=None, full=True, scale=1, url=URL):
    """steps: list of (name, js_or_None, wait_ms). Names starting with '_' take no screenshot."""
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=scale, color_scheme=tema or 'light', locale='pt-BR', timezone_id='America/Sao_Paulo')
        pg = ctx.new_page(); fixa(pg)
        pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
        pg.goto(url); pg.wait_for_timeout(900)
        for name, js, wait in steps:
            if js:
                try:
                    r = pg.evaluate(js)
                    if r is not None: print(f'  {name} ->', json.dumps(r, ensure_ascii=False)[:1500])
                except Exception as e:
                    errs.append(f'[eval {name}] {e}')
            pg.wait_for_timeout(wait)
            if name and not name.startswith('_'):
                pg.screenshot(path=f'{TMP}/shots/{name}.png', full_page=full)
        b.close()
    return errs
