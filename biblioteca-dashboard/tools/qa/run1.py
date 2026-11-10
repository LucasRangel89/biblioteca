from shot import run
steps = [('geral-1440', None, 500)]
for v in ['biblioteca', 'recs', 'desejos', 'precos']:
    steps.append((f'{v}-1440', f"document.querySelector('#nav [data-ir={v}]').click()", 1200))
e = run(steps)
print('erros:', len(e)); [print(' ', x) for x in e[:10]]
