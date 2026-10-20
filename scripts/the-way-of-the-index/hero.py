"""Pixel-art hero for "The Way of the Index": a top-down, Sims-style cutaway of
Thiruvalluvar's study at night. He sits on a mat writing on a palm leaf by an
oil lamp; palm-leaf bundles on a shelf, a loom in the corner, a water pot,
moonlight through the window, a kolam at the door and coconut palms outside.

Drawn on a small pixel grid, lit (warm lamp, cool moon) with ordered dithering
so the light falls off in pixel-art bands, then scaled up with nearest-neighbour.

Usage: python hero.py <out.png>
"""
import math
import random
import sys

from PIL import Image

W, H, SCALE = 480, 192, 4
rng = random.Random(7)


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# Albedo (unlit colour) and an emissive mask (flame, glow) on the grid.
base = [[hexc("#1f3a1c")] * W for _ in range(H)]
emissive = [[False] * W for _ in range(H)]
indoor = [[False] * W for _ in range(H)]


def put(x, y, c, glow=False):
    if 0 <= x < W and 0 <= y < H:
        base[y][x] = hexc(c) if isinstance(c, str) else c
        if glow:
            emissive[y][x] = True


def rect(x0, y0, x1, y1, c, glow=False):
    for y in range(y0, y1):
        for x in range(x0, x1):
            put(x, y, c, glow)


def textured(x0, y0, x1, y1, shades):
    for y in range(y0, y1):
        for x in range(x0, x1):
            put(x, y, shades[rng.randrange(len(shades))])


def ellipse(cx, cy, rx, ry, c, glow=False):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                put(x, y, c, glow)


# --- Outside: grass, path, palms -------------------------------------------
textured(0, 0, W, H, ["#1f3a1c", "#24421f", "#2b4a23", "#1a321a", "#22401e"])
for _ in range(500):  # grass tufts
    x, y = rng.randrange(W), rng.randrange(H)
    put(x, y, "#35592b")
textured(340, 86, W, 106, ["#5a4126", "#4e3820", "#55402a"])  # path from the door
for x in range(340, W):
    if rng.random() < 0.5:
        put(x, 85, "#4a361f")
    if rng.random() < 0.5:
        put(x, 106, "#4a361f")

# Kolam: rice-flour dots and loops on the path at the threshold.
for i in range(4):
    for j in range(4):
        put(348 + i * 5, 88 + j * 5, "#efe9dc")
for t in range(0, 360, 12):
    a = math.radians(t)
    put(int(355.5 + 9 * math.cos(a)), int(95.5 + 8 * math.sin(a)), "#d9d2c2")


def shrub(cx, cy, r):
    """A bush from above: a dark mass with lighter clumps toward the moonlit side."""
    ellipse(cx, cy, r, r * 0.9, "#1d3a1b")
    for _ in range(int(r * r * 0.6)):
        a, d = rng.random() * 2 * math.pi, rng.random() * r * 0.85
        x, y = cx + d * math.cos(a), cy + d * math.sin(a) * 0.9
        lit = (x - cx) + (y - cy) < 0
        put(int(x), int(y), rng.choice(["#2f5a2a", "#3a6a30"] if lit else ["#24461f", "#2a4f24"]))


def palm(cx, cy, r, fronds=9, rot=0.0):
    """Coconut palm from above: tapered fronds radiating from the crown."""
    for k in range(fronds):
        a = rot + k * 2 * math.pi / fronds + rng.uniform(-0.12, 0.12)
        for s in range(2, r):
            bend = 0.25 * (s / r) ** 2
            x = cx + s * math.cos(a + bend)
            y = cy + s * math.sin(a + bend)
            half = 3.2 * math.sin(math.pi * s / r) + 0.6   # widest mid-frond
            for w in range(-int(half), int(half) + 1):
                lx = x + w * math.cos(a + bend + math.pi / 2)
                ly = y + w * math.sin(a + bend + math.pi / 2)
                if w == 0:
                    col = "#5d7a3a"                          # midrib
                elif (s + w) % 3 == 0:
                    col = "#1f3d1c"                          # gaps between leaflets
                else:
                    col = "#4a7d3a" if w < 0 else "#36652d"
                put(int(lx), int(ly), col)
    ellipse(cx, cy, 2.5, 2.5, "#6b5636"); put(cx, cy, "#8a7048")


