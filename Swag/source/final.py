import math, sys, os
OUT = sys.argv[1]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.py')).read()
exec(src.split('def mark(')[0].replace("OUT = sys.argv[1]\nos.makedirs(OUT, exist_ok=True)\n", ''))
# text_path / text_width available; ORANGE, BLACK, WHITE
O, K, W = ORANGE, BLACK, WHITE
def half(cx, cy, R, side):
    big = 0 if side == 'L' else 1; h = R/2
    return f'M{cx},{cy-R} A{R},{R} 0 0 {big} {cx},{cy+R} A{h},{h} 0 0 0 {cx},{cy} A{h},{h} 0 0 1 {cx},{cy-R} Z'
def star(cx, cy, r, col):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r*0.42
        a = math.radians(-90 + i*36)
        pts.append(f'{cx+rr*math.cos(a):.2f},{cy+rr*math.sin(a):.2f}')
    return f'<path d="M{" L".join(pts)} Z" fill="{col}"/>'
def mark(cx, cy, s=1.0, us_col=K, ring_col=O):
    R, rr = 165*s, 222*s
    g = (f'<circle cx="{cx}" cy="{cy}" r="{R:.2f}" fill="none" stroke="{O}" stroke-width="{10*s:.2f}"/>'
         f'<path d="{half(cx,cy,R,"L")}" fill="{O}"/>')
    for i in range(13):
        a = math.radians(-90 + i*360/13)
        g += star(cx + rr*math.cos(a), cy + rr*math.sin(a), (25 if i == 0 else 16)*s, ring_col)
    g += f'<path d="{text_path("NotoSerifTC.ttf", "中", 104*s, cx, cy - R/2 + 37*s, "middle")}" fill="{O}"/>'
    g += f'<path d="{text_path("BlackOps.ttf", "US", 74*s, cx, cy + R/2 + 26*s, "middle")}" fill="{us_col}"/>'
    return g
def svg(w, h, body, bg=None, title='Free Eva', vb=None):
    bgr = f'<rect x="{vb[0] if vb else 0}" y="{vb[1] if vb else 0}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    v = f'{vb[0]} {vb[1]} {w} {h}' if vb else f'0 0 {w} {h}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{v}" width="{w}" height="{h}" role="img" aria-label="{title}"><title>{title}</title>{bgr}{body}</svg>\n')
def write(n, c): open(os.path.join(OUT, n), 'w').write(c)
# 1 mark only, transparent (works on dark or light)
write('mark.svg', svg(520, 520, mark(260, 268), title='Free Eva mark: 中 / US yin-yang with 13 stars'))
# 2 app icon
write('app-icon.svg', svg(512, 512, f'<rect width="512" height="512" rx="96" fill="{K}"/>' + mark(256, 263, 0.98), title='Free Eva'))
# 3 favicon (simplified: no small-star clutter is kept, just bigger)
write('favicon.svg', svg(64, 64, f'<rect width="64" height="64" rx="12" fill="{K}"/>' + mark(32, 33, 0.125), title='Free Eva'))
# 4 stacked lockup, dark
foot = (f'<path d="{text_path("BigShoulders.ttf", "MUTUAL RESPECT", 100, 400, 640, "middle", 0.03)}" fill="{W}"/>'
        f'<path d="{text_path("NotoSerifTC.ttf", "中美相互尊重", 54, 400, 718, "middle", 0.15)}" fill="{W}" fill-opacity="0.85"/>'
        f'<path d="{text_path("BlackOps.ttf", "STEP ONE: FREE EVA", 44, 400, 798, "middle")}" fill="{O}"/>')
write('logo-stacked-dark.svg', svg(800, 860, mark(400, 300) + foot, bg=K, title='Free Eva: Mutual Respect 中美相互尊重'))
# 5 horizontal lockup, dark
tx = 560
hz = mark(270, 270, 0.92)
hz += f'<path d="{text_path("BlackOps.ttf", "FREE EVA", 150, tx, 225)}" fill="{O}"/>'
hz += f'<path d="{text_path("BigShoulders.ttf", "MUTUAL RESPECT", 92, tx+4, 340, tracking=0.03)}" fill="{W}"/>'
hz += f'<path d="{text_path("NotoSerifTC.ttf", "中美相互尊重", 60, tx+6, 430, tracking=0.18)}" fill="{W}" fill-opacity="0.85"/>'
write('logo-horizontal-dark.svg', svg(1400, 540, hz, bg=K, title='Free Eva: Mutual Respect 中美相互尊重'))
# 6 light versions of the lockups (black text on white; US stays black on orange)
write('logo-horizontal-light.svg', svg(1400, 540, hz.replace(f'fill="{W}"', f'fill="{K}"'), bg='#FFFFFF', title='Free Eva: Mutual Respect 中美相互尊重'))
write('logo-stacked-light.svg', svg(800, 860, (mark(400, 300) + foot).replace(f'fill="{W}"', f'fill="{K}"'), bg='#FFFFFF', title='Free Eva: Mutual Respect 中美相互尊重'))
print(text_width("BlackOps.ttf", "FREE EVA", 150), text_width("BigShoulders.ttf", "MUTUAL RESPECT", 92, 0.03))
