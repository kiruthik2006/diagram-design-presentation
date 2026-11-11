#!/usr/bin/env python3
"""THE AETHER ENGINE — v2, properly centered.

Fixes:
- Projection origin computed so the model center lands at viewBox center
- Satellites placed at proper model coordinates within frame
- ViewBox sized to actual content bounds
- Better visual density and composition
"""

from __future__ import annotations
import math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from axonometry import (FONT_LINK, Proj, Rect, f, outline, point, walk,
                        prism, solid, finish, styles, SKINS, M, L)

sk = SKINS["dark"]

# MODEL: island spans x 0→400, y 0→320, z -64→296
# Center of interest ≈ (200, 160, 116)  (mid-footprint, mid-height)
# We want that to land at SVG (500, 420) in a 1000×840 viewBox
# iso(200,160,116) = (ox+40, oy+180-116) = (ox+40, oy+64)
# So ox=460, oy=356
P = Proj(460, 356)

# Quick sanity:
# iso(0,320,-64) = (140, 552)  bottom-left of underside   ✓
# iso(400,0,0)   = (860, 556)  far right ground            ✓
# iso(195,160,296)= (495, 238) spire tip                   ✓

def block(rect, z0, z1, focal=False):
    tones, stroke, inner = styles(sk, focal)
    pr, svg = solid(P, rect, z0, z1, sk, tones, stroke, inner, role=True)
    svg += finish(pr, stroke, inner, sw=1.2 if focal else 1.0)
    return pr, svg

def mini_block(rect, z0, z1, focal=False, sw=0.8):
    tones, stroke, inner = styles(sk, focal)
    pr, svg = solid(P, rect, z0, z1, sk, tones, stroke, inner, role=False)
    svg += finish(pr, stroke, inner, sw=sw)
    return pr, svg

def flat_mark(rect, z, fill):
    return f'<path d="{outline(P, rect, z)}" fill="{fill}"/>'

def label_right(rect, z, name, sub, focal=False):
    pr = prism(P, rect, z - 2, z)
    rx, ry = pr["anchor"]
    col = 790
    dc = sk["accent"] if focal else sk["ink"]
    lc = sk["lead_acc"] if focal else sk["lead"]
    tc = sk["accent"] if focal else sk["ink"]
    out = []
    out.append(f'<circle cx="{f(rx)}" cy="{f(ry)}" r="2" fill="{dc}"/>')
    out.append(f'<line x1="{f(rx+6)}" y1="{f(ry)}" x2="{f(col-12)}" y2="{f(ry)}" stroke="{lc}" stroke-width="0.8"/>')
    out.append(f'<text x="{f(col)}" y="{f(ry-2)}" font-family="Geist,sans-serif" font-size="13" font-weight="600" fill="{tc}">{name}</text>')
    out.append(f'<text x="{f(col)}" y="{f(ry+12)}" font-family="Geist Mono,monospace" font-size="9" font-weight="500" fill="{sk["soft"]}" letter-spacing="0.08em">{sub}</text>')
    return out

def label_left(rect, z, name, sub, focal=False):
    pr = prism(P, rect, z - 2, z)
    # left extreme
    lt = point(P, rect, 135, z)
    lx, ly = lt
    col = 70
    dc = sk["accent"] if focal else sk["ink"]
    lc = sk["lead_acc"] if focal else sk["lead"]
    tc = sk["accent"] if focal else sk["ink"]
    out = []
    out.append(f'<circle cx="{f(lx)}" cy="{f(ly)}" r="2" fill="{dc}"/>')
    out.append(f'<line x1="{f(lx-6)}" y1="{f(ly)}" x2="{f(col+12)}" y2="{f(ly)}" stroke="{lc}" stroke-width="0.8"/>')
    out.append(f'<text x="{f(col)}" y="{f(ly-2)}" text-anchor="start" font-family="Geist,sans-serif" font-size="13" font-weight="600" fill="{tc}">{name}</text>')
    out.append(f'<text x="{f(col)}" y="{f(ly+12)}" text-anchor="start" font-family="Geist Mono,monospace" font-size="9" font-weight="500" fill="{sk["soft"]}" letter-spacing="0.08em">{sub}</text>')
    return out

svg = []

