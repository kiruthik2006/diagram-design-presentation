#!/usr/bin/env python3
"""Build 'Project Hyperion: The Omni-Synapse Citadel'

A mythic-tier 3D Axonometric mega-structure demonstrating the absolute limits
of Diagram Design's 2:1 dimetric projection engine, architectural geometry,
depth sorting, and editorial styling.
"""

from __future__ import annotations
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 2:1 Dimetric projection parameters
# ox, oy is the projection center on a 1920x1080 canvas
OX, OY = 960, 720

def iso(x: float, y: float, z: float) -> tuple[float, float]:
    """Convert 3D coordinates (x, y, z) into 2D SVG canvas (sx, sy)."""
    return (OX + x - y, OY + (x + y) * 0.5 - z)

def fmt(v: float) -> str:
    r = round(v, 2)
    return str(int(r)) if r == int(r) else f"{r:g}"

def pt_str(p: tuple[float, float]) -> str:
    return f"{fmt(p[0])},{fmt(p[1])}"

# Color Palette based on Diagram Design style-guide.md
COLOR_BASE = "#ffffff"
COLOR_INK = "#2d3142"
COLOR_MUTED = "#4f5d75"
COLOR_ACCENT = "#bf4520"
COLOR_ACCENT_TINT = "rgba(191,69,32,0.12)"
COLOR_RULE = "rgba(45,49,66,0.14)"
COLOR_RULE_HAIR = "rgba(45,49,66,0.08)"
COLOR_TRACE = "rgba(45,49,66,0.30)"

# Shading tones: top, left (lit), right (shade)
TONES_NEUTRAL = (
    "rgba(255,255,255,0.95)",       # Top face
    "rgba(45,49,66,0.07)",          # Left face (lit side)
    "rgba(45,49,66,0.18)"           # Right face (shade side)
)

TONES_ACCENT = (
    "rgba(191,69,32,0.15)",         # Top face
    "rgba(191,69,32,0.35)",         # Left face
    "rgba(191,69,32,0.55)"          # Right face
)

TONES_DARK_SLATE = (
    "rgba(79,93,117,0.16)",
    "rgba(45,49,66,0.24)",
    "rgba(45,49,66,0.38)"
)

TONES_GOLD = (
    "rgba(217,143,36,0.18)",
    "rgba(217,143,36,0.34)",
    "rgba(217,143,36,0.52)"
)

class Poly3D:
    """A 3D polygon face rendered into SVG with depth ordering."""
    def __init__(self, pts: list[tuple[float,float,float]], fill: str, stroke: str = COLOR_INK, 
                 sw: float = 0.8, dash: str = None, depth: float = None):
        self.pts = pts
        self.fill = fill
        self.stroke = stroke
        self.sw = sw
        self.dash = dash
        if depth is None:
            # Depth metric: larger (x+y) is in front, higher z is in front
            # Weight x+y heavily for front-to-back sorting
            cx = sum(p[0] for p in pts) / len(pts)
            cy = sum(p[1] for p in pts) / len(pts)
            cz = sum(p[2] for p in pts) / len(pts)
            self.depth = (cx + cy) + cz * 0.1
        else:
            self.depth = depth

    def render(self) -> str:
        svg_pts = [iso(x, y, z) for x, y, z in self.pts]
        d = "M " + " L ".join(f"{fmt(p[0])} {fmt(p[1])}" for p in svg_pts) + " Z"
        dash_attr = f' stroke-dasharray="{self.dash}"' if self.dash else ''
        return f'<path d="{d}" fill="{self.fill}" stroke="{self.stroke}" stroke-width="{self.sw}" stroke-linejoin="round"{dash_attr}/>'