# Dense garden around the hut: shrubs first, palms over them.
for _ in range(70):
    x, y = rng.randrange(W), rng.randrange(H)
    if 128 <= x <= 352 and 10 <= y <= 182:
        continue
    if x > 340 and 80 <= y <= 112:
        continue
    shrub(x, y, rng.uniform(5, 11))
for (cx, cy, r, rot) in [(58, 36, 30, 0.2), (100, 158, 28, 1.0), (18, 104, 26, 0.6),
                         (112, 74, 22, 0.9), (404, 32, 30, 0.4), (452, 150, 30, 1.3),
                         (378, 176, 22, 0.1), (470, 60, 22, 0.7), (8, 176, 22, 0.3)]:
    palm(cx, cy, r, rot=rot)

# --- The hut: floor, walls, door, window -----------------------------------
HX0, HY0, HX1, HY1, T = 140, 22, 340, 170, 6
textured(HX0 + T, HY0 + T, HX1 - T, HY1 - T, ["#6e3b22", "#733f25", "#683720", "#6b3a23"])
for y in range(HY0, HY1):
    for x in range(HX0, HX1):
        indoor[y][x] = True


def wall(x0, y0, x1, y1):
    """Cut-away mud wall seen from above: its sunlit top surface, with edges."""
    textured(x0, y0, x1, y1, ["#c2834f", "#b97a47", "#c88b55"])
    for x in range(x0, x1):
        put(x, y0, "#9a5c33"); put(x, y1 - 1, "#9a5c33")
    for y in range(y0, y1):
        put(x0, y, "#9a5c33"); put(x1 - 1, y, "#9a5c33")


wall(HX0, HY0, HX1, HY0 + T)            # top
wall(HX0, HY1 - T, HX1, HY1)            # bottom
wall(HX0, HY0, HX0 + T, HY1)            # left
wall(HX1 - T, HY0, HX1, 82)             # right, above the door
wall(HX1 - T, 110, HX1, HY1)            # right, below the door
textured(HX1 - T, 82, HX1, 110, ["#5f3a20", "#664026"])   # threshold
# Walls cast a soft shadow onto the floor along their inner faces.
for x in range(HX0 + T, HX1 - T):
    for k, c in enumerate(["#4a2716", "#58301b"]):
        put(x, HY0 + T + k, c)
for y in range(HY0 + T, HY1 - T):
    for k, c in enumerate(["#4a2716", "#58301b"]):
        put(HX0 + T + k, y, c)

# Window in the top wall: wooden bars.
rect(198, HY0, 224, HY0 + T, "#2a3550")
for x in range(200, 224, 5):
    rect(x, HY0, x + 1, HY0 + T, "#5b3a1f")

# --- Furniture and objects -------------------------------------------------
# Woven mat (paai).
rect(186, 68, 254, 120, "#b99858")
for y in range(68, 120):
    for x in range(186, 254):
        if (x + y) % 4 == 0 or (x - y) % 4 == 0:
            put(x, y, "#a58748")
rect(186, 68, 254, 69, "#8f733c"); rect(186, 119, 254, 120, "#8f733c")

# Shelf of palm-leaf bundles along the top wall.
rect(250, 29, 326, 39, "#5b3a1f")
for i, x in enumerate(range(253, 322, 11)):
    rect(x, 30, x + 9, 38, "#e2cf98")
    rect(x, 30, x + 1, 38, "#3e2814"); rect(x + 8, 30, x + 9, 38, "#3e2814")  # wooden covers
    put(x + 4, 34, "#7e3420")  # cord

# Chest.
rect(150, 31, 176, 49, "#5b3a1f"); rect(151, 32, 175, 48, "#7a5130")
rect(151, 39, 175, 40, "#4a2f18"); rect(161, 37, 165, 42, "#c9a23c")

# Loom in the lower-left corner: frame, warp threads, woven cloth, bench.
rect(150, 126, 200, 162, "#5b3a1f"); rect(152, 128, 198, 160, "#3b2615")
for x in range(154, 197, 2):
    rect(x, 128, x + 1, 146, "#e9e2d0")
rect(153, 146, 197, 159, "#2f3f7a")
for x in range(153, 197, 3):
    put(x, 150, "#46589a"); put(x + 1, 155, "#46589a")
rect(162, 162, 188, 166, "#7a5130")