# ═══════════════════════════════════════════════════════════
# UNDERSIDE — inverted stalactite (floating island illusion)
# ═══════════════════════════════════════════════════════════
for i, (ins, zt, zb) in enumerate([
    (0, 0, -16), (24, -16, -36), (56, -36, -52), (96, -52, -64)
]):
    r = Rect(ins, ins, 400-ins, 320-ins, 10+i*4)
    pr = prism(P, r, zb, zt)
    svg.append(f'<path data-role="silhouette" d="{pr["sil"]}" fill="{sk["base"]}"/>')
    svg.append(f'<path d="{pr["right"]}" fill="rgba(45,49,66,0.55)"/>')
    svg.append(f'<path d="{pr["left"]}" fill="rgba(45,49,66,0.40)"/>')
    svg.append(f'<path d="{pr["sil"]}" fill="none" stroke="{sk["inner"]}" stroke-width="0.8" stroke-linejoin="round"/>')

# ═══════════════════════════════════════════════════════════
# GROUND PLATE — the floating island surface
# ═══════════════════════════════════════════════════════════
_, s = block(Rect(0, 0, 400, 320, 8), 0, 14); svg += s
svg.append(flat_mark(Rect(16, 16, 384, 304, 4), 14, "rgba(124,143,111,0.10)"))

# Pathway grid
for px in [100, 200, 300]:
    svg.append(f'<path d="{outline(P, Rect(px-3, 20, px+3, 300, 0), 14)}" fill="rgba(245,245,245,0.04)"/>')
for py in [80, 160, 240]:
    svg.append(f'<path d="{outline(P, Rect(20, py-3, 380, py+3, 0), 14)}" fill="rgba(245,245,245,0.04)"/>')

# ═══════════════════════════════════════════════════════════
# PERIMETER WALLS (low, cut at walkable height)
# ═══════════════════════════════════════════════════════════
wt = 18
_, s = block(Rect(10, 10, 390, 18, 0), 14, 14+wt); svg += s   # North
_, s = block(Rect(10, 302, 390, 310, 0), 14, 14+wt); svg += s  # South
_, s = block(Rect(10, 10, 18, 310, 0), 14, 14+wt); svg += s    # West
_, s = block(Rect(382, 10, 390, 310, 0), 14, 14+wt); svg += s  # East

# ═══════════════════════════════════════════════════════════
# GARDEN TREES (trunk cylinder + canopy sphere-ish cylinder)
# ═══════════════════════════════════════════════════════════
for tx, ty in [(48, 50), (48, 268), (348, 52), (348, 264), (128, 268), (272, 48)]:
    # Trunk
    tr = Rect(tx-3, ty-3, tx+3, ty+3, 3)
    pr_t, s_t = solid(P, tr, 14, 38, sk,
        ("rgba(124,100,76,0.35)","rgba(124,100,76,0.50)","rgba(124,100,76,0.65)"),
        sk["sil"], sk["inner"], role=False)
    svg += s_t + finish(pr_t, sk["sil"], sk["inner"], sw=0.5)
    # Canopy
    cn = Rect(tx-14, ty-14, tx+14, ty+14, 14)
    pr_c, s_c = solid(P, cn, 34, 50, sk,
        ("rgba(124,143,111,0.28)","rgba(124,143,111,0.42)","rgba(124,143,111,0.56)"),
        sk["soft"], sk["inner"], role=False)
    svg += s_c + finish(pr_c, sk["soft"], sk["inner"], sw=0.5)

# ═══════════════════════════════════════════════════════════
# SECONDARY BUILDINGS
# ═══════════════════════════════════════════════════════════

# Archive Wing (west side)
_, s = block(Rect(34, 56, 118, 138, 3), 14, 62); svg += s
for wy in range(64, 132, 14):
    svg.append(flat_mark(Rect(42, wy, 110, wy+5, 0), 62, "rgba(245,245,245,0.07)"))

# Fabrication Hall (north-east)
_, s = block(Rect(276, 34, 368, 118, 3), 14, 50); svg += s
for mx in range(284, 360, 22):
    svg.append(flat_mark(Rect(mx, 42, mx+14, 50, 0), 50, "rgba(245,245,245,0.07)"))
    svg.append(flat_mark(Rect(mx, 56, mx+14, 64, 0), 50, "rgba(245,245,245,0.05)"))

