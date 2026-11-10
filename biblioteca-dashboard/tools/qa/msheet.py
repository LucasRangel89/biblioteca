from caminhos import TMP
import sys
from PIL import Image
for nome in sys.argv[1:]:
    im = Image.open(f'{TMP}/shots/{nome}.png'); seg = 1500; n = -(-im.height // seg); w = im.width
    for part in range(0, n, 4):
        cols = [im.crop((0, i * seg, w, min(im.height, (i + 1) * seg))) for i in range(part, min(n, part + 4))]
        out = Image.new('RGB', (w * len(cols) + 12 * (len(cols) - 1), seg), (110, 110, 110))
        for i, c in enumerate(cols): out.paste(c, (i * (w + 12), 0))
        out.save(f'{TMP}/shots/{nome}-s{part // 4}.png')
    print(nome, im.size, n)
