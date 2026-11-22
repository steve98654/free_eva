import math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
src = open(os.path.join(HERE, 'final.py')).read()
exec(src.split('# 1 mark only')[0].replace("OUT = sys.argv[1]", "OUT = sys.argv[1]"))
GOLD = '#F2B134'
_n = [0]
def mono(cx, cy, s, col):
    """Single-ink mark; US is knocked out so the background shows through."""
    _n[0] += 1; mid = f'm{_n[0]}'
    R, rr = 165*s, 222*s
    us = text_path("BlackOps.ttf", "US", 74*s, cx, cy + R/2 + 26*s, "middle")
    g = (f'<defs><mask id="{mid}" maskUnits="userSpaceOnUse" x="{cx-300*s}" y="{cy-300*s}" width="{600*s}" height="{600*s}">'
         f'<rect x="{cx-300*s}" y="{cy-300*s}" width="{600*s}" height="{600*s}" fill="#fff"/><path d="{us}" fill="#000"/></mask></defs>'
         f'<g fill="{col}"><circle cx="{cx}" cy="{cy}" r="{R:.2f}" fill="none" stroke="{col}" stroke-width="{10*s:.2f}"/>'
         f'<path d="{half(cx,cy,R,"L")}" mask="url(#{mid})"/>')
    for i in range(13):
        a = math.radians(-90 + i*360/13)
        g += star(cx + rr*math.cos(a), cy + rr*math.sin(a), (25 if i == 0 else 16)*s, col)
    g += f'<path d="{text_path("NotoSerifTC.ttf", "中", 104*s, cx, cy - R/2 + 37*s, "middle")}"/></g>'
    return g
def arc_text(font, text, size, cx, cy, r, center_deg, col, bottom=False, tracking=0.08):
    t, gs, cmap, hmtx, upm = font_(font)
    widths = [hmtx[cmap[ord(c)]][0]*size/upm + tracking*size for c in text]
    total = sum(widths) - tracking*size
    ang = total / r
    out = ''
    a = math.radians(center_deg) - (ang/2 if not bottom else -ang/2)
    for c, w in zip(text, widths):
        step = w / r
        mid = a + (step/2 if not bottom else -step/2)
        deg = math.degrees(mid)
        gw = w - tracking*size
        if not bottom:
            p = text_path(font, c, size, cx - gw/2, cy - r, 'start')
            out += f'<path d="{p}" fill="{col}" transform="rotate({deg-(-90):.3f} {cx} {cy})"/>'
        else:
            p = text_path(font, c, size, cx - gw/2, cy + r + size*0.72, 'start')
            out += f'<path d="{p}" fill="{col}" transform="rotate({deg-90:.3f} {cx} {cy})"/>'
        a += step if not bottom else -step
    return out
def font_(name): return font(name)
def W_(n, c): open(os.path.join(OUT, n), 'w').write(c)

# ---------- single colour
W_('mono-white.svg', svg(520, 520, mono(260, 268, 1, W), title='Free Eva mark, white'))
W_('mono-black.svg', svg(520, 520, mono(260, 268, 1, K), title='Free Eva mark, black'))
W_('mono-black-on-orange.svg', svg(800, 860, mono(400, 300, 1, K)
   + f'<path d="{text_path("BigShoulders.ttf", "MUTUAL RESPECT", 100, 400, 640, "middle", 0.03)}" fill="{K}"/>'
   + f'<path d="{text_path("NotoSerifTC.ttf", "中美相互尊重", 54, 400, 718, "middle", 0.15)}" fill="{K}"/>'
   + f'<path d="{text_path("BlackOps.ttf", "STEP ONE: FREE EVA", 44, 400, 798, "middle")}" fill="{W}"/>', bg=O, title='Free Eva, black on orange'))
# ---------- shirt / print: stacked, transparent, white text
foot_w = (f'<path d="{text_path("BigShoulders.ttf", "MUTUAL RESPECT", 100, 400, 640, "middle", 0.03)}" fill="{W}"/>'
          f'<path d="{text_path("NotoSerifTC.ttf", "中美相互尊重", 54, 400, 718, "middle", 0.15)}" fill="{W}"/>'
          f'<path d="{text_path("BlackOps.ttf", "STEP ONE: FREE EVA", 44, 400, 798, "middle")}" fill="{O}"/>')
