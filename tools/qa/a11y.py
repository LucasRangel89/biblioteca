"""Auditoria rápida de acessibilidade em tempo de execução: ids duplicados, controles sem nome acessível, campos sem rótulo,
contraste de texto (WCAG AA) em todos os temas, medido com a tela assentada (depois das animações de entrada),
alvos de toque pequenos no celular.

No tema padrão (claro e escuro), cada tela é auditada duas vezes: com os dados de exemplo (gráficos e tabelas cheios) e
como o painel abre, só com o catálogo — é aí que aparecem os estados vazios, as abas sem nenhum livro e as linhas zeradas.
Cada um dos outros temas (os que estão em TEMAS, em src/js/30-state.js) passa pelas mesmas telas: no computador com os
dados de exemplo, e no celular só com o catálogo. Tema novo entra na auditoria sozinho.

Para auditar só alguns temas:  python a11y.py lovecraft holmes"""
from caminhos import PAINEL_LIMPO, PAINEL_URL, RAIZ
from relogio import fixa
from playwright.sync_api import sync_playwright
import re, sys
URL = PAINEL_URL
# os temas que não são o padrão, lidos de onde o painel os define
TEMAS = [t for t in re.findall(r"\{ id: '(\w+)', n: '", (RAIZ / 'src' / 'js' / '30-state.js').read_text(encoding='utf-8')) if t not in ('claro', 'escuro')]
assert len(TEMAS) >= 3, TEMAS
EXEMPLO, LIMPO = ('exemplo', URL), ('limpo', PAINEL_LIMPO)
CENARIOS = [(w, h, esquema, '', (EXEMPLO, LIMPO)) for w, h, esquema in [(1440, 900, 'light'), (1440, 900, 'dark'), (390, 844, 'light'), (390, 844, 'dark')]]
for t in TEMAS: CENARIOS += [(1440, 900, 'light', t, (EXEMPLO,)), (390, 844, 'light', t, (LIMPO,))]
if len(sys.argv) > 1: CENARIOS = [c for c in CENARIOS if c[3] in sys.argv[1:]]
AUD = r"""() => {
  const vis = e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden'; };
  const out = { ids: [], semNome: [], semRotulo: [] };
  const ids = {}; for (const e of document.querySelectorAll('[id]')) ids[e.id] = (ids[e.id] || 0) + 1;
  out.ids = Object.keys(ids).filter(k => ids[k] > 1);
  const nome = e => (e.getAttribute('aria-label') || '').trim() || (e.getAttribute('aria-labelledby') ? (document.getElementById(e.getAttribute('aria-labelledby').split(' ')[0]) || {}).textContent || '' : '').trim() || (e.textContent || '').trim() || (e.getAttribute('title') || '').trim();
  for (const e of document.querySelectorAll('button, a[href], [role=button], [role=tab]')) if (vis(e) && !nome(e)) out.semNome.push(e.outerHTML.slice(0, 120));
  for (const e of document.querySelectorAll('input:not([type=hidden]):not([type=file]), select, textarea')) {
    if (!vis(e)) continue;
    const rot = e.getAttribute('aria-label') || e.getAttribute('aria-labelledby') || (e.id && document.querySelector('label[for="' + e.id + '"]')) || e.closest('label');
    if (!rot) out.semRotulo.push(e.outerHTML.slice(0, 120));
  }
  return out;
}"""
CONTRASTE = r"""async () => {
  // Mede a tela assentada, não o meio de uma animação de entrada: a opacidade passageira de `.visao.entra`
  // misturava texto e fundo e podia derrubar um par aprovado (ex.: "Atualizado" no escuro, 4,48 em vez de 5,26).
  // Esperar o fim das animações/transições mantém a conta da opacidade real, sem abrir exceção no limite AA.
  await Promise.all(document.getAnimations().map(a => a.finished.catch(() => {})));
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', { willReadFrequently: true });
  const rgba = s => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = s; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
  const sobre = (a, b) => [0, 1, 2].map(i => a[i] * a[3] + b[i] * (1 - a[3])).concat([1]);
  const fundo = e => { let pilha = []; for (let n = e; n && n.nodeType === 1; n = n.parentElement) { const cs = getComputedStyle(n); if (cs.backgroundImage && cs.backgroundImage !== 'none') return null; const c = rgba(cs.backgroundColor); if (c[3] > 0) { pilha.push(c); if (c[3] >= 0.999) break; } } let base = [255, 255, 255, 1]; for (let i = pilha.length - 1; i >= 0; i--) base = sobre(pilha[i], base); return base; };
  const ruins = {}; let n = 0;
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const t = w.currentNode, txt = t.textContent.trim(); if (!txt) continue;
    const e = t.parentElement; if (!e || e.closest('svg, [hidden], script, style, .so-leitor')) continue;
    const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || +cs.opacity === 0) continue;
    let op = 1; for (let x = e; x && x.nodeType === 1; x = x.parentElement) op *= +getComputedStyle(x).opacity; 
    const bg = fundo(e); if (!bg) continue;
    let fg = rgba(cs.color); fg = sobre([fg[0], fg[1], fg[2], fg[3] * op], bg);
    const l1 = lum(fg), l2 = lum(bg), razao = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    const tam = parseFloat(cs.fontSize), peso = +cs.fontWeight || 400, grande = tam >= 24 || (tam >= 18.66 && peso >= 700), min = grande ? 3 : 4.5;
    n++;
    if (razao < min - 0.005) { const desab = e.closest('button:disabled, [aria-disabled=true], .off, [disabled]'); const k = (desab ? '(desativado) ' : '') + (e.className && typeof e.className === 'string' ? e.tagName.toLowerCase() + '.' + e.className.split(' ').slice(0, 2).join('.') : e.tagName.toLowerCase()) + ' ' + cs.color + ' em ' + 'rgb(' + bg.slice(0, 3).map(Math.round).join(',') + ')'; if (!ruins[k] || razao < ruins[k].r) ruins[k] = { r: +razao.toFixed(2), ex: txt.slice(0, 30), tam, peso }; }
  }
  return { n, ruins };
}"""
TOQUE = "() => [...document.querySelectorAll('button, a[href], select, input:not([type=hidden]):not([type=file]), [role=button]')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden' && (r.width < 24 || r.height < 24) && !e.closest('.so-leitor'); }).map(e => (e.id || e.className || e.tagName) + ' ' + Math.round(e.getBoundingClientRect().width) + 'x' + Math.round(e.getBoundingClientRect().height)).filter((v, i, a) => a.indexOf(v) === i).slice(0, 12)"
achados = {}
def junta(rot, r):
    for k in ('ids', 'semNome', 'semRotulo'):
        if r[k]: achados.setdefault(k, {})[rot] = r[k][:6]