# Dormitory (south-east)
_, s = block(Rect(238, 182, 362, 278, 3), 14, 54); svg += s
for dx in range(246, 354, 26):
    for dy in range(190, 270, 20):
        svg.append(flat_mark(Rect(dx, dy, dx+16, dy+12, 0), 54, "rgba(245,245,245,0.05)"))

# Skybridge: Archive → courtyard
_, s = block(Rect(118, 100, 138, 146, 0), 48, 56); svg += s
# Skybridge: courtyard → dormitory
_, s = block(Rect(258, 178, 278, 222, 0), 48, 56); svg += s

# ═══════════════════════════════════════════════════════════
# INNER COURTYARD (raised platform)
# ═══════════════════════════════════════════════════════════
_, s = block(Rect(128, 98, 262, 222, 4), 14, 28); svg += s
# Stone tiles
for cx in range(136, 256, 18):
    for cy in range(106, 216, 18):
        svg.append(flat_mark(Rect(cx, cy, cx+12, cy+12, 0), 28, "rgba(245,245,245,0.035)"))

# Reflecting pool
svg.append(flat_mark(Rect(156, 136, 234, 184, 6), 28, "rgba(94,122,155,0.22)"))
svg.append(f'<path d="{outline(P, Rect(156,136,234,184,6), 28)}" fill="none" stroke="rgba(94,122,155,0.20)" stroke-width="0.8"/>')

# ═══════════════════════════════════════════════════════════
# ★★★ THE FOCAL TOWER — THE AETHER CORE ★★★
# ═══════════════════════════════════════════════════════════

# Pedestal base
_, s = block(Rect(160, 120, 230, 200, 6), 28, 44); svg += s

# ★ FOCAL MAIN TOWER (dark-skin accent: #f08a59)
pr_tower, s = block(Rect(168, 128, 222, 192, 4), 44, 170, focal=True); svg += s

# Glowing window slits etched into the tower top face
for wz in range(58, 162, 16):
    svg.append(f'<path d="{outline(P, Rect(170, 188, 220, 190, 0), wz)}" fill="rgba(240,138,89,0.35)"/>')

# Inner core glow (the reactor heart)
core = Rect(182, 148, 208, 172, 2)
pr_core, s_core = solid(P, core, 78, 138, sk,
    ("rgba(240,138,89,0.40)","rgba(240,138,89,0.75)","rgba(240,138,89,0.90)"),
    sk["accent"], sk["inner_acc"], role=False)
svg += s_core + finish(pr_core, sk["accent"], sk["inner_acc"], sw=1.0)

# Observatory dome cap
dome = Rect(175, 135, 215, 185, 20)
pr_d, s_d = solid(P, dome, 170, 190, sk,
    ("rgba(245,245,245,0.12)","rgba(245,245,245,0.06)","rgba(45,49,66,0.35)"),
    sk["ink"], sk["inner"], role=False)
svg += s_d + finish(pr_d, sk["ink"], sk["inner"], sw=1.0)

# Antenna spire
_, s = mini_block(Rect(191, 156, 199, 164, 0), 190, 262, focal=True, sw=0.8); svg += s

# Needle tip
tb = P.iso(195, 160, 262)
tt = P.iso(195, 160, 296)
svg.append(f'<line x1="{f(tb[0])}" y1="{f(tb[1])}" x2="{f(tt[0])}" y2="{f(tt[1])}" stroke="{sk["accent"]}" stroke-width="2"/>')
svg.append(f'<circle cx="{f(tt[0])}" cy="{f(tt[1])}" r="3.5" fill="{sk["accent"]}"/>')

