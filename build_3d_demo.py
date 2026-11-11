#!/usr/bin/env python3
"""Build a custom complex 3D Exploded Axonometric Architecture diagram.

Demonstrating Diagram Design's 2:1 dimetric parallel projection engine.
Generates an Exploded Autonomous AI Agent Supercluster Stack.
"""

from __future__ import annotations
import math
import sys
from pathlib import Path

# Add repo root to import axonometry
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from axonometry import Proj, Rect, prism, solid, finish, styles, SKINS, FONT_LINK, point, outline, walk, M, L

def build_complex_3d_demo():
    sk = SKINS["light"]
    P = Proj(500, 780)
    
    W = 480
    D = 360
    
    # 5 Architectural Layers (bottom to top)
    layers = [
        {
            "id": "compute",
            "name": "Tensor Compute & Hardware Fabric",
            "sub": "H100 NVLink cluster, liquid manifold, 3.2 Tbps InfiniBand",
            "rect": Rect(0, 0, W, D, 12),
            "t": 28,
            "z": 0,
            "focal": False,
            "kind": "compute"
        },
        {
            "id": "vector",
            "name": "Vector Store & Persistent Vault",
            "sub": "Distributed HNSW graph, Redis cache, encrypted secrets",
            "rect": Rect(16, 16, W - 16, D - 16, 10),
            "t": 20,
            "z": 100,
            "focal": False,
            "kind": "vector"
        },
        {
            "id": "reasoning",
            "name": "Cognitive Engine & Reasoning Core",
            "sub": "Chain-of-thought planner, dynamic context window, attention bus",
            "rect": Rect(24, 24, W - 24, D - 24, 8),
            "t": 32,
            "z": 210,
            "focal": True,  # Focal layer!
            "kind": "reasoning"
        },
        {
            "id": "harness",
            "name": "Agent Harness & Tool Registry",
            "sub": "Model Context Protocol (MCP), Python sandbox, skill execution",
            "rect": Rect(32, 32, W - 32, D - 32, 8),
            "t": 22,
            "z": 330,
            "focal": False,
            "kind": "harness"
        },
        {
            "id": "interface",
            "name": "Multimodal Interface & Governance",
            "sub": "Streaming websocket bus, telemetry ledger, human-in-the-loop gate",
            "rect": Rect(40, 40, W - 40, D - 40, 6),
            "t": 16,
            "z": 440,
            "focal": False,
            "kind": "interface"
        }
    ]
    
    # Generate SVG markup
    svg_elements = []
    
    # Trace lines (vertical dashed lines connecting the 4 outer corners)
    trace_rect = layers[0]["rect"]
    z_min = 0
    z_max = layers[-1]["z"] + layers[-1]["t"]
    corners_angles = [135, 45, -45, 225]
    for angle in [135, -45]:  # Far left and far right extremes
        p_bottom = point(P, trace_rect, angle, z_min)
        p_top = point(P, trace_rect, angle, z_max)
        svg_elements.append(
            f'<line x1="{p_bottom[0]:.2f}" y1="{p_bottom[1]:.2f}" '
            f'x2="{p_top[0]:.2f}" y2="{p_top[1]:.2f}" '
            f'stroke="{sk["trace"]}" stroke-width="1.2" stroke-dasharray="4,4"/>'
        )

    labels = []
    col_x = 940  # Right column for editorial labels

    # Draw each layer from bottom to top
    for layer in layers:
        r = layer["rect"]
        z0 = layer["z"]
        z1 = z0 + layer["t"]
        focal = layer["focal"]
        tones, stroke, inner = styles(sk, focal)
        
        pr, sol = solid(P, r, z0, z1, sk, tones, stroke, inner, role=True)
        svg_elements.extend(sol)
        
        # Internal surface detail geometry per layer
        if layer["kind"] == "compute":
            # Grid of server GPU dies
            die_w, die_d = 50, 40
            for dx in range(60, W - 100, 80):
                for dy in range(60, D - 90, 70):
                    die_rect = Rect(dx, dy, dx + die_w, dy + die_d, 2)
                    dpr, dsol = solid(P, die_rect, z1, z1 + 4, sk, 
                                      ("rgba(45,49,66,0.14)", "rgba(45,49,66,0.20)", "rgba(45,49,66,0.28)"),
                                      sk["sil"], sk["inner"], role=False)
                    svg_elements.extend(dsol)
                    svg_elements.extend(finish(dpr, sk["sil"], sk["inner"], sw=0.8))
        
        elif layer["kind"] == "vector":
            # Partitioned memory banks
            for px in range(50, W - 80, 110):
                bank_rect = Rect(px, 50, px + 80, D - 60, 4)
                bpr, bsol = solid(P, bank_rect, z1, z1 + 3, sk,
                                  ("rgba(79,93,117,0.12)", "rgba(79,93,117,0.18)", "rgba(79,93,117,0.26)"),
                                  sk["sil"], sk["inner"], role=False)
                svg_elements.extend(bsol)
                svg_elements.extend(finish(bpr, sk["sil"], sk["inner"], sw=0.8))

        elif layer["kind"] == "reasoning":
            # Focal layer: central neural core chip with radiating buses
            core_rect = Rect((W - 140) / 2, (D - 140) / 2, (W + 140) / 2, (D + 140) / 2, 6)
            cpr, csol = solid(P, core_rect, z1, z1 + 6, sk,
                              ("rgba(191,69,32,0.22)", "rgba(191,69,32,0.36)", "rgba(191,69,32,0.50)"),
                              sk["accent"], sk["inner_acc"], role=False)
            svg_elements.extend(csol)
            svg_elements.extend(finish(cpr, sk["accent"], sk["inner_acc"], sw=1.2))
            
            # Radiating bus traces
            p_center = point(P, Rect(W/2, D/2, W/2, D/2), 0, z1 + 6)
            for angle in [0, 90, 180, 270]:
                t1 = point(P, core_rect, angle, z1 + 6)
                t2 = point(P, r.inset(16), angle, z1)
                svg_elements.append(
                    f'<line x1="{t1[0]:.2f}" y1="{t1[1]:.2f}" x2="{t2[0]:.2f}" y2="{t2[1]:.2f}" '
                    f'stroke="{sk["accent"]}" stroke-width="1.5" stroke-dasharray="3,3"/>'
                )

        elif layer["kind"] == "harness":
            # Multiple modular sandbox containers
            for ix, iy in [(60, 60), (260, 60), (60, 180), (260, 180)]:
                box_rect = Rect(ix, iy, ix + 120, iy + 80, 3)
                xpr, xsol = solid(P, box_rect, z1, z1 + 4, sk,
                                  ("rgba(45,49,66,0.10)", "rgba(45,49,66,0.16)", "rgba(45,49,66,0.22)"),
                                  sk["sil"], sk["inner"], role=False)
                svg_elements.extend(xsol)
                svg_elements.extend(finish(xpr, sk["sil"], sk["inner"], sw=0.8))

        elif layer["kind"] == "interface":
            # Terminal & Monitor viewport panel
            panel_rect = Rect(70, 70, W - 70, D - 70, 3)
            ppr, psol = solid(P, panel_rect, z1, z1 + 2, sk,
                              ("rgba(45,49,66,0.08)", "rgba(45,49,66,0.12)", "rgba(45,49,66,0.18)"),
                              sk["sil"], sk["inner"], role=False)
            svg_elements.extend(psol)
            svg_elements.extend(finish(ppr, sk["sil"], sk["inner"], sw=0.8))

        # Finish outer prism stroke
        svg_elements.extend(finish(pr, stroke, inner, sw=1.4 if focal else 1.1))
        
        # Leader line from right edge of part to editorial label column
        rx, ry = pr["anchor"]
        lead_color = sk["lead_acc"] if focal else sk["lead"]
        dot_color = sk["accent"] if focal else sk["sil"]
        
        # Horizontal leader line (guaranteed non-crossing by height stratification)
        svg_elements.append(
            f'<circle cx="{rx:.2f}" cy="{ry:.2f}" r="2.5" fill="{dot_color}"/>'
        )
        svg_elements.append(
            f'<line x1="{rx + 6:.2f}" y1="{ry:.2f}" x2="{col_x - 14:.2f}" y2="{ry:.2f}" '
            f'stroke="{lead_color}" stroke-width="1"/>'
        )
        
        # Label card at col_x
        title_color = sk["accent"] if focal else sk["ink"]
        sub_color = sk["muted"]
        badge = '<span style="font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; background: rgba(191,69,32,0.12); color: #bf4520; padding: 2px 6px; border-radius: 3px; margin-left: 8px;">Focal Layer</span>' if focal else ''
        
        labels.append(f"""
        <g transform="translate({col_x}, {ry - 16:.2f})">
          <text x="0" y="14" font-family="'Geist', -apple-system, sans-serif" font-size="16" font-weight="700" fill="{title_color}">{layer['name']}</text>
          <text x="0" y="30" font-family="'Geist Mono', ui-monospace, monospace" font-size="11" font-weight="500" fill="{sub_color}">{layer['sub']}</text>
        </g>
        """)

    # Combine SVG
    svg_content = "\n".join(svg_elements) + "\n" + "\n".join(labels)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Autonomous AI Agent Stack · 3D Exploded Axonometric</title>
  <link href="{FONT_LINK}" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --color-paper:   #f5f5f5;
      --color-ink:     #2d3142;
      --color-muted:   #4f5d75;
      --color-accent:  #bf4520;
      --font-sans:     'Geist', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-serif:    'Instrument Serif', serif;
      --font-mono:     'Geist Mono', ui-monospace, monospace;
    }}

    body {{
      font-family: var(--font-sans);
      background: var(--color-paper);
      color: var(--color-ink);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 3rem 2rem;
    }}

    .frame {{
      max-width: 1400px;
      width: 100%;
      background: #ffffff;
      border: 1px solid rgba(45, 49, 66, 0.12);
      border-radius: 12px;
      padding: 40px 48px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.04);
    }}

    .header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid rgba(45, 49, 66, 0.1);
      padding-bottom: 24px;
      margin-bottom: 32px;
    }}

    .eyebrow {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--color-accent);
      margin-bottom: 6px;
    }}

    h1 {{
      font-size: 32px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #111827;
      margin-bottom: 6px;
    }}

    .subtitle {{
      font-size: 15px;
      color: var(--color-muted);
    }}

    .badge-3d {{
      background: rgba(191, 69, 32, 0.08);
      border: 1px solid rgba(191, 69, 32, 0.2);
      color: #bf4520;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      padding: 6px 12px;
      border-radius: 6px;
    }}

    .diagram-container {{
      width: 100%;
      overflow-x: auto;
      display: flex;
      justify-content: center;
    }}

    svg {{
      width: 100%;
      max-width: 1300px;
      height: auto;
      display: block;
    }}

    .editorial-cards {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-top: 36px;
      padding-top: 28px;
      border-top: 1px solid rgba(45, 49, 66, 0.1);
    }}

    .ed-card {{
      background: #f7f8fa;
      border: 1px solid rgba(45, 49, 66, 0.08);
      border-radius: 8px;
      padding: 16px 20px;
    }}

    .ed-card-title {{
      font-size: 14px;
      font-weight: 700;
      color: #111827;
      margin-bottom: 6px;
    }}

    .ed-card-text {{
      font-size: 13px;
      line-height: 1.5;
      color: #4f5d75;
    }}
  </style>
