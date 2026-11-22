import math, sys, os, re
D = sys.argv[1]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yy9.py')).read()
exec(src.split('L = []')[0].replace('D = sys.argv[1]', ''))   # helpers: O,W,K,G, foot, half, S, yy, star, clip
GOLD = '#F2B134'
def clip(id_, shape, inner):
    return f'<defs><clipPath id="{id_}"><path d="{shape}"/></clipPath></defs><g clip-path="url(#{id_})">{inner}</g>'
def ring(cx, cy, r, size, cols=None, n=13, start=-90):
    s = ''
    for i in range(n):
        a = math.radians(start + i*360/n)
        x, y = cx + r*math.cos(a), cy + r*math.sin(a)
        c = cols(i, x) if cols else W
        s += star(x, y, size, c)
    return s
def fix(b): return b.replace('{T}', O).replace('{B}', W)
L = []
# 1 Classic
L.append(('Classic', 'The chosen idea, refined: an orange and white yin-yang inside the 13-star ring of the 1777 Betsy Ross flag.',
  fix(yy(400, 265, 132)) + ring(400, 265, 190, 20)))
# 2 Mirrored ring
L.append(('Mirrored Ring', 'Stars on the white side are orange and stars on the orange side are white, so the ring takes part in the balance too.',
  fix(yy(400, 265, 132)) + ring(400, 265, 190, 20, lambda i, x: O if x > 400.5 else W)))
# 3 Stars within
b = fix(yy(400, 265, 200, dots=False))
inner = ring(400, 265, 130, 17, n=13)
b += clip('rw', half(400, 265, 200, 'R'), inner.replace(f'fill="{W}"', f'fill="{O}"'))
b += clip('ro', half(400, 265, 200, 'L'), inner)
L.append(('Stars Within', 'The 13-star ring placed inside the yin-yang, each star taking the color of the other half. Bold, and it holds up well at small sizes.', b))
# 4 Seal
b = (f'<circle cx="400" cy="262" r="212" fill="none" stroke="{W}" stroke-width="5"/><circle cx="400" cy="262" r="150" fill="none" stroke="{W}" stroke-width="3"/>'
     f'<path id="st" d="M228,262 A172,172 0 0 1 572,262" fill="none"/><path id="sb" d="M208,262 A192,192 0 0 0 592,262" fill="none"/>'
     f'<text font-family="Shoulders" font-weight="800" font-size="34" letter-spacing="5" fill="{W}"><textPath href="#st" startOffset="50%" text-anchor="middle">MUTUAL RESPECT</textPath></text>'
     f'<text font-family="SerifTC" font-weight="900" font-size="32" letter-spacing="8" fill="{W}" dominant-baseline="middle"><textPath href="#sb" startOffset="50%" text-anchor="middle" dy="0">中美相互尊重</textPath></text>'
     f'<path d="M{400-205},{262} m0,0" />'
     + star(205, 262, 12, O) + star(595, 262, 12, O)
     + fix(yy(400, 262, 92)) + ring(400, 262, 122, 11, n=13))
L.append(('Seal', 'A round official seal: yin-yang and 13 stars at the center, with MUTUAL RESPECT and 中美相互尊重 running around the rim.', b))
# 5 Star dots
b = f'<g><path d="{half(400,265,175,"L")}" fill="{O}"/><path d="{half(400,265,175,"R")}" fill="{W}"/></g>'
b += star(400, 265-87.5, 30, O) + star(400, 265+87.5, 30, W) + ring(400, 265, 222, 15)
L.append(('Star Dots', 'The two dots of the yin-yang become stars: each side carries a star of the other. The 13-star ring sits lightly around it.', b))
# 6 First star
L.append(('First Star', 'Twelve white stars and one orange star at the top. The orange star is step one, freeing Eva, which the rest can follow.',
  fix(yy(400, 265, 132)) + ring(400, 265, 190, 20, lambda i, x: O if i == 0 else W).replace(f'fill="{O}"', f'fill="{O}" stroke="{O}" stroke-width="2"', 1)))
# 7 Thirteen and five
b = fix(yy(400, 265, 132))
for i in range(13):
    a = math.radians(-92 + i*(184/12))
    b += star(400 + 192*math.cos(a), 265 + 192*math.sin(a), 15, W)
