from shot import run
e = run([('_', "document.querySelector('#aviso .pri').click()", 300), ('t820-geral', None, 500)], w=820, h=1000)
print('820 erros:', len(e)); [print(' ', x) for x in e[:10]]
e = run([('_', "document.querySelector('#aviso .pri').click()", 300), ('t600-desejos', "document.querySelector('#nav-m [data-ir=desejos]').click()", 1100)], w=600, h=900)
print('600 erros:', len(e)); [print(' ', x) for x in e[:10]]
e = run([('_', "document.querySelector('#aviso .pri').click()", 300),
         ('_', "document.querySelector('#nav-m [data-ir=desejos]').click()", 900),
         ('m-gaveta', "document.querySelector('#p-tab-desejos tbody tr').click()", 800),
         ('m-gaveta-2', "(() => { const c = document.querySelector('#gaveta .gv-c'); c.scrollTop = c.scrollHeight; })()", 400),
         ('m-dlg-comprei', "document.querySelector('#gaveta [data-acao=comprei]').click()", 600),
         ('_', "document.querySelector('#dlg header [data-fechar]').click()", 400),
         ('_', "document.querySelector('#gaveta [data-fechar]').click()", 500),
         ('m-dlg-novo', "document.querySelector('#b-novo').click()", 700),
         ('_', "document.querySelector('#dlg header [data-fechar]').click()", 400),
         ('m-busca', "(() => { document.querySelector('#busca-b, [data-busca], .b-busca')?.click(); })()", 500),
        ], w=390, h=844, full=False)
print('390 erros:', len(e)); [print(' ', x) for x in e[:10]]
e = run([('_', "document.querySelector('#aviso .pri').click()", 300), ('_', "document.querySelector('#pop-tema [data-tema-id=escuro]').click()", 400),
         ('md-geral', None, 500), ('md-gaveta', "document.querySelector('#p-ranking .li').click()", 800)], w=390, h=844, full=False)
print('390 escuro erros:', len(e)); [print(' ', x) for x in e[:10]]
