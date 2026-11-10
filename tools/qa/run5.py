from shot import run
steps = [('m-geral', "document.querySelector('#aviso .pri').click()", 600)]
for v in ['biblioteca', 'recs', 'desejos', 'precos']:
    steps.append((f'm-{v}', f"document.querySelector('#nav-m [data-ir={v}]').click()", 1200))
e = run(steps, w=390, h=844)
print('erros:', len(e)); [print(' ', x) for x in e[:10]]
