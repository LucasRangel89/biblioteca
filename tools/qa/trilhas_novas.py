"""Smoke test das novas trilhas e dos atalhos do painel (requer Playwright e Chromium)."""
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
    page.wait_for_timeout(500)
    assert page.locator('#p-trilhas .li').count() == 68
    assert 'de ' in page.locator('#p-trilhas .card-f').inner_text()
    page.locator('#p-trilhas .seg [data-v=agora]').click()
    assert page.locator('#p-trilhas .seg [data-v=agora]').get_attribute('aria-pressed') == 'true'
    page.locator('#p-trilhas .li').filter(has=page.locator('.li-m b', has_text='Rosas e Espadas')).click()
    assert 'Trilha 37' in page.locator('#dlg h2').inner_text()
    assert page.locator('#dlg .tr-l li').count() == 11
    assert page.locator('#dlg [data-tr-tempo]').count() == 1
    antes = page.locator('#dlg [data-tr-tempo]').inner_text()
    page.locator('#dlg [data-tr-ritmo]').fill('60')
    depois = page.locator('#dlg [data-tr-tempo]').inner_text()
    assert antes != depois
    assert page.locator('#dlg [data-tr-rel]').first.inner_text() == 'Aço e Fé'
    page.locator('#dlg [data-tr-rel]').first.click()
    assert 'Trilha 12' in page.locator('#dlg h2').inner_text()
    assert not erros, erros
    browser.close()
print('OK: trilhas novas, cobertura, ritmo, ordem e ligações')
print('ERROS: 0')
