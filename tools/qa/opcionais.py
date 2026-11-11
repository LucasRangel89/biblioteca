"""Só o título é obrigatório: livro sem data de aquisição, compra sem valor e leitura sem data.

O painel é aberto como o usuário o abre (sem dados de exemplo). Confere que:
  · um livro novo entra só com o título; sem título, o formulário avisa e não fecha;
  · "Já tenho" e "Comprei" aceitam data, loja e valor em branco — e continuam recusando valor ilegível e data futura;
  · "Já li" não inventa a data de hoje: em branco, a leitura conta no total e fica fora dos recortes por período;
  · "Terminei hoje" preenche a data; apagar uma data ao editar o livro funciona;
  · nada disso se perde ao recarregar nem num backup exportado e importado de volta.
"""
from caminhos import PAINEL_LIMPO, TMP
from relogio import fixa
import json
from playwright.sync_api import sync_playwright

CHAVE = 'biblioteca-lucas:v1'
errs = []; falhas = []
K = "() => Object.fromEntries([...document.querySelectorAll('.visao:not([hidden]) .kpi')].map(k => [k.dataset.k, {v: k.querySelector('.kpi-v b').textContent.replace(/\\u00a0/g, ' '), s: k.querySelector('.kpi-s').textContent.replace(/\\u00a0/g, ' ')}]))"
TOAST = "() => { const t = [...document.querySelectorAll('#toasts .toast')].map(t => t.textContent.replace(/\\u00a0/g, ' ')); return t[t.length - 1] || ''; }"
FATOS = "() => Object.fromEntries([...document.querySelectorAll('#gaveta .fatos > div')].map(d => [d.querySelector('dt').textContent, d.querySelector('dd').innerText.replace(/\\u00a0/g, ' ').replace(/\\s+/g, ' ').trim()]))"
CAMPOS = "() => Object.fromEntries([...document.querySelectorAll('#dlg.on [data-f]')].filter(x => x.offsetParent).map(x => [x.dataset.f, x.value]))"
OPCIONAIS = "() => [...document.querySelectorAll('#dlg.on label.cp')].filter(l => l.offsetParent && l.querySelector('small') && l.querySelector('small').textContent.trim() === 'opcional').map(l => l.querySelector('[data-f]').dataset.f)"
# o campo recusado fica marcado (classe "erro") e o motivo sai num aviso: devolve "campo: motivo", ou '' se nenhum campo foi recusado
ERRO = "() => { const e = document.querySelector('#dlg.on [data-f].erro'), t = [...document.querySelectorAll('#toasts .toast')].map(x => x.textContent); return e ? e.dataset.f + ': ' + (t[t.length - 1] || '') : ''; }"
DLG = "() => document.querySelector('#dlg').classList.contains('on') ? document.querySelector('#dlg h2').textContent : ''"
HOJE = '2026-11-09'