</head>
<body>

  <div class="frame">
    <div class="header">
      <div>
        <div class="eyebrow">Diagram Design · 2:1 Dimetric Projection Showcase</div>
        <h1>Autonomous AI Agent Stack · 3D Exploded View</h1>
        <div class="subtitle">Five architectural planes pulled apart on one vertical axis, computed via deterministic 3D-to-SVG projection geometry.</div>
      </div>
      <div class="badge-3d">Type 18 · 3D Axonometric</div>
    </div>

    <div class="diagram-container">
      <svg viewBox="0 0 1350 860" xmlns="http://www.w3.org/2000/svg">
        {svg_content}
      </svg>
    </div>

    <div class="editorial-cards">
      <div class="ed-card">
        <div class="ed-card-title">Mathematical Projection</div>
        <div class="ed-card-text">Every coordinate is computed via <code>iso(x, y, z) = [x - y, (x + y)/2 - z]</code> at 26.565° ground angles so all polygon edges land on whole pixels.</div>
      </div>
      <div class="ed-card">
        <div class="ed-card-title">Focal Layer Shading</div>
        <div class="ed-card-text">The Reasoning Core takes the burnt-tangerine <code>accent</code> tint with three calibrated shading faces (top 0.22, left lit 0.36, right shade 0.50).</div>
      </div>
      <div class="ed-card">
        <div class="ed-card-title">Zero Runtime Overhead</div>
        <div class="ed-card-text">Pure vector SVG output: zero WebGL, zero canvas rasterization, zero JavaScript. Infinitely scalable, lightweight, and accessible.</div>
      </div>
    </div>
  </div>

</body>
</html>
"""
    
    out_path = ROOT / "presentation/demo_3d_complex_agent_stack.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Generated 3D exploded diagram: {out_path}")

if __name__ == "__main__":
    build_complex_3d_demo()
