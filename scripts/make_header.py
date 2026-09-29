#!/usr/bin/env python3
"""Generate the pixel-art profile header (assets/header-{light,dark}.svg).

A night (dark theme, with aurora) or day (light theme) scene: name and focus
areas in a 5x7 pixel font on the left; fjord mountains, a hovering drone, a
patrolling warehouse AMR and an autonomous car on the right. Run it again
after changing the text below.
"""

import math
import pathlib
import random

TOP = "OSLO, NORWAY"
TITLE = "AHMET BURAK TEKTAS"
SUBTITLE = "ROBOTICS · SIMULATION · LOCAL LLMS"

W, H = 1200, 280
CELL = 8  # scene pixel size
SPRITE_PX = 6  # pixel size of the drone, AMR and car
COLS = W // CELL
ROAD_ROW = 29  # first row of the road
WHEEL_Y = ROAD_ROW * CELL + 16  # where the vehicles' wheels touch the road

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"

PALETTES = {
    "dark": {
        "sky": ["#0b1026", "#101735", "#151e43", "#1b2550"],
        "star": "#e6edf3", "moon": "#f5e6a8",
        "aurora": ["#b48cff", "#4fe0b0", "#9dffd6"],
        "far": "#2d3b7a", "near": "#1c2657", "snow": "#8d9fd6",
        "ground": "#15321f", "road": "#1f232b", "lane": "#d6b44a",
        "top": "#58a6ff", "title": "#f0f6fc", "shadow": "#34427f", "sub": "#9fb0d8",
        "drone": "#c9d1d9", "led": "#ff5f56", "prop": "#8b949e",
        "car": "#4493f8", "window": "#a5d0ff", "tire": "#0d1117", "lidar": "#7ee787",
        "light": "#ffe28a", "border": "#30363d",
        "amr": "#c9d1d9", "band": "#f0883e", "crate": "#b08850", "strap": "#7d5f36",
    },
    "light": {
        "sky": ["#a9d8ff", "#bfe2ff", "#d4ecff", "#e8f5ff"],
        "cloud": "#ffffff", "sun": "#ffcf3f",
        "far": "#a3bde0", "near": "#7394c4", "snow": "#ffffff",
        "ground": "#79bf77", "road": "#4a4f59", "lane": "#ffe066",
        "top": "#0969da", "title": "#1f2328", "shadow": "#a3bde0", "sub": "#4b5563",
        "drone": "#24292f", "led": "#e5534b", "prop": "#6e7781",
        "car": "#0969da", "window": "#cfe8ff", "tire": "#1f2328", "lidar": "#1a7f37",
        "light": "#ffd33d", "border": "#d0d7de",
        "amr": "#e6ebf0", "band": "#fb8f44", "crate": "#c69c6d", "strap": "#8a6436",
    },
}

FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["###", ".#.", ".#.", ".#.", ".#.", ".#.", "###"],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    ",": ["..", "..", "..", "..", "..", ".#", "#."],
    ".": [".", ".", ".", ".", ".", ".", "#"],
    "·": [".", ".", ".", "#", ".", ".", "."],
    " ": ["..", "..", "..", "..", "..", "..", ".."],
}

# Sprites: each character maps to a palette key ('.' is transparent).
DRONE = [
    "PPPPP.....PPPPP",
    "..d.........d..",
    "..ddddddddddd..",
    "....ddddddd....",
    "....d.dLd.d....",
    "...d.......d...",
]
CAR = [
    "........G.........",
    ".....ccccccc......",
    "....cwwwcwwwc.....",
    "...cwwwwcwwwwc....",
    ".cccccccccccccccc.",
    "ccccccccccccccccch",
    ".ccTTTcccccccTTTc.",
    "...TTT.......TTT..",
]
AMR = [
    "....kkKKkkkk....",
    "....kkKKkkkk....",
    "....kkKKkkkk....",
    ".aaaaaaaaaaaaaa.",
    "aaaaaaaaaaaaaaaG",
    "aOOOOOOOOOOOOOOa",
    "aaaaaaaaaaaaaaaa",
    ".TT..........TT.",
]
SPRITE_KEYS = {"P": "prop", "d": "drone", "L": "led", "c": "car", "w": "window",
               "T": "tire", "G": "lidar", "h": "light", "a": "amr", "O": "band",
               "k": "crate", "K": "strap"}