W_('print-stacked-transparent.svg', svg(800, 860, mono(400, 300, 1, O) + foot_w, title='Free Eva print artwork'))
# ---------- Chinese-language lockup
zh = (mark(400, 300) + f'<path d="{text_path("NotoSerifTC.ttf", "釋放謝翌", 120, 400, 668, "middle", 0.1)}" fill="{O}"/>'
      + f'<path d="{text_path("NotoSerifTC.ttf", "中美相互尊重", 66, 400, 780, "middle", 0.2)}" fill="{W}"/>')
W_('logo-chinese-dark.svg', svg(800, 860, zh, bg=K, title='釋放謝翌 中美相互尊重'))
# ---------- round sticker / button
st = (f'<circle cx="400" cy="400" r="396" fill="{O}"/><circle cx="400" cy="400" r="300" fill="{K}"/>'
      + arc_text("BlackOps.ttf", "FREE EVA", 62, 400, 400, 322, -90, K, tracking=0.12)
      + arc_text("BigShoulders.ttf", "MUTUAL RESPECT", 54, 400, 400, 312, 90, K, bottom=True, tracking=0.08)
      + star(400-300-48+15, 400, 18, K).replace('', '') + star(400+300+33, 400, 18, K)
      + mark(400, 410, 1.08, us_col=K))
W_('sticker-round.svg', svg(800, 800, st, title='Free Eva sticker'))
# ---------- social: avatar (circle-safe)
W_('social-avatar.svg', svg(1080, 1080, mark(540, 552, 1.75), bg=K, title='Free Eva'))
# ---------- social: share card 1200x630
sc = mark(285, 322, 1.0)
sc += f'<path d="{text_path("BlackOps.ttf", "FREE EVA", 108, 570, 250)}" fill="{O}"/>'
sc += f'<path d="{text_path("BigShoulders.ttf", "MUTUAL RESPECT", 78, 574, 350, tracking=0.03)}" fill="{W}"/>'
sc += f'<path d="{text_path("NotoSerifTC.ttf", "中美相互尊重", 50, 576, 430, tracking=0.18)}" fill="{W}" fill-opacity=".85"/>'
sc += f'<path d="{text_path("VT323.ttf", "evaxie.us", 52, 576, 520)}" fill="{W}"/>'
W_('social-share-card.svg', svg(1200, 630, sc, bg=K, title='Free Eva share card'))
# ---------- X header 1500x500 and Facebook cover 1640x624 (keep content centred for avatar overlap)
def banner(w, h, s, cx):
    b = mark(cx, h/2 + 8*s, 0.8*s)
    tx = cx + 240*s
    b += f'<path d="{text_path("BlackOps.ttf", "FREE EVA", 120*s, tx, h/2 - 22*s)}" fill="{O}"/>'
    b += f'<path d="{text_path("BigShoulders.ttf", "MUTUAL RESPECT · 中美相互尊重".split(" · ")[0], 70*s, tx+4*s, h/2 + 70*s, tracking=0.03)}" fill="{W}"/>'
    mw = text_width("BigShoulders.ttf", "MUTUAL RESPECT", 70*s, 0.03)
    b += f'<path d="{text_path("NotoSerifTC.ttf", "中美相互尊重", 46*s, tx + mw + 30*s, h/2 + 66*s, tracking=0.15)}" fill="{W}" fill-opacity=".85"/>'
    b += f'<path d="{text_path("VT323.ttf", "evaxie.us", 40*s, tx+6*s, h/2 + 138*s)}" fill="{W}" fill-opacity=".8"/>'
    return svg(w, h, b, bg=K, title='Free Eva banner')
W_('social-banner-x.svg', banner(1500, 500, 1.0, 430))
W_('social-banner-facebook.svg', banner(1640, 624, 1.15, 420))
print('ok')
