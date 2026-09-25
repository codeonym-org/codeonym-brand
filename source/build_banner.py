"""LinkedIn banner (1584x396) for codeonym, as a pure-path SVG.

Story, left to right: an agent graph (user -> supervisor -> tools/MCP, memory, sub-agents
-> AG-UI) flows into the headline "AI agents that level up", the loadout (stack) and an XP bar.
The bottom-left is kept free of content: LinkedIn puts the profile photo there.

Run: python build_banner.py  (same venv as build_logo.py)
"""
import math
import os
import re

from build_logo import (ARCANE, ARCANE_HOT, PAPER, RANK_S, SYSTEM, VOID, Font, MICH,
                        hexagon, mark, sparkle)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'svg')
ICONS = os.path.join(HERE, 'icons')
W, H = 1584, 396

PLEX = Font('/usr/share/fonts/TTF/IBMPlexSans-Medium.ttf')
MONO = Font('/usr/share/fonts/TTF/JetBrainsMono-Medium.ttf')

EYEBROW = 'SOFTWARE ENGINEER  ·  AI AGENT ENGINEER'
HEAD1, HEAD2a, HEAD2b = 'AI AGENTS', 'THAT ', 'LEVEL UP.'
SUB = ('Production-grade multi-agent systems, grounded in enterprise data via MCP '
       'and delivered through CopilotKit & AG-UI.')
LOADOUT = [('LangChain', 'langchain'), ('LangGraph', 'langgraph'), ('CopilotKit', 'copilotkit-mark'),
           ('AG-UI', None), ('MCP', 'modelcontextprotocol'), ('Next.js', 'nextdotjs'),
           ('TypeScript', 'typescript'), ('Python', 'python')]
URL = 'portfolio.codeonym.work'


def icon(name, x, y, size, fill):
    """Place an icon's paths (any viewBox) into a size x size box, single colour."""
    src = open(os.path.join(ICONS, name + '.svg')).read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
    s = size / max(vb[2], vb[3])
    ox = x + (size - vb[2] * s) / 2 - vb[0] * s
    oy = y + (size - vb[3] * s) / 2 - vb[1] * s
    paths = re.findall(r'<path[^>]*\sd="([^"]+)"', src)
    d = ' '.join(paths)
    return f'<path transform="translate({ox:.2f},{oy:.2f}) scale({s:.4f})" d="{d}" fill="{fill}"/>'


def text(font, s, x, baseline, cap, fill, tracking=0.0, extra=''):
    d, w = font.path(s, x, baseline, cap, tracking)
    return f'<path d="{d}" fill="{fill}"{extra}/>', w


def width(font, s, cap, tracking=0.0):
    return font.path(s, 0, 0, cap, tracking)[1]


# ---------- background ----------
def background():
    # hex grid pattern (pointy-top), faded by a mask
    r = 22
    hw, hh = math.sqrt(3) * r, 1.5 * r
    cell = hexagon(hw / 2, r, r).replace('M', 'M ')
    cell2 = hexagon(hw, r + hh, r)
    return f'''
  <defs>
    <radialGradient id="glowA" cx="0.72" cy="0.45" r="0.55">
      <stop offset="0" stop-color="{ARCANE}" stop-opacity=".34"/><stop offset="1" stop-color="{ARCANE}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="0.16" cy="0.2" r="0.42">
      <stop offset="0" stop-color="{SYSTEM}" stop-opacity=".20"/><stop offset="1" stop-color="{SYSTEM}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/>
    </linearGradient>
    <pattern id="hex" width="{hw:.3f}" height="{2 * hh:.3f}" patternUnits="userSpaceOnUse">
      <path d="{cell} {cell2}" fill="none" stroke="{ARCANE_HOT}" stroke-width=".8"/>
    </pattern>
    <radialGradient id="hexFade" cx="0.62" cy="0.5" r="0.62">
      <stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".7" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <mask id="hexMask"><rect width="{W}" height="{H}" fill="url(#hexFade)"/></mask>
    <linearGradient id="edgeGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{SYSTEM}"/><stop offset="1" stop-color="{ARCANE_HOT}"/>
    </linearGradient>
    <linearGradient id="levelUp" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ARCANE_HOT}"/><stop offset=".5" stop-color="{ARCANE}"/><stop offset="1" stop-color="{SYSTEM}"/>
    </linearGradient>
    <linearGradient id="xp" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{RANK_S}"/><stop offset="1" stop-color="#ffd978"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ARCANE_HOT}" stop-opacity=".0"/><stop offset=".15" stop-color="{ARCANE_HOT}" stop-opacity=".55"/>
      <stop offset="1" stop-color="{SYSTEM}" stop-opacity="0"/>
    </linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .05 0"/>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="{VOID}"/>
  <rect width="{W}" height="{H}" fill="url(#glowA)"/>
  <rect width="{W}" height="{H}" fill="url(#glowB)"/>
  <rect width="{W}" height="{H}" fill="url(#hex)" opacity=".10" mask="url(#hexMask)"/>
  <!-- giant badge watermark bleeding off the right edge -->
  <g opacity=".10" fill="none" stroke="url(#levelUp)" stroke-linejoin="round">
    <path d="{hexagon(1470, 200, 250)}" stroke-width="18"/>
    <path d="{hexagon(1470, 200, 212)}" stroke-width="3"/>
  </g>
  <rect width="{W}" height="{H}" fill="url(#floor)"/>'''


