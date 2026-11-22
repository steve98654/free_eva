import math, sys, os
D = sys.argv[1]
O, W, K = '#E77500', '#FFFFFF', '#151515'
foot = (f'<text x="400" y="588" text-anchor="middle" font-family="Shoulders" font-weight="800" font-size="100" letter-spacing="3" fill="{W}">MUTUAL RESPECT</text>'
        f'<text x="400" y="664" text-anchor="middle" font-family="SerifTC" font-weight="900" font-size="54" letter-spacing="8" fill="{W}" fill-opacity=".85">中美相互尊重</text>'
        f'<text x="400" y="745" text-anchor="middle" font-family="BlackOps" font-size="44" fill="{O}">STEP ONE: FREE EVA</text>')
def pt(cx, cy, r, a): return (cx + r*math.cos(math.radians(a)), cy + r*math.sin(math.radians(a)))
def f(p): return f'{p[0]:.1f},{p[1]:.1f}'
L = []
# 1 Keystone bridge
cx, cy, ri, ro, n = 400, 410, 140, 240, 9
b = ''
for i in range(n):
    a1 = 180 + i*180/n + 1.2; a2 = 180 + (i+1)*180/n - 1.2
    key = i == n//2
    rr = ro + (22 if key else 0)
    b += (f'<path d="M{f(pt(cx,cy,ri,a1))} L{f(pt(cx,cy,rr,a1))} L{f(pt(cx,cy,rr,a2))} L{f(pt(cx,cy,ri,a2))} Z" fill="{O if key else W}"/>')
b += f'<path d="M110,418 H690" stroke="{W}" stroke-width="10" stroke-opacity=".5"/>'
b += (f'<text x="210" y="462" text-anchor="middle" font-family="SerifTC" font-weight="900" font-size="34" fill="{W}" fill-opacity=".7">中國</text>'
      f'<text x="590" y="462" text-anchor="middle" font-family="Shoulders" font-weight="800" font-size="38" fill="{W}" fill-opacity=".7">USA</text>')
L.append(('Keystone', 'A stone arch between China and the US. Freeing Eva is the orange keystone: put it in place and the whole bridge holds.', b))
# 2 Embrace
e = (f'<path d="M{f(pt(400,265,165,110))} A165,165 0 0 1 {f(pt(400,265,165,250))}" fill="none" stroke="{O}" stroke-width="44" stroke-linecap="round"/>'
     f'<path d="M{f(pt(400,265,165,-70))} A165,165 0 0 1 {f(pt(400,265,165,70))}" fill="none" stroke="{W}" stroke-width="44" stroke-linecap="round"/>'
     f'<circle cx="400" cy="265" r="34" fill="{O}"/>')
L.append(('Embrace', 'Two arcs, orange and white, reaching around to form one circle. Two equal partners, with Eva held safe in the middle.', e))
# 3 Reset
r = (f'<path d="M{f(pt(400,275,150,-55))} A150,150 0 1 1 {f(pt(400,275,150,235))}" fill="none" stroke="{O}" stroke-width="40" stroke-linecap="round"/>'
     f'<path d="M400,95 V265" stroke="{W}" stroke-width="40" stroke-linecap="round"/>')
L.append(('Reset', 'A power and reset button. The relationship needs a restart, and freeing Eva is the press of the button.', r))
# 4 Puzzle
pz = (f'<path d="M405,150 H600 V350 H405 V280 A40,40 0 0 0 405,220 Z" fill="{W}"/>'
      f'<path d="M200,150 H395 V214 A44,44 0 1 1 395,286 V350 H200 Z" fill="{O}"/>')
L.append(('Puzzle Pieces', 'Two pieces cut to fit each other exactly. Neither side is complete alone; collaboration is the whole picture.', pz))
# 5 Full circle arrows
def arrow(a1, a2, col):
    p1, p2 = pt(400,265,160,a1), pt(400,265,160,a2)
    tip = pt(400,265,160,a2+18); l = pt(400,265,125,a2); rr_ = pt(400,265,195,a2)
    return (f'<path d="M{f(p1)} A160,160 0 0 1 {f(p2)}" fill="none" stroke="{col}" stroke-width="36"/>'
            f'<path d="M{f(l)} L{f(tip)} L{f(rr_)} Z" fill="{col}"/>')
fc = arrow(195, 320, O) + arrow(15, 140, W)
fc += f'<text x="400" y="292" text-anchor="middle" font-family="BlackOps" font-size="76" fill="{O}">EVA</text>'
L.append(('Full Circle', 'Two arrows chasing each other in a loop: what each side gives comes back. The circle starts moving again with Eva.', fc))
# 6 Ping-pong
def paddle(cx, cy, ang, col):
    return (f'<g transform="rotate({ang} {cx} {cy})"><rect x="{cx-17}" y="{cy+70}" width="34" height="110" rx="12" fill="{col}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="98" fill="{col}"/></g>')
