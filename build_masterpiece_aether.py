#!/usr/bin/env python3
"""THE AETHER ENGINE — Mastercraft 3D Axonometric Architecture.
Mathematically centered:
- Canvas: 1200 x 860
- Center X = 600 (Spire & Core are on axis x=600)
- Center Y = 430 (Focal Core at y=420)
- Left / Right labels perfectly balanced (col_left=80..260, col_right=940..1120)
- High architectural density using solid() + finish() engine from diagram-design
"""

from __future__ import annotations
import math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from axonometry import (FONT_LINK, Proj, Rect, f, outline, point, walk,
                        prism, solid, finish, styles, SKINS, M, L)

sk = SKINS["dark"]

# Master coordinate projection
# Origin (ox, oy):
# Center of model footprint is (0, 0)
# iso(0, 0, z) = (ox + 0 - 0, oy + 0 - z) = (ox, oy - z)
# In 1200 x 880 viewBox:
# ox = 600 -> Center X is EXACTLY 600
# oy = 500 -> z=80 (Core) is at y = 420 (optical center of 880 height)
ox, oy = 600, 500
P = Proj(ox, oy)

def block(rect, z0, z1, focal=False, sw=1.0):
    tones, stroke, inner = styles(sk, focal)
    pr, svg = solid(P, rect, z0, z1, sk, tones, stroke, inner, role=True)
    svg += finish(pr, stroke, inner, sw=sw)
    return pr, svg

def custom_block(rect, z0, z1, tones, stroke, inner, sw=0.8):
    pr, svg = solid(P, rect, z0, z1, sk, tones, stroke, inner, role=False)
    svg += finish(pr, stroke, inner, sw=sw)
    return pr, svg

def flat_tile(rect, z, fill):
    return f'<path d="{outline(P, rect, z)}" fill="{fill}"/>'

