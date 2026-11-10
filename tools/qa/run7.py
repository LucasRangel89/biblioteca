from shot import run
e = run([('m-topo', "document.querySelector('#nav-m [data-ir=desejos]').click()", 900),
         ('m-filtros', "document.querySelector('#f-abrir').click()", 700),
         ('_', "document.querySelector('#f-tipo button[data-v=NF]').click()", 500),
         ('_', "document.querySelector('#pop-eixo input[value=\"4\"]').click()", 500),
         ('m-filtros-2', "(() => { document.querySelector('.f-corpo').scrollTop = 520; return {n: document.querySelector('#f-n').textContent, folha: document.querySelector('#filtros').className, trav: document.documentElement.className}; })()", 500),
         ('m-filtrado', "document.querySelector('#f-ver').click()", 900),
         ('_', "({folha: document.querySelector('#filtros').className, trav: document.documentElement.className, chips: document.querySelector('#f-ativos').innerText})", 100),
        ], w=390, h=844, full=False)
print('390 erros:', len(e)); [print(' ', x) for x in e[:10]]