with sync_playwright() as p:
    b = p.chromium.launch()
    # cada tamanho e tema: com os dados de exemplo (telas cheias) e como o painel abre (só o catálogo: telas vazias)
    for w, h, esquema, tema_id, modos in CENARIOS:
      tema = tema_id or esquema
      for modo, url in modos:
        ctx = b.new_context(viewport={'width': w, 'height': h}, color_scheme=esquema, locale='pt-BR', timezone_id='America/Sao_Paulo')
        pg = ctx.new_page(); fixa(pg)
        pg.on('pageerror', lambda e: achados.setdefault('pageerror', {}).update({str(e)[:80]: 1}))
        pg.goto(url); pg.wait_for_timeout(1000)
        if tema_id:                         # o tema é escolhido como o usuário escolhe: pelo quadro da paleta
            pg.click('#b-tema'); pg.wait_for_timeout(200); pg.click(f'#pop-tema [data-tema-id={tema_id}]'); pg.wait_for_timeout(500); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
            if pg.evaluate("() => document.documentElement.dataset.tema") != tema_id: achados.setdefault('tema', {})[tema_id] = 'não foi aplicado'
        nav = '#nav' if w > 820 else '#nav-m'; contr = {}; tot = 0; R = f'{w}{tema}{"" if modo == "exemplo" else "-limpo"}'
        def contraste(rot):
            global tot
            c = pg.evaluate(CONTRASTE)
            for k, v in c['ruins'].items():
                if k not in contr or v['r'] < contr[k][0]['r']: contr[k] = (v, rot)
            return c['n']
        def camada(rot, abrir, fechar=True):
            """Abre uma camada (gaveta, diálogo, folha), audita e fecha."""
            abrir(); pg.wait_for_timeout(600); junta(f'{R}/{rot}', pg.evaluate(AUD)); m = contraste(rot)
            if fechar: pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
            return m
        junta(f'{R}/aviso', pg.evaluate(AUD)); n = contraste('aviso')
        pg.click('#aviso .pri'); pg.wait_for_timeout(200)
        for v in ['geral', 'biblioteca', 'recs', 'financas', 'desejos', 'precos']:
            pg.evaluate(f"() => document.querySelector('{nav} [data-ir={v}]').click()"); pg.wait_for_timeout(900)
            junta(f'{R}/{v}', pg.evaluate(AUD)); n += contraste(v)
            if w <= 820 and tema == 'light':
                t = pg.evaluate(TOQUE)
                if t: achados.setdefault('toque<24', {})[f'{v}{"" if modo == "exemplo" else "-limpo"}'] = t
        if modo == 'exemplo':               # um item da lista de compra: gaveta, cotação e edição
            pg.evaluate(f"() => document.querySelector('{nav} [data-ir=desejos]').click()"); pg.wait_for_timeout(700)
            n += camada('gaveta', lambda: pg.click('#p-tab-desejos tbody tr'), fechar=False)
            n += camada('dlg-cotar', lambda: pg.click('#gaveta [data-acao=cotar]'))
            n += camada('dlg-editar', lambda: pg.click('#gv-acoes [data-acao=editar]'))
        else:                               # um livro do acervo sem nada registrado: gaveta, "Já li" (com "Terminei hoje") e edição
            pg.evaluate(f"() => document.querySelector('{nav} [data-ir=biblioteca]').click()"); pg.wait_for_timeout(700)
            n += camada('gaveta', lambda: pg.click('#p-tab-biblioteca tbody tr[data-id]'), fechar=False)
            n += camada('dlg-lido', lambda: pg.click('#gv-acoes [data-acao=lido]'))
            n += camada('dlg-editar', lambda: pg.click('#gv-acoes [data-acao=editar]'))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        n += camada('dlg-novo', lambda: pg.click('#b-novo'))
        n += camada('dlg-dados', lambda: pg.click('#b-dados'))
        n += camada('temas', lambda: pg.click('#b-tema'))
        if w <= 820: n += camada('folha', lambda: pg.click('#f-abrir'))
        else: n += camada('mais-filtros', lambda: pg.click('#pw-mais .pop-b'))
        print(f'== {w}px {tema} · {"com exemplos" if modo == "exemplo" else "só o catálogo"}: {n} textos medidos; abaixo de AA: {len(contr)}')
        for k, (v, rot) in sorted(contr.items(), key=lambda kv: kv[1][0]['r']): print(f'   {v["r"]:>5}  {k}  [{rot}] “{v["ex"]}” {v["tam"]}px/{v["peso"]}')
        # as estrelas da nota são desenho (a nota vai no aria-label): vazias são decorativas, cheias precisam de 3:1
        for k, (v, rot) in contr.items():
            if v['ex'] == '★' and (k.startswith('i ') or (k.startswith('i.on ') and v['r'] >= 3)): continue
            achados.setdefault('contraste', {})[f'{R} {k}'] = v['r']
        ctx.close()
    b.close()
print('ACHADOS:'); [print('  ', k, v) for k, v in achados.items()]
print('FALHAS:', sorted(achados.keys()))
print('ERROS:', len(achados.get('pageerror', {})))