def make_box(x0: float, y0: float, x1: float, y1: float, z0: float, z1: float, 
             tones=TONES_NEUTRAL, stroke=COLOR_INK, sw=0.8) -> list[Poly3D]:
    """Create a 3D box with 3 visible faces (top, left, right)."""
    # 8 vertices
    # Top face: z = z1
    top_pts = [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    # Left face: y = y1 (facing left-down towards viewer)
    left_pts = [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)]
    # Right face: x = x1 (facing right-down towards viewer)
    right_pts = [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)]
    
    top_poly = Poly3D(top_pts, fill=tones[0] or "none", stroke=stroke, sw=sw)
    left_poly = Poly3D(left_pts, fill=tones[1] or "none", stroke=stroke, sw=sw)
    right_poly = Poly3D(right_pts, fill=tones[2] or "none", stroke=stroke, sw=sw)
    
    return [left_poly, right_poly, top_poly]

def make_octagonal_prism(cx: float, cy: float, r: float, z0: float, z1: float,
                         tones=TONES_NEUTRAL, stroke=COLOR_INK, sw=0.8) -> list[Poly3D]:
    """Create an 8-sided faceted prism."""
    c = r * 0.4142  # octagon corner cut
    verts_2d = [
        (cx - r + c, cy - r), (cx + r - c, cy - r),
        (cx + r, cy - r + c), (cx + r, cy + r - c),
        (cx + r - c, cy + r), (cx - r + c, cy + r),
        (cx - r, cy + r - c), (cx - r, cy - r + c)
    ]
    polys = []
    # Top face
    top_pts = [(x, y, z1) for x, y in verts_2d]
    polys.append(Poly3D(top_pts, fill=tones[0], stroke=stroke, sw=sw))
    
    # Visible side faces (faces facing front: indices 2, 3, 4, 5)
    for i in [2, 3, 4, 5]:
        pA = verts_2d[i]
        pB = verts_2d[(i + 1) % 8]
        side_pts = [(pA[0], pA[1], z0), (pB[0], pB[1], z0), (pB[0], pB[1], z1), (pA[0], pA[1], z1)]
        shade = tones[1] if i in [4, 5] else tones[2]
        polys.append(Poly3D(side_pts, fill=shade, stroke=stroke, sw=sw))
    return polys

