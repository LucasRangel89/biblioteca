from shot import run
# gaveta de item da lista (claro 1440), com cotação própria -> link "apagar"; depois escuro
passos = [('_', "document.querySelector('#nav [data-ir=precos]').click()", 900),
          ('_', "(() => { const f = document.querySelector('#p-cotacao'); f.querySelector('input[data-c=preco]').value = '31,90'; f.querySelector('[data-c=ok]').click(); })()", 900),
          ('_', "document.querySelector('#p-tab-precos tbody tr').click()", 700)]
e = run(passos + [('gv-claro', None, 300), ('gv-claro-2', "(() => { const c = document.querySelector('#gaveta .gv-c'); c.scrollTop = 420; })()", 400)], w=1440, h=900, full=False)
print('erros:', len(e)); [print(' ', x) for x in e[:10]]
e = run(passos + [('gv-escuro', "(() => { const c = document.querySelector('#gaveta .gv-c'); c.scrollTop = 420; })()", 400)], w=1440, h=900, full=False, tema='dark')
print('erros:', len(e)); [print(' ', x) for x in e[:10]]
