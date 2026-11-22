"""Generate Free Eva logo SVGs with all text converted to outlines."""
import math, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

F = '/tmp/claude-0/fonts/'
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
ORANGE = '#E77500'
BLACK = '#151515'
WHITE = '#FFFFFF'

_fonts = {}
def font(name):
    if name not in _fonts:
        t = TTFont(F + name)
        _fonts[name] = (t, t.getGlyphSet(), t.getBestCmap(), t['hmtx'], t['head'].unitsPerEm)
    return _fonts[name]

def text_width(name, text, size, tracking=0):
    t, gs, cmap, hmtx, upm = font(name)
    w = sum(hmtx[cmap[ord(c)]][0] for c in text) * size / upm
    return w + tracking * size * (len(text) - 1)

def text_path(name, text, size, x, y, anchor='start', tracking=0):
    """Return SVG path 'd' for text with baseline at y."""
    t, gs, cmap, hmtx, upm = font(name)
    s = size / upm
    w = text_width(name, text, size, tracking)
    if anchor == 'middle': x -= w / 2
    elif anchor == 'end': x -= w
    pen = SVGPathPen(gs)
    cx = x
    for c in text:
        g = cmap[ord(c)]
        tp = TransformPen(pen, (s, 0, 0, -s, cx, y))
        gs[g].draw(tp)
        cx += hmtx[g][0] * s + tracking * size
    return pen.getCommands()

def mark(fg=WHITE, accent=ORANGE, cx=256, cy=256, scale=1.0):
    """Ring with an opening + mortarboard. Designed on a 512 grid."""
    def P(x, y):
        return f'{cx + (x - 256) * scale:.2f},{cy + (y - 256) * scale:.2f}'
    r, sw = 222 * scale, 34 * scale
    # opening in the ring at the upper right (the door that should be open)
    a1, a2 = math.radians(-28), math.radians(-62)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
    ring = (f'<path d="M{x1:.2f},{y1:.2f} A{r:.2f},{r:.2f} 0 1 1 {x2:.2f},{y2:.2f}" '
            f'fill="none" stroke="{accent}" stroke-width="{sw:.2f}" stroke-linecap="butt"/>')
    board = f'<path d="M{P(256,140)} L{P(412,206)} L{P(256,272)} L{P(100,206)} Z" fill="{fg}"/>'
    base = (f'<path d="M{P(168,246)} L{P(168,318)} Q{P(256,366)} {P(344,318)} '
            f'L{P(344,246)} L{P(256,284)} Z" fill="{fg}"/>')
    tassel = (f'<path d="M{P(256,206)} L{P(378,230)} L{P(378,318)}" fill="none" stroke="{accent}" '
              f'stroke-width="{9*scale:.2f}" stroke-linejoin="round" stroke-linecap="round"/>'
              f'<path d="M{P(366,312)} L{P(390,312)} L{P(396,356)} L{P(360,356)} Z" fill="{accent}"/>'
              f'<circle cx="{cx:.2f}" cy="{cy + (206-256)*scale:.2f}" r="{11*scale:.2f}" fill="{accent}"/>')
    return ring + board + base + tassel

def svg(w, h, body, bg=None, title='Free Eva'):
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{bgr}{body}</svg>\n')

def write(name, content):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(content)

def variants(fg):
    return fg, (WHITE if fg == WHITE else BLACK)

for theme, fg, bg in [('dark', WHITE, BLACK), ('light', BLACK, None)]:
    # 1. Icon mark (square)
    write(f'mark-{theme}.svg', svg(512, 512, mark(fg), None, 'Free Eva mark'))
    if theme == 'dark':
        write('app-icon.svg', svg(512, 512, f'<rect width="512" height="512" rx="96" fill="{BLACK}"/>' + mark(fg, scale=0.86), None, 'Free Eva'))
    # 2. Stacked lockup
    W, H = 900, 930
    body = mark(fg, cx=450, cy=270, scale=0.95)
    body += f'<path d="{text_path("BlackOps.ttf", "FREE EVA", 150, 450, 690, "middle")}" fill="{ORANGE}"/>'
    body += f'<path d="{text_path("NotoSerifTC.ttf", "釋放謝翌", 118, 450, 850, "middle", 0.06)}" fill="{fg}"/>'
    write(f'logo-stacked-{theme}.svg', svg(W, H, body, bg, 'Free Eva 釋放謝翌'))
    # 3. Horizontal lockup (site header)
    W, H = 1320, 400
    body = mark(fg, cx=200, cy=200, scale=0.62)
    body += f'<path d="{text_path("BlackOps.ttf", "FREE EVA", 170, 400, 222)}" fill="{ORANGE}"/>'
    body += f'<path d="{text_path("NotoSerifTC.ttf", "釋放謝翌", 92, 404, 340, tracking=0.12)}" fill="{fg}"/>'
    tw = text_width("NotoSerifTC.ttf", "釋放謝翌", 92, 0.12)
    body += f'<path d="{text_path("BigShoulders.ttf", "WE ARE EVA", 66, 404 + tw + 40, 334, tracking=0.06)}" fill="{fg}" fill-opacity="0.75"/>'
    write(f'logo-horizontal-{theme}.svg', svg(W, H, body, bg, 'Free Eva 釋放謝翌'))

print('ok', text_width("BlackOps.ttf", "FREE EVA", 170))