def ok(nome, cond, extra=''):
    print(('  ok   ' if cond else '  FALHA') + ' ' + nome + (' — ' + str(extra) if extra != '' else ''))
    if not cond: falhas.append(nome)


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo', accept_downloads=True)
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)

    def ir(v): pg.keyboard.press('Escape'); pg.wait_for_timeout(150); pg.click(f'#nav [data-ir={v}]'); pg.wait_for_timeout(900); return pg.evaluate(K)
    def abrir(busca, titulo):
        """Abre a gaveta do livro pela tabela da visão geral."""
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        if not pg.is_visible('#p-tab-geral'): pg.click('#nav [data-ir=geral]'); pg.wait_for_timeout(800)
        pg.fill('#p-tab-geral input[type=search]', busca); pg.wait_for_timeout(600)
        pg.locator('#p-tab-geral tbody tr[data-id]').filter(has=pg.locator('.tt b', has_text=titulo)).first.click(); pg.wait_for_timeout(700)
    def acao(a): pg.click(f'#gv-acoes [data-acao={a}]'); pg.wait_for_timeout(500)
    def confirma(): pg.click('#dlg footer .pri'); pg.wait_for_timeout(800)
    def periodo(v):
        if not pg.is_visible('#pop-mais'): pg.click('#pw-mais .pop-b'); pg.wait_for_timeout(250)
        pg.click(f'#f-periodo button[data-v="{v}"]'); pg.wait_for_timeout(800); k = pg.evaluate(K); pg.keyboard.press('Escape'); pg.wait_for_timeout(200); return k
    guardado = lambda titulo: pg.evaluate("t => (JSON.parse(localStorage.getItem('%s')).livros.find(x => x.t === t) || null)" % CHAVE, titulo)

    k0 = ir('geral')
    ok('ponto de partida: 2.124 no acervo, 3 leituras, 487 recomendações na fila', (k0['acervo']['v'], k0['leituras']['v'], k0['recs']['v']) == ('2.124', '3', '487'), {a: k0[a]['v'] for a in k0})

    print('LIVRO NOVO: SÓ O TÍTULO')
    pg.click('#b-novo'); pg.wait_for_timeout(500)
    nota = pg.inner_text('#dlg .form-n.ini')
    ok('o formulário diz que só o título é obrigatório', 'Só o título é obrigatório' in nota and 'opcional' in nota, nota)
    ok('o campo do título é o único marcado como obrigatório', pg.evaluate("() => [...document.querySelectorAll('#dlg.on [aria-required=true], #dlg.on [required]')].map(x => x.dataset.f)") == ['t'])
    pg.select_option('#dlg [data-f=col]', 'acervo'); pg.wait_for_timeout(200)
    op = pg.evaluate(OPCIONAIS); ok('as datas de aquisição e de leitura trazem a palavra "opcional"', 'adq' in op and 'lidoEm' in op, op)
    confirma()
    ok('sem título: o formulário avisa e continua aberto', pg.evaluate(DLG) == 'Novo livro' and pg.evaluate(ERRO) == 't: Informe o título do livro.', (pg.evaluate(DLG), pg.evaluate(ERRO)))
    pg.fill('#dlg [data-f=t]', 'Zz Livro Só com Título'); confirma()
    f = pg.evaluate(FATOS)
    ok('com o título e mais nada: o livro entra no acervo', pg.evaluate(TOAST) == 'Livro adicionado.' and pg.evaluate(DLG) == '' and pg.inner_text('#gaveta.on h2').strip() == 'Zz Livro Só com Título', (pg.evaluate(TOAST), pg.evaluate(DLG)))
    ok('a ficha mostra "sem data" e nenhum valor inventado', f.get('Adquirido em') == 'sem data' and f.get('Valor pago', '') == '' and 'R$' not in ' '.join(f.values()), f)
    g = guardado('Zz Livro Só com Título')
    ok('o que foi guardado não tem data, valor nem loja', g is not None and all(g.get(c) in (None, '', 0) for c in ('adq', 'pago', 'loja', 'lidoEm')), g)
    k = ir('geral'); ok('o acervo passou a 2.125', k['acervo']['v'] == '2.125', k['acervo'])
    k = ir('financas'); ok('nenhum gasto apareceu: investido R$ 0, preço médio "—"', k['investido']['v'] == 'R$ 0' and k['medio']['v'] == '—', (k['investido'], k['medio']))

    print('"JÁ TENHO": SEM DATA, SEM LOJA, SEM VALOR')
    abrir('Ensaio sobre a Cegueira Saramago', 'Ensaio sobre a Cegueira'); acao('tenho')
    c = pg.evaluate(CAMPOS); op = pg.evaluate(OPCIONAIS)
    ok('abre com data, loja e valor em branco e a condição "Não informada"', pg.evaluate(DLG) == 'Já tenho este livro' and (c.get('adq'), c.get('loja'), c.get('pago'), c.get('cond')) == ('', '', '', ''), c)
    ok('data, loja, valor e condição marcados como opcionais', op == ['adq', 'loja', 'pago', 'cond'], op)
    confirma(); f = pg.evaluate(FATOS)
    ok('confirmar sem preencher nada: entra no acervo, sem data', pg.evaluate(TOAST) == 'Adicionado ao acervo.' and f.get('Adquirido em') == 'sem data' and f.get('Valor pago', '') == '', (pg.evaluate(TOAST), f))
    k = ir('geral'); ok('acervo 2.126; a recomendação saiu da fila (486)', k['acervo']['v'] == '2.126' and k['recs']['v'] == '486', (k['acervo']['v'], k['recs']['v']))
    ir('financas')
    ok('sem valor e sem loja, o livro não aparece nas compras registradas', pg.inner_text('#p-tab-financas .tb-info').strip() == 'Nenhum livro', pg.inner_text('#p-tab-financas .tb-info'))

    print('"COMPREI": A DATA VEM PREENCHIDA, MAS PODE SER APAGADA')
    abrir('Nome da Rosa Eco', 'O Nome da Rosa'); acao('desejar'); acao('comprei')
    c = pg.evaluate(CAMPOS)
    ok('abre com a data de hoje sugerida', pg.evaluate(DLG) == 'Registrar compra' and c.get('adq') == HOJE, c)
    pg.fill('#dlg [data-f=pago]', 'quarenta'); confirma()
    ok('valor ilegível: avisa e não fecha', pg.evaluate(DLG) == 'Registrar compra' and pg.evaluate(ERRO).startswith('pago: Informe um valor válido'), pg.evaluate(ERRO))
    pg.fill('#dlg [data-f=pago]', ''); pg.fill('#dlg [data-f=adq]', '2031-01-01'); confirma()
    ok('data futura: avisa e não fecha', pg.evaluate(DLG) == 'Registrar compra' and pg.evaluate(ERRO) == 'adq: A data não pode estar no futuro.', pg.evaluate(ERRO))
    pg.fill('#dlg [data-f=adq]', ''); pg.fill('#dlg [data-f=loja]', 'Sebo da Esquina'); confirma(); f = pg.evaluate(FATOS)
    ok('data apagada e só a loja informada: a compra é registrada sem data e sem valor', pg.evaluate(TOAST) == 'Adicionado ao acervo.' and f.get('Adquirido em') == 'sem data' and f.get('Valor pago', '') == '' and 'Sebo da Esquina' in ' '.join(f.values()), f)
    ir('financas')
    abas = pg.evaluate("() => Object.fromEntries([...document.querySelectorAll('#p-tab-financas .abas [data-a]')].map(a => [a.dataset.a, a.querySelector('.cont').textContent.trim()]))")
    k = pg.evaluate(K)
    ok('a compra aparece em Finanças na aba "Sem valor", e o investido continua R$ 0', abas == {'todos': '1', 'pagas': '0', 'gratis': '0', 'semvalor': '1'} and k['investido']['v'] == 'R$ 0', (abas, k['investido']))
    abrir('Guerra e Paz Tolstói', 'Guerra e Paz'); acao('editar')
    pg.fill('#dlg [data-f=pago]', '35,5'); confirma(); k = ir('financas')
    ok('valor sem data: entra no investido (R$ 36) e no preço médio', k['investido']['v'] == 'R$ 36' and k['medio']['v'] == 'R$ 35,50', (k['investido'], k['medio']))
    k = periodo('12m'); ok('…mas, sem data, fica fora do recorte de 12 meses', k['investido']['v'] == 'R$ 0', k['investido'])
    periodo('tudo')

    print('"JÁ LI": SEM DATA')
    abrir('Peste Camus', 'A Peste'); acao('lido')
    c = pg.evaluate(CAMPOS); op = pg.evaluate(OPCIONAIS)
    ok('a data da leitura abre em branco (não vem "hoje")', pg.evaluate(DLG) == 'Concluir leitura' and c.get('em') == '', c)
    ok('data e nota marcadas como opcionais', op == ['em', 'nota'], op)
    confirma(); f = pg.evaluate(FATOS)
    ok('leitura concluída sem data', pg.evaluate(TOAST) == 'Leitura concluída.' and f.get('Leitura') == 'Lido' and f.get('Concluído em') == 'sem data', f)
    k = ir('geral'); ok('a leitura sem data conta: 4 leituras', k['leituras']['v'] == '4', k['leituras'])
    k = periodo('12m'); ok('…e fica fora do recorte de 12 meses', k['leituras']['v'] == '0', k['leituras'])
    periodo('tudo')
    ir('biblioteca')
    lidos = pg.evaluate("() => document.querySelector('#p-tab-biblioteca .abas [data-a=lido] .cont').textContent.trim()")
    ok('na Biblioteca, a aba "Lidos" conta o livro', lidos == '1', lidos)

    print('"TERMINEI HOJE"')
    abrir('Cavernas de Aço Asimov', 'As Cavernas de Aço'); acao('lido')
    pg.click('#dlg [data-hoje]'); pg.wait_for_timeout(200); c = pg.evaluate(CAMPOS)
    ok('o botão preenche a data de hoje', c.get('em') == HOJE, c)
    confirma(); f = pg.evaluate(FATOS)
    ok('a leitura fica com a data', f.get('Concluído em') == '09/11/2026', f)
    k = ir('geral'); ok('5 leituras no total', k['leituras']['v'] == '5', k['leituras'])
    k = periodo('30d'); ok('…e 1 nos últimos 30 dias', k['leituras']['v'] == '1', k['leituras'])
    periodo('tudo')
    # reler e concluir de novo: a data que o livro já tinha vem no campo (confirmar sem mexer não apaga o que se sabia)
    abrir('Cavernas de Aço Asimov', 'As Cavernas de Aço'); acao('ler'); acao('lido'); c = pg.evaluate(CAMPOS)
    ok('reler e concluir de novo: o campo traz a data que o livro já tinha', pg.evaluate(DLG) == 'Concluir leitura' and c.get('em') == HOJE, c)
    confirma(); f = pg.evaluate(FATOS)
    ok('confirmar sem mexer mantém a data', f.get('Leitura') == 'Lido' and f.get('Concluído em') == '09/11/2026', f)

    print('EDITAR: APAGAR UMA DATA; DATA FUTURA')
    acao('editar'); pg.fill('#dlg [data-f=lidoEm]', ''); pg.fill('#dlg [data-f=adq]', '2020-03-15'); confirma(); f = pg.evaluate(FATOS)
    ok('apagar a data da leitura e pôr a de aquisição', pg.evaluate(TOAST) == 'Alterações salvas.' and f.get('Concluído em') == 'sem data' and f.get('Adquirido em') == '15/03/2020' and f.get('Leitura') == 'Lido', f)
    acao('editar'); pg.fill('#dlg [data-f=adq]', '2031-01-01'); confirma()
    ok('data de aquisição no futuro: avisa e não fecha', pg.evaluate(DLG) == 'Editar livro' and pg.evaluate(ERRO) == 'adq: A data não pode estar no futuro.', (pg.evaluate(DLG), pg.evaluate(ERRO)))
    pg.fill('#dlg [data-f=adq]', ''); pg.fill('#dlg [data-f=lidoEm]', '2031-01-01'); confirma()
    ok('data de leitura no futuro: avisa e não fecha', pg.evaluate(DLG) == 'Editar livro' and pg.evaluate(ERRO) == 'lidoEm: A data não pode estar no futuro.', (pg.evaluate(DLG), pg.evaluate(ERRO)))
    pg.fill('#dlg [data-f=lidoEm]', ''); confirma(); f = pg.evaluate(FATOS)
    ok('com as duas datas apagadas, salva', pg.evaluate(TOAST) == 'Alterações salvas.' and f.get('Adquirido em') == 'sem data' and f.get('Concluído em') == 'sem data', f)

    print('RECARREGAR E BACKUP')
    antes = {v: ir(v) for v in ('geral', 'biblioteca', 'financas')}
    pg.wait_for_timeout(700); pg.reload(); pg.wait_for_timeout(1300)
    depois = {v: ir(v) for v in ('geral', 'biblioteca', 'financas')}
    ok('ao recarregar, os indicadores são os mesmos', antes == depois, {v: {a: depois[v][a]['v'] for a in depois[v]} for v in depois})
    ok('visão geral: 2.127 no acervo, 5 leituras', depois['geral']['acervo']['v'] == '2.127' and depois['geral']['leituras']['v'] == '5', {a: depois['geral'][a]['v'] for a in depois['geral']})
    pg.click('#b-dados'); pg.wait_for_timeout(400)
    with pg.expect_download() as d: pg.click('#dlg [data-x=exportar]')
    d.value.save_as(f'{TMP}/opcionais-backup.json'); bk = json.load(open(f'{TMP}/opcionais-backup.json', encoding='utf-8'))
    meus = {x['t']: x for x in bk['livros'] if x.get('u')}
    ok('o backup traz os seis livros mexidos', sorted(meus) == ['A Peste', 'As Cavernas de Aço', 'Ensaio sobre a Cegueira', 'Guerra e Paz', 'O Nome da Rosa', 'Zz Livro Só com Título'], sorted(meus))
    ok('no backup: leitura sem data, compra sem valor, exemplos desligados', meus.get('A Peste', {}).get('leit') == 'lido' and 'lidoEm' not in meus.get('A Peste', {}) and 'pago' not in meus.get('O Nome da Rosa', {}) and meus.get('O Nome da Rosa', {}).get('loja') == 'Sebo da Esquina' and bk.get('exemplos') is False and 'demo' not in bk,
       {t: {c: meus[t].get(c) for c in ('leit', 'lidoEm', 'adq', 'pago', 'loja')} for t in meus})
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    pg.context.close()

    # o backup importado num navegador que nunca viu o painel
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, locale='pt-BR', timezone_id='America/Sao_Paulo')
    pg = ctx.new_page(); fixa(pg)
    pg.on('console', lambda m: errs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append(f'[pageerror] {e}'))
    pg.goto(PAINEL_LIMPO); pg.wait_for_timeout(1200); pg.click('#aviso .pri'); pg.wait_for_timeout(200)
    pg.click('#b-dados'); pg.wait_for_timeout(400); pg.set_input_files('#arq', f'{TMP}/opcionais-backup.json'); pg.wait_for_timeout(800)
    pg.click('#dlg footer .pri'); pg.wait_for_timeout(1200)
    for _ in range(2): pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
    importado = {v: ir(v) for v in ('geral', 'biblioteca', 'financas')}
    ok('importado em outro navegador, dá os mesmos indicadores', importado == depois, {v: {a: importado[v][a]['v'] for a in importado[v]} for v in importado})
    abrir('Peste Camus', 'A Peste'); f = pg.evaluate(FATOS)
    ok('e a leitura sem data continua sem data', f.get('Leitura') == 'Lido' and f.get('Concluído em') == 'sem data', f)
    b.close()
print('FALHAS:', falhas); print('ERROS:', len(errs) + len(falhas)); [print('  ', x[:300]) for x in errs[:10]]