for i in range(5):
    a = math.radians(128 + i*(104/4))
    b += star(400 + 192*math.cos(a), 265 + 192*math.sin(a), 24 if i == 2 else 16, GOLD)
L.append(('13 + 5', 'The right arc carries the 13 American stars, the left arc carries 5 gold stars as a nod to China\'s flag. Both countries share the one ring.', b))
# 8 Free Eva first (text hierarchy)
b = fix(yy(400, 230, 118)) + ring(400, 230, 170, 18)
L.append(('Free Eva Lockup', 'The same mark with FREE EVA as the headline and mutual respect underneath, for campaign use while Eva is still detained.',
  b + '{FOOT2}'))
# 9 One color
b = (f'<circle cx="400" cy="265" r="132" fill="none" stroke="{O}" stroke-width="10"/>'
     f'<path d="{S(400,265,132)}" fill="none" stroke="{O}" stroke-width="10"/>'
     f'<path d="{half(400,265,132,"L")}" fill="{O}"/>'
     f'<circle cx="400" cy="{265-66}" r="19" fill="{O}"/><circle cx="400" cy="{265+66}" r="19" fill="{K}"/>'
     + ring(400, 265, 190, 20).replace(f'fill="{W}"', f'fill="{O}"'))
L.append(('One Color', 'A single-color orange version for screen printing, stamps, stickers and embroidery, with no white ink needed.', b))
foot2 = (f'<text x="400" y="560" text-anchor="middle" font-family="BlackOps" font-size="120" fill="{O}">FREE EVA</text>'
         f'<text x="400" y="650" text-anchor="middle" font-family="SerifTC" font-weight="900" font-size="64" letter-spacing="8" fill="{W}">釋放謝翌</text>'
         f'<text x="400" y="735" text-anchor="middle" font-family="Shoulders" font-weight="800" font-size="52" letter-spacing="3" fill="{W}" fill-opacity=".8">MUTUAL RESPECT · 中美相互尊重</text>')
def body_full(b): return b.replace('{FOOT2}', foot2) if '{FOOT2}' in b else b + foot
L = [(n, d, body_full(b)) for n, d, b in L]
CSS = open(os.path.join(D, '..', 'hero', 'base.css')).read().split(':root')[0] + '*{margin:0}body{background:#151515}'
for i, (name, desc, body) in enumerate(L, 1):
    slug = f'stars-{i}-' + re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    open(os.path.join(D, slug + '.html'), 'w').write(
        f'<html data-size="800x800"><head><style>{CSS}html,body{{width:800px;height:800px;overflow:hidden}}</style></head><body><svg viewBox="0 0 800 800" width="800" height="800">{body}</svg></body></html>')
def uniq(body, i): return re.sub(r'(id="|url\(#|href="#)(\w+)', lambda m: f'{m.group(1)}{m.group(2)}{i}', body)
cells = ''.join(f'<div class=c><svg viewBox="0 0 800 800">{uniq(body,i)}</svg><h3><b>{i}</b> {name}</h3><p>{desc}</p></div>' for i, (name, desc, body) in enumerate(L, 1))
open(os.path.join(D, 'stars-ideas-sheet.html'), 'w').write(f'''<html data-size="1800x2400"><head><style>{CSS}
html,body{{width:1800px;height:2400px;overflow:hidden;background:#151515;color:#fff;font-family:Inter}}
.hd{{padding:56px 64px 8px;display:flex;justify-content:space-between;align-items:baseline}}
.hd h1{{font-family:Shoulders;font-weight:800;font-size:64px;letter-spacing:2px}}.hd h1 span{{color:#E77500}}.hd em{{color:#aaa;font-size:24px;font-style:normal}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;padding:28px 64px}}
.c{{background:#1e1e1e;border-radius:14px;padding:24px 24px 28px}}.c svg{{width:100%;aspect-ratio:1;display:block;background:#151515;border-radius:8px}}
.c h3{{font-size:28px;margin-top:20px}}.c h3 b{{color:#E77500;margin-right:6px}}.c p{{color:#bdbdbd;font-size:19px;line-height:1.4;margin-top:8px;height:108px}}
</style></head><body><div class=hd><h1>THIRTEEN STARS <span>· 9 variations</span></h1><em>Yin-yang + the 1777 star ring</em></div><div class=g>{cells}</div></body></html>''')
for i, (name, desc, _) in enumerate(L, 1): print(f'{i}. {name}: {desc}')