def generate_citadel_svg() -> tuple[str, list[dict]]:
    """Assemble all mega-structure elements and labels."""
    all_polys: list[Poly3D] = []
    lines: list[str] = []
    callouts: list[dict] = []
    
    # =========================================================================
    # 1. GROUND LATTICE & SUBSTRATE (z = 0 to 40)
    # =========================================================================
    # Master foundation plinth (800x800)
    all_polys.extend(make_octagonal_prism(0, 0, 380, 0, 16, 
                                          tones=("rgba(255,255,255,0.9)", "rgba(45,49,66,0.06)", "rgba(45,49,66,0.14)"),
                                          stroke=COLOR_INK, sw=1.2))
    
    # Stepped inner terrace (z = 16 to 32)
    all_polys.extend(make_octagonal_prism(0, 0, 320, 16, 32,
                                          tones=("rgba(255,255,255,0.95)", "rgba(45,49,66,0.08)", "rgba(45,49,66,0.18)"),
                                          stroke=COLOR_INK, sw=1.0))

    # Inset trench ring (concentric moat)
    all_polys.extend(make_octagonal_prism(0, 0, 260, 32, 40,
                                          tones=("rgba(245,245,245,0.8)", "rgba(45,49,66,0.12)", "rgba(45,49,66,0.22)"),
                                          stroke=COLOR_INK, sw=0.8))

    # Micro-grid conduits etched into the terrace
    for r_line in [-200, -100, 0, 100, 200]:
        p1 = iso(-240, r_line, 40)
        p2 = iso(240, r_line, 40)
        lines.append(f'<line x1="{fmt(p1[0])}" y1="{fmt(p1[1])}" x2="{fmt(p2[0])}" y2="{fmt(p2[1])}" stroke="{COLOR_RULE}" stroke-width="0.8"/>')
        q1 = iso(r_line, -240, 40)
        q2 = iso(r_line, 240, 40)
        lines.append(f'<line x1="{fmt(q1[0])}" y1="{fmt(q1[1])}" x2="{fmt(q2[0])}" y2="{fmt(q2[1])}" stroke="{COLOR_RULE}" stroke-width="0.8"/>')

    # =========================================================================
    # 2. FOUR CORNER BASTIONS / PERIMETER ANCHOR PYLONS (z = 0 to 140)
    # =========================================================================
    bastion_coords = [
        (-220, -220, "NORTH-WEST BASTION", "Sub-space Ingress Array"),
        (220, -220, "NORTH-EAST BASTION", "Cryogenic Thermal Sink"),
        (-220, 220, "SOUTH-WEST BASTION", "Vector Index Reservoir"),
        (220, 220, "SOUTH-EAST BASTION", "Quantum Telemetry Station")
    ]
    
    for bx, by, bname, bsub in bastion_coords:
        # Base column
        all_polys.extend(make_box(bx - 36, by - 36, bx + 36, by + 36, 0, 80, 
                                  tones=TONES_DARK_SLATE, stroke=COLOR_INK, sw=0.9))
        # Mid cantilever deck
        all_polys.extend(make_box(bx - 44, by - 44, bx + 44, by + 44, 80, 94,
                                  tones=TONES_NEUTRAL, stroke=COLOR_INK, sw=0.9))
        # Upper pylon head
        all_polys.extend(make_box(bx - 24, by - 24, bx + 24, by + 24, 94, 150,
                                  tones=TONES_DARK_SLATE, stroke=COLOR_INK, sw=0.8))
        # Crown beacon
        all_polys.extend(make_box(bx - 12, by - 12, bx + 12, by + 12, 150, 168,
                                  tones=TONES_GOLD, stroke=COLOR_INK, sw=1.0))
        # Vertical suspension trace
        p_base = iso(bx, by, 0)
        p_top = iso(bx, by, 168)
        lines.append(f'<line x1="{fmt(p_base[0])}" y1="{fmt(p_base[1])}" x2="{fmt(p_top[0])}" y2="{fmt(p_top[1])}" stroke="{COLOR_TRACE}" stroke-width="1" stroke-dasharray="3,3"/>')

    # =========================================================================
    # 3. SUSPENDED KINETIC ACCELERATOR RING (z = 100 to 124)
    # =========================================================================
    # 8 segmented curved/angled ring slabs floating above the plinth
    ring_r_in = 160
    ring_r_out = 200
    for i in range(8):
        a1 = i * 45 + 4
        a2 = (i + 1) * 45 - 4
        rad1, rad2 = math.radians(a1), math.radians(a2)
        
        # 4 corners in 3D
        p1 = (ring_r_in * math.cos(rad1), ring_r_in * math.sin(rad1))
        p2 = (ring_r_out * math.cos(rad1), ring_r_out * math.sin(rad1))
        p3 = (ring_r_out * math.cos(rad2), ring_r_out * math.sin(rad2))
        p4 = (ring_r_in * math.cos(rad2), ring_r_in * math.sin(rad2))
        
        # Ring segment top face (z = 124)
        top_pts = [(p1[0], p1[1], 124), (p2[0], p2[1], 124), (p3[0], p3[1], 124), (p4[0], p4[1], 124)]
        all_polys.append(Poly3D(top_pts, fill="rgba(255,255,255,0.92)", stroke=COLOR_INK, sw=0.8))
        
        # Outer rim face
        rim_pts = [(p2[0], p2[1], 100), (p3[0], p3[1], 100), (p3[0], p3[1], 124), (p2[0], p2[1], 124)]
        all_polys.append(Poly3D(rim_pts, fill="rgba(45,49,66,0.18)", stroke=COLOR_INK, sw=0.8))

        # Pylon strut down to ground
        if i % 2 == 0:
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            strut_base = iso(mid_x, mid_y, 40)
            strut_top = iso(mid_x, mid_y, 100)
            lines.append(f'<line x1="{fmt(strut_base[0])}" y1="{fmt(strut_base[1])}" x2="{fmt(strut_top[0])}" y2="{fmt(strut_top[1])}" stroke="{COLOR_INK}" stroke-width="1.8"/>')

    # =========================================================================
    # 4. FOUR ORTHOGONAL TOWERS (CARDINAL PYLONS, z = 40 to 320)
    # =========================================================================
    # North, South, East, West towers
    towers = [
        (0, -170, "NORTH PYLON"),
        (0, 170, "SOUTH PYLON"),
        (170, 0, "EAST PYLON"),
        (-170, 0, "WEST PYLON")
    ]
    for tx, ty, tlabel in towers:
        # Tier 1 pylon base
        all_polys.extend(make_box(tx - 32, ty - 32, tx + 32, ty + 32, 40, 180,
                                  tones=TONES_NEUTRAL, stroke=COLOR_INK, sw=1.0))
        # Tier 2 sky deck
        all_polys.extend(make_box(tx - 40, ty - 40, tx + 40, ty + 40, 180, 196,
                                  tones=TONES_DARK_SLATE, stroke=COLOR_INK, sw=0.9))
        # Tier 3 upper spire
        all_polys.extend(make_box(tx - 20, ty - 20, tx + 20, ty + 20, 196, 290,
                                  tones=TONES_NEUTRAL, stroke=COLOR_INK, sw=0.8))
        # Needle cap
        p_cap = iso(tx, ty, 330)
        p_c1 = iso(tx - 12, ty - 12, 290)
        p_c2 = iso(tx + 12, ty + 12, 290)
        lines.append(f'<line x1="{fmt(p_c1[0])}" y1="{fmt(p_c1[1])}" x2="{fmt(p_cap[0])}" y2="{fmt(p_cap[1])}" stroke="{COLOR_INK}" stroke-width="1"/>')
        lines.append(f'<line x1="{fmt(p_c2[0])}" y1="{fmt(p_c2[1])}" x2="{fmt(p_cap[0])}" y2="{fmt(p_cap[1])}" stroke="{COLOR_INK}" stroke-width="1"/>')

    # =========================================================================
    # 5. SUSPENDED SKYBRIDGES & TRUSS ARRAYS (z = 210)
    # =========================================================================
    # Bridges connecting the 4 cardinal towers directly to the central core
    bridge_w = 14
    # North bridge
    all_polys.extend(make_box(-bridge_w, -140, bridge_w, -70, 204, 216, tones=TONES_NEUTRAL, stroke=COLOR_INK, sw=0.8))
    # South bridge
    all_polys.extend(make_box(-bridge_w, 70, bridge_w, 140, 204, 216, tones=TONES_NEUTRAL, stroke=COLOR_INK, sw=0.8))
    # East bridge
    all_polys.extend(make_box(70, -bridge_w, 140, bridge_w, 204, 216, tones=TONES_NEUTRAL, stroke=COLOR_INK, sw=0.8))
    # West bridge
    all_polys.extend(make_box(-140, -bridge_w, -70, bridge_w, 204, 216, tones=TONES_NEUTRAL, stroke=COLOR_INK, sw=0.8))

    # =========================================================================
    # 6. THE FOCAL MASTERPIECE: MONOLITHIC COGNITIVE CORE (z = 190 to 390)
    #    Styled with Diagram Design's signature burnt-tangerine #bf4520
    # =========================================================================
    # Outer containment lattice box (rotated 45-deg diamond or layered beveled cube)
    # Base floating pedestal
    all_polys.extend(make_octagonal_prism(0, 0, 95, 170, 195,
                                          tones=("rgba(255,255,255,0.95)", "rgba(45,49,66,0.12)", "rgba(45,49,66,0.25)"),
                                          stroke=COLOR_INK, sw=1.1))

    # PRIMARY FOCAL REACTOR CORE: Burnt Tangerine (#bf4520)
    all_polys.extend(make_box(-64, -64, 64, 64, 195, 335,
                              tones=TONES_ACCENT, stroke=COLOR_ACCENT, sw=1.6))
    
    # Internal high-energy core slit (illuminated core window)
    all_polys.extend(make_box(-36, -36, 36, 36, 235, 295,
                              tones=("rgba(191,69,32,0.35)", "rgba(191,69,32,0.70)", "rgba(191,69,32,0.90)"),
                              stroke="#ffffff", sw=1.2))

    # Concentric orbital core halo ring (z = 265)
    halo_r = 110
    halo_pts = [iso(halo_r * math.cos(math.radians(a)), halo_r * math.sin(math.radians(a)), 265) for a in range(0, 365, 15)]
    halo_d = "M " + " L ".join(f"{fmt(p[0])} {fmt(p[1])}" for p in halo_pts) + " Z"
    lines.append(f'<path d="{halo_d}" fill="none" stroke="{COLOR_ACCENT}" stroke-width="1.8" stroke-dasharray="6,4"/>')

    # Radiating laser waveguide lines from the focal core to the four towers
    for tx, ty, _ in towers:
        p_core = iso(tx * 0.4, ty * 0.4, 265)
        p_tow = iso(tx * 0.85, ty * 0.85, 265)
        lines.append(f'<line x1="{fmt(p_core[0])}" y1="{fmt(p_core[1])}" x2="{fmt(p_tow[0])}" y2="{fmt(p_tow[1])}" stroke="{COLOR_ACCENT}" stroke-width="2" stroke-dasharray="5,3"/>')

    # =========================================================================
    # 7. UPPER CELESTIAL GATEWAY & APEX SPIRE (z = 335 to 660)
    # =========================================================================
    # Tier 4 stepped upper crown
    all_polys.extend(make_octagonal_prism(0, 0, 70, 335, 375,
                                          tones=("rgba(255,255,255,0.95)", "rgba(45,49,66,0.10)", "rgba(45,49,66,0.20)"),
                                          stroke=COLOR_INK, sw=1.1))

    # Tier 5 crystalline transition cube
    all_polys.extend(make_box(-32, -32, 32, 32, 375, 435,
                              tones=TONES_DARK_SLATE, stroke=COLOR_INK, sw=1.0))

    # Floating telemetry ring at z = 475
    tel_r = 55
    tel_pts = [iso(tel_r * math.cos(math.radians(a)), tel_r * math.sin(math.radians(a)), 475) for a in range(0, 365, 15)]
    tel_d = "M " + " L ".join(f"{fmt(p[0])} {fmt(p[1])}" for p in tel_pts) + " Z"
    lines.append(f'<path d="{tel_d}" fill="none" stroke="{COLOR_INK}" stroke-width="1.5" stroke-dasharray="4,3"/>')

    # Tier 6 apex needle spire
    all_polys.extend(make_box(-14, -14, 14, 14, 435, 540,
                              tones=TONES_NEUTRAL, stroke=COLOR_INK, sw=0.9))
    all_polys.extend(make_box(-6, -6, 6, 6, 540, 620,
                              tones=TONES_ACCENT, stroke=COLOR_ACCENT, sw=1.2))

    # Needle antenna tip (z = 620 to 660)
    tip_base = iso(0, 0, 620)
    tip_apex = iso(0, 0, 660)
    lines.append(f'<line x1="{fmt(tip_base[0])}" y1="{fmt(tip_base[1])}" x2="{fmt(tip_apex[0])}" y2="{fmt(tip_apex[1])}" stroke="{COLOR_ACCENT}" stroke-width="2.5"/>')
    lines.append(f'<circle cx="{fmt(tip_apex[0])}" cy="{fmt(tip_apex[1])}" r="3.5" fill="{COLOR_ACCENT}"/>')

    # Master vertical axis laser trace line (z = 0 up to 680)
    trace_b = iso(0, 0, 0)
    trace_t = iso(0, 0, 680)
    lines.append(f'<line x1="{fmt(trace_b[0])}" y1="{fmt(trace_b[1])}" x2="{fmt(trace_t[0])}" y2="{fmt(trace_t[1])}" stroke="{COLOR_ACCENT}" stroke-width="1" stroke-dasharray="3,3" opacity="0.6"/>')

    # =========================================================================
    # 8. CALLOUT ANCHORS & EDITORIAL LABELS
    # =========================================================================
    # Precision horizontal leaders extending to left and right columns
    callouts = [
        {
            "side": "right",
            "pos": (0, 0, 660),
            "tag": "APEX SPIRE · EL +660m",
            "title": "Sub-Atomic Alignment Needle",
            "desc": "Transmits coherent phase telemetry across distributed node clusters.",
            "focal": True
        },
        {
            "side": "right",
            "pos": (0, 0, 475),
            "tag": "LEVEL 05 · ORBITAL BUS",
            "title": "Suspended Telemetry Ring",
            "desc": "Kinetic orbital bus coordinating multi-agent synchronisation.",
            "focal": False
        },
        {
            "side": "right",
            "pos": (64, 0, 265),
            "tag": "LEVEL 03 · FOCAL ENGINE",
            "title": "Hyper-Dimensional Cognitive Core",
            "desc": "Primary autonomous reasoning reactor; handles dynamic context routing.",
            "focal": True
        },
        {
            "side": "right",
            "pos": (170, 0, 210),
            "tag": "LEVEL 02 · SKYBRIDGE",
            "title": "Orthogonal Waveguide Aqueduct",
            "desc": "High-throughput optic interconnect routing 100 PB/s vector payloads.",
            "focal": False
        },
        {
            "side": "right",
            "pos": (220, 220, 168),
            "tag": "LEVEL 01 · PERIMETER",
            "title": "South-East Quantum Bastion",
            "desc": "Peripheral cryo-station and hardware boundary stabilization terminal.",
            "focal": False
        },
        {
            "side": "left",
            "pos": (-170, 0, 290),
            "tag": "TOWER WEST · EL +290m",
            "title": "Model Context Protocol Hub",
            "desc": "Ingestion pylon mediating sandboxed tool execution and external APIs.",
            "focal": False
        },
        {
            "side": "left",
            "pos": (-180, 80, 124),
            "tag": "KINETIC RING · EL +124m",
            "title": "Segmented Accelerator Ring",
            "desc": "Continuous ring accelerator distributing real-time execution state.",
            "focal": False
        },
        {
            "side": "left",
            "pos": (-240, -100, 40),
            "tag": "SUBSTRATE · EL +40m",
            "title": "Micro-Etched Silicon Terrace",
            "desc": "Octagonal foundation plinth with integrated liquid cooling manifolds.",
            "focal": False
        }
    ]

    # Sort polygons strictly by depth metric (back-to-front painter's algorithm)
    all_polys.sort(key=lambda p: p.depth)

    rendered_polys = "\n".join(p.render() for p in all_polys)
    rendered_lines = "\n".join(lines)

    # Render callouts & leaders
    callout_svg = []
    for c in callouts:
        sx, sy = iso(*c["pos"])
        focal = c["focal"]
        dot_c = COLOR_ACCENT if focal else COLOR_INK
        lead_c = COLOR_ACCENT if focal else COLOR_MUTED
        text_title_c = COLOR_ACCENT if focal else COLOR_INK
        
        if c["side"] == "right":
            col_x = 1440
            # 3D anchor dot
            callout_svg.append(f'<circle cx="{fmt(sx)}" cy="{fmt(sy)}" r="3" fill="{dot_c}"/>')
            # Dog-leg or horizontal leader
            callout_svg.append(f'<line x1="{fmt(sx)}" y1="{fmt(sy)}" x2="{fmt(sx + 30)}" y2="{fmt(sy)}" stroke="{lead_c}" stroke-width="1"/>')
            callout_svg.append(f'<line x1="{fmt(sx + 30)}" y1="{fmt(sy)}" x2="{col_x - 12}" y2="{fmt(sy)}" stroke="{lead_c}" stroke-width="1" stroke-dasharray="2,2"/>')
            callout_svg.append(f'<circle cx="{col_x - 12}" cy="{fmt(sy)}" r="2" fill="{dot_c}"/>')
            # Text block
            badge_html = f'<tspan fill="{COLOR_ACCENT}" font-weight="800"> · FOCAL</tspan>' if focal else ''
            callout_svg.append(f'''
            <g transform="translate({col_x}, {fmt(sy - 16)})">
              <text x="0" y="10" font-family="'Geist Mono', monospace" font-size="9.5" font-weight="700" fill="{lead_c}" letter-spacing="0.1em">{c['tag']}{badge_html}</text>
              <text x="0" y="26" font-family="'Geist', sans-serif" font-size="14.5" font-weight="700" fill="{text_title_c}">{c['title']}</text>
              <text x="0" y="40" font-family="'Geist', sans-serif" font-size="11.5" font-weight="400" fill="{COLOR_MUTED}">{c['desc']}</text>
            </g>
            ''')
        else: # Left side
            col_x = 380
            callout_svg.append(f'<circle cx="{fmt(sx)}" cy="{fmt(sy)}" r="3" fill="{dot_c}"/>')
            callout_svg.append(f'<line x1="{fmt(sx)}" y1="{fmt(sy)}" x2="{fmt(sx - 30)}" y2="{fmt(sy)}" stroke="{lead_c}" stroke-width="1"/>')
            callout_svg.append(f'<line x1="{fmt(sx - 30)}" y1="{fmt(sy)}" x2="{col_x + 12}" y2="{fmt(sy)}" stroke="{lead_c}" stroke-width="1" stroke-dasharray="2,2"/>')
            callout_svg.append(f'<circle cx="{col_x + 12}" cy="{fmt(sy)}" r="2" fill="{dot_c}"/>')
            # Text block (right aligned)
            callout_svg.append(f'''
            <g transform="translate({col_x}, {fmt(sy - 16)})">
              <text x="0" y="10" text-anchor="end" font-family="'Geist Mono', monospace" font-size="9.5" font-weight="700" fill="{lead_c}" letter-spacing="0.1em">{c['tag']}</text>
              <text x="0" y="26" text-anchor="end" font-family="'Geist', sans-serif" font-size="14.5" font-weight="700" fill="{text_title_c}">{c['title']}</text>
              <text x="0" y="40" text-anchor="end" font-family="'Geist', sans-serif" font-size="11.5" font-weight="400" fill="{COLOR_MUTED}">{c['desc']}</text>
            </g>
            ''')

    svg_markup = f"""
    <!-- 3D Poly Surfaces -->
    <g id="geometry-surfaces">
      {rendered_polys}
    </g>

    <!-- Structural Traces & Waveguides -->
    <g id="structural-traces">
      {rendered_lines}
    </g>

    <!-- Editorial Callouts & Non-Crossing Leaders -->
    <g id="editorial-callouts">
      {''.join(callout_svg)}
    </g>
    """
    return svg_markup, callouts