def flat_stroke(rect, z, stroke, sw=0.8, dash=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{outline(P, rect, z)}" fill="none" stroke="{stroke}" stroke-width="{sw}"{da}/>'

def label_right(rect, z, name, sub, focal=False):
    pr = prism(P, rect, z - 2, z)
    rx, ry = pr["anchor"]
    col = 950
    dc = sk["accent"] if focal else sk["ink"]
    lc = sk["lead_acc"] if focal else sk["lead"]
    tc = sk["accent"] if focal else sk["ink"]
    out = []
    out.append(f'<circle cx="{f(rx)}" cy="{f(ry)}" r="2.5" fill="{dc}"/>')
    out.append(f'<line x1="{f(rx+6)}" y1="{f(ry)}" x2="{f(col-16)}" y2="{f(ry)}" stroke="{lc}" stroke-width="0.8"/>')
    out.append(f'<text x="{f(col)}" y="{f(ry-3)}" font-family="Geist,sans-serif" font-size="13" font-weight="600" fill="{tc}">{name}</text>')
    out.append(f'<text x="{f(col)}" y="{f(ry+11)}" font-family="Geist Mono,monospace" font-size="9" font-weight="500" fill="{sk["soft"]}" letter-spacing="0.08em">{sub}</text>')
    return out

def label_left(rect, z, name, sub, focal=False):
    pr = prism(P, rect, z - 2, z)
    lt = point(P, rect, 135, z)
    lx, ly = lt
    col = 250
    dc = sk["accent"] if focal else sk["ink"]
    lc = sk["lead_acc"] if focal else sk["lead"]
    tc = sk["accent"] if focal else sk["ink"]
    out = []
    out.append(f'<circle cx="{f(lx)}" cy="{f(ly)}" r="2.5" fill="{dc}"/>')
    out.append(f'<line x1="{f(lx-6)}" y1="{f(ly)}" x2="{f(col+16)}" y2="{f(ly)}" stroke="{lc}" stroke-width="0.8"/>')
    out.append(f'<text x="{f(col)}" y="{f(ly-3)}" text-anchor="end" font-family="Geist,sans-serif" font-size="13" font-weight="600" fill="{tc}">{name}</text>')
    out.append(f'<text x="{f(col)}" y="{f(ly+11)}" text-anchor="end" font-family="Geist Mono,monospace" font-size="9" font-weight="500" fill="{sk["soft"]}" letter-spacing="0.08em">{sub}</text>')
    return out

elements = []

# ═══════════════════════════════════════════════════════════
# 1. FLOATING ISLE KEEL (Inverted Stalactites descending into void)
# ═══════════════════════════════════════════════════════════
keel_layers = [
    (170, 170, 0, -22, 12),
    (140, 140, -22, -46, 16),
    (105, 105, -46, -72, 20),
    (65, 65, -72, -98, 24),
    (28, 28, -98, -120, 14)
]
for hw, hd, zt, zb, r in keel_layers:
    rk = Rect(-hw, -hd, hw, hd, r)
    pr = prism(P, rk, zb, zt)
    elements.append(f'<path data-role="silhouette" d="{pr["sil"]}" fill="{sk["base"]}"/>')
    elements.append(f'<path d="{pr["right"]}" fill="rgba(45,49,66,0.60)"/>')
    elements.append(f'<path d="{pr["left"]}" fill="rgba(45,49,66,0.42)"/>')
    elements.append(f'<path d="{pr["sil"]}" fill="none" stroke="{sk["inner"]}" stroke-width="0.8" stroke-linejoin="round"/>')

# Keel focal crystal tip
tip_top = P.iso(0, 0, -120)
tip_bot = P.iso(0, 0, -140)
elements.append(f'<line x1="{f(tip_top[0])}" y1="{f(tip_top[1])}" x2="{f(tip_bot[0])}" y2="{f(tip_bot[1])}" stroke="{sk["accent"]}" stroke-width="1.8"/>')
elements.append(f'<circle cx="{f(tip_bot[0])}" cy="{f(tip_bot[1])}" r="3" fill="{sk["accent"]}"/>')

# ═══════════════════════════════════════════════════════════
# 2. MAIN FOUNDATION SLAB (Tier 0: Basalt Bedrock Platform)
# ═══════════════════════════════════════════════════════════
slab = Rect(-185, -185, 185, 185, 10)
_, s = block(slab, 0, 16, sw=1.2); elements += s

# Ground level decorative lawn / courtyard stone texture
elements.append(flat_tile(Rect(-175, -175, 175, 175, 6), 16, "rgba(245,245,245,0.035)"))
# Radial coordinate grid rings on ground
for rad in [60, 110, 160]:
    ring_pts = [P.iso(rad*math.cos(math.radians(a)), rad*math.sin(math.radians(a)), 16) for a in range(0, 361, 6)]
    elements.append(f'<path d="M ' + ' L '.join(f"{f(p[0])} {f(p[1])}" for p in ring_pts) + f'" fill="none" stroke="rgba(245,245,245,0.05)" stroke-width="0.8" stroke-dasharray="4,6"/>')

# Cardinal axis paving lines
elements.append(f'<line x1="{f(P.iso(-175,0,16)[0])}" y1="{f(P.iso(-175,0,16)[1])}" x2="{f(P.iso(175,0,16)[0])}" y2="{f(P.iso(175,0,16)[1])}" stroke="rgba(245,245,245,0.08)" stroke-width="0.8"/>')
elements.append(f'<line x1="{f(P.iso(0,-175,16)[0])}" y1="{f(P.iso(0,-175,16)[1])}" x2="{f(P.iso(0,175,16)[0])}" y2="{f(P.iso(0,175,16)[1])}" stroke="rgba(245,245,245,0.08)" stroke-width="0.8"/>')

# ═══════════════════════════════════════════════════════════
# 3. PERIMETER FORTIFIED WALLS & BASTIONS
# ═══════════════════════════════════════════════════════════
# Low perimeter parapets
pw = 8
# NW wall
_, s = block(Rect(-180, -180, 180, -180+pw, 0), 16, 26, sw=0.7); elements += s
# NE wall
_, s = block(Rect(180-pw, -180, 180, 180, 0), 16, 26, sw=0.7); elements += s
# SW wall
_, s = block(Rect(-180, -180, -180+pw, 180, 0), 16, 26, sw=0.7); elements += s
# SE wall
_, s = block(Rect(-180, 180-pw, 180, 180, 0), 16, 26, sw=0.7); elements += s

# Corner Bastions (raised pillboxes)
for bx, by in [(-180, -180), (180, -180), (-180, 180), (180, 180)]:
    _, s = block(Rect(bx-12, by-12, bx+12, by+12, 3), 16, 32, sw=0.8); elements += s
    elements.append(flat_tile(Rect(bx-6, by-6, bx+6, by+6, 1), 32, "rgba(240,138,89,0.25)"))

# ═══════════════════════════════════════════════════════════
# 4. ARCHITECTURAL WINGS
# ═══════════════════════════════════════════════════════════

# A. WEST WING: The Codex Archive (Knowledge Repository)
_, s = block(Rect(-160, -60, -95, 60, 4), 16, 56, sw=0.9); elements += s
# Tiered clerestory roof
_, s = block(Rect(-152, -50, -103, 50, 2), 56, 72, sw=0.8); elements += s
# Window slits (recessed light channels)
for wy in range(-45, 45, 12):
    elements.append(flat_tile(Rect(-156, wy, -99, wy+4, 0), 56, "rgba(245,245,245,0.07)"))

# B. EAST WING: The Quantum Foundry (Fabrication & Power)
_, s = block(Rect(95, -60, 160, 60, 4), 16, 52, sw=0.9); elements += s
# Heat dissipation fin banks
for fx in range(104, 152, 10):
    _, s = custom_block(Rect(fx, -52, fx+4, 52, 0), 52, 66,
                        ("rgba(245,245,245,0.08)", "rgba(45,49,66,0.5)", "rgba(45,49,66,0.3)"),
                        sk["inner"], sk["inner"], sw=0.6)
    elements += s

# C. NORTH WING: Starlight Cloister & Gardens
# Sunken stone court
elements.append(flat_tile(Rect(-60, -165, 60, -95, 4), 16, "rgba(124,143,111,0.12)"))
# Colonnade gallery
_, s = block(Rect(-65, -170, -45, -90, 2), 16, 42, sw=0.7); elements += s
_, s = block(Rect(45, -170, 65, -90, 2), 16, 42, sw=0.7); elements += s
# Cypress-style garden trees in court
for gx, gy in [(-30, -145), (30, -145), (-15, -115), (15, -115)]:
    # Trunk
    pr_t, s_t = solid(P, Rect(gx-2, gy-2, gx+2, gy+2, 2), 16, 34, sk,
                      ("rgba(124,100,76,0.35)", "rgba(124,100,76,0.50)", "rgba(124,100,76,0.65)"),
                      sk["sil"], sk["inner"], role=False)
    elements += s_t + finish(pr_t, sk["sil"], sk["inner"], sw=0.4)
    # Canopy
    pr_c, s_c = solid(P, Rect(gx-10, gy-10, gx+10, gy+10, 10), 30, 48, sk,
                      ("rgba(124,143,111,0.28)", "rgba(124,143,111,0.45)", "rgba(124,143,111,0.60)"),
                      sk["soft"], sk["inner"], role=False)
    elements += s_c + finish(pr_c, sk["soft"], sk["inner"], sw=0.5)

# D. SOUTH WING: Data Nexus & Reflecting Pools
# Tiered approach plaza
_, s = block(Rect(-70, 95, 70, 165, 4), 16, 32, sw=0.8); elements += s
# Twin reflecting pools with water shimmer
elements.append(flat_tile(Rect(-55, 105, -10, 155, 4), 32, "rgba(94,155,180,0.26)"))
elements.append(flat_stroke(Rect(-55, 105, -10, 155, 4), 32, "rgba(94,155,180,0.45)", sw=0.8))
elements.append(flat_tile(Rect(10, 105, 55, 155, 4), 32, "rgba(94,155,180,0.26)"))
elements.append(flat_stroke(Rect(10, 105, 55, 155, 4), 32, "rgba(94,155,180,0.45)", sw=0.8))

# Skybridges connecting wings to central sanctum
_, s = block(Rect(-95, -12, -55, 12, 0), 44, 52, sw=0.7); elements += s # West bridge
_, s = block(Rect(55, -12, 95, 12, 0), 44, 52, sw=0.7); elements += s  # East bridge
_, s = block(Rect(-12, -95, 12, -55, 0), 36, 44, sw=0.7); elements += s # North bridge
_, s = block(Rect(-12, 55, 12, 95, 0), 32, 40, sw=0.7); elements += s   # South bridge

# ═══════════════════════════════════════════════════════════
# 5. THE CENTRAL SANCTUM — THE AETHER REACTOR & SPIRE
# (Centered right at 0, 0 in model coordinates -> lands on x=600!)
# ═══════════════════════════════════════════════════════════

# Tier 1 Plinth (Octagonal / Chamfered stepped dais)
_, s = block(Rect(-55, -55, 55, 55, 8), 16, 36, sw=1.0); elements += s
elements.append(flat_tile(Rect(-48, -48, 48, 48, 6), 36, "rgba(240,138,89,0.08)"))

# Tier 2 Pedestal with containment pylons
_, s = block(Rect(-42, -42, 42, 42, 6), 36, 56, sw=1.0); elements += s

# ★★★ FOCAL REACTOR HEART (Warm Tangerine Accent #f08a59) ★★★
core_rect = Rect(-28, -28, 28, 28, 4)
pr_core, s = block(core_rect, 56, 126, focal=True, sw=1.3); elements += s

# Luminous horizontal reactor core bands
for cz in range(68, 120, 12):
    elements.append(f'<path d="{outline(P, Rect(-29, -29, 29, 29, 4), cz)}" fill="none" stroke="{sk["accent"]}" stroke-width="1.2" opacity="0.85"/>')

# Observatory Rotunda / Dome
dome = Rect(-22, -22, 22, 22, 22) # perfect cylinder
pr_dome, s_dome = solid(P, dome, 126, 154, sk,
                        ("rgba(245,245,245,0.18)", "rgba(45,49,66,0.5)", "rgba(45,49,66,0.3)"),
                        sk["ink"], sk["inner"], role=False)
elements += s_dome + finish(pr_dome, sk["ink"], sk["inner"], sw=1.0)

# Observation deck walkway railing
elements.append(f'<path d="{outline(P, Rect(-26, -26, 26, 26, 26), 132)}" fill="none" stroke="{sk["ink"]}" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.6"/>')

# Chrono-Spire Mast (Upper transmission antenna)
_, s = block(Rect(-8, -8, 8, 8, 0), 154, 210, focal=True, sw=0.9); elements += s
_, s = block(Rect(-4, -4, 4, 4, 0), 210, 252, focal=True, sw=0.8); elements += s

# Needle tip & High-frequency beacon orb
p_base = P.iso(0, 0, 252)
p_tip  = P.iso(0, 0, 282)
elements.append(f'<line x1="{f(p_base[0])}" y1="{f(p_base[1])}" x2="{f(p_tip[0])}" y2="{f(p_tip[1])}" stroke="{sk["accent"]}" stroke-width="2.2"/>')
elements.append(f'<circle cx="{f(p_tip[0])}" cy="{f(p_tip[1])}" r="4.5" fill="{sk["accent"]}"/>')
elements.append(f'<circle cx="{f(p_tip[0])}" cy="{f(p_tip[1])}" r="8.5" fill="none" stroke="{sk["accent"]}" stroke-width="1.0" opacity="0.5"/>')

# ═══════════════════════════════════════════════════════════
# 6. ORBITAL HALO RINGS (Projected Ellipses around Central Axis)
# ═══════════════════════════════════════════════════════════
halo_configs = [
    (90, 115, 1.4, "6,4", 0.55),
    (154, 85, 1.1, "4,4", 0.45),
    (210, 52, 0.9, "3,3", 0.60)
]
for hz, hr, hsw, hdash, hopac in halo_configs:
    pts = [P.iso(hr*math.cos(math.radians(a)), hr*math.sin(math.radians(a)), hz) for a in range(0, 361, 4)]
    d_str = "M " + " L ".join(f"{f(pt[0])} {f(pt[1])}" for pt in pts)
    elements.append(f'<path d="{d_str}" fill="none" stroke="{sk["accent"]}" stroke-width="{hsw}" stroke-dasharray="{hdash}" opacity="{hopac}"/>')
    # Orbital node satellites on the ring
    for node_angle in [45, 135, 225, 315]:
        npt = P.iso(hr*math.cos(math.radians(node_angle)), hr*math.sin(math.radians(node_angle)), hz)
        elements.append(f'<circle cx="{f(npt[0])}" cy="{f(npt[1])}" r="2.5" fill="{sk["accent"]}"/>')

# ═══════════════════════════════════════════════════════════
# 7. FLOATING OUTPOST SATELLITES (Balanced left & right)
# ═══════════════════════════════════════════════════════════
satellites = [
    # (center_x, center_y, size, z, height, name, side)
    (-170, 70, 38, 90, 18, "Relay West", "left"),
    (-70, 170, 34, 70, 14, "Beacon South-West", "left"),
    (70, -170, 34, 80, 16, "Lookout North-East", "right"),
    (170, -70, 38, 95, 20, "Conduit East", "right"),
]

for scx, scy, ssz, sz, sh, sname, side in satellites:
    hs = ssz / 2
    srect = Rect(scx - hs, scy - hs, scx + hs, scy + hs, 6)
    # Floating base slab
    pr_s, sv_s = solid(P, srect, sz, sz + 6, sk, sk["shade"], sk["sil"], sk["inner"], role=False)
    elements += sv_s + finish(pr_s, sk["sil"], sk["inner"], sw=0.8)
    # Pylon superstructure
    in_rect = srect.inset(8, r=2)
    pr_si, sv_si = solid(P, in_rect, sz + 6, sz + 6 + sh, sk, sk["shade"], sk["sil"], sk["inner"], role=False)
    elements += sv_si + finish(pr_si, sk["sil"], sk["inner"], sw=0.6)
    # Beacon light
    s_top = P.iso(scx, scy, sz + 6 + sh)
    elements.append(f'<circle cx="{f(s_top[0])}" cy="{f(s_top[1])}" r="2" fill="{sk["ink"]}"/>')
    # Tether / Laser conduit to central core
    core_conn = P.iso(0, 0, 100)
    elements.append(f'<line x1="{f(s_top[0])}" y1="{f(s_top[1])}" x2="{f(core_conn[0])}" y2="{f(core_conn[1])}" stroke="{sk["trace"]}" stroke-width="0.75" stroke-dasharray="4,5"/>')

# ═══════════════════════════════════════════════════════════
# 8. EDITORIAL LABELS (Symmetrically balanced columns)
# ═══════════════════════════════════════════════════════════
# Right column labels (col = 950)
elements += label_right(Rect(-4, -4, 4, 4, 0), 282, "Alignment Spire", "EL +282 · COHERENCE BEACON", focal=True)
elements += label_right(core_rect, 126, "Aether Core", "FOCAL REACTOR · #f08a59", focal=True)
elements += label_right(Rect(95, -60, 160, 60, 4), 52, "Quantum Foundry", "TIER 02 · ENERGY CONVERSION")
elements += label_right(Rect(70, -170, 70, -170, 6), 95, "Conduit Outpost", "ORBITAL NODE · 4.8 GHz")

# Left column labels (col = 250, text-anchor="end")
elements += label_left(Rect(-160, -60, -95, 60, 4), 72, "Codex Archive", "TIER 02 · KNOWLEDGE VAULT")
elements += label_left(Rect(-60, -165, 60, -95, 4), 42, "Starlight Cloister", "TIER 01 · ARBORETUM")
elements += label_left(Rect(-70, 95, 70, 165, 4), 32, "Data Nexus", "REFLECTING POOLS · EL +32")
elements += label_left(slab, 16, "Basalt Foundation", "ISLE KEEL · SUB-LEVEL -140")

# ═══════════════════════════════════════════════════════════
# ASSEMBLE SVG & COMPLETE STANDALONE HTML
# ═══════════════════════════════════════════════════════════
body_svg = "\n".join(elements)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Aether Engine · 3D Axonometric Architecture</title>
  <link href="{FONT_LINK}" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --color-paper: {sk["paper"]};
      --color-paper-2: #393e53;
      --color-ink: {sk["ink"]};
      --color-muted: {sk["muted"]};
      --color-soft: {sk["soft"]};
      --color-rule: {sk["rule"]};
      --color-accent: {sk["accent"]};
      --font-sans: 'Geist', system-ui, -apple-system, sans-serif;
      --font-serif: 'Instrument Serif', Georgia, serif;
      --font-mono: 'Geist Mono', ui-monospace, monospace;
    }}
    body {{
      font-family: var(--font-sans);
      background: var(--color-paper);
      color: var(--color-ink);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      padding: 2.5rem 1.5rem;
    }}
    .frame {{
      max-width: 1240px;
      width: 100%;
      margin: 0 auto;
    }}
    .header {{
      text-align: center;
      margin-bottom: 2rem;
    }}
    .eyebrow {{
      font-family: var(--font-mono);
      font-size: 0.68rem;
      font-weight: 500;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: var(--color-muted);
      margin-bottom: 0.5rem;
    }}
    h1 {{
      font-family: var(--font-serif);
      font-size: clamp(2rem, 3.5vw + 1rem, 3rem);
      font-weight: 400;
      letter-spacing: -0.02em;
      line-height: 1.1;
      margin-bottom: 0.6rem;
    }}
    .subtitle {{
      font-size: 0.95rem;
      line-height: 1.6;
      color: var(--color-muted);
      max-width: 64ch;
      margin: 0 auto;
    }}
    .diagram-stage {{
      background: rgba(0, 0, 0, 0.15);
      border: 1px solid var(--color-rule);
      border-radius: 8px;
      padding: 1rem 0;
      box-shadow: 0 20px 40px rgba(0,0,0,0.25);
      margin-bottom: 2rem;
      overflow-x: auto;
    }}
    svg {{
      width: 100%;
      max-width: 1200px;
      height: auto;
      display: block;
      margin: 0 auto;
    }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.25rem;
      margin-bottom: 2rem;
    }}
    @media (max-width: 860px) {{
      .cards {{ grid-template-columns: 1fr; }}
    }}
    .card {{
      background: var(--color-paper-2);
      border: 1px solid var(--color-rule);
      border-radius: 6px;
      padding: 1.25rem 1.5rem;
    }}
    .card-eyebrow {{
      font-family: var(--font-mono);
      font-size: 0.58rem;
      font-weight: 500;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--color-muted);
      margin-bottom: 0.4rem;
    }}
    .card-title {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.95rem;
      font-weight: 600;
      margin-bottom: 0.6rem;
    }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; }}
    .dot.coral {{ background: var(--color-accent); }}
    .dot.white {{ background: var(--color-ink); }}
    .dot.slate {{ background: var(--color-muted); }}
    .card p {{
      color: var(--color-muted);
      font-size: 0.82rem;
      line-height: 1.55;
    }}
    .footer {{
      display: flex;
      justify-content: space-between;
      border-top: 1px solid var(--color-rule);
      padding-top: 1.25rem;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      letter-spacing: 0.08em;
      color: var(--color-soft);
    }}
  </style>
