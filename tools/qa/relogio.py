"""O que todo teste do painel precisa para dar sempre o mesmo resultado: o relógio parado e as capas sem internet.

Relógio — os dados de exemplo são gerados a partir da data de hoje, então os números esperados só valem se "hoje"
for sempre o mesmo dia (09/11/2026, 10h de Brasília).

Capas — as imagens vêm da Open Library (covers.openlibrary.org) e da Apple Books (is…-ssl.mzstatic.com). Nos testes
ninguém vai à internet: cada pedido de capa é respondido aqui mesmo, com uma imagem pequena de cor fixa (a cor sai do
número da capa ou do endereço). Para ensaiar uma capa que não existe, passe em `faltam` o número (Open Library) ou o
endereço inteiro (Apple): esses recebem 404.

Fonte — as medidas de largura no celular (os nomes da barra de baixo, os botões do filtro Tipo) dependem da letra com
que o navegador de teste desenha. Foram calibradas com Open Sans; com uma letra bem mais larga (DejaVu Sans, a única
instalada em muita máquina Linux) esses testes acusam estouro sem que o painel tenha mudado. `fonte_usada` diz qual
foi usada, e os testes de largura a mostram quando falham.
"""
import datetime, re, struct, zlib
HOJE = datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc)
CAPAS = 'https://covers.openlibrary.org/**'
CAPAS_APPLE = re.compile(r'^https://is\d+-ssl\.mzstatic\.com/')
CAPA_APPLE = re.compile(r'https://is\d+-ssl\.mzstatic\.com/image/thumb/[\w./%+-]+/200x300bb\.jpg', re.ASCII)      # a forma do endereço que o painel pede


def eh_capa(url):
    """O endereço é de uma das duas fontes de capas?"""
    return url.startswith('https://covers.openlibrary.org/b/id/') or bool(CAPAS_APPLE.match(url))


def png(r, g, b, w=40, h=60):
    """Uma imagem PNG de uma cor só (sem depender de biblioteca nenhuma)."""
    def bloco(tipo, dados):
        return struct.pack('>I', len(dados)) + tipo + dados + struct.pack('>I', zlib.crc32(tipo + dados) & 0xffffffff)
    linhas = b''.join(b'\x00' + bytes((r, g, b)) * w for _ in range(h))
    return b'\x89PNG\r\n\x1a\n' + bloco(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + bloco(b'IDAT', zlib.compress(linhas, 9)) + bloco(b'IEND', b'')


def capas_de_mentira(pg, faltam=(), pedidos=None):
    """Responde aos pedidos de capa sem sair para a internet. `pedidos` (lista) recebe o endereço de cada um."""
    faltam = {str(n) for n in faltam}

    def responde(rota):
        url = rota.request.url
        if pedidos is not None: pedidos.append(url)
        m = re.search(r'/b/id/(\d+)-[SML]\.jpg', url)
        if not m or m.group(1) in faltam:
            return rota.fulfill(status=404, content_type='text/plain', body='')
        n = int(m.group(1))
        rota.fulfill(status=200, content_type='image/png', body=png(70 + n % 150, 70 + n // 7 % 150, 70 + n // 49 % 150))

    def responde_apple(rota):
        url = rota.request.url
        if pedidos is not None: pedidos.append(url)
        if url in faltam:
            return rota.fulfill(status=404, content_type='text/plain', body='')
        n = zlib.crc32(url.encode('utf-8'))
        rota.fulfill(status=200, content_type='image/png', body=png(70 + n % 150, 70 + n // 7 % 150, 70 + n // 49 % 150))
    pg.route(CAPAS, responde)
    pg.route(CAPAS_APPLE, responde_apple)
    return pg


def fixa(pg, quando=None):
    pg.clock.set_fixed_time(quando or HOJE)
    capas_de_mentira(pg)
    return pg


def fonte_usada(pg, seletor='body'):
    """O nome da fonte com que o navegador desenhou o elemento (só no Chromium; em outro navegador, '?')."""
    try:
        s = pg.context.new_cdp_session(pg); s.send('DOM.enable'); s.send('CSS.enable')
        raiz = s.send('DOM.getDocument')['root']['nodeId']
        no = s.send('DOM.querySelector', {'nodeId': raiz, 'selector': seletor})['nodeId']
        fontes = s.send('CSS.getPlatformFontsForNode', {'nodeId': no})['fonts']; s.detach()
        return ', '.join(sorted({f['familyName'] for f in fontes})) or '?'
    except Exception as e:
        return f'? ({type(e).__name__})'
