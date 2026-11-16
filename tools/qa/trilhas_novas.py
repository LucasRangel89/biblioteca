"""Guia Trilhas: navegação, filtros, estados, ficha e celular (requer Playwright e Chromium)."""
import os
from caminhos import PAINEL_LIMPO
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    opcoes = {'headless': True}
    if os.environ.get('BIBLIOTECA_QA_CHROMIUM'):
        opcoes.update(executable_path=os.environ['BIBLIOTECA_QA_CHROMIUM'], args=['--no-sandbox'])
    browser = p.chromium.launch(**opcoes)
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    erros = []
    page.on('pageerror', lambda erro: erros.append(str(erro)))
    page.goto(PAINEL_LIMPO)
    page.wait_for_timeout(500)
    if page.locator('#aviso .pri').is_visible():
        page.locator('#aviso .pri').click()
    page.locator('#nav [data-ir=recs]').click()
    assert page.locator('#p-trilhas-atalho [data-ir=trilhas]').is_visible()
    assert page.locator('#p-trilhas').count() == 0
    page.locator('#p-trilhas-atalho [data-ir=trilhas]').click()
    assert page.locator('#v-trilhas').is_visible()
    assert page.locator('#filtros').is_hidden()
    assert page.locator('#p-trilhas .li').count() == 68
    assert '406 de 2124' in page.locator('#p-trilhas .card-f').inner_text()
    assert page.locator('#v-trilhas .kpi').count() == 4
    assert page.locator('#v-trilhas [data-k=concluidas] .num').inner_text() == '0'  # ter todos não é ler todos
    query = page.locator('#p-trilhas [data-tr-f=q]')
    query.fill('Mestre da Guerra')
    assert page.locator('#p-trilhas .li').count() == 1
    assert 'Rosas e Espadas' in page.locator('#p-trilhas .li').inner_text()
    query.fill('autor inexistente xyz')
    assert page.locator('#p-trilhas .li').count() == 0
    assert 'Nenhuma trilha' in page.locator('#p-trilhas .card-b').inner_text()
    page.locator('[data-tr-limpar]').click()
    assert page.locator('#p-trilhas .li').count() == 68
    page.locator('[data-tr-f=eixo]').select_option('6')
    assert 0 < page.locator('#p-trilhas .li').count() < 68
    page.locator('[data-tr-f=dif]').select_option('3')
    assert 0 < page.locator('#p-trilhas .li').count() < 68
    page.locator('[data-tr-limpar]').click()
    page.locator('[data-tr-f=tema]').select_option('romance-historico')
    assert 0 < page.locator('#p-trilhas .li').count() < 68
    assert page.locator('#p-trilhas [data-trilha=trilha-rosas-e-espadas]').count() == 1
    page.locator('[data-tr-limpar]').click()
    page.locator('[data-tr-f=posse]').select_option('todos')
    assert page.locator('#p-trilhas .li').count() > 0
    assert page.locator('#v-trilhas [data-k=roteiros] .num').inner_text() == '68'  # totais independem dos filtros
    page.locator('[data-tr-limpar]').click()
    page.locator('[data-tr-f=progresso]').select_option('concluida')
    assert page.locator('#p-trilhas .li').count() == 0
    page.locator('[data-tr-limpar]').click()
    page.locator('#p-trilhas .seg [data-v=agora]').click()
    assert page.locator('#p-trilhas .seg [data-v=agora]').get_attribute('aria-pressed') == 'true'
    page.locator('#p-trilhas [data-trilha=trilha-rosas-e-espadas]').click()
    assert 'Trilha 37' in page.locator('#dlg h2').inner_text()
    assert page.locator('#dlg .tr-l li').count() == 11
    antes = page.locator('#dlg [data-tr-tempo]').inner_text()
    page.locator('#dlg [data-tr-ritmo]').fill('60')
    assert antes != page.locator('#dlg [data-tr-tempo]').inner_text()
    assert page.locator('#dlg [data-tr-rel]').first.inner_text() == 'Aço e Fé'
    page.locator('#dlg [data-tr-rel]').first.click()
    assert 'Trilha 12' in page.locator('#dlg h2').inner_text()
    page.keyboard.press('Escape')
    page.reload()
    page.wait_for_timeout(700)
    assert page.locator('#v-trilhas').is_visible()
    assert page.locator('#p-trilhas .seg [data-v=agora]').get_attribute('aria-pressed') == 'true'
    # Exercita estados no armazenamento isolado do navegador de teste, sem alterar o catálogo.
    page.evaluate("""() => { const k = 'biblioteca-lucas:v1', d = JSON.parse(localStorage.getItem(k)); d.livros.filter(b => b.tags.includes('trilha-rosas-e-espadas')).forEach(b => { b.leit = 'lido'; b.u = 1; }); localStorage.setItem(k, JSON.stringify(d)); }""")
    page.reload(); page.wait_for_timeout(500)
    assert int(page.locator('#v-trilhas [data-k=concluidas] .num').inner_text()) >= 1
    page.locator('[data-tr-f=progresso]').select_option('concluida')
    assert page.locator('#p-trilhas [data-trilha=trilha-rosas-e-espadas]').count() == 1
    page.evaluate("""() => { const k = 'biblioteca-lucas:v1', d = JSON.parse(localStorage.getItem(k)); d.livros.find(b => b.tags.includes('trilha-rosas-e-espadas')).leit = 'lendo'; localStorage.setItem(k, JSON.stringify(d)); }""")
    page.reload(); page.wait_for_timeout(500)
    page.locator('[data-tr-f=progresso]').select_option('concluida')
    assert page.locator('#p-trilhas [data-trilha=trilha-rosas-e-espadas]').count() == 0
    page.locator('[data-tr-f=progresso]').select_option('andamento')
    assert page.locator('#p-trilhas [data-trilha=trilha-rosas-e-espadas]').count() == 1
    page.locator('[data-tr-f=progresso]').select_option('agora')
    assert page.locator('#p-trilhas [data-trilha=trilha-rosas-e-espadas]').count() == 0
    page.locator('#nav [data-ir=recs]').click()
    assert page.locator('#filtros').is_visible()
    assert not erros, erros
    page.close()

    for largura in (360, 320):
        phone = browser.new_page(viewport={'width': largura, 'height': 800}, is_mobile=True, has_touch=True)
        phone.goto(PAINEL_LIMPO)
        phone.wait_for_timeout(400)
        if phone.locator('#aviso .pri').is_visible(): phone.locator('#aviso .pri').click()
        phone.locator('#nav-m [data-ir=trilhas]').click()
        assert phone.locator('#v-trilhas').is_visible()
        assert phone.locator('#nav-m button').count() == 7
        assert phone.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert phone.evaluate("() => [...document.querySelectorAll('#nav-m button')].every(e => {const r=e.getBoundingClientRect(), s=e.querySelector('.nv-c'); return r.width >= 44 && r.left >= 0 && r.right <= innerWidth && s.scrollWidth <= s.clientWidth + 1;})")
        phone.locator('#p-trilhas [data-trilha=trilha-rosas-e-espadas]').click()
        assert phone.locator('#dlg h2').inner_text().startswith('Trilha 37')
        assert phone.evaluate('document.documentElement.scrollWidth <= innerWidth')
        phone.close()
    browser.close()
print('OK: guia, filtros, resumo, fichas, atalhos e celular')
print('ERROS: 0')
