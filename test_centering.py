import sys, math
from pathlib import Path
ROOT = Path('.').resolve()
sys.path.insert(0, str(ROOT / "scripts"))
from axonometry import Proj, Rect, prism, solid, finish, SKINS

sk = SKINS["dark"]
# Canvas size: 1200 x 860
# Center X = 600
# Center Y = 430
ox = 600
oy = 500  # focal core at z=80 lands at y = 500 - 80 = 420!
P = Proj(ox, oy)

print(f"Spire tip at (0, 0, 260): {P.iso(0, 0, 260)}")
print(f"Core center at (0, 0, 80): {P.iso(0, 0, 80)}")
print(f"Ground slab center at (0, 0, 0): {P.iso(0, 0, 0)}")
print(f"Ground slab front corner (150, 150, 0): {P.iso(150, 150, 0)}")
print(f"Ground slab left corner (-150, 150, 0): {P.iso(-150, 150, 0)}")
print(f"Ground slab right corner (150, -150, 0): {P.iso(150, -150, 0)}")
print(f"Ground slab back corner (-150, -150, 0): {P.iso(-150, -150, 0)}")
