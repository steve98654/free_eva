import math, sys, os
D = sys.argv[1]
O, W, K = '#E77500', '#FFFFFF', '#151515'
foot = (f'<text x="400" y="650" text-anchor="middle" font-family="BlackOps" font-size="104" fill="{O}">FREE EVA</text>'
        f'<text x="400" y="742" text-anchor="middle" font-family="SerifTC" font-weight="900" font-size="58" letter-spacing="6" fill="{W}">釋放謝翌</text>')
def arcpath(cx, cy, r, a1, a2):
    p = lambda a: (cx + r*math.cos(math.radians(a)), cy + r*math.sin(math.radians(a)))
    (x1, y1), (x2, y2) = p(a1), p(a2)
    return f'M{x1:.1f},{y1:.1f} A{r},{r} 0 0 1 {x2:.1f},{y2:.1f}'
L = []
# 1 Open ring
L.append(('Open Ring', 'Graduation cap inside an orange ring with a gap: a student, and the door that should open.',
  '<image href="mark-dark.svg" x="170" y="40" width="460" height="460"/>' + foot))
# 2 Stencil block
L.append(('Stencil E', 'A solid orange block with a cut-out stencil E, in the shirt\'s stencil type. Reads clearly even as a tiny favicon.',
  f'<rect x="230" y="90" width="340" height="340" rx="18" fill="{O}"/>'
  f'<text x="400" y="380" text-anchor="middle" font-family="BlackOps" font-size="330" fill="{K}">E</text>' + foot))
# 3 Seal
seal = f'<rect x="250" y="80" width="300" height="300" rx="22" fill="{O}"/><rect x="266" y="96" width="268" height="268" rx="12" fill="none" stroke="{K}" stroke-width="6"/>'
for ch, x, y in [('釋', 468, 214), ('放', 468, 336), ('謝', 332, 214), ('翌', 332, 336)]:
    seal += f'<text x="{x}" y="{y}" text-anchor="middle" font-family="SerifTC" font-weight="900" font-size="108" fill="{K}">{ch}</text>'
L.append(('Name Seal', 'A traditional Chinese name chop (印章) carved with 釋放謝翌, read top to bottom, right to left. Signals the Chinese community standing behind her.',
  seal + f'<text x="400" y="650" text-anchor="middle" font-family="BlackOps" font-size="104" fill="{O}">FREE EVA</text>'
  f'<text x="400" y="736" text-anchor="middle" font-family="Shoulders" font-weight="800" font-size="60" letter-spacing="4" fill="{W}">WE ARE EVA</text>'))
# 4 Linked rings
rings = (f'<circle cx="320" cy="260" r="120" fill="none" stroke="{O}" stroke-width="34"/>'
         f'<circle cx="480" cy="260" r="120" fill="none" stroke="{W}" stroke-width="34"/>'
         f'<path d="{arcpath(320,260,120,-58,-25)}" fill="none" stroke="{O}" stroke-width="34"/>')
L.append(('Linked Rings', 'Two equal rings, orange and white, interlocked: China and the US bound together as equals. The mutual-respect message in one shape.',
  rings + foot))
# 5 Exchange arrows
arr = (f'<path d="M210,205 H520" stroke="{O}" stroke-width="44"/><path d="M500,140 L600,205 L500,270 Z" fill="{O}"/>'
       f'<path d="M590,325 H280" stroke="{W}" stroke-width="44"/><path d="M300,260 L200,325 L300,390 Z" fill="{W}"/>'
       f'<text x="210" y="462" font-family="Shoulders" font-weight="800" font-size="52" letter-spacing="4" fill="{W}" fill-opacity=".7">CHINA</text>'
       f'<text x="590" y="462" text-anchor="end" font-family="Shoulders" font-weight="800" font-size="52" letter-spacing="4" fill="{W}" fill-opacity=".7">US</text>')
L.append(('Two-Way Street', 'The ⇄ from the shirt back as its own symbol: respect has to flow both ways between China and the US.',
  arr + foot))
# 6 Bars opening
bars = f'<path d="M210,110 H590 M210,420 H590" stroke="{W}" stroke-width="18"/>'
for x in (240, 560): bars += f'<path d="M{x},110 V420" stroke="{W}" stroke-width="20"/>'
bars += f'<path d="M320,110 Q285,265 320,420" fill="none" stroke="{W}" stroke-width="20"/><path d="M480,110 Q515,265 480,420" fill="none" stroke="{W}" stroke-width="20"/>'
bars += f'<path d="M400,215 L470,245 L400,275 L330,245 Z" fill="{O}"/><path d="M360,262 V300 Q400,322 440,300 V262 L400,280 Z" fill="{O}"/>'
L.append(('Bars Bent Open', 'Detention bars pushed apart around a graduation cap. Says plainly that a student is being held, and that she should walk out.',
  bars + foot))
# 7 Homecoming
home = (f'<path d="M250,250 L400,125 L550,250 V420 H250 Z" fill="none" stroke="{W}" stroke-width="22" stroke-linejoin="round"/>'
        f'<path d="M370,420 V330 H430 V420" fill="none" stroke="{W}" stroke-width="18"/>'
        f'<path d="M120,180 Q190,120 260,160" fill="none" stroke="{O}" stroke-width="8" stroke-dasharray="16 14" stroke-linecap="round"/>'
        f'<path d="M262,150 L350,190 L290,205 Z M290,205 L300,232 L312,200 Z" fill="{O}"/>')