# ---------- agent graph ----------
NODES = {  # id: (x, y, label, kind)
    'user':   (70, 118, 'USER', 'io'),
    'super':  (196, 84, 'SUPERVISOR', 'core'),
    'mcp':    (318, 44, 'MCP TOOLS', 'tool'),
    'mem':    (326, 150, 'MEMORY', 'tool'),
    'res':    (440, 92, 'SUB-AGENTS', 'agent'),
    'eval':   (452, 202, 'EVALS', 'tool'),
    'ui':     (566, 150, 'AG-UI', 'io'),
}
EDGES = [('user', 'super'), ('super', 'mcp'), ('super', 'mem'), ('super', 'res'), ('mcp', 'res'),
         ('mem', 'res'), ('res', 'eval'), ('res', 'ui'), ('eval', 'ui')]


def graph():
    out = ['<g>']
    for a, b in EDGES:
        x1, y1 = NODES[a][:2]
        x2, y2 = NODES[b][:2]
        mx = (x1 + x2) / 2
        d = f'M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}'
        out.append(f'<path d="{d}" fill="none" stroke="url(#edgeGrad)" stroke-width="1.4" opacity=".45"/>')
        # a data packet travelling along the edge (at t = .62), with a short trail
        for t, op, rr in ((.62, .95, 2.6), (.55, .45, 1.8), (.49, .2, 1.3)):
            px = (1 - t) ** 3 * x1 + 3 * (1 - t) ** 2 * t * mx + 3 * (1 - t) * t ** 2 * mx + t ** 3 * x2
            py = (1 - t) ** 3 * y1 + 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3 * y2
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rr}" fill="{SYSTEM}" opacity="{op}"/>')
    for x, y, label, kind in NODES.values():
        r = {'core': 17, 'agent': 15, 'io': 12, 'tool': 11}[kind]
        col = {'core': ARCANE_HOT, 'agent': ARCANE_HOT, 'io': SYSTEM, 'tool': SYSTEM}[kind]
        out.append(f'<circle cx="{x}" cy="{y}" r="{r * 2.2}" fill="{col}" opacity=".16" filter="url(#soft)"/>')
        out.append(f'<path d="{hexagon(x, y, r)}" fill="{VOID}" stroke="{col}" stroke-width="1.6" stroke-linejoin="round"/>')
        if kind in ('core', 'agent'):
            out.append(f'<path d="{sparkle(x, y, r * .55)}" fill="{col}"/>')
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="{r * .28:.1f}" fill="{col}"/>')
        lw = width(MONO, label, 6.2, .25)
        t, _ = text(MONO, label, x - lw / 2, y + r + 15, 6.2, PAPER, .25, ' opacity=".55"')
        out.append(t)
    out.append('</g>')
    return '\n'.join(out)


# ---------- right column ----------
X0 = 640


