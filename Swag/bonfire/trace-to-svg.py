import sys, subprocess, re, numpy as np
from PIL import Image
src, out, title = sys.argv[1], sys.argv[2], sys.argv[3]
im = np.array(Image.open(src).convert('RGBA')).astype(int)
h, w = im.shape[:2]
a = im[..., 3] > 127
rgb = im[..., :3]
d_or = ((rgb - [231,117,0])**2).sum(-1)
d_wh = ((rgb - [255,255,255])**2).sum(-1)
layers = {'#E77500': a & (d_or < d_wh), '#FFFFFF': a & (d_wh <= d_or)}
paths = ''
for col, m in layers.items():
    if not m.any(): continue
    Image.fromarray(((~m)*255).astype('uint8')).convert('1').save('l.pbm')
    subprocess.run(['potrace','l.pbm','-b','svg','-o','l.svg','--flat','-t','4','-a','1.0','-O','0.4','-C',col], check=True)
    s = open('l.svg').read()
    g = re.search(r'(<g transform=.*</g>)', s, re.S).group(1)
    paths += f'<g id="{"orange" if col=="#E77500" else "white"}-ink">' + g + '</g>'
W, H = w/300, h/300
svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W:.3f}in" height="{H:.3f}in" viewBox="0 0 {w} {h}">'
       f'<title>{title}</title>{paths}</svg>\n')
open(out,'w').write(svg)
print(out, f'{W:.2f}x{H:.2f} in', len(svg)//1024, 'KB')
