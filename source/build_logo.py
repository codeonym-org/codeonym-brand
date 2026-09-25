"""Generate the codeonym logo kit as pure-path SVGs (no font dependency).

Concept — the mark reads left to right as the brand statement:
  hexagon  = rank badge / game gem        -> gamification
  < >      = code brackets                -> software
  sparkle  = the universal "AI" glyph      -> AI agents
  XP bar   = segmented progress, 4/5 full -> levelling up
The colors come from the portfolio's "System" theme (arcane, system, rank-S).

Run: python build_logo.py  (needs fonttools + brotli for the Michroma .woff2)
"""
import math
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'svg')
MICHROMA = os.path.expanduser('~/apps/portfolio/src/fonts/michroma-latin.woff2')
MONO = '/usr/share/fonts/TTF/JetBrainsMono-SemiBold.ttf'

NAME = 'CODEONYM'
TAGLINE = 'GAMIFYING AI AGENTS & SOFTWARE'


# ---------- color: portfolio tokens (OKLCH) -> sRGB hex ----------
def oklch(l, c, h):
    a, b = c * math.cos(math.radians(h)), c * math.sin(math.radians(h))
    l_, m_, s_ = (l + 0.3963377774 * a + 0.2158037573 * b) ** 3, (l - 0.1055613458 * a - 0.0638541728 * b) ** 3, (l - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
           -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
           -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
    enc = lambda x: 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
    return '#' + ''.join(f'{round(max(0, min(1, enc(v))) * 255):02x}' for v in rgb)


ARCANE, ARCANE_HOT = oklch(0.62, 0.22, 295), oklch(0.74, 0.17, 300)
SYSTEM, RANK_S = oklch(0.76, 0.14, 230), oklch(0.80, 0.15, 80)
VOID, INK, PAPER = '#05040b', '#15102a', '#f4f2fb'


# ---------- text -> path ----------
class Font:
    def __init__(self, path):
        self.f = TTFont(path)
        self.gs, self.cmap = self.f.getGlyphSet(), self.f.getBestCmap()
        self.upm = self.f['head'].unitsPerEm
        self.cap = self.f['OS/2'].sCapHeight

    def path(self, text, x, baseline, cap_px, tracking=0.0):
        """Return (svg path d, advance width px); cap_px = rendered cap height."""
        s = cap_px / self.cap
        pen, cx = SVGPathPen(self.gs), x
        for ch in text:
            g = self.cmap[ord(ch)]
            self.gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, baseline)))
            cx += self.gs[g].width * s + tracking * cap_px
        return pen.getCommands(), cx - x - tracking * cap_px


# ---------- the mark (drawn in a 512 box) ----------
def hexagon(cx, cy, r):
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(-90, 270, 60)]
    return 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in pts) + ' Z'


def sparkle(cx, cy, r, pinch=0.16):
    """4-point AI star with concave sides."""
    k = r * pinch
    return (f'M{cx},{cy - r} C{cx + k},{cy - k} {cx + k},{cy - k} {cx + r},{cy} '
            f'C{cx + k},{cy + k} {cx + k},{cy + k} {cx},{cy + r} '
            f'C{cx - k},{cy + k} {cx - k},{cy + k} {cx - r},{cy} '
            f'C{cx - k},{cy - k} {cx - k},{cy - k} {cx},{cy - r} Z')


def mark(style, uid):
    """style: color-dark | color-light | black | white. Returns (defs, body)."""
    mono = style in ('black', 'white')
    solid = {'black': INK, 'white': '#ffffff'}.get(style)
    frame = solid or f'url(#{uid}-edge)'
    code = solid or (PAPER if style == 'color-dark' else INK)
    star = solid or f'url(#{uid}-core)'
    xp_on = solid or RANK_S
    defs = '' if mono else f'''
    <linearGradient id="{uid}-edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{ARCANE_HOT}"/><stop offset=".55" stop-color="{ARCANE}"/><stop offset="1" stop-color="{SYSTEM}"/>
    </linearGradient>
    <linearGradient id="{uid}-core" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{SYSTEM}"/><stop offset="1" stop-color="{ARCANE_HOT}"/>
    </linearGradient>
    <radialGradient id="{uid}-aura" cx=".5" cy=".46" r=".5">
      <stop offset="0" stop-color="{ARCANE}" stop-opacity=".45"/><stop offset="1" stop-color="{ARCANE}" stop-opacity="0"/>
    </radialGradient>'''
    aura = f'<circle cx="256" cy="236" r="190" fill="url(#{uid}-aura)"/>' if style == 'color-dark' else ''

    # XP bar: 5 segments, 4 earned
    segs, x0, w, gap, y, h = [], 176, 26, 8, 338, 14
    for i in range(5):
        xi = x0 + i * (w + gap)
        if i < 4:
            segs.append(f'<rect x="{xi}" y="{y}" width="{w}" height="{h}" rx="3" fill="{xp_on}"/>')
        else:
            segs.append(f'<rect x="{xi + 1.5}" y="{y + 1.5}" width="{w - 3}" height="{h - 3}" rx="2.5" fill="none" stroke="{xp_on}" stroke-width="3" opacity="{1 if mono else .55}"/>')

    body = f'''{aura}
    <path d="{hexagon(256, 256, 222)}" fill="none" stroke="{frame}" stroke-width="24" stroke-linejoin="round"/>
    <path d="{hexagon(256, 256, 186)}" fill="none" stroke="{frame}" stroke-width="4" stroke-linejoin="round" opacity="{.8 if mono else .45}"/>
    <g fill="none" stroke="{code}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round">
      <path d="M178,178 L122,236 L178,294"/>
      <path d="M334,178 L390,236 L334,294"/>
    </g>
    <path d="{sparkle(256, 240, 62)}" fill="{star}"/>
    <path d="{sparkle(297, 184, 14, .2)}" fill="{star}"/>
    {"".join(segs)}'''
    return defs, body


