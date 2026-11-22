import math, sys, os, re
D = sys.argv[1]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yy9.py')).read()
exec(src.split('L = []')[0].replace('D = sys.argv[1]', ''))
CX, CY, R = 400, 258, 165
TOP = (CX, CY - R/2)   # black lobe -> China, drawn orange
BOT = (CX, CY + R/2)   # orange lobe -> US, drawn black
def base():
    s = (f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{O}" stroke-width="10"/>'
         f'<path d="{half(CX,CY,R,"L")}" fill="{O}"/>')
    for i in range(13):
        a = math.radians(-90 + i*360/13)
        s += star(CX + 222*math.cos(a), CY + 222*math.sin(a), 16, O)
    return s
def t(x, y, txt, font, size, col, dy, extra=''):
    return f'<text x="{x}" y="{y+dy}" text-anchor="middle" font-family="{font}" font-size="{size}" fill="{col}" {extra}>{txt}</text>'
# --- symbol painters: (x,y) center, c = symbol colour, bg = lobe colour
def zhong(x, y, c, bg): return t(x, y, '中', 'SerifTC', 104, c, 37, 'font-weight="900"')
def mei(x, y, c, bg): return t(x, y, '美', 'SerifTC', 100, c, 35, 'font-weight="900"')
def us(x, y, c, bg): return t(x, y, 'US', 'BlackOps', 74, c, 26)
def prc_stars(x, y, c, bg):
    s = star(x-20, y-4, 32, c)
    for ang in (-50, -18, 14, 46):
        a = math.radians(ang); s += star(x+8+42*math.cos(a), y-4+42*math.sin(a), 10, c)
    return s
def ring13(x, y, c, bg):
    return ''.join(star(x+44*math.cos(math.radians(-90+i*360/13)), y+44*math.sin(math.radians(-90+i*360/13)), 8, c) for i in range(13))
def plum(x, y, c, bg):
    s = ''.join(f'<circle cx="{x+24*math.cos(math.radians(-90+i*72)):.1f}" cy="{y+24*math.sin(math.radians(-90+i*72)):.1f}" r="21" fill="{c}"/>' for i in range(5))
    s += f'<circle cx="{x}" cy="{y}" r="11" fill="{bg}"/>'
    for i in range(5):
        a = math.radians(-54 + i*72); s += f'<circle cx="{x+14*math.cos(a):.1f}" cy="{y+14*math.sin(a):.1f}" r="3" fill="{bg}"/>'
    return s
def bigstar(x, y, c, bg): return star(x, y+4, 54, c)
def lantern(x, y, c, bg):
    return (f'<rect x="{x-18}" y="{y-46}" width="36" height="10" rx="2" fill="{c}"/><ellipse cx="{x}" cy="{y}" rx="44" ry="38" fill="{c}"/>'
            f'<path d="M{x-16},{y-36} Q{x-30},{y} {x-16},{y+36} M{x},{y-38} V{y+38} M{x+16},{y-36} Q{x+30},{y} {x+16},{y+36}" fill="none" stroke="{bg}" stroke-width="3"/>'
            f'<rect x="{x-18}" y="{y+36}" width="36" height="10" rx="2" fill="{c}"/><path d="M{x},{y+46} V{y+66}" stroke="{c}" stroke-width="5"/>'
            f'<path d="M{x},{y-46} V{y-58}" stroke="{c}" stroke-width="4"/>')
def bell(x, y, c, bg):
    return (f'<rect x="{x-24}" y="{y-56}" width="48" height="10" rx="3" fill="{c}"/><rect x="{x-5}" y="{y-47}" width="10" height="8" fill="{c}"/>'
            f'<path d="M{x-24},{y-40} Q{x-30},{y-40} {x-30},{y-30} L{x-34},{y+16} Q{x-36},{y+30} {x-52},{y+40} H{x+52} Q{x+36},{y+30} {x+34},{y+16} L{x+30},{y-30} Q{x+30},{y-40} {x+24},{y-40} Z" fill="{c}"/>'
            f'<path d="M{x-14},{y+40} L{x-10},{y+22} L{x-16},{y+10} L{x-11},{y-4}" fill="none" stroke="{bg}" stroke-width="3"/>'
            f'<circle cx="{x}" cy="{y+50}" r="7" fill="{c}"/>')
def temple(x, y, c, bg):
    s = ''
    for i, (w, yy_) in enumerate([(44, y-40), (66, y-14), (88, y+12)]):
        s += f'<path d="M{x-w/2-8},{yy_+12} Q{x},{yy_-8} {x+w/2+8},{yy_+12} Z" fill="{c}"/>'
        s += f'<rect x="{x-w/2+6}" y="{yy_+12}" width="{w-12}" height="12" fill="{c}"/>'
    s += f'<path d="M{x},{y-58} V{y-44}" stroke="{c}" stroke-width="5"/><circle cx="{x}" cy="{y-60}" r="5" fill="{c}"/>'
    s += f'<rect x="{x-58}" y="{y+38}" width="116" height="10" fill="{c}"/><rect x="{x-50}" y="{y+48}" width="100" height="8" fill="{c}"/>'
    return s