# Clay water pot (kudam).
ellipse(318, 132, 7, 7, "#7c3a1f"); ellipse(317, 131, 6, 6, "#9a4a28")
ellipse(315, 129, 2, 2, "#c46a3c"); ellipse(318, 132, 2, 2, "#4a2212")

# Thiruvalluvar, seated cross-legged, writing on a palm leaf.
ellipse(220, 99, 12, 9, "#cfc5ab")       # crossed legs, robe
ellipse(220, 98, 11, 8, "#ece4cf")
ellipse(220, 90, 8, 5, "#e3dac2")        # shoulders
for x in range(214, 227):                # shawl edge over one shoulder
    put(x, 88 + (x - 214) // 4, "#d8a64a")
ellipse(220, 87, 4, 4, "#8a5634")        # head from above
ellipse(220, 85, 2, 2, "#3a3633")        # hair knot
put(219, 84, "#55504b")
rect(211, 102, 229, 104, "#e6d39c")      # palm leaf in his hands
for x in range(213, 227, 2):
    put(x, 102, "#8c7a4a")                # lines of writing
rect(227, 99, 228, 103, "#2b2213")       # stylus

# A stack of palm leaves beside him, waiting to be written.
for k in range(4):
    rect(196, 96 - k, 206, 98 - k, "#e2cf98" if k % 2 else "#d4bf86")
rect(196, 98, 206, 99, "#3e2814")

# Basket of cotton by the loom.
ellipse(212, 146, 7, 6, "#6b4a26"); ellipse(212, 146, 5, 4, "#8a6234")
for (dx, dy) in [(-2, -1), (1, 0), (-1, 2), (2, -2), (0, 1)]:
    ellipse(212 + dx, 146 + dy, 1.5, 1.5, "#f2ede0")

# Rolled sleeping mat along the right wall, and a low stool.
rect(322, 44, 330, 76, "#a58748"); rect(322, 44, 330, 46, "#8f733c"); rect(322, 74, 330, 76, "#8f733c")
for y in range(48, 74, 4):
    rect(322, y, 330, y + 1, "#8f733c")
rect(284, 120, 296, 128, "#5b3a1f"); rect(285, 121, 295, 127, "#7a5130")

# Brass vessels beside the water pot.
ellipse(304, 142, 4, 4, "#8c6a20"); ellipse(304, 142, 3, 3, "#c9a23c"); put(303, 141, "#f0d77a")
ellipse(312, 147, 3, 3, "#8c6a20"); ellipse(312, 147, 2, 2, "#c9a23c")

# Brass oil lamp (kuthuvilakku) beside him.
LAMP = (258, 88)
ellipse(*LAMP, 4, 4, "#8c6a20"); ellipse(*LAMP, 3, 3, "#c9a23c")
ellipse(LAMP[0], LAMP[1] - 1, 1.6, 1.6, "#ffe08a", glow=True)
put(LAMP[0], LAMP[1] - 2, "#fff4c8", glow=True)

# --- Lighting ---------------------------------------------------------------
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
WARM, COOL = (1.0, 0.78, 0.52), (0.55, 0.66, 0.95)
STEP = 0.07


def band(v, x, y):
    """Quantise light to bands with ordered dithering at the edges."""
    t = (BAYER[y % 4][x % 4] + 0.5) / 16
    return math.floor(v / STEP + t) * STEP


img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    for x in range(W):
        c = base[y][x]
        if emissive[y][x]:
            px[x, y] = c
            continue
        d = math.hypot(x - LAMP[0], (y - LAMP[1]) * 1.15)
        lamp = 1.15 * max(0.0, 1 - d / 140) ** 1.5
        if not indoor[y][x]:
            lamp *= 0.35                      # light leaks out through the door and window
        moon = 0.62 if not indoor[y][x] else 0.30
        # moonlight falling through the window onto the floor
        if indoor[y][x] and 28 <= y < 64 and 194 + (y - 28) * 0.3 <= x < 226 + (y - 28) * 0.3:
            moon += 0.30
        lamp, moon = band(lamp, x, y), band(moon, x, y)
        px[x, y] = tuple(min(255, int(c[i] * (lamp * WARM[i] + moon * COOL[i]))) for i in range(3))

img.resize((W * SCALE, H * SCALE), Image.NEAREST).save(sys.argv[1])
print("wrote", sys.argv[1], img.size[0] * SCALE, "x", img.size[1] * SCALE)