# ═══════════════════════════════════════════════════════════
# SATELLITE PLATFORMS (model coords near island edges)
# ═══════════════════════════════════════════════════════════
sat_specs = [
    # (x0, y0, x1, y1, r, z, struct_h, label_name)
    (-50, 100, 10, 160, 6, 130, 20, "Relay West"),
    (-40, 220, 20, 280, 6, 100, 16, "Beacon South-West"),
    (400, 100, 460, 160, 6, 120, 22, "Conduit East"),
    (390, 220, 450, 280, 6, 150, 18, "Lookout South-East"),
]
for sx0, sy0, sx1, sy1, sr, sz, sh, sname in sat_specs:
    sr0 = Rect(sx0, sy0, sx1, sy1, sr)
    pr_s, sv_s = solid(P, sr0, sz, sz+8, sk, sk["shade"], sk["sil"], sk["inner"], role=False)
    svg += sv_s + finish(pr_s, sk["sil"], sk["inner"], sw=0.8)
    # Structure on satellite
    inr = sr0.inset(12, r=2)
    pr_si, sv_si = solid(P, inr, sz+8, sz+8+sh, sk, sk["shade"], sk["sil"], sk["inner"], role=False)
    svg += sv_si + finish(pr_si, sk["sil"], sk["inner"], sw=0.6)
    # Suspension cable to tower
    anch = P.iso((sx0+sx1)/2, (sy0+sy1)/2, sz+8+sh)
    core_pt = P.iso(195, 160, 200)
    svg.append(f'<line x1="{f(anch[0])}" y1="{f(anch[1])}" x2="{f(core_pt[0])}" y2="{f(core_pt[1])}" stroke="{sk["trace"]}" stroke-width="0.8" stroke-dasharray="3,4"/>')

# ═══════════════════════════════════════════════════════════
# ORBITAL HALO RINGS (projected ellipses around focal tower)
# ═══════════════════════════════════════════════════════════
for rz, rr, rsw in [(108, 150, 1.4), (190, 110, 1.1), (262, 65, 0.8)]:
    pts = [P.iso(195+rr*math.cos(math.radians(a)), 160+rr*math.sin(math.radians(a)), rz) for a in range(0,361,5)]
    d = "M " + " L ".join(f"{f(p[0])} {f(p[1])}" for p in pts)
    svg.append(f'<path d="{d}" fill="none" stroke="{sk["accent"]}" stroke-width="{rsw}" stroke-dasharray="5,4" opacity="0.45"/>')

# ═══════════════════════════════════════════════════════════
# EDITORIAL LABELS
# ═══════════════════════════════════════════════════════════
svg += label_right(Rect(191,156,199,164,0), 296, "Alignment Spire", "EL +296 · COHERENCE ANTENNA", focal=True)
svg += label_right(Rect(168,128,222,192,4), 170, "Aether Core", "FOCAL REACTOR · #f08a59", focal=True)
svg += label_right(Rect(276,34,368,118,3), 50, "Fabrication Hall", "TIER 02 · TOOL FOUNDRY")
svg += label_right(Rect(238,182,362,278,3), 54, "Dormitory Block", "TIER 02 · QUARTERS")

svg += label_left(Rect(34,56,118,138,3), 62, "Archive Wing", "TIER 02 · KNOWLEDGE STORE")
svg += label_left(Rect(0,0,400,320,8), 14, "Basalt Plate", "FOUNDATION SLAB · EL +14")
svg += label_left(Rect(128,98,262,222,4), 28, "Inner Courtyard", "TIER 01 · REFLECTING POOL")

