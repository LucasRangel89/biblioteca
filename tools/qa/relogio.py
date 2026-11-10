"""O que todo teste do painel precisa para dar sempre o mesmo resultado: o relógio parado e as capas sem internet.

Relógio — os dados de exemplo são gerados a partir da data de hoje, então os números esperados só valem se "hoje"
for sempre o mesmo dia (09/11/2026, 10h de Brasília).

Capas — as imagens vêm da Open Library (covers.openlibrary.org). Nos testes ninguém vai à internet: cada pedido de
capa é respondido aqui mesmo, com uma imagem pequena de cor fixa (a cor sai do número da capa). Para ensaiar uma
capa que não existe, passe os números em `faltam`: esses recebem 404.
"""
import datetime, re, struct, zlib
HOJE = datetime.datetime(2026, 11, 9, 13, 0, tzinfo=datetime.timezone.utc)
CAPAS = 'https://covers.openlibrary.org/**'


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
    pg.route(CAPAS, responde)
    return pg


def fixa(pg, quando=None):
    pg.clock.set_fixed_time(quando or HOJE)
    capas_de_mentira(pg)
    return pg
