from shot import run
e = run([('_', "document.querySelector('#pop-tema [data-tema-id=escuro]').click()", 500), ('d-geral', None, 600),
         ('d-precos', "document.querySelector('#nav [data-ir=precos]').click()", 1100)], w=1440, h=900)
print('escuro 1440 erros:', len(e)); [print(' ', x) for x in e[:10]]
e = run([('t1100-geral', None, 400), ('t1100-desejos', "document.querySelector('#nav [data-ir=desejos]').click()", 1100)], w=1100, h=800)
print('1100 erros:', len(e)); [print(' ', x) for x in e[:10]]
e = run([('t820-geral', None, 400), ('t820-biblioteca', "document.querySelector('#nav-m [data-ir=biblioteca]').click()", 1100)], w=820, h=1000)
print('820 erros:', len(e)); [print(' ', x) for x in e[:10]]
e = run([('m-topo', "document.querySelector('#nav-m [data-ir=desejos]').click()", 900),
         ('m-filtros', "document.querySelector('#f-abrir').click()", 700)], w=390, h=844, full=False)
print('390 erros:', len(e)); [print(' ', x) for x in e[:10]]
