import math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(HERE, 'brand.py')).read()
exec(src.split('# ---------- single colour')[0])
def emb(cx, cy, s, col, knock=True, star_r=(25, 16), ring_w=10):
    """Single-ink mark with adjustable star size (bigger for embroidery)."""
    _n[0] += 1; mid = f'e{_n[0]}'
    R, rr = 165*s, 222*s
    us = text_path("BlackOps.ttf", "US", 74*s, cx, cy + R/2 + 26*s, "middle")
    g = (f'<defs><mask id="{mid}" maskUnits="userSpaceOnUse" x="{cx-300*s}" y="{cy-300*s}" width="{600*s}" height="{600*s}">'
         f'<rect x="{cx-300*s}" y="{cy-300*s}" width="{600*s}" height="{600*s}" fill="#fff"/><path d="{us}" fill="#000"/></mask></defs>'
         f'<g fill="{col}"><circle cx="{cx}" cy="{cy}" r="{R:.2f}" fill="none" stroke="{col}" stroke-width="{ring_w*s:.2f}"/>'
         f'<path d="{half(cx,cy,R,"L")}" mask="url(#{mid})"/>')
    for i in range(13):
        a = math.radians(-90 + i*360/13)
        g += star(cx + rr*math.cos(a), cy + rr*math.sin(a), (star_r[0] if i == 0 else star_r[1])*s, col)
    g += f'<path d="{text_path("NotoSerifTC.ttf", "中", 104*s, cx, cy - R/2 + 37*s, "middle")}"/></g>'
    return g
def T(font, text, size, x, y, col, anchor='middle', tr=0, op=None):
    o = f' fill-opacity="{op}"' if op else ''
    return f'<path d="{text_path(font, text, size, x, y, anchor, tr)}" fill="{col}"{o}/>'

# Print items are drawn at 100 units per inch; render at 3x for 300 DPI.
# 1. Buttons, 2.25 in (art includes the 0.25 in wrap past the dashed face line)
for name, bg, ink in [('button-orange', O, K), ('button-black', K, O)]:
    c = 112.5
    b = f'<circle cx="{c}" cy="{c}" r="{c}" fill="{bg}"/>' + emb(c, c-14, 0.235, ink)
    b += T('BlackOps.ttf', 'FREE EVA', 19, c, c+70, ink if bg == O else W)
    W_(f'{name}.svg', svg(225, 225, b, title='Free Eva button'))
# 2. Enamel pin, 1.25 in: black + orange enamel, gold metal lines
c = 62.5; s = 0.235
pin = f'<circle cx="{c}" cy="{c}" r="61" fill="{K}" stroke="{GOLD}" stroke-width="3"/>'
R = 165*s
pin += f'<circle cx="{c}" cy="{c}" r="{R:.2f}" fill="{K}" stroke="{GOLD}" stroke-width="2.2"/>'
pin += f'<path d="{half(c,c,R,"L")}" fill="{O}" stroke="{GOLD}" stroke-width="1.2"/>'
for i in range(13):
    a = math.radians(-90 + i*360/13)
    pin += star(c + 222*s*math.cos(a), c + 222*s*math.sin(a), (30 if i == 0 else 20)*s, GOLD)
pin += T('NotoSerifTC.ttf', '中', 104*s, c, c - R/2 + 37*s, GOLD)
pin += T('BlackOps.ttf', 'US', 74*s, c, c + R/2 + 26*s, GOLD)
W_('enamel-pin.svg', svg(125, 125, pin, title='Free Eva enamel pin: black and orange enamel, gold metal'))
# 3. Tote bag, 10 x 11 in, one ink
def tote(ink):
    t = emb(500, 380, 1.15, ink)
    t += T('BlackOps.ttf', 'FREE EVA', 170, 500, 860, ink)
    t += T('BigShoulders.ttf', 'MUTUAL RESPECT', 98, 500, 975, ink, tr=0.04)
    t += T('NotoSerifTC.ttf', '中美相互尊重', 62, 500, 1065, ink, tr=0.2)
    return svg(1000, 1100, t, title='Free Eva tote print')
