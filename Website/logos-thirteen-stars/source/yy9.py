import math, sys, os
D = sys.argv[1]
O, W, K, G = '#E77500', '#FFFFFF', '#151515', '#F2B134'
foot = (f'<text x="400" y="588" text-anchor="middle" font-family="Shoulders" font-weight="800" font-size="100" letter-spacing="3" fill="{W}">MUTUAL RESPECT</text>'
        f'<text x="400" y="664" text-anchor="middle" font-family="SerifTC" font-weight="900" font-size="54" letter-spacing="8" fill="{W}" fill-opacity=".85">中美相互尊重</text>'
        f'<text x="400" y="745" text-anchor="middle" font-family="BlackOps" font-size="44" fill="{O}">STEP ONE: FREE EVA</text>')
def half(cx, cy, R, side):
    big = 0 if side == 'L' else 1
    h = R/2
    return f'M{cx},{cy-R} A{R},{R} 0 0 {big} {cx},{cy+R} A{h},{h} 0 0 0 {cx},{cy} A{h},{h} 0 0 1 {cx},{cy-R} Z'
def S(cx, cy, R):  # the dividing S-curve
    h = R/2
    return f'M{cx},{cy-R} A{h},{h} 0 0 0 {cx},{cy} A{h},{h} 0 0 1 {cx},{cy+R}'
def yy(cx, cy, R, a=O, b=W, dots=True, rot=0):
    s = f'<g transform="rotate({rot} {cx} {cy})"><path d="{half(cx,cy,R,"L")}" fill="{a}"/><path d="{half(cx,cy,R,"R")}" fill="{b}"/>'
    if dots:
        s += f'<circle cx="{cx}" cy="{cy-R/2}" r="{R/7:.1f}" fill="{{T}}"/><circle cx="{cx}" cy="{cy+R/2}" r="{R/7:.1f}" fill="{{B}}"/>'
    return s + '</g>'
def star(cx, cy, r, col):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r*0.42
        a = math.radians(-90 + i*36)
        pts.append(f'{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}')
    return f'<path d="M{" L".join(pts)} Z" fill="{col}"/>'
L = []
def clip(id_, shape, inner):
    return f'<defs><clipPath id="{id_}"><path d="{shape}"/></clipPath></defs><g clip-path="url(#{id_})">{inner}</g>'
# 1 Pure
L.append(('Pure Yin-Yang', 'The classic yin-yang in orange and white: two opposite halves that fit together, each holding a dot of the other.',
  yy(400, 265, 190)))
# 2 13 stars
s = yy(400, 265, 135)
for i in range(13):
    a = math.radians(-90 + i*360/13); s += star(400+192*math.cos(a), 265+192*math.sin(a), 20, W)
L.append(('Thirteen Stars', 'A yin-yang inside the ring of 13 stars from the 1777 Betsy Ross flag, the colonies joined as one union, all equal.', s))
# 3 E Pluribus Unum
s = yy(400, 225, 140)
s += (f'<path d="M130,385 Q265,350 400,385 Q535,420 670,385 L670,445 Q535,480 400,445 Q265,410 130,445 Z" fill="{W}"/>'
      f'<path id="rb" d="M150,425 Q265,392 400,425 Q535,458 650,425" fill="none"/>'
      f'<text font-family="Shoulders" font-weight="800" font-size="40" letter-spacing="3" fill="{K}"><textPath href="#rb" startOffset="50%" text-anchor="middle">E PLURIBUS UNUM · 合眾為一</textPath></text>')
L.append(('E Pluribus Unum', 'A yin-yang over the ribbon from the Great Seal: "E Pluribus Unum, out of many, one," with the Chinese 合眾為一 alongside.', s))
# 4 Golden Spike
s = yy(400, 265, 175, dots=False)
p = S(400, 265, 175)
s += (f'<path d="{p}" fill="none" stroke="#7a5a3a" stroke-width="54" stroke-dasharray="9 13"/>'
      f'<path d="{p}" fill="none" stroke="{K}" stroke-width="34"/>'
      f'<path d="{p}" fill="none" stroke="#9a7a5a" stroke-width="20" stroke-dasharray="9 13"/>'
      f'<path d="{p}" fill="none" stroke="#d0d0d0" stroke-width="4" transform="translate(-12 0)"/>'
      f'<path d="{p}" fill="none" stroke="#d0d0d0" stroke-width="4" transform="translate(12 0)"/>'
      f'<path d="M386,214 H414 L404,312 L400,326 L396,312 Z" fill="{G}" stroke="{K}" stroke-width="4"/>')
L.append(('Golden Spike', 'The dividing line becomes a railroad, joined at the center by the golden spike of 1869. Chinese workers helped build that first transcontinental line.', s))
# 5 Liberty Bell
bell = 'M312,150 Q300,150 300,176 L292,320 Q288,362 248,392 H552 Q512,362 508,320 L500,176 Q500,150 488,150 Z'
s = (f'<rect x="330" y="104" width="140" height="30" rx="6" fill="{W}"/><rect x="385" y="132" width="30" height="20" fill="{W}"/>'
     + clip('bc', bell, yy(400, 272, 168, rot=0).replace('{T}', O).replace('{B}', W))
     + f'<path d="M352,392 L360,350 L348,330 L358,300 L350,280" fill="none" stroke="{K}" stroke-width="5"/>'
     + f'<circle cx="400" cy="408" r="16" fill="{W}"/>')