# ---------- assemble ----------
MICH, JBM = Font(MICHROMA), Font(MONO)


def svg(w, h, defs, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">'
            f'<title>codeonym</title><defs>{defs}</defs>{rect}{body}</svg>\n')


def words(style, x, top, cap, align='left', width=None):
    """Wordmark + tagline. Returns (body, width, height)."""
    name_fill = {'color-dark': PAPER, 'color-light': INK, 'black': INK, 'white': '#ffffff'}[style]
    tag_fill = {'color-dark': SYSTEM, 'color-light': ARCANE, 'black': INK, 'white': '#ffffff'}[style]
    _, nw = MICH.path(NAME, 0, 0, cap, .22)
    tcap = cap * .34
    _, tw = JBM.path(TAGLINE, 0, 0, tcap, .5)
    tw_target = nw  # tagline justified to the wordmark width
    ttrack = .5 + (tw_target - tw) / (tcap * (len(TAGLINE) - 1))
    if align == 'center':
        x = (width - nw) / 2
    nd, _ = MICH.path(NAME, x, top + cap, cap, .22)
    td, _ = JBM.path(TAGLINE, x, top + cap * 1.62 + tcap, tcap, ttrack)
    rule_y = top + cap * 1.36
    rule_x = x + (nw * .41 if align == 'center' else 0)
    body = (f'<path d="{nd}" fill="{name_fill}"/>'
            f'<rect x="{rule_x:.1f}" y="{rule_y:.1f}" width="{nw * .18:.1f}" height="{cap * .05:.1f}" fill="{tag_fill}"/>'
            f'<path d="{td}" fill="{tag_fill}"/>')
    return body, nw, cap * 1.62 + tcap


BG = {'color-dark': VOID, 'color-light': PAPER, 'black': None, 'white': None}


def build(style, bg=False):
    b = BG[style] if bg else None
    out = {}
    d, m = mark(style, 'm')
    out['mark'] = svg(512, 512, d, m, b)

    # horizontal: mark 240px, wordmark to the right
    body, nw, th = words(style, 290, 0, 64)
    H = 280
    wy = (H - th) / 2
    body, nw, th = words(style, 290, wy, 64)
    W = 290 + nw + 30
    out['logo-horizontal'] = svg(W, H, d, f'<g transform="translate(20,20) scale({240 / 512})">{m}</g>{body}', b)

    # stacked
    cap = 72
    _, nw, _ = words(style, 0, 0, cap)
    W = nw + 120
    body, nw, th = words(style, 0, 400, cap, 'center', W)
    out['logo-stacked'] = svg(W, 400 + th + 60, d, f'<g transform="translate({(W - 360) / 2},30) scale({360 / 512})">{m}</g>{body}', b)

    # wordmark only
    body, nw, th = words(style, 20, 20, 64)
    out['wordmark'] = svg(nw + 40, th + 40, '', body, b)
    return out


def favicon():
    """Small-size mark (<= 48 px): same idea, heavier strokes, no fine detail."""
    return svg(512, 512, f'''
    <linearGradient id="f-edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{ARCANE_HOT}"/><stop offset=".55" stop-color="{ARCANE}"/><stop offset="1" stop-color="{SYSTEM}"/>
    </linearGradient>''', f'''
    <path d="{hexagon(256, 256, 214)}" fill="{VOID}" stroke="url(#f-edge)" stroke-width="44" stroke-linejoin="round"/>
    <g fill="none" stroke="{PAPER}" stroke-width="44" stroke-linecap="round" stroke-linejoin="round">
      <path d="M170,168 L104,240 L170,312"/><path d="M342,168 L408,240 L342,312"/>
    </g>
    <path d="{sparkle(256, 240, 74, .2)}" fill="{SYSTEM}"/>
    <rect x="176" y="346" width="160" height="26" rx="8" fill="{RANK_S}"/>''')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for style in ('color-dark', 'color-light', 'black', 'white'):
        for kind, text in build(style).items():
            open(os.path.join(OUT, f'{kind}-{style}.svg'), 'w').write(text)
    # presentation cards with background baked in
    for style in ('color-dark', 'color-light'):
        for kind, text in build(style, bg=True).items():
            open(os.path.join(OUT, f'{kind}-{style}-bg.svg'), 'w').write(text)
    open(os.path.join(OUT, 'favicon.svg'), 'w').write(favicon())
    print('palette', dict(arcane=ARCANE, arcane_hot=ARCANE_HOT, system=SYSTEM, rank_s=RANK_S, void=VOID, ink=INK, paper=PAPER))
    print('\n'.join(sorted(os.listdir(OUT))))
