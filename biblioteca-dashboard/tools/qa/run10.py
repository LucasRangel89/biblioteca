from shot import run
e = run([('_', "document.querySelector('#nav [data-ir=desejos]').click()", 900),
         ('_', "document.querySelector('#p-tab-desejos tbody tr').click()", 600),
         ('_', "document.querySelector('#gaveta [data-acao=comprei]').click()", 500),
         ('_', "document.querySelector('#dlg footer .pri').click()", 900),
         ('gaveta-acervo', None, 300),
         ('gaveta-acervo-2', "(() => { const c = document.querySelector('#gaveta .gv-c'); c.scrollTop = c.scrollHeight; })()", 400)], w=1440, h=900, full=False)
print('erros:', len(e)); [print(' ', x) for x in e[:10]]
