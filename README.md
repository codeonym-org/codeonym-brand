# codeonym — brand kit

**Gamifying AI agents & software.**

## The mark

The badge spells out what I do, from the outside in:

| Element | Means |
|---|---|
| Hexagon badge | Game rank badge or gem, for gamification |
| `<` `>` | Code, for software |
| 4-point sparkle | AI, for agents |
| Segmented bar, 4/5 filled | XP bar, for always levelling up |

Colors and type match the portfolio's "System" theme (`~/apps/portfolio/src/app/globals.css`).

## Palette

| Token | Hex | OKLCH | Use |
|---|---|---|---|
| arcane | `#945ff9` | 0.62 0.22 295 | Primary, badge frame |
| arcane-hot | `#bc8fff` | 0.74 0.17 300 | Gradient highlight |
| system | `#30c0f8` | 0.76 0.14 230 | AI sparkle, tagline on dark |
| rank-s | `#f0b135` | 0.80 0.15 80 | XP bar, achievements |
| void | `#05040b` | — | Dark background |
| ink | `#15102a` | — | Text on light, one-color logo |
| paper | `#f4f2fb` | — | Light background, text on dark |

## Type

- Wordmark: **Michroma**, tracked +22 %, converted to paths.
- Tagline: **JetBrains Mono SemiBold**, justified to the wordmark width.

## Files

```
svg/       masters (pure paths, no fonts needed)
           mark · logo-horizontal · logo-stacked · wordmark
           × color-dark (on dark) · color-light (on light) · black · white
           *-bg.svg = with background baked in (previews, social)
           favicon.svg = simplified mark for ≤ 48 px
export/    PNG 512/1024/2048 + PDF per master, optimized copies, icons/ (favicon.ico, PWA, apple-touch)
source/    build_logo.py, which generates everything in svg/
```

## Rules

- Use `color-dark` on dark backgrounds and `color-light` on light ones. Use `black` or `white` for single-color printing, embossing and stamps.
- Below 48 px, use `favicon.svg`, never the full mark.
- Clear space: keep at least the height of the XP bar × 3 around the logo.
- Don't recolor the sparkle or the XP bar separately, don't stretch the mark, and don't add effects.

## Rebuild

```bash
python -m venv .venv && .venv/bin/pip install fonttools brotli
.venv/bin/python source/build_logo.py
bash ~/.claude/plugins/cache/codeonym/codeonym-arch-design/*/skills/graphic-design/scripts/svg-export.sh svg/<file>.svg 512 1024 2048
```
