from caminhos import TMP
import sys
from PIL import Image
src, y0, y1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
x0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
x1 = int(sys.argv[5]) if len(sys.argv) > 5 else None
im = Image.open(f'{TMP}/shots/{src}.png')
x1 = x1 or im.width
im.crop((x0, y0, x1, min(y1, im.height))).save(f'{TMP}/shots/{src}-c.png')
print(im.size)