</head>
<body>
  <div class="frame">
    <div class="header">
      <p class="eyebrow">Diagram Design · 3D Isometric Engine · Dark Editorial</p>
      <h1>The Aether Engine</h1>
      <p class="subtitle">A monolithic floating computational citadel projected mathematically in true 3D axonometry. Featuring multi-tier stalactite keels, fortified bastions, quantum foundries, orbital halos, and the focal Aether Core.</p>
    </div>

    <div class="diagram-stage">
      <svg viewBox="0 0 1200 860" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The Aether Engine 3D Axonometric Blueprint">
        <rect width="100%" height="100%" fill="{sk["paper"]}"/>
        {body_svg}
      </svg>
    </div>

    <div class="cards">
      <div class="card">
        <p class="card-eyebrow">Mathematical Purity</p>
        <div class="card-title"><span class="dot coral"></span>True Isometric Projection</div>
        <p>Every element is governed by <code>iso(x,y,z) = [x − y, (x + y)/2 − z]</code>. Zero perspective warping. Parallel lines remain strictly parallel across all axes.</p>
      </div>
      <div class="card">
        <p class="card-eyebrow">Visual Depth System</p>
        <div class="card-title"><span class="dot white"></span>Dual-Tone Shading &amp; Stroke</div>
        <p>Faces use opaque base fills under tone overlays with distinct inner edge (0.8px) and outer silhouette (1.2px) strokes to generate authentic structural volume.</p>
      </div>
      <div class="card">
        <p class="card-eyebrow">Editorial Restraint</p>
        <div class="card-title"><span class="dot slate"></span>Single Accent Focal Hierarchy</div>
        <p>The warm tangerine accent (<code>#f08a59</code>) is reserved exclusively for the central Aether Core and its orbital halos, maintaining strict typographic discipline.</p>
      </div>
    </div>

    <div class="footer">
      <span>THE AETHER ENGINE · AXONOMETRIC SPECIFICATION</span>
      <span>DIAGRAM DESIGN BY CATHRYN LAVERY</span>
    </div>
  </div>
</body>
</html>
"""

out = ROOT / "presentation" / "aether_engine.html"
out.write_text(html, encoding="utf-8")
print(f"Generated -> {out}")