class Canvas:
    def __init__(self):
        self.parts = []

    def rect(self, x, y, w, h, color, extra=""):
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"{extra}/>'
        )

    def bitmap(self, rows, x, y, px, color_of):
        """Draw a bitmap, merging horizontal runs of one colour into one rect."""
        for r, row in enumerate(rows):
            c = 0
            while c < len(row):
                color = color_of(row[c])
                if not color:
                    c += 1
                    continue
                start = c
                while c < len(row) and color_of(row[c]) == color:
                    c += 1
                self.rect(x + start * px, y + r * px, (c - start) * px, px, color)


def sprite(rows, p, blink_key, blink_dur, blink_values="1;0.2;1"):
    """Render a sprite as SVG, making the pixels of blink_key blink."""
    cv = Canvas()
    cv.bitmap(rows, 0, 0, SPRITE_PX, lambda ch: p.get(SPRITE_KEYS.get(ch, ""), None))
    return "".join(cv.parts).replace(
        f'fill="{p[blink_key]}"/>',
        f'fill="{p[blink_key]}"><animate attributeName="opacity" '
        f'values="{blink_values}" dur="{blink_dur}s" repeatCount="indefinite"/></rect>',
    )


def text_rows(text):
    rows = [""] * 7
    for i, ch in enumerate(text):
        glyph = FONT[ch]
        for r in range(7):
            rows[r] += glyph[r] + ("." if i < len(text) - 1 else "")
    return rows


def mountains(base, amp, start, period):
    """Column heights (in cells) of a row of evenly spaced triangular peaks."""
    heights = []
    for c in range(COLS):
        if c < start:
            heights.append(0)
            continue
        phase = (c - start) % period
        peak = period // 2
        heights.append(round(base + amp * (1 - abs(phase - peak) / peak)))
    return heights