W_('tote-black-ink.svg', tote(K)); W_('tote-orange-ink.svg', tote(O))
# 4. Hat embroidery: 2.25 in wide front, bigger stars and thicker ring so stitches hold
W_('hat-front-embroidery.svg', svg(225, 225, emb(112.5, 112.5, 0.44, O, star_r=(32, 23), ring_w=16), title='Free Eva hat front, embroidery'))
W_('hat-back-embroidery.svg', svg(300, 50, T('BlackOps.ttf', 'FREE EVA', 44, 150, 41, O), title='Free Eva hat back, embroidery'))
# 5. Pen imprint, 2 x 0.3 in, one ink
p = emb(15, 15, 0.058, K) + T('BlackOps.ttf', 'FREE EVA', 17, 34, 21.5, K, 'start') + T('Inter-600.ttf', '· evaxie.us', 13, 34 + text_width('BlackOps.ttf', 'FREE EVA', 17) + 5, 21, K, 'start')
W_('pen-imprint.svg', svg(200, 30, p, title='Free Eva pen imprint'))
print('ok')
# pen: text only (the emblem is unreadable at pen size)
tw = text_width('BlackOps.ttf', 'FREE EVA', 17) + 5 + text_width('Inter-600.ttf', '· evaxie.us', 13)
x0 = 100 - tw/2
p = T('BlackOps.ttf', 'FREE EVA', 17, x0, 21.5, K, 'start') + T('Inter-600.ttf', '· evaxie.us', 13, x0 + text_width('BlackOps.ttf', 'FREE EVA', 17) + 5, 21, K, 'start')
W_('pen-imprint.svg', svg(200, 30, p, title='Free Eva pen imprint'))
# digital: phone wallpaper and video-call backgrounds
DIG = sys.argv[2]; os.makedirs(DIG, exist_ok=True)
glow = lambda w, h, cx, cy, r: (f'<defs><radialGradient id="g" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">'
    f'<stop offset="0" stop-color="#3a2410"/><stop offset="1" stop-color="{K}"/></radialGradient></defs><rect width="{w}" height="{h}" fill="url(#g)"/>')
ph = glow(1290, 2796, 645, 1150, 1100) + mark(645, 1150, 1.9)
ph += T('BlackOps.ttf', 'FREE EVA', 190, 645, 1900, O)
ph += T('BigShoulders.ttf', 'MUTUAL RESPECT', 110, 645, 2040, W, tr=0.04)
ph += T('NotoSerifTC.ttf', '中美相互尊重', 72, 645, 2150, W, tr=0.2, op=0.85)
ph += T('Inter-600.ttf', 'evaxie.us', 52, 645, 2560, W, op=0.6)
open(os.path.join(DIG, 'wallpaper-phone.svg'), 'w').write(svg(1290, 2796, ph, title='Free Eva phone wallpaper'))
# video call: emblem and words to the right, the middle stays calm for your face
z = glow(1920, 1080, 1560, 470, 700) + mark(1560, 420, 1.0)
z += T('BlackOps.ttf', 'FREE EVA', 96, 1560, 790, O)
z += T('BigShoulders.ttf', 'MUTUAL RESPECT', 58, 1560, 865, W, tr=0.04)
z += T('NotoSerifTC.ttf', '中美相互尊重', 40, 1560, 925, W, tr=0.2, op=0.85)
z += T('Inter-600.ttf', 'evaxie.us', 30, 1560, 990, W, op=0.6)
open(os.path.join(DIG, 'video-background-dark.svg'), 'w').write(svg(1920, 1080, z, title='Free Eva video call background'))
zl = (f'<rect width="1920" height="1080" fill="#F7F5F2"/>' + mark(1560, 420, 1.0)
     + T('BlackOps.ttf', 'FREE EVA', 96, 1560, 790, O) + T('BigShoulders.ttf', 'MUTUAL RESPECT', 58, 1560, 865, K, tr=0.04)
     + T('NotoSerifTC.ttf', '中美相互尊重', 40, 1560, 925, K, tr=0.2, op=0.85) + T('Inter-600.ttf', 'evaxie.us', 30, 1560, 990, K, op=0.6))
open(os.path.join(DIG, 'video-background-light.svg'), 'w').write(svg(1920, 1080, zl, title='Free Eva video call background, light'))