def capitol(x, y, c, bg):
    s = f'<path d="M{x},{y-62} V{y-48}" stroke="{c}" stroke-width="5"/><rect x="{x-6}" y="{y-50}" width="12" height="10" fill="{c}"/>'
    s += f'<path d="M{x-36},{y-4} A36,40 0 0 1 {x+36},{y-4} Z" fill="{c}"/>'
    s += f'<rect x="{x-40}" y="{y-4}" width="80" height="22" fill="{c}"/>'
    for i in range(5): s += f'<rect x="{x-32+i*15}" y="{y}" width="5" height="16" fill="{bg}"/>'
    s += f'<rect x="{x-62}" y="{y+18}" width="124" height="12" fill="{c}"/><rect x="{x-66}" y="{y+32}" width="132" height="16" fill="{c}"/>'
    return s
def tower(x, y, c, bg):
    s = f'<rect x="{x-46}" y="{y-30}" width="92" height="84" fill="{c}"/>'
    for i in range(5): s += f'<rect x="{x-46+i*20}" y="{y-48}" width="12" height="20" fill="{c}"/>'
    s += f'<path d="M{x-16},{y+54} V{y+20} A16,16 0 0 1 {x+16},{y+20} V{y+54} Z" fill="{bg}"/>'
    s += f'<rect x="{x-30}" y="{y-14}" width="12" height="16" fill="{bg}"/><rect x="{x+18}" y="{y-14}" width="12" height="16" fill="{bg}"/>'
    s += f'<rect x="{x-82}" y="{y+16}" width="36" height="38" fill="{c}"/><rect x="{x+46}" y="{y+16}" width="36" height="38" fill="{c}"/>'
    for xx in (x-82, x-62, x+50, x+70): s += f'<rect x="{xx}" y="{y+6}" width="12" height="12" fill="{c}"/>'
    return s
def torch(x, y, c, bg):
    return (f'<path d="M{x},{y-64} C{x+26},{y-36} {x+34},{y-18} {x+22},{y-2} Q{x+12},{y+8} {x},{y+8} Q{x-12},{y+8} {x-22},{y-2} C{x-34},{y-18} {x-26},{y-36} {x},{y-64} Z" fill="{c}"/>'
            f'<path d="M{x},{y-30} C{x+10},{y-18} {x+12},{y-8} {x},{y+2} C{x-12},{y-8} {x-10},{y-18} {x},{y-30} Z" fill="{bg}"/>'
            f'<path d="M{x-30},{y+14} H{x+30} L{x+20},{y+32} H{x-20} Z" fill="{c}"/><rect x="{x-9}" y="{y+32}" width="18" height="34" rx="3" fill="{c}"/>')
def chop(x, y, c, bg):
    return (f'<rect x="{x-50}" y="{y-50}" width="100" height="100" rx="12" fill="{c}"/>'
            f'<rect x="{x-42}" y="{y-42}" width="84" height="84" rx="6" fill="none" stroke="{bg}" stroke-width="4"/>'
            + t(x, y, '中', 'SerifTC', 76, bg, 27, 'font-weight="900"'))
def shield(x, y, c, bg):
    p = f'M{x-46},{y-52} H{x+46} V{y+2} Q{x+46},{y+40} {x},{y+58} Q{x-46},{y+40} {x-46},{y+2} Z'
    s = f'<path d="{p}" fill="{c}"/><path d="M{x-46},{y-24} H{x+46}" stroke="{bg}" stroke-width="5"/>'
    for i in range(6): s += f'<rect x="{x-36+i*14}" y="{y-16}" width="6" height="66" fill="{bg}"/>'
    return f'<defs><clipPath id="shc"><path d="{p}"/></clipPath></defs><path d="{p}" fill="{c}"/><g clip-path="url(#shc)"><path d="M{x-46},{y-24} H{x+46}" stroke="{bg}" stroke-width="5"/>' + ''.join(f'<rect x="{x-38+i*14}" y="{y-16}" width="6" height="80" fill="{bg}"/>' for i in range(6)) + '</g>'
def paddle(x, y, c, bg):
    return (f'<g transform="rotate(-35 {x} {y})"><rect x="{x-9}" y="{y+18}" width="18" height="46" rx="6" fill="{c}"/><circle cx="{x}" cy="{y-8}" r="38" fill="{c}"/></g>'
            f'<circle cx="{x+46}" cy="{y-40}" r="10" fill="{c}"/>')