def build(theme):
    p = PALETTES[theme]
    cv = Canvas()

    # Sky bands.
    band = ROAD_ROW * CELL // len(p["sky"])
    for i, color in enumerate(p["sky"]):
        cv.rect(0, i * band, W, band + 1, color)

    rnd = random.Random(7)
    if theme == "dark":
        for _ in range(38):
            x, y = rnd.randrange(COLS), rnd.randrange(ROAD_ROW - 8)
            if x * CELL < 640 and 24 < y * CELL < 180:  # keep the text clear
                continue
            twinkle = rnd.random() < 0.25
            anim = (
                f'><animate attributeName="opacity" values="1;0.2;1" '
                f'dur="{rnd.choice([3, 4, 5])}s" begin="{rnd.random() * 3:.1f}s" '
                f'repeatCount="indefinite"/></rect>'
            )
            size = CELL // 2 if rnd.random() < 0.7 else CELL // 2 + 2
            if twinkle:
                cv.parts.append(
                    f'<rect x="{x * CELL}" y="{y * CELL}" width="{size}" height="{size}" '
                    f'fill="{p["star"]}"{anim}'
                )
            else:
                cv.rect(x * CELL, y * CELL, size, size, p["star"], ' opacity="0.7"')
        # Aurora: two shimmering ribbons of vertical streaks behind the mountains.
        top, mid, low = p["aurora"]
        start = 80
        for phase, base, amp, opacity, dur in [(0.0, 3, 2, 0.5, 7), (2.1, 5, 1.5, 0.28, 9)]:
            rects = []
            for c in range(start, COLS):
                y = round(base + amp * math.sin(c / 7 + phase) + math.sin(c / 3) * 0.6)
                length = 2 + round(1 + math.sin(c / 5 + phase))
                fade = min(1, (c - start + 1) / 14)  # soft left edge
                for i in range(length):
                    color = top if i == 0 else low if i == length - 1 else mid
                    rects.append(
                        f'<rect x="{c * CELL}" y="{(y + i) * CELL}" width="{CELL}" '
                        f'height="{CELL}" fill="{color}" opacity="{fade:.2f}"/>'
                    )
            rects = "".join(rects)
            cv.parts.append(
                f'<g opacity="{opacity}">{rects}<animate attributeName="opacity" '
                f'values="{opacity};{opacity * 0.45:.2f};{opacity}" dur="{dur}s" '
                f'repeatCount="indefinite"/></g>'
            )
        # Crescent moon.
        moon = [".###.", "##...", "##...", "##...", ".###."]
        cv.bitmap(moon, 1096, 24, CELL, lambda ch: p["moon"] if ch == "#" else None)
    else:
        sun = [".###.", "#####", "#####", "#####", ".###."]
        cv.bitmap(sun, 1096, 24, CELL, lambda ch: p["sun"] if ch == "#" else None)
        cloud = ["..####....", ".######...", "##########"]
        for cx, cy in [(600, 36), (940, 104)]:
            cv.bitmap(cloud, cx, cy, CELL, lambda ch: p["cloud"] if ch == "#" else None)

    # Mountains (far, then near with snow caps).
    ground_y = ROAD_ROW * CELL
    for heights, color, snowline in [
        (mountains(4, 13, 84, 24), p["far"], 13),
        (mountains(1, 9, 76, 18), p["near"], None),
    ]:
        for c, h in enumerate(heights):
            if h <= 0:
                continue
            cv.rect(c * CELL, ground_y - h * CELL, CELL, h * CELL, color)
            if snowline and h > snowline:
                cv.rect(c * CELL, ground_y - h * CELL, CELL, (h - snowline) * CELL, p["snow"])

    # Ground, road and lane markings.
    cv.rect(0, ground_y - CELL, W, CELL, p["ground"])
    cv.rect(0, ground_y, W, H - ground_y, p["road"])
    for c in range(0, COLS, 6):
        cv.rect(c * CELL, ground_y + 2 * CELL + 4, 3 * CELL, CELL // 2, p["lane"])

    # Warehouse AMR carrying a crate, patrolling back and forth.
    cv.parts.append(
        f'<g transform="translate(680 {WHEEL_Y - len(AMR) * SPRITE_PX})"><g>'
        f'{sprite(AMR, p, "lidar", 0.8)}'
        '<animateTransform attributeName="transform" type="translate" '
        'values="0 0;150 0;150 0;0 0;0 0" keyTimes="0;0.4;0.5;0.9;1" dur="16s" '
        'repeatCount="indefinite"/></g></g>'
    )

    # Autonomous car with a blinking roof sensor.
    cv.parts.append(
        f'<g transform="translate(960 {WHEEL_Y - len(CAR) * SPRITE_PX})">'
        f'{sprite(CAR, p, "lidar", 1.2)}</g>'
    )

    # Hovering drone with a blinking LED.
    cv.parts.append(
        f'<g transform="translate(820 100)"><g>{sprite(DRONE, p, "led", 1, "1;0;1")}'
        '<animateTransform attributeName="transform" type="translate" '
        'values="0 0;0 -6;0 0;0 6;0 0" calcMode="discrete" dur="2.4s" '
        'repeatCount="indefinite"/></g></g>'
    )

    # Text.
    def draw_text(text, x, y, px, color, shadow=None):
        rows = text_rows(text)
        if shadow:
            cv.bitmap(rows, x + px // 2, y + px // 2, px, lambda ch: shadow if ch == "#" else None)
        cv.bitmap(rows, x, y, px, lambda ch: color if ch == "#" else None)

    draw_text(TOP, 56, 44, 3, p["top"])
    draw_text(TITLE, 56, 78, 5, p["title"], p["shadow"])
    draw_text(SUBTITLE, 56, 140, 3, p["sub"])

    body = "\n  ".join(cv.parts)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="crispEdges" role="img" aria-label="{TITLE.title()}: robotics, autonomous-driving simulation and local LLMs. Pixel-art fjord scene with a drone, a warehouse robot and an autonomous car.">
  <defs><clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
  <g clip-path="url(#card)">
  {body}
  </g>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="15" fill="none" stroke="{p['border']}" stroke-width="2"/>
</svg>
"""


if __name__ == "__main__":
    for theme in PALETTES:
        path = OUT / f"header-{theme}.svg"
        path.write_text(build(theme), encoding="utf-8")
        print(f"wrote {path}")