L.append(('Liberty Bell', 'The Liberty Bell, crack included, filled with a yin-yang. It first rang for a nation of different states agreeing to be one.', s))
# 6 House United
house = 'M400,80 L620,250 V440 H180 V250 Z'
s = clip('hc', house, yy(400, 280, 230).replace('{T}', O).replace('{B}', W))
L.append(('House United', 'A house filled with a yin-yang. Lincoln warned that "a house divided against itself cannot stand"; this one stands because its halves fit.', s))
# 7 Stars & Stripes
s = yy(400, 265, 185, dots=False)
stripes = ''.join(f'<rect x="200" y="{80+i*28}" width="400" height="14" fill="{O}"/>' for i in range(14))
s += clip('wh', half(400, 265, 185, 'R'), stripes)
sts = ''
for (x, y) in [(330,150),(372,200),(318,232),(300,300),(352,300),(305,370),(360,400),(410,345)]:
    sts += star(x, y, 17, W)
s += clip('oh', half(400, 265, 185, 'L'), sts)
s += f'<circle cx="400" cy="265" r="185" fill="none" stroke="{W}" stroke-width="6"/>'
L.append(('Stars & Stripes', 'A yin-yang with stripes in one half and stars in the other: the American flag\'s two halves folded into a single circle of balance.', s))
# 8 Liberty Torch
flame = 'M400,70 C470,150 515,215 485,290 Q455,345 400,345 Q345,345 315,290 C285,215 330,150 400,70 Z'
s = clip('fc', flame, yy(400, 225, 150, rot=0).replace('{T}', O).replace('{B}', W))
s += (f'<path d="M322,352 H478 L452,398 H348 Z" fill="{W}"/><rect x="380" y="398" width="40" height="64" rx="4" fill="{W}"/>')
L.append(('Liberty Torch', 'The Statue of Liberty\'s torch with a yin-yang flame. The light that welcomed immigrants, burning with both halves together.', s))
# 9 Union Shield
shield = 'M250,100 H550 V250 Q550,380 400,450 Q250,380 250,250 Z'
s = clip('sc', shield, yy(400, 285, 210).replace('{T}', O).replace('{B}', W))
s += f'<path d="M250,160 H550" stroke="{K}" stroke-width="10"/><path d="{shield}" fill="none" stroke="{W}" stroke-width="10"/>'
L.append(('Union Shield', 'The shield from the Great Seal, whose top band stands for the union holding the states together, filled with a yin-yang.', s))
L = [(n, d, b.replace('{T}', O).replace('{B}', W)) for n, d, b in L]
CSS = open(os.path.join(D, '..', 'hero', 'base.css')).read().split(':root')[0] + '*{margin:0}body{background:#151515}'
for i, (name, desc, body) in enumerate(L, 1):
    slug = f'yinyang-{i}-' + ''.join(c for c in name.lower().replace(' ', '-') if c.isalnum() or c == '-').replace('--','-')
    open(os.path.join(D, slug + '.html'), 'w').write(
        f'<html data-size="800x800"><head><style>{CSS}html,body{{width:800px;height:800px;overflow:hidden}}</style></head><body><svg viewBox="0 0 800 800" width="800" height="800">{body}{foot}</svg></body></html>')
import re
def uniq(body, i): return re.sub(r'(id="|url\(#|href="#)(\w+)', lambda m: f'{m.group(1)}{m.group(2)}{i}', body)
cells = ''.join(f'<div class=c><svg viewBox="0 0 800 800">{uniq(body,i)}{foot}</svg><h3><b>{i}</b> {name}</h3><p>{desc}</p></div>' for i, (name, desc, body) in enumerate(L, 1))
open(os.path.join(D, 'yinyang-ideas-sheet.html'), 'w').write(f'''<html data-size="1800x2400"><head><style>{CSS}
html,body{{width:1800px;height:2400px;overflow:hidden;background:#151515;color:#fff;font-family:Inter}}
.hd{{padding:56px 64px 8px;display:flex;justify-content:space-between;align-items:baseline}}
.hd h1{{font-family:Shoulders;font-weight:800;font-size:64px;letter-spacing:2px}}.hd h1 span{{color:#E77500}}.hd em{{color:#aaa;font-size:24px;font-style:normal}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;padding:28px 64px}}
.c{{background:#1e1e1e;border-radius:14px;padding:24px 24px 28px}}.c svg{{width:100%;aspect-ratio:1;display:block;background:#151515;border-radius:8px}}
.c h3{{font-size:28px;margin-top:20px}}.c h3 b{{color:#E77500;margin-right:6px}}.c p{{color:#bdbdbd;font-size:19px;line-height:1.4;margin-top:8px;height:108px}}
</style></head><body><div class=hd><h1>YIN-YANG <span>· 9 logo ideas, round 3</span></h1><em>China and the US, in balance</em></div><div class=g>{cells}</div></body></html>''')
for i, (name, desc, _) in enumerate(L, 1): print(f'{i}. {name}: {desc}')