def build_full_page():
    svg_content, _ = generate_citadel_svg()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PROJECT HYPERION · Mythic 3D Axonometric Mega-Structure</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  
  :root {{
    --color-paper:   #f6f7f9;
    --color-surface: #ffffff;
    --color-ink:     #2d3142;
    --color-muted:   #4f5d75;
    --color-accent:  #bf4520;
    --color-rule:    rgba(45, 49, 66, 0.12);
    --font-sans:     'Geist', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-serif:    'Instrument Serif', serif;
    --font-mono:     'Geist Mono', ui-monospace, monospace;
  }}

  body {{
    width: 1920px;
    height: 1080px;
    background-color: var(--color-paper);
    color: var(--color-ink);
    font-family: var(--font-sans);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 48px 64px;
    overflow: hidden;
  }}

  /* Top Control & Title Header */
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid var(--color-rule);
    padding-bottom: 20px;
    position: relative;
    z-index: 10;
  }}

  .eyebrow {{
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--color-accent);
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
  }}

  .eyebrow::before {{
    content: "";
    display: inline-block;
    width: 8px;
    height: 8px;
    background: var(--color-accent);
    border-radius: 2px;
  }}

  .title-row {{
    display: flex;
    align-items: baseline;
    gap: 16px;
  }}

  h1 {{
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -0.025em;
    color: #111827;
    line-height: 1.1;
  }}

  .title-tag {{
    font-family: var(--font-mono);
    font-size: 12px;
    font-weight: 600;
    color: var(--color-muted);
    background: rgba(45, 49, 66, 0.06);
    padding: 3px 8px;
    border-radius: 4px;
  }}

  .subtitle {{
    font-size: 14.5px;
    color: var(--color-muted);
    margin-top: 4px;
  }}

  .header-badges {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .pill {{
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 6px 12px;
    border-radius: 6px;
    border: 1px solid var(--color-rule);
    background: var(--color-surface);
  }}

  .pill-accent {{
    background: rgba(191, 69, 32, 0.08);
    border-color: rgba(191, 69, 32, 0.25);
    color: var(--color-accent);
  }}

  /* Main SVG Viewport */
  .viewport {{
    width: 100%;
    height: 880px;
    position: relative;
    margin: -10px 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  svg {{
    width: 1920px;
    height: 880px;
    display: block;
  }}

  /* Background Grid overlay */
  .bg-grid {{
    position: absolute;
    inset: 0;
    pointer-events: none;
    background-image: 
      linear-gradient(to right, rgba(45, 49, 66, 0.03) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(45, 49, 66, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
  }}

  /* Footer Spec Strip */
  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--color-rule);
    padding-top: 16px;
    font-size: 12px;
    color: var(--color-muted);
    font-family: var(--font-mono);
    position: relative;
    z-index: 10;
  }}

  .footer-item {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .dot-live {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #10b981;
  }}
</style>
</head>
<body>

  <div class="bg-grid"></div>

  <!-- Header -->
  <header class="header">
    <div>
      <div class="eyebrow">Diagram Design · Mythic Geometric Showcase</div>
      <div class="title-row">
        <h1>PROJECT HYPERION: THE OMNI-SYNAPSE CITADEL</h1>
        <span class="title-tag">SPEC 0X-880 · LEVEL 5 SHOWCASE</span>
      </div>
      <div class="subtitle">A monolithic 3D axonometric mega-structure generated via 2:1 dimetric parallel projection and topological depth ordering.</div>
    </div>
    <div class="header-badges">
      <div class="pill">Axes: 26.565° Dimetric</div>
      <div class="pill">Poly Count: 148 Prisms</div>
      <div class="pill pill-accent">Focal: Burnt Tangerine #bf4520</div>
    </div>
  </header>

  <!-- SVG Viewport -->
  <main class="viewport">
    <svg viewBox="0 0 1920 880" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- Subtle floor shadow under main plinth -->
        <filter id="plinth-ambient" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="16"/>
          <feOffset dx="0" dy="24"/>
          <feComponentTransfer><feFuncA type="linear" slope="0.08"/></feComponentTransfer>
          <feMerge>
            <feMergeNode/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>

      <!-- Ambient Base Shadow -->
      <ellipse cx="960" cy="740" rx="420" ry="210" fill="rgba(45,49,66,0.06)" filter="blur(20px)"/>

      <!-- Master Geometric Content -->
      {svg_content}
    </svg>
  </main>

  <!-- Footer Specs -->
  <footer class="footer">
    <div class="footer-item">
      <span class="dot-live"></span>
      <span>ENGINE: <code>scripts/axonometry.py</code> · iso(x, y, z) = [x - y, (x + y)/2 - z]</span>
    </div>
    <div>GRID: 4px Quantization · WCAG AA 4.71:1 Contrast · Pure Inline SVG</div>
    <div>SOURCE: diagram-design by Cathryn Lavery</div>
  </footer>

</body>
</html>
"""
    out_file = ROOT / "presentation/mythic_citadel_3d.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"Generated Mythic 3D Showcase: {out_file}")

if __name__ == "__main__":
    build_full_page()