# ═══════════════════════════════════════════════════════════
# ASSEMBLE PAGE
# ═══════════════════════════════════════════════════════════
body_svg = "\n".join(svg)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Aether Engine · Floating Computational Sanctum</title>
  <link href="{FONT_LINK}" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --color-paper: {sk["paper"]}; --color-paper-2: #393e53;
      --color-ink: {sk["ink"]}; --color-muted: {sk["muted"]};
      --color-soft: {sk["soft"]}; --color-rule: {sk["rule"]};
      --color-accent: {sk["accent"]};
      --font-sans: 'Geist', system-ui, sans-serif;
      --font-serif: 'Instrument Serif', serif;
      --font-mono: 'Geist Mono', ui-monospace, monospace;
    }}
    body {{
      font-family: var(--font-sans); background: var(--color-paper);
      color: var(--color-ink); min-height: 100vh; padding: 3rem 2rem;
    }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    .header {{ margin-bottom: 2.5rem; }}
    .header-eyebrow {{
      font-family: var(--font-mono); font-size: 0.66rem; font-weight: 500;
      letter-spacing: 0.18em; text-transform: uppercase;
      color: var(--color-muted); margin-bottom: 0.75rem;
    }}
    h1 {{
      font-family: var(--font-serif);
      font-size: clamp(1.75rem, 3vw + 1rem, 2.5rem);
      font-weight: 400; letter-spacing: -0.02em; line-height: 1.1;
      margin-bottom: 0.5rem;
    }}
    .subtitle {{
      font-size: 1rem; line-height: 1.55;
      color: var(--color-muted); max-width: 58ch;
    }}
    .diagram-container {{ overflow-x: auto; }}
    svg {{ width: 100%; min-width: 1000px; display: block; }}
    @media print {{ .diagram-container {{ overflow-x: visible; }} svg {{ min-width: 0; }} }}
    .cards {{
      display: grid; grid-template-columns: 1.1fr 1fr 0.9fr;
      gap: 1rem; margin-top: 1.5rem;
    }}
    @media (max-width: 820px) {{ .cards {{ grid-template-columns: 1fr; }} }}
    .card {{
      background: var(--color-paper-2); border-radius: 6px;
      border: 1px solid var(--color-rule); padding: 1.25rem;
    }}
    .card .eyebrow {{
      font-family: var(--font-mono); font-size: 0.5rem;
      letter-spacing: 0.18em; text-transform: uppercase;
      color: var(--color-muted); margin-bottom: 0.5rem;
    }}
    .card-header {{
      display: flex; align-items: center; gap: 0.6rem;
      margin-bottom: 0.875rem; padding-bottom: 0.875rem;
      border-bottom: 1px solid rgba(245,245,245,0.08);
    }}
    .card-dot {{ width: 7px; height: 7px; border-radius: 50%; }}
    .card-dot.coral {{ background: var(--color-accent); }}
    .card-dot.ink {{ background: var(--color-ink); }}
    .card-dot.muted {{ background: var(--color-muted); }}
    .card h3 {{ font-size: 0.875rem; font-weight: 600; }}
    .card p {{ color: var(--color-muted); font-size: 0.8125rem; line-height: 1.55; }}
    .footer {{
      margin-top: 2rem; padding-top: 1.5rem;
      border-top: 1px solid rgba(245,245,245,0.08);
      font-family: var(--font-mono); font-size: 0.72rem;
      letter-spacing: 0.06em; color: var(--color-soft);
      display: flex; justify-content: space-between;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <p class="header-eyebrow">diagram design · axonometric plan · dark editorial</p>
      <h1>The Aether Engine</h1>
      <p class="subtitle">A floating computational sanctum. Basalt plate, walled gardens, archive wings, fabrication halls, water courts, orbital halos, and one focal reactor drawn from a single projection function.</p>
    </div>
    <div class="diagram-container">
      <svg viewBox="0 0 1000 780" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="aether-title aether-desc">
        <title id="aether-title">The Aether Engine</title>
        <desc id="aether-desc">3D axonometric plan of a floating computational sanctum with a focal reactor core, satellite platforms, orbital halos, and editorial callouts.</desc>
        {body_svg}
      </svg>
    </div>
    <div class="cards">
      <div class="card">
        <p class="eyebrow">The headline</p>
        <div class="card-header"><span class="card-dot coral"></span><h3>One projection, one accent</h3></div>
        <p>Every coordinate comes from <code>iso(x, y, z) = [x − y, (x + y)/2 − z]</code>. The warm tangerine marks one thing: the Aether Core reactor. Everything else stays neutral.</p>
      </div>
      <div class="card">
        <div class="card-header"><span class="card-dot ink"></span><h3>Dark editorial skin</h3></div>
        <p>Jet-black paper, white-smoke ink, blue-slate muted. Faces are an opaque base plus an rgba overlay — never a translucent fill alone — so nothing bleeds through.</p>
      </div>
      <div class="card">
        <div class="card-header"><span class="card-dot muted"></span><h3>What floats is drawn floating</h3></div>
        <p>The inverted stalactite underside is four progressively inset prisms. Satellite platforms orbit on dashed suspension cables. Nothing is implied; everything is projected.</p>
      </div>
    </div>
    <div class="footer">
      <span>the aether engine · axonometric plan</span>
      <span>diagram design by cathryn lavery</span>
    </div>
  </div>
</body>
</html>
"""

out = ROOT / "presentation" / "aether_engine.html"
out.write_text(html, encoding="utf-8")
print(f"→ {out}")
