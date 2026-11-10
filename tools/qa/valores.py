"""Leitura de valores digitados: milhar com ponto, decimal com vírgula ou ponto, lixo recusado (formulário de cotação e Novo livro)."""
from caminhos import PAINEL_URL
from relogio import fixa
from playwright.sync_api import sync_playwright
URL = PAINEL_URL
errs = []; falhas = []
TOAST = "() => { const t = [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent); return (t[t.length - 1] || '').replace(/\\u00a0/g, ' '); }"
def confere(nome, ok, extra=''):
    print(('ok   ' if ok else 'FALHA') + ' ' + nome + (' — ' + extra if extra else ''))
    if not ok: falhas.append(nome)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(URL); pg.wait_for_timeout(1000); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    pg.click('#nav [data-ir=precos]'); pg.wait_for_timeout(800)
    f = '#p-cotacao '
    casos = [('1.250', 'R$ 1.250,00'), ('45.90', 'R$ 45,90'), ('R$ 1.234,56', 'R$ 1.234,56'), ('39,9', 'R$ 39,90'), ('72', 'R$ 72,00')]
    for i, (digitado, esperado) in enumerate(casos):
        pg.fill(f + 'input[data-c=preco]', digitado); pg.fill(f + 'input[data-c=data]', f'2026-11-0{i + 2}')
        pg.click(f + '[data-c=ok]'); pg.wait_for_timeout(500)
        t = pg.evaluate(TOAST); confere(f'cotação "{digitado}" → {esperado}', esperado in t, t[:90])
    NQ = "() => document.querySelectorAll('#gaveta.on [data-apagar]').length"
    def cotacoes_do_item():
        # nº de cotações do usuário no item do formulário (links "apagar" na gaveta)
        pg.evaluate("() => { const s = document.querySelector('#p-cotacao select[data-c=livro]'); window.__id = s.value; }")
        return pg.evaluate("() => (document.querySelector('#p-px-loja .card-s') || {}).textContent || ''")
    ref = pg.evaluate("() => [...document.querySelectorAll('#p-px-loja .pr-i')].map(x => x.innerText).join('|')")
    for ruim in ['abc', '12abc', '-5', '1.2.3', '1,2,3']:
        pg.fill(f + 'input[data-c=preco]', ruim); pg.click(f + '[data-c=ok]'); pg.wait_for_timeout(300)
        msg = pg.evaluate("() => { const e = document.querySelector('#p-cotacao .erro-c, #p-cotacao .erro, #p-cotacao [role=alert]'); return e ? e.textContent : ''; }")
        t = pg.evaluate(TOAST); agora = pg.evaluate("() => [...document.querySelectorAll('#p-px-loja .pr-i')].map(x => x.innerText).join('|')")
        confere(f'cotação "{ruim}" recusada com mensagem e sem alterar o resumo', 'válido' in (msg + ' ' + t) and agora == ref, (msg or t)[:90])
    # Novo livro: alvo com milhar
    pg.click('#b-novo'); pg.wait_for_timeout(400)
    pg.fill('#dlg [data-f=t]', 'Zz Obra Completa'); pg.fill('#dlg [data-f=a]', 'Fulano')
    pg.select_option('#dlg [data-f=col]', 'desejo'); pg.fill('#dlg [data-f=alvo]', '1.250'); pg.fill('#dlg [data-f=capa]', '1.499,90')
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
    fatos = pg.evaluate("() => [...document.querySelectorAll('#gaveta.on .fatos > div')].map(d => d.innerText.replace(/\\n/g, ' ').replace(/\\u00a0/g, ' ')).join(' | ')")
    confere('Novo livro: alvo "1.250" = R$ 1.250,00', 'R$ 1.250,00' in fatos, fatos[:200])
    confere('Novo livro: capa "1.499,90" = R$ 1.499,90', 'R$ 1.499,90' in fatos)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    pg.click('#b-novo'); pg.wait_for_timeout(400)
    pg.fill('#dlg [data-f=t]', 'Zz Outro'); pg.select_option('#dlg [data-f=col]', 'desejo'); pg.fill('#dlg [data-f=alvo]', '12x')
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(400)
    aberto = pg.evaluate("() => document.querySelector('#dlg').classList.contains('on')")
    msg = pg.evaluate("() => (document.querySelector('#dlg .erro, #dlg .erro-c, #dlg [role=alert]') || {}).textContent || ''")
    confere('Novo livro: alvo "12x" recusado (diálogo continua aberto)', aberto, msg[:90])
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs)); [print('  ', e[:300]) for e in errs[:10]]