def baseball(x, y, c, bg):
    return (f'<circle cx="{x}" cy="{y}" r="50" fill="{c}"/>'
            f'<path d="M{x-30},{y-40} Q{x-10},{y} {x-30},{y+40}" fill="none" stroke="{bg}" stroke-width="4" stroke-dasharray="6 5"/>'
            f'<path d="M{x+30},{y-40} Q{x+10},{y} {x+30},{y+40}" fill="none" stroke="{bg}" stroke-width="4" stroke-dasharray="6 5"/>')
PAIRS = [
 ('Zhong and Mei (中 / 美)', zhong, mei, 'The two characters of 中美, "China–US". 中 (middle) sits in the dark half and 美 (beautiful, short for America) in the orange half.'),
 ('Zhong and US (中 / US)', zhong, us, '中 in one half and US in the other. The most direct pairing, readable in both languages at a glance.'),
 ('Five Stars and Thirteen Stars', prc_stars, ring13, 'The five-star cluster from China\'s flag and the 13-star ring from the 1777 American flag, each tucked inside the other\'s color.'),
 ('Plum Blossom and Star', plum, bigstar, 'The plum blossom, a long-loved Chinese emblem of resilience, opposite a single American star.'),
 ('Lantern and Liberty Bell', lantern, bell, 'A Chinese paper lantern facing the Liberty Bell: a light and a bell, both symbols of celebration and freedom.'),
 ('Temple of Heaven and Capitol', temple, capitol, 'Beijing\'s Temple of Heaven and the US Capitol dome, two landmark buildings, each holding the place of a dot.'),
 ('Great Wall and Liberty Torch', tower, torch, 'A Great Wall watchtower and the Statue of Liberty\'s torch, the two most recognizable landmarks of each country.'),
 ('Seal and Shield', chop, shield, 'A square Chinese seal carved with 中, opposite the striped shield from the US Great Seal. Two national seals, one circle.'),
 ('Ping-Pong and Baseball', paddle, baseball, 'Each country\'s favorite game: a ping-pong paddle (a nod to 1971 ping-pong diplomacy) opposite a baseball.'),
]
L = []
for name, cn, usf, desc in PAIRS:
    b = base() + cn(TOP[0], TOP[1], O, K) + usf(BOT[0], BOT[1], K, O)
    L.append((name, desc, b + foot))
CSS = open(os.path.join(D, '..', 'hero', 'base.css')).read().split(':root')[0] + '*{margin:0}body{background:#151515}'
for i, (name, desc, body) in enumerate(L, 1):
    slug = f'symbols-{i}-' + (re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') or 'zhong-mei')
    open(os.path.join(D, slug + '.html'), 'w').write(
        f'<html data-size="800x800"><head><style>{CSS}html,body{{width:800px;height:800px;overflow:hidden}}</style></head><body><svg viewBox="0 0 800 800" width="800" height="800">{body}</svg></body></html>')
def uniq(body, i): return re.sub(r'(id="|url\(#|href="#)(\w+)', lambda m: f'{m.group(1)}{m.group(2)}{i}', body)
cells = ''.join(f'<div class=c><svg viewBox="0 0 800 800">{uniq(body,i)}</svg><h3><b>{i}</b> {name}</h3><p>{desc}</p></div>' for i, (name, desc, body) in enumerate(L, 1))
open(os.path.join(D, 'symbols-ideas-sheet.html'), 'w').write(f'''<html data-size="1800x2480"><head><style>{CSS}
html,body{{width:1800px;height:2480px;overflow:hidden;background:#151515;color:#fff;font-family:Inter}}
.hd{{padding:56px 64px 8px;display:flex;justify-content:space-between;align-items:baseline}}
.hd h1{{font-family:Shoulders;font-weight:800;font-size:64px;letter-spacing:2px}}.hd h1 span{{color:#E77500}}.hd em{{color:#aaa;font-size:24px;font-style:normal}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;padding:28px 64px}}
.c{{background:#1e1e1e;border-radius:14px;padding:24px 24px 28px}}.c svg{{width:100%;aspect-ratio:1;display:block;background:#151515;border-radius:8px}}
.c h3{{font-size:28px;margin-top:20px}}.c h3 b{{color:#E77500;margin-right:6px}}.c p{{color:#bdbdbd;font-size:19px;line-height:1.4;margin-top:8px;height:108px}}
</style></head><body><div class=hd><h1>SYMBOL DOTS <span>· 9 China / US pairs</span></h1><em>China in the dark half, US in the orange</em></div><div class=g>{cells}</div></body></html>''')
for i, (name, desc, _) in enumerate(L, 1): print(f'{i}. {name}: {desc}')
