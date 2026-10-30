import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

COLS = 12     # squares per row
ROWS = 22     # number of rows
NOISE = 35    # max random rotation in degrees, reached in the bottom row
SHIFT = 0.35   # max random offset in square widths, reached in the bottom row

rng = np.random.default_rng()

fig, ax = plt.subplots(figsize=(4, 12))

for row in range(ROWS):
    amount = row / (ROWS - 1)  # 0.0 in the top row, 1.0 in the bottom row
    for col in range(COLS):
        angle = rng.uniform(-1, 1) * NOISE * amount
        dx = rng.uniform(-1, 1) * SHIFT * amount   # new
        dy = rng.uniform(-1, 1) * SHIFT * amount   # new
        square = Rectangle((col + dx, row + dy), 1, 1, angle=angle, rotation_point="center",
                           # changed: (col, row) → (col + dx, row + dy)
                           fill=False, linewidth=1)
        ax.add_patch(square)

ax.set_xlim(-1, COLS + 1)
ax.set_ylim(ROWS + 1, -1)  # flipped so that row 0 is at the top
ax.set_aspect("equal")
ax.axis("off")

out_dir = os.path.join(os.path.dirname(__file__),
                       "Exercise_1_Output")  # next to this script
# create the folder if it doesn't exist yet
os.makedirs(out_dir, exist_ok=True)

version = 1
# find the first unused number
while os.path.exists(os.path.join(out_dir, f"squares_v{version}.png")):
    version += 1
plt.savefig(os.path.join(
    out_dir, f"squares_v{version}.png"), dpi=200, bbox_inches="tight")
os.startfile(os.path.join(out_dir, f"squares_v{version}.png"))