pp = paddle(270, 260, -30, O) + paddle(530, 260, 30, W)
pp += f'<path d="M300,140 Q400,40 500,140" fill="none" stroke="{W}" stroke-width="5" stroke-dasharray="4 14" stroke-linecap="round" stroke-opacity=".7"/><circle cx="400" cy="92" r="24" fill="{W}"/>'
L.append(('Ping-Pong', 'Two paddles and a ball, after the 1971 ping-pong diplomacy that helped reopen China–US relations. A small human gesture can reset things again.', pp))
# 7 Moon gate
mg = (f'<path d="M170,140 H630 V440 H170 Z M400,135 m-0,0 M270,290 A130,130 0 1 0 530,290 A130,130 0 1 0 270,290 Z" fill="{W}" fill-rule="evenodd"/>'
      f'<path d="M140,140 L190,92 H610 L660,140 Z" fill="{O}"/>'
      f'<path d="M392,330 H408 L480,440 H320 Z" fill="{O}"/><path d="M276,330 H524" stroke="{O}" stroke-width="4" stroke-opacity=".6"/>'
      f'<path d="M170,440 H630" stroke="{W}" stroke-width="8"/>')
mg = mg.replace(' M400,135 m-0,0', '')
L.append(('Moon Gate', 'A round Chinese garden "moon gate" with a path running through it. An open doorway, and the way forward starts there.', mg))
# 8 First step
fs = (f'<rect x="170" y="330" width="150" height="110" fill="{O}"/>'
      f'<rect x="328" y="230" width="150" height="210" fill="none" stroke="{W}" stroke-width="10"/>'
      f'<rect x="486" y="130" width="150" height="310" fill="none" stroke="{W}" stroke-width="10"/>'
      f'<text x="245" y="398" text-anchor="middle" font-family="BlackOps" font-size="40" fill="{K}">EVA</text>'
      f'<text x="403" y="296" text-anchor="middle" font-family="Shoulders" font-weight="800" font-size="40" fill="{W}">TRUST</text>'
      f'<text x="561" y="196" text-anchor="middle" font-family="Shoulders" font-weight="800" font-size="34" fill="{W}">RESPECT</text>'
      f'<text x="245" y="320" text-anchor="middle" font-family="BlackOps" font-size="42" fill="{O}">1</text>'
      f'<text x="403" y="220" text-anchor="middle" font-family="BlackOps" font-size="42" fill="{W}" fill-opacity=".6">2</text>'
      f'<text x="561" y="120" text-anchor="middle" font-family="BlackOps" font-size="42" fill="{W}" fill-opacity=".6">3</text>')
L.append(('First Step', 'A staircase up to respect. The first step, in orange, is freeing Eva; trust and respect are built on it.', fs))
# 9 人
ren = (f'<path d="M418,96 C424,96 440,104 436,128 C420,260 340,380 214,446 C206,450 198,442 204,436 C300,350 362,240 390,118 C394,100 408,96 418,96 Z" fill="{O}"/>'
       f'<path d="M392,250 C420,330 500,410 610,436 C622,439 624,450 612,452 C500,470 410,420 372,300 C366,280 386,236 392,250 Z" fill="{W}"/>')
L.append(('人 (People)', 'The character 人, "person", drawn as two strokes leaning on each other: orange and white, neither standing alone. Respect between people comes first.', ren))
CSS = open(os.path.join(D, '..', 'hero', 'base.css')).read().split(':root')[0] + '*{margin:0}body{background:#151515}'
for i, (name, desc, body) in enumerate(L, 1):
    slug = f'respect-{i}-' + ''.join(c for c in name.lower().replace(' ', '-') if c.isascii() and (c.isalnum() or c == '-')).strip('-')
    open(os.path.join(D, slug + '.html'), 'w').write(
        f'<html data-size="800x800"><head><style>{CSS}html,body{{width:800px;height:800px;overflow:hidden}}</style></head><body><svg viewBox="0 0 800 800" width="800" height="800">{body}{foot}</svg></body></html>')
cells = ''.join(f'<div class=c><svg viewBox="0 0 800 800">{body}{foot}</svg><h3><b>{i}</b> {name}</h3><p>{desc}</p></div>' for i, (name, desc, body) in enumerate(L, 1))
open(os.path.join(D, 'respect-ideas-sheet.html'), 'w').write(f'''<html data-size="1800x2400"><head><style>{CSS}
html,body{{width:1800px;height:2400px;overflow:hidden;background:#151515;color:#fff;font-family:Inter}}
.hd{{padding:56px 64px 8px;display:flex;justify-content:space-between;align-items:baseline}}
.hd h1{{font-family:Shoulders;font-weight:800;font-size:64px;letter-spacing:2px}}.hd h1 span{{color:#E77500}}.hd em{{color:#aaa;font-size:24px;font-style:normal}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;padding:28px 64px}}
.c{{background:#1e1e1e;border-radius:14px;padding:24px 24px 28px}}.c svg{{width:100%;aspect-ratio:1;display:block;background:#151515;border-radius:8px}}
.c h3{{font-size:28px;margin-top:20px}}.c h3 b{{color:#E77500;margin-right:6px}}.c p{{color:#bdbdbd;font-size:19px;line-height:1.4;margin-top:8px;height:108px}}
</style></head><body><div class=hd><h1>MUTUAL RESPECT <span>· 9 logo ideas, round 2</span></h1><em>Step one: free Eva</em></div><div class=g>{cells}</div></body></html>''')
for i, (name, desc, _) in enumerate(L, 1): print(f'{i}. {name}: {desc}')