L.append(('Homecoming', 'A paper plane on its way into a house: she was flying home from a conference. The ask is simple, let her come home.',
  home + foot))
# 8 Conference badge
badge = (f'<path d="M330,40 L380,150 M470,40 L420,150" stroke="{O}" stroke-width="18" stroke-linecap="round"/>'
         f'<rect x="370" y="140" width="60" height="30" rx="6" fill="#bbb"/>'
         f'<rect x="220" y="160" width="360" height="270" rx="20" fill="{W}"/>'
         f'<path d="M220,180 a20,20 0 0 1 20,-20 h320 a20,20 0 0 1 20,20 v70 h-360 z" fill="{O}"/>'
         f'<text x="400" y="203" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" letter-spacing="6" fill="{W}">HELLO</text>'
         f'<text x="400" y="236" text-anchor="middle" font-family="Inter" font-weight="600" font-size="22" fill="{W}">my name is</text>'
         f'<text x="400" y="375" text-anchor="middle" font-family="BlackOps" font-size="120" fill="{K}">EVA</text>'
         f'<text x="400" y="414" text-anchor="middle" font-family="Inter" font-weight="600" font-size="20" letter-spacing="3" fill="#666">PHD STUDENT · PRINCETON</text>')
L.append(('Conference Badge', 'A "Hello, my name is" conference lanyard badge. Points straight at the story: she was a student attending a conference.',
  badge + foot))
# 9 Rally button
btn = (f'<circle cx="400" cy="400" r="350" fill="{O}"/><circle cx="400" cy="400" r="300" fill="none" stroke="{K}" stroke-width="5"/>'
       f'<path id="t" d="M400,400 m-322,0 a322,322 0 1 1 644,0 a322,322 0 1 1 -644,0" fill="none"/>'
       f'<text font-family="Shoulders" font-weight="800" font-size="38" letter-spacing="5" fill="{K}"><textPath href="#t" startOffset="0">MUTUAL RESPECT · 中美相互尊重 · CHINA ⇄ US · FREE EVA ·</textPath></text>'
       f'<text x="400" y="310" text-anchor="middle" font-family="SerifTC" font-weight="900" font-size="84" letter-spacing="4" fill="{K}">釋放謝翌</text>'
       f'<text x="400" y="470" text-anchor="middle" font-family="Shoulders" font-weight="800" font-size="165" fill="{W}">WE ARE</text>'
       f'<text x="400" y="590" text-anchor="middle" font-family="BlackOps" font-size="150" fill="{K}">EVA</text>')
L.append(('Rally Button', 'A round pin-back campaign button: WE ARE EVA, with MUTUAL RESPECT · 中美相互尊重 arched around the rim. Made for buttons, stickers and avatars.',
  btn))
CSS = open(os.path.join(D, '..', 'hero', 'base.css')).read().split(':root')[0]
CSS += '*{margin:0}body{background:#151515}'
for i, (name, desc, body) in enumerate(L, 1):
    slug = f'logo-{i}-' + name.lower().replace(' ', '-').replace('-way', 'way')
    html = f'<html data-size="800x800"><head><style>{CSS}html,body{{width:800px;height:800px;overflow:hidden}}</style></head><body><svg viewBox="0 0 800 800" width="800" height="800">{body}</svg></body></html>'
    open(os.path.join(D, slug + '.html'), 'w').write(html)
# contact sheet 3x3
cells = ''
for i, (name, desc, body) in enumerate(L, 1):
    cells += (f'<div class=c><svg viewBox="0 0 800 800">{body.replace("id=\"t\"", f"id=\"t{i}\"").replace("#t\"", f"#t{i}\"")}</svg>'
              f'<h3><b>{i}</b> {name}</h3><p>{desc}</p></div>')
sheet = f'''<html data-size="1800x2330"><head><style>{CSS}
html,body{{width:1800px;height:2330px;overflow:hidden;background:#151515;color:#fff;font-family:Inter}}
.hd{{padding:56px 64px 8px;display:flex;justify-content:space-between;align-items:baseline}}
.hd h1{{font-family:BlackOps;color:#E77500;font-size:56px;font-weight:400}}.hd span{{color:#aaa;font-size:24px}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;padding:28px 64px}}
.c{{background:#1e1e1e;border-radius:14px;padding:24px 24px 28px}}.c svg{{width:100%;aspect-ratio:1;display:block;background:#151515;border-radius:8px}}
.c h3{{font-size:28px;margin-top:20px}}.c h3 b{{color:#E77500;margin-right:6px}}.c p{{color:#bdbdbd;font-size:19px;line-height:1.4;margin-top:8px;height:80px}}
</style></head><body><div class=hd><h1>FREE EVA · 9 logo ideas</h1><span>evaxie.us</span></div><div class=g>{cells}</div></body></html>'''
open(os.path.join(D, 'logo-ideas-sheet.html'), 'w').write(sheet)
for i, (name, desc, _) in enumerate(L, 1): print(f'{i}. {name}: {desc}')