def content():
    out = []
    # brand lockup + eyebrow
    defs, body = mark('color-dark', 'bm')
    out.append(f'<defs>{defs}</defs><g transform="translate({X0},34) scale({40 / 512})">{body}</g>')
    t, nw = text(MICH, 'CODEONYM', X0 + 54, 61, 13, PAPER, .30)
    out.append(t)
    sep = X0 + 54 + nw + 18
    out.append(f'<rect x="{sep:.1f}" y="46" width="1.2" height="17" fill="{PAPER}" opacity=".25"/>')
    t, _ = text(MONO, EYEBROW, sep + 18, 61, 9.6, SYSTEM, .32)
    out.append(t)

    # headline
    cap = 36
    t, _ = text(MICH, HEAD1, X0 - 2, 128, cap, PAPER, .06)
    out.append(t)
    t, w2 = text(MICH, HEAD2a, X0 - 2, 128 + cap * 1.52, cap, PAPER, .06)
    out.append(t)
    lx = X0 - 2 + w2 + cap * .06
    d, lw = MICH.path(HEAD2b, lx, 128 + cap * 1.52, cap, .06)
    out.append(f'<path d="{d}" fill="url(#levelUp)" opacity=".55" filter="url(#glow)"/>')
    out.append(f'<path d="{d}" fill="url(#levelUp)"/>')
    # level-up arrow chevrons after the headline
    ax, ay = lx + lw + 20, 128 + cap * 1.52 - cap / 2
    for i, op in enumerate((1, .6, .3)):
        yy = ay - i * 11
        out.append(f'<path d="M{ax},{yy + 6} L{ax + 9},{yy - 3} L{ax + 18},{yy + 6}" fill="none" stroke="{RANK_S}" '
                   f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')

    # subline
    t, _ = text(PLEX, SUB, X0, 226, 10.6, PAPER, .01, ' opacity=".78"')
    out.append(t)

    # loadout
    y, x, ch, cap = 250, X0, 30, 8.2
    t, lw_ = text(MONO, 'LOADOUT', x, y + ch / 2 + cap / 2, 7.2, ARCANE_HOT, .35)
    out.append(t)
    x += lw_ + 14
    for label, ic in LOADOUT:
        tw = width(MONO, label, cap, .06)
        iw = 15 if ic else 0
        cw = 10 + (iw + 6 if ic else 0) + tw + 10
        hero = label in ('LangChain', 'LangGraph', 'CopilotKit', 'MCP', 'AG-UI')
        stroke = ARCANE_HOT if hero else PAPER
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{ch}" rx="7" fill="{PAPER}" fill-opacity=".045" '
                   f'stroke="{stroke}" stroke-opacity="{.55 if hero else .18}" stroke-width="1"/>')
        cx = x + 10
        if ic:
            out.append(icon(ic, cx, y + (ch - iw) / 2, iw, PAPER))
            cx += iw + 6
        t, _ = text(MONO, label, cx, y + ch / 2 + cap / 2, cap, PAPER, .06, ' opacity=".92"')
        out.append(t)
        x += cw + 7
    loadout_end = x - 7

    # XP bar + url
    by = 318
    t, lvw = text(MONO, 'LV.82', X0, by + 4.5, 8.4, RANK_S, .2)
    out.append(t)
    bx = X0 + lvw + 14
    bw = 340
    out.append(f'<rect x="{bx:.1f}" y="{by - 3}" width="{bw}" height="6" rx="3" fill="{PAPER}" fill-opacity=".08"/>')
    out.append(f'<rect x="{bx:.1f}" y="{by - 3}" width="{bw * .78:.1f}" height="6" rx="3" fill="url(#xp)"/>')
    out.append(f'<rect x="{bx:.1f}" y="{by - 3}" width="{bw * .78:.1f}" height="6" rx="3" fill="url(#xp)" opacity=".6" filter="url(#glow)"/>')
    for i in range(1, 10):  # segment ticks
        out.append(f'<rect x="{bx + bw * i / 10 - .6:.1f}" y="{by - 3}" width="1.2" height="6" fill="{VOID}" opacity=".7"/>')
    t, _ = text(MONO, 'NEXT RANK: S', bx + bw + 14, by + 4.5, 8.4, PAPER, .2, ' opacity=".55"')
    out.append(t)
    uw = width(MONO, URL, 8.4, .12)
    ux = loadout_end - uw
    t, _ = text(MONO, URL, ux, by + 4.5, 8.4, SYSTEM, .12)
    out.append(t)
    out.append(f'<path d="{sparkle(ux - 12, by, 5)}" fill="{SYSTEM}"/>')
    # divider rule above the XP row
    out.append(f'<rect x="{X0}" y="296" width="{ux + uw - X0:.0f}" height="1" fill="url(#rule)"/>')
    return '\n'.join(out), loadout_end


def build():
    body, end = content()
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
           f'<title>codeonym — LinkedIn banner</title>{background()}<g transform="translate(0,14)">{graph()}</g>'
           f'<g transform="translate(0,16)">{body}</g>'
           f'<rect width="{W}" height="{H}" filter="url(#grain)"/></svg>\n')
    return svg, end


if __name__ == '__main__':
    svg, end = build()
    open(os.path.join(OUT, 'linkedin-banner.svg'), 'w').write(svg)
    print('loadout ends at x =', round(end), '(canvas', W, ')')
