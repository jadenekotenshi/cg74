"""Modern heavy cruiser -- hull + superstructure study (work in progress).

Superstructure massing aft-to-fwd:
  flight deck (aftmost, w/ deck markings + an MH-60R-esque helicopter
  for scale, visible in both views) | hangar (Mk57 x3 1x4 modules P/S
  along its periphery, RAM Mk49 launcher at its aft end, 2x Phalanx
  CIWS on its roof) | aft VLS superstructure, full beam, raised to
  hangar height (ref: Flight III Arleigh Burke) -- real-scale 64-cell
  Mk41 on its roof, nearly flush w/ the deck, flanked by Mk57 x2 1x4
  modules P/S | 16-cell large-diameter VLS (LD-VLS), flanked at the
  outer deck edges by Mk57 x1 1x4 module P/S | midships
  truncated-pyramid superstructure (narrowed fore-and-aft, shallow
  incline) w/ Mk32 triple torpedo tubes flanking its fwd end, topped
  by a truncated-pyramid mack (steeper taper than the superstructure
  below it) | inward-canted UNREP kingposts (P/S) | shortened,
  aft-shifted stretched octagonal superstructure, full beam, shallow
  inward-canted walls, w/ SPY-6 AESA panels on its 4 diagonal faces, a
  Burke-style projecting platform on its fwd face, an octagonal
  LPD-17-style stealth mast (SPQ-9B atop) somewhat fwd of center
  flanked by 2x Phalanx CIWS, and a RAM Mk49 launcher at its fwd edge
  | fwd 64-cell Mk41 w/ Mk57 x2 1x4 modules P/S flanking it | Mk 142
  8"/65 (203 mm) main gun, twin barrel, true-scale | ogive bow

Also adds SPECIFICATIONS and GUIDED-WEAPON LOADOUT insets top-right.

Principal dims: 750 ft (229 m) LOA, 93 ft (28 m) beam, scaled from an
840 ft/104 ft/30 ft study to hold the same L/B and L/draft ratios.
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 2000, 1900

BG = (10, 21, 38)
HULL_FILL = (66, 74, 88)
HULL_LINE = (150, 160, 172)
CENTERLINE = (90, 100, 115)
WATERLINE = (176, 48, 48)
DIM_LINE = (140, 152, 168)
TEXT_WHITE = (232, 236, 240)
TEXT_DIM = (140, 152, 168)

DECK_FILL = (92, 100, 114)
SUPER_FILL = (108, 116, 130)
MISSILE_DECK_FILL = (86, 98, 124)
PYRAMID_FILL = (100, 108, 122)
MACK_FILL = (120, 128, 142)
OCT_FILL = (104, 112, 126)

FONT_DIR = "/System/Library/Fonts/Supplemental/"
f_title = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 36)
f_subtitle = ImageFont.truetype(FONT_DIR + "Arial.ttf", 19)
f_section = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 21)
f_dim = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 15)
f_label = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 16)
f_label_sub = ImageFont.truetype(FONT_DIR + "Arial.ttf", 14)
f_panel_head = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 17)
f_panel_row = ImageFont.truetype(FONT_DIR + "Arial.ttf", 15)
f_panel_row_sm = ImageFont.truetype(FONT_DIR + "Arial.ttf", 13)
f_hull_number = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 46)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)


def eased_segment(p_a, p_b, n=30):
    """Points along p_a->p_b w/ x sampled evenly and y eased (smoothstep),
    so consecutive segments blend without a kink at the shared endpoint."""
    pts = []
    for i in range(n + 1):
        t = i / n
        smooth = t * t * (3 - 2 * t)
        x = p_a[0] + t * (p_b[0] - p_a[0])
        y = p_a[1] + smooth * (p_b[1] - p_a[1])
        pts.append((x, y))
    return pts


def dim_line(p0, p1, label, tick=8):
    """Double-headed dimension line with end ticks and a centered label."""
    (x0, y0), (x1, y1) = p0, p1
    draw.line([p0, p1], fill=DIM_LINE, width=1)
    if abs(x1 - x0) > abs(y1 - y0):
        draw.line([(x0, y0 - tick), (x0, y0 + tick)], fill=DIM_LINE, width=1)
        draw.line([(x1, y0 - tick), (x1, y0 + tick)], fill=DIM_LINE, width=1)
        draw.text(((x0 + x1) / 2, y0 - 6), label, font=f_dim, fill=TEXT_WHITE, anchor="mb")
    else:
        draw.line([(x0 - tick, y0), (x0 + tick, y0)], fill=DIM_LINE, width=1)
        draw.line([(x0 - tick, y1), (x0 + tick, y1)], fill=DIM_LINE, width=1)
        draw.text((x0 + 10, (y0 + y1) / 2), label, font=f_dim, fill=TEXT_WHITE, anchor="lm")


def leader_label(point, text_xy, text, sub=None, anchor="ma"):
    draw.line([point, text_xy], fill=DIM_LINE, width=1)
    r = 2.5
    draw.ellipse([point[0] - r, point[1] - r, point[0] + r, point[1] + r], fill=TEXT_WHITE)
    draw.text(text_xy, text, font=f_label, fill=TEXT_WHITE, anchor=anchor)
    if sub:
        sub_anchor = "m" + anchor[1] if anchor[0] == "m" else anchor
        draw.text((text_xy[0], text_xy[1] + 20), sub, font=f_label_sub, fill=TEXT_DIM, anchor=sub_anchor)


def place_tiered(entries, tiers, clamp=(120, W - 120)):
    entries = sorted(entries, key=lambda e: e[0][0])
    for i, (point, text, sub) in enumerate(entries):
        tier_y = tiers[i % len(tiers)]
        x = min(max(point[0], clamp[0]), clamp[1])
        leader_label(point, (x, tier_y), text, sub, anchor="ma")


def hatch_rect(x0, y0, x1, y1, fill, spacing=11):
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=HULL_LINE)
    x = x0 - (y1 - y0)
    while x < x1:
        p0 = (max(x, x0), y0)
        p1 = (min(x + (y1 - y0), x1), y1)
        if p0[0] < p1[0]:
            draw.line([p0, p1], fill=HULL_LINE, width=1)
        x += spacing


def cell_grid(x0, y0, x1, y1, rows, cols, fill, pad=6):
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=HULL_LINE)
    ix0, iy0, ix1, iy1 = x0 + pad, y0 + pad, x1 - pad, y1 - pad
    cw, ch = (ix1 - ix0) / cols, (iy1 - iy0) / rows
    for r in range(rows):
        for c in range(cols):
            cx0, cy0 = ix0 + c * cw + 1.5, iy0 + r * ch + 1.5
            draw.rectangle([cx0, cy0, cx0 + cw - 3, cy0 + ch - 3], outline=BG, width=1)


def quad_modules(x0, y0, x1, y1, n_modules, fill, gap=6, cells_per_module=4):
    """Mk57 look: separate 1x4 modules w/ gaps between them, vs. the
    dense uniform Mk41 strongback grid."""
    total_w = x1 - x0
    mod_w = (total_w - gap * (n_modules - 1)) / n_modules
    for i in range(n_modules):
        mx0 = x0 + i * (mod_w + gap)
        mx1 = mx0 + mod_w
        draw.rectangle([mx0, y0, mx1, y1], fill=fill, outline=HULL_LINE)
        cw = mod_w / cells_per_module
        for c in range(1, cells_per_module):
            cx = mx0 + c * cw
            draw.line([(cx, y0), (cx, y1)], fill=BG, width=1)


def dashed_circle(cx, cy, r, fill, width=1, dash_deg=9, gap_deg=7):
    a = 0.0
    while a < 360:
        a2 = a + dash_deg
        p0 = (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
        p1 = (cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2)))
        draw.line([p0, p1], fill=fill, width=width)
        a += dash_deg + gap_deg


def torpedo_mount(cx, cy, side, fill):
    """Mk32 SVTT-style fixed triple-tube mount: 3 short parallel tubes
    fanning outward from the hull and canted slightly aft."""
    ang = math.radians(25)  # tilt aft from the pure-athwartship line
    dx, dy = -math.sin(ang), math.cos(ang) * side
    px, py = -dy, dx
    tube_len, tube_w, gap = 26, 5, 3
    for k in (-1, 0, 1):
        ox, oy = cx + px * k * (tube_w + gap), cy + py * k * (tube_w + gap)
        ex, ey = ox + dx * tube_len, oy + dy * tube_len
        hw = tube_w / 2
        draw.polygon([
            (ox + px * hw, oy + py * hw), (ex + px * hw, ey + py * hw),
            (ex - px * hw, ey - py * hw), (ox - px * hw, oy - py * hw),
        ], fill=fill, outline=HULL_LINE)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=SUPER_FILL, outline=HULL_LINE)


def ram_launcher_plan(cx, cy, r=13):
    """Mk49 RAM-style 21-cell box launcher, plan view: a trainable round
    base with the hex-packed tube cluster showing as a stippled disc."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(66, 72, 84), outline=HULL_LINE)
    rows = [3, 4, 5, 4, 3]
    row_h = (r * 1.6) / len(rows)
    y0 = cy - row_h * (len(rows) - 1) / 2
    for i, n in enumerate(rows):
        ry = y0 + i * row_h
        rw = r * 1.5 * (n / max(rows))
        x0 = cx - rw / 2
        for j in range(n):
            dx = x0 + (j + 0.5) * (rw / n)
            draw.ellipse([dx - 1.2, ry - 1.2, dx + 1.2, ry + 1.2], fill=(28, 32, 40))


def ram_launcher_profile(cx, base_y, height=24, width=22):
    """Mk49 RAM-style box launcher, profile view: pedestal + tilted-face
    box w/ a hint of the tube cluster on its face."""
    draw.rectangle([cx - width * 0.22, base_y - height * 0.35, cx + width * 0.22, base_y],
                   fill=(66, 72, 84), outline=HULL_LINE)
    top_y = base_y - height
    draw.polygon([
        (cx - width / 2, base_y - height * 0.35), (cx - width / 2, top_y + 5),
        (cx - width / 2 + 5, top_y), (cx + width / 2 - 5, top_y),
        (cx + width / 2, top_y + 5), (cx + width / 2, base_y - height * 0.35),
    ], fill=(74, 80, 94), outline=HULL_LINE)
    for row_y in (top_y + 8, top_y + 14):
        for i in range(4):
            dx = cx - width / 2 + 7 + i * (width - 14) / 3
            draw.ellipse([dx - 1.2, row_y - 1.2, dx + 1.2, row_y + 1.2], fill=(28, 32, 40))


def ciws_plan(cx, cy, r=10, angle_deg=0):
    """Phalanx-style CIWS, plan view: white dome on a round base w/ the
    barrel cluster shown as a short dark bar pointing the mount's arc."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(210, 214, 220), outline=HULL_LINE)
    rad = math.radians(angle_deg)
    dx, dy = math.cos(rad), math.sin(rad)
    bx, by = cx + dx * (r + 9), cy + dy * (r + 9)
    draw.line([(cx, cy), (bx, by)], fill=(60, 64, 72), width=4)


def ciws_profile(cx, base_y, height=20, r=9, facing=1):
    """Phalanx-style CIWS, profile view: pedestal + white R2-D2-style
    dome w/ the gatling barrel cluster protruding from the face."""
    draw.rectangle([cx - 4, base_y - height * 0.3, cx + 4, base_y], fill=(70, 76, 88), outline=HULL_LINE)
    dome_cy = base_y - height * 0.3 - r
    draw.ellipse([cx - r, dome_cy - r, cx + r, dome_cy + r], fill=(220, 224, 228), outline=HULL_LINE)
    bx0 = cx if facing > 0 else cx - 14
    bx1 = cx + 14 if facing > 0 else cx
    draw.rectangle([bx0, dome_cy - 2, bx1, dome_cy + 2], fill=(60, 64, 72), outline=HULL_LINE)


def edge_panel(p0, p1, center, thickness=10, margin=0.12, fill=(40, 70, 95)):
    """Flat SPY-6-style AESA panel flush against a polygon edge, inset
    inward (toward `center`) and shrunk from the edge's full length so it
    doesn't reach into the adjoining corners."""
    ex, ey = p1[0] - p0[0], p1[1] - p0[1]
    elen = math.hypot(ex, ey)
    ux, uy = ex / elen, ey / elen
    a = (p0[0] + ux * elen * margin, p0[1] + uy * elen * margin)
    b = (p1[0] - ux * elen * margin, p1[1] - uy * elen * margin)
    nx, ny = -uy, ux
    cx, cy = center
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    if (mx + nx - cx) ** 2 + (my + ny - cy) ** 2 > (mx - cx) ** 2 + (my - cy) ** 2:
        nx, ny = -nx, -ny
    p_in0 = (b[0] + nx * thickness, b[1] + ny * thickness)
    p_in1 = (a[0] + nx * thickness, a[1] + ny * thickness)
    draw.polygon([a, b, p_in0, p_in1], fill=fill, outline=HULL_LINE)


def laser_plan(cx, cy, r=11, angle_deg=0):
    """~500 kW shipboard laser mount, plan view: a hexagonal sensor
    turret w/ a circular aperture (lens) facing its bearing."""
    pts = [(cx + r * math.cos(math.radians(60 * i + 30)), cy + r * math.sin(math.radians(60 * i + 30)))
           for i in range(6)]
    draw.polygon(pts, fill=(58, 64, 76), outline=HULL_LINE)
    rad = math.radians(angle_deg)
    lx, ly = cx + math.cos(rad) * r * 0.65, cy + math.sin(rad) * r * 0.65
    draw.ellipse([lx - 4, ly - 4, lx + 4, ly + 4], fill=(90, 160, 200), outline=HULL_LINE)


def laser_profile(cx, base_y, height=18, r=8, facing=1):
    draw.rectangle([cx - 4, base_y - height * 0.3, cx + 4, base_y], fill=(70, 76, 88), outline=HULL_LINE)
    dome_cy = base_y - height * 0.3 - r
    draw.ellipse([cx - r, dome_cy - r, cx + r, dome_cy + r], fill=(58, 64, 76), outline=HULL_LINE)
    lx = cx + (r * 0.6 if facing > 0 else -r * 0.6)
    draw.ellipse([lx - 3, dome_cy - 3, lx + 3, dome_cy + 3], fill=(90, 160, 200), outline=HULL_LINE)


def gun76_plan(cx, cy, angle_deg=0):
    """OTO Melara 76/62 STRALES, plan view: the real turret is a low,
    asymmetric "home-plate" stealth shape -- flat wide back, faceted
    sides tapering to a narrow front where the single 62-caliber barrel
    exits -- plus the DAVIDE-guidance EO/IR tracker pod on the roof,
    offset to one side. Rotated to face `angle_deg`."""
    l, w = 24, 15
    local = [
        (-l * 0.5, -w * 0.5), (-l * 0.5, w * 0.5),
        (l * 0.12, w * 0.42), (l * 0.5, 0), (l * 0.12, -w * 0.42),
    ]
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    pts = [(cx + lx * ca - ly * sa, cy + lx * sa + ly * ca) for lx, ly in local]
    draw.polygon(pts, fill=(70, 76, 88), outline=HULL_LINE)
    dlx, dly = -l * 0.08, w * 0.22
    dx, dy = cx + dlx * ca - dly * sa, cy + dlx * sa + dly * ca
    draw.ellipse([dx - 2.5, dy - 2.5, dx + 2.5, dy + 2.5], fill=(30, 34, 42), outline=HULL_LINE)
    bx, by = cx + ca * (l * 0.5 + 24), cy + sa * (l * 0.5 + 24)
    draw.line([(cx + ca * l * 0.5, cy + sa * l * 0.5), (bx, by)], fill=(180, 184, 190), width=3)


def gun76_profile(cx, base_y, height=15, facing=1):
    """STRALES turret, profile: low sloped stealth wedge -- taller,
    flat-faced at the rear, with the roofline sloping down (past a
    slight ridge where the EO/IR pod sits) to a low front where the
    long, thin barrel exits near the bottom of the face."""
    rear_x = cx - facing * 10
    front_x = cx + facing * 10
    ridge_x = cx - facing * 2
    draw.polygon([
        (rear_x, base_y), (rear_x, base_y - height),
        (ridge_x, base_y - height * 1.1),
        (front_x, base_y - height * 0.4), (front_x, base_y),
    ], fill=(70, 76, 88), outline=HULL_LINE)
    ridge_y = base_y - height * 1.1
    draw.ellipse([ridge_x - 2.5, ridge_y - 4, ridge_x + 2.5, ridge_y], fill=(30, 34, 42), outline=HULL_LINE)
    by = base_y - height * 0.4
    draw.line([(front_x, by), (front_x + facing * 22, by)], fill=(180, 184, 190), width=3)


def deck_box_launcher(cx, cy, angle_deg=0, w=10, l=14, fill=(66, 72, 84), tube_dots=0):
    """Small trainable box launcher (Nulka decoy / SRBOC chaff), plan
    view, oriented along `angle_deg`; optionally hints at tube openings."""
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    local = [(-l / 2, -w / 2), (l / 2, -w / 2), (l / 2, w / 2), (-l / 2, w / 2)]
    pts = [(cx + lx * ca - ly * sa, cy + lx * sa + ly * ca) for lx, ly in local]
    draw.polygon(pts, fill=fill, outline=HULL_LINE)
    if tube_dots:
        rows, cols = tube_dots
        for r in range(rows):
            for c in range(cols):
                lx = -l / 2 + (c + 0.5) * (l / rows)
                ly = -w / 2 + (r + 0.5) * (w / cols)
                px, py = cx + lx * ca - ly * sa, cy + lx * sa + ly * ca
                draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(28, 32, 40))


def twin50_plan(cx, cy, angle_deg=0):
    """Stabilized twin .50 cal RWS, plan view: a round mount w/ two
    parallel barrels pointing along `angle_deg`, plus a small offset
    EO/IR sensor ball indicating remote (not manual) operation."""
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=SUPER_FILL, outline=HULL_LINE)
    rad = math.radians(angle_deg)
    dx, dy = math.cos(rad), math.sin(rad)
    px, py = -dy, dx
    for off in (-2.5, 2.5):
        ox, oy = cx + px * off, cy + py * off
        draw.line([(ox, oy), (ox + dx * 11, oy + dy * 11)], fill=(180, 184, 190), width=2)
    slx, sly = -dx * 4 - px * 6, -dy * 4 - py * 6
    draw.ellipse([cx + slx - 2, cy + sly - 2, cx + slx + 2, cy + sly + 2], fill=(220, 224, 228), outline=HULL_LINE)


def twin50_profile(cx, base_y):
    """Stabilized twin .50 cal RWS, profile view: pedestal + barrels,
    plus a small EO/IR sensor ball above the mount."""
    draw.line([(cx, base_y), (cx, base_y - 8)], fill=(150, 160, 172), width=2)
    draw.line([(cx - 6, base_y - 9), (cx + 6, base_y - 9)], fill=(180, 184, 190), width=2)
    draw.ellipse([cx - 2, base_y - 15, cx + 2, base_y - 11], fill=(220, 224, 228), outline=HULL_LINE)


def mk38_plan(cx, cy, angle_deg=0):
    """Mk 38 25mm stabilized RWS, plan view: a small boxy housing w/ a
    single chain-gun barrel and an offset EO/IR sensor ball, on a
    trainable pedestal facing `angle_deg`."""
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    hl, hw = 8, 6
    local = [(-hl, -hw), (hl, -hw), (hl, hw), (-hl, hw)]
    pts = [(cx + lx * ca - ly * sa, cy + lx * sa + ly * ca) for lx, ly in local]
    draw.polygon(pts, fill=(72, 78, 90), outline=HULL_LINE)
    slx, sly = -hl * 0.3, hw * 1.3
    sx, sy = cx + slx * ca - sly * sa, cy + slx * sa + sly * ca
    draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(220, 224, 228), outline=HULL_LINE)
    bx, by = cx + ca * (hl + 16), cy + sa * (hl + 16)
    draw.line([(cx + ca * hl, cy + sa * hl), (bx, by)], fill=(180, 184, 190), width=3)


def mk38_profile(cx, base_y, height=14, facing=1):
    draw.rectangle([cx - 3, base_y - height * 0.3, cx + 3, base_y], fill=(70, 76, 88), outline=HULL_LINE)
    box_y0 = base_y - height
    box_y1 = base_y - height * 0.3
    draw.rectangle([cx - 7, box_y0, cx + 7, box_y1], fill=(74, 80, 94), outline=HULL_LINE)
    draw.ellipse([cx - 3 - facing * 2, box_y0 - 6, cx + 3 - facing * 2, box_y0], fill=(220, 224, 228), outline=HULL_LINE)
    by = (box_y0 + box_y1) / 2
    draw.line([(cx + facing * 7, by), (cx + facing * 20, by)], fill=(180, 184, 190), width=3)


def radome_plan(cx, cy, r):
    """SATCOM radome, plan view: a golf-ball-style dome w/ a subtle
    cross-seam pattern."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(222, 226, 230), outline=HULL_LINE)
    draw.line([(cx - r * 0.6, cy), (cx + r * 0.6, cy)], fill=HULL_LINE, width=1)
    draw.line([(cx, cy - r * 0.6), (cx, cy + r * 0.6)], fill=HULL_LINE, width=1)


def radome_profile(cx, base_y, r):
    """SATCOM radome, profile view: a hemispherical dome sitting on the deck/roof."""
    draw.pieslice([cx - r, base_y - 2 * r, cx + r, base_y], 180, 360, fill=(222, 226, 230), outline=HULL_LINE)
    draw.line([(cx - r * 0.55, base_y - r), (cx + r * 0.55, base_y - r)], fill=HULL_LINE, width=1)


def surface_radar_plan(cx, cy, angle_deg=0):
    """Small rotating surface-search radar (bar-type), plan view."""
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    hl, hw = 9, 1.5
    local = [(-hl, -hw), (hl, -hw), (hl, hw), (-hl, hw)]
    pts = [(cx + lx * ca - ly * sa, cy + lx * sa + ly * ca) for lx, ly in local]
    draw.polygon(pts, fill=(200, 204, 210), outline=HULL_LINE)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(72, 78, 90), outline=HULL_LINE)


def surface_radar_profile(cx, base_y, height=10):
    draw.line([(cx, base_y), (cx, base_y - height)], fill=(150, 160, 172), width=2)
    draw.line([(cx - 8, base_y - height), (cx + 8, base_y - height)], fill=(200, 204, 210), width=3)


def rhib_davit_plan(cx, cy, side, angle_deg=0):
    """RHIB on davits, plan view: small boat hull (pointed bow, flat
    stern) plus a short davit arm toward the hull side."""
    rad = math.radians(angle_deg)
    ca, sa = math.cos(rad), math.sin(rad)
    local = [(-11, -5), (-5.5, -6.5), (7, -6.5), (11, 0), (7, 6.5), (-5.5, 6.5), (-11, 5)]
    pts = [(cx + lx * ca - ly * sa, cy + lx * sa + ly * ca) for lx, ly in local]
    draw.polygon(pts, fill=(72, 78, 90), outline=HULL_LINE)
    draw.line([(cx, cy), (cx, cy + side * 14)], fill=(150, 160, 172), width=2)


def rhib_davit_profile(cx, base_y, height=16):
    draw.polygon([
        (cx - 9, base_y), (cx - 9, base_y - 4), (cx - 6, base_y - 7),
        (cx + 6, base_y - 7), (cx + 9, base_y - 4), (cx + 9, base_y),
    ], fill=(72, 78, 90), outline=HULL_LINE)
    draw.line([(cx - 9, base_y - 7), (cx - 9, base_y - height)], fill=(150, 160, 172), width=2)
    draw.line([(cx + 9, base_y - 7), (cx + 9, base_y - height)], fill=(150, 160, 172), width=2)
    draw.line([(cx - 9, base_y - height), (cx + 9, base_y - height)], fill=(150, 160, 172), width=2)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
draw.text((40, 28), "CG-74 DENVER-CLASS CRUISER — CONJECTURAL SKETCH", font=f_title, fill=TEXT_WHITE)
draw.text((40, 72), "WIP · twin Mk 142 8\"/65 gun fwd · 750 ft (229 m) LOA",
          font=f_subtitle, fill=TEXT_DIM)
draw.line([(40, 104), (1500, 104)], fill=(70, 90, 120), width=2)

# ---------------------------------------------------------------------------
# Shared hull geometry
# ---------------------------------------------------------------------------
STERN_X, BOW_X = 140, 1860
# 750 ft LOA; beam and draft scaled from the 840 ft/104 ft/30 ft study to
# hold the same ratios (750/840 = 0.893).
LOA_FT = 750
BEAM_FT = round(104 * LOA_FT / 840)
DRAFT_FT = round(30 * LOA_FT / 840)
FT_PX = (BOW_X - STERN_X) / LOA_FT
BEAM = BEAM_FT * FT_PX / 2
MK41_CELL_PX = 5.3 * FT_PX   # real Mk41 module pitch, ~5.3 ft
MK57_CELL_PX = 6.3 * FT_PX   # real Mk57/PVLS pitch, larger than Mk41


def hull_x(t):
    return STERN_X + t * (BOW_X - STERN_X)


# Tangent-ogive bow: true circular-arc nose, tangent to the parallel hull
# at BOW_START_T, coming to a point at t=1.0 -- a clean shell-like taper
# with no flare knuckle.
BOW_START_T = 0.84
OGIVE_L = (1.0 - BOW_START_T) * (BOW_X - STERN_X)
OGIVE_R = BEAM
OGIVE_RHO = (OGIVE_R ** 2 + OGIVE_L ** 2) / (2 * OGIVE_R)


# Stern taper: narrows from full beam at STERN_TAPER_T down to 85% of
# beam at the transom (t=0). Beyond STERN_TAPER_T the hull runs at full
# beam (a flat parallel body) until the ogive bow taper takes over.
STERN_TAPER_T = 0.20
STERN_TAPER = 0.85


def half_beam(t):
    if t < STERN_TAPER_T:
        frac = t / STERN_TAPER_T
        smooth = frac * frac * (3 - 2 * frac)
        return BEAM * STERN_TAPER + smooth * BEAM * (1 - STERN_TAPER)
    if t < BOW_START_T:
        return BEAM
    d = min((t - BOW_START_T) * (BOW_X - STERN_X), OGIVE_L)
    return math.sqrt(max(OGIVE_RHO ** 2 - d ** 2, 0)) + OGIVE_R - OGIVE_RHO


# Superstructure t-ranges, aft -> fwd
FLIGHT_DECK = (0.03, 0.15)
HANGAR = (0.15, 0.27)
AFT_VLS = (0.27, 0.35)
MIDSHIPS = (0.435, 0.555)   # narrowed fore-and-aft from (0.42, 0.57)
MACK = (0.47, 0.52)
# Shortened from (0.63,0.81) and moved aft, freeing room fwd for a new
# 64-cell VLS plus the (not-yet-drawn) gun.
FWD_OCT = (0.58, 0.71)
FWD_VLS64 = (0.73, 0.785)

# ---------------------------------------------------------------------------
# Plan view
# ---------------------------------------------------------------------------
draw.text((40, 128), "PLAN VIEW", font=f_section, fill=TEXT_WHITE)
PLAN_Y = 720

draw.line([(STERN_X - 20, PLAN_Y), (BOW_X + 20, PLAN_Y)], fill=CENTERLINE, width=1)

N = 80
top_edge = [(hull_x(i / N), PLAN_Y - half_beam(i / N)) for i in range(N + 1)]
bottom_edge = [(hull_x(i / N), PLAN_Y + half_beam(i / N)) for i in range(N + 1)]
draw.polygon(top_edge + list(reversed(bottom_edge)), fill=HULL_FILL, outline=HULL_LINE)


def deck_rect(t_range, beam_frac, fill):
    t0, t1 = t_range
    x0, x1 = hull_x(t0), hull_x(t1)
    hb = min(half_beam(t0), half_beam(t1)) * beam_frac
    draw.rectangle([x0, PLAN_Y - hb, x1, PLAN_Y + hb], fill=fill, outline=HULL_LINE)
    return (x0, PLAN_Y - hb, x1, PLAN_Y + hb)


# Mk 38 25mm stabilized RWS (P/S), on the fantail (aftmost mount, was
# twin .50 cal -- upgraded for real fire control against small/fast
# surface and air threats).
fantail_t = 0.02
fantail_cx = hull_x(fantail_t)
for side in (-1, 1):
    mk38_plan(fantail_cx, PLAN_Y + side * 78, angle_deg=90 if side > 0 else 270)

fd_box = deck_rect(FLIGHT_DECK, 0.90, DECK_FILL)

# Flight deck markings (touchdown circle, centerline stripe, rotor-sweep
# hint) + an example MH-60R silhouette, real-scale, for scale reference.
fd_cx, fd_cy = (fd_box[0] + fd_box[2]) / 2, PLAN_Y
td_r = 30.5 * FT_PX       # touchdown circle, w/ clearance around the rotor sweep
rotor_r = 26.85 * FT_PX   # MH-60R main rotor radius (53.7 ft diameter)
draw.ellipse([fd_cx - td_r, fd_cy - td_r, fd_cx + td_r, fd_cy + td_r], outline=(210, 214, 220), width=2)
draw.line([(fd_box[0] + 10, fd_cy), (fd_box[2] - 10, fd_cy)], fill=(140, 152, 168), width=1)
dashed_circle(fd_cx, fd_cy, rotor_r, (150, 160, 172), width=1)
for ang in (0, 90, 180, 270):
    rad = math.radians(ang)
    draw.line([(fd_cx, fd_cy), (fd_cx + rotor_r * math.cos(rad), fd_cy + rotor_r * math.sin(rad))],
              fill=(150, 160, 172), width=1)

heli_len, heli_w = 32 * FT_PX, 10 * FT_PX
tail_len, tail_rotor_r = 20 * FT_PX, 4 * FT_PX
heli_nose_x = fd_cx + heli_len / 2
heli_cab_x = fd_cx - heli_len / 2
tail_x0 = heli_cab_x
tail_x1 = tail_x0 - tail_len
# fuselage: tapered nose, boxier cabin -- closer to an MH-60R's silhouette
# than a plain ellipse
draw.polygon([
    (heli_nose_x, fd_cy),
    (fd_cx + heli_len * 0.12, fd_cy - heli_w / 2),
    (tail_x0 + 6, fd_cy - heli_w * 0.34),
    (tail_x0, fd_cy - 3),
    (tail_x0, fd_cy + 3),
    (tail_x0 + 6, fd_cy + heli_w * 0.34),
    (fd_cx + heli_len * 0.12, fd_cy + heli_w / 2),
], fill=(60, 66, 78), outline=(150, 160, 172))
# stub-wing sponsons (external fuel tank pylons) -- a hallmark Seahawk feature
for sp_side in (-1, 1):
    sp_y0 = fd_cy + sp_side * heli_w * 0.42
    sp_y1 = fd_cy + sp_side * (heli_w / 2 + 7)
    draw.rectangle([fd_cx - heli_len * 0.06, min(sp_y0, sp_y1), fd_cx + heli_len * 0.14, max(sp_y0, sp_y1)],
                   fill=(60, 66, 78), outline=(150, 160, 172))
# tail boom rising slightly to the canted tail-rotor pylon
draw.line([(tail_x0, fd_cy), (tail_x1, fd_cy)], fill=(60, 66, 78), width=5)
draw.line([(tail_x1 - 8, fd_cy - 9), (tail_x1 + 6, fd_cy + 9)], fill=(150, 160, 172), width=2)  # horiz. stabilizer
draw.ellipse([tail_x1 - tail_rotor_r, fd_cy - tail_rotor_r, tail_x1 + tail_rotor_r, fd_cy + tail_rotor_r],
             outline=(150, 160, 172), width=1)

hangar_box = deck_rect(HANGAR, 0.62, SUPER_FILL)

hang_cx = (hangar_box[0] + hangar_box[2]) / 2
hang_hb = (hangar_box[3] - hangar_box[1]) / 2

# RHIB davits (P/S), flanking the hangar along the deck periphery --
# in the space the hangar-flanking Mk57 VLS used to occupy.
rhib_y = hang_hb + (half_beam((HANGAR[0] + HANGAR[1]) / 2) - hang_hb) * 0.6
rhib_boxes = {}
for side in (-1, 1):
    ry = PLAN_Y + side * rhib_y
    rhib_davit_plan(hang_cx, ry, side)
    rhib_boxes[side] = (hang_cx, ry)

# RAM (Mk49) trainable box launcher, at the aft end of the hangar roof.
ram_hangar_cx = hangar_box[0] + 28
ram_launcher_plan(ram_hangar_cx, PLAN_Y)

# 2x Phalanx CIWS, atop the hangar roof (P/S), facing aft.
ciws_hangar_cx = hang_cx + 15
for side in (-1, 1):
    ciws_plan(ciws_hangar_cx, PLAN_Y + side * hang_hb * 0.6, angle_deg=180)

# 500 kW laser mount, fwd end of the hangar roof (opposite the RAM at the aft end).
laser_hangar_cx = hangar_box[2] - 28
laser_plan(laser_hangar_cx, PLAN_Y, angle_deg=0)

# Aft VLS superstructure -- raised to hangar height, running from the
# hangar's fwd edge to the VLS deck's old fwd edge. A real-scale 64-cell
# Mk41 sits centered on its roof, flanked port/stbd by 4x 1x4 Mk57
# modules (32 cells total) along the periphery.
vls_box = deck_rect(AFT_VLS, 0.90, SUPER_FILL)
vls_cx = (vls_box[0] + vls_box[2]) / 2
vls_hb = (vls_box[3] - vls_box[1]) / 2

mk41_size = 8 * MK41_CELL_PX
mk41_x0, mk41_x1 = vls_cx - mk41_size / 2, vls_cx + mk41_size / 2
cell_grid(mk41_x0, PLAN_Y - mk41_size / 2, mk41_x1, PLAN_Y + mk41_size / 2, rows=8, cols=8, fill=MISSILE_DECK_FILL, pad=3)

mk57_mod_len = 4 * MK57_CELL_PX
mk57_mod_w = MK57_CELL_PX
mk57_gap = 6

# Two 1x4 Mk57 sets (P/S) flanking the aft Mk41, on the missile deck
# roof -- distinct from the single row flanking LD-VLS further fwd.
amk57_block_w = 2 * mk57_mod_len + mk57_gap
amk57_block_x0 = vls_cx - amk57_block_w / 2
amk57_boxes = {}
for side in (-1, 1):
    y_center = PLAN_Y + side * (vls_hb - mk57_mod_w / 2 - 6)
    y0, y1 = y_center - mk57_mod_w / 2, y_center + mk57_mod_w / 2
    quad_modules(amk57_block_x0, y0, amk57_block_x0 + amk57_block_w, y1,
                 n_modules=2, fill=MISSILE_DECK_FILL, gap=mk57_gap)
    amk57_boxes[side] = (amk57_block_x0, y0, amk57_block_x0 + amk57_block_w, y1)

# Large-diameter VLS (LD-VLS): 16 cells, larger-pitch tubes for
# strategic-strike / hypersonic-class rounds, sited in the gap between
# the aft VLS superstructure and midships. Pitch scaled up 1.3x from the
# original 6.8 ft (down from 1.5x when the cell count doubled 8->16,
# grown as 2x8 rather than 4x4 to keep the tight fore-aft gap to the
# midships pyramid) -- the beam dim line (below) was pulled in tight
# against the aft VLS superstructure to leave room for it.
LD_CELL_PX = 6.8 * 1.3 * FT_PX
ld_t = 0.418
ld_cx = hull_x(ld_t)
ld_w, ld_h = 2 * LD_CELL_PX, 8 * LD_CELL_PX
ld_x0, ld_y0, ld_x1, ld_y1 = ld_cx - ld_w / 2, PLAN_Y - ld_h / 2, ld_cx + ld_w / 2, PLAN_Y + ld_h / 2
cell_grid(ld_x0, ld_y0, ld_x1, ld_y1, rows=8, cols=2, fill=MISSILE_DECK_FILL, pad=2)

# Midships: truncated pyramid (base + inset top) topped by a mack that
# tapers in more sharply (a smaller top relative to its own base). The
# superstructure's own taper is shallow -- less sharply inclined walls,
# read from above as a wide inset roof close to the base footprint.
pyr_box = deck_rect(MIDSHIPS, 0.68, PYRAMID_FILL)
pyr_x0, pyr_y0, pyr_x1, pyr_y1 = pyr_box
pyr_inset_x = (pyr_x1 - pyr_x0) * 0.08
pyr_top_hb = (pyr_y1 - pyr_y0) / 2 * 0.78
draw.rectangle([pyr_x0 + pyr_inset_x, PLAN_Y - pyr_top_hb, pyr_x1 - pyr_inset_x, PLAN_Y + pyr_top_hb],
               outline=HULL_LINE, width=2)

# Mk32 SVTT-style triple torpedo tubes flanking the fwd end of the
# midships superstructure, mounted near the deck edge.
torp_y_off = half_beam(MIDSHIPS[0]) - 14
for side in (-1, 1):
    torpedo_mount(pyr_x0 - 4, PLAN_Y + side * torp_y_off, side, SUPER_FILL)

# 4x OTO Melara 76mm STRALES (2 P/S), flanking midships along its
# length, facing outward -- plus a twin .50 cal amidships between them.
gun76_y = 96
gun76_aft_x = pyr_x0 + 40
gun76_fwd_x = pyr_x1 - 40
gun76_positions = {}
for side in (-1, 1):
    ang = 90 if side > 0 else 270
    for label_key, gx in (("aft", gun76_aft_x), ("fwd", gun76_fwd_x)):
        gun76_plan(gx, PLAN_Y + side * gun76_y, angle_deg=ang)
        gun76_positions[(side, label_key)] = (gx, PLAN_Y + side * gun76_y)
    twin50_plan(gun76_aft_x + (gun76_fwd_x - gun76_aft_x) / 2, PLAN_Y + side * gun76_y, angle_deg=ang)

# Mk57 flanking LD-VLS, at the outer deck edges -- a single row, tucked
# in just aft of the Mk32 mounts (the aft Mk41 has its own flanking
# Mk57 sets back on the missile deck, above).
mk57_n = 1
mk57_block_w = mk57_mod_len  # single module wide (fore-aft) -- keeps it compact in the tight gap
mk57_block_h = mk57_n * (mk57_mod_w + mk57_gap) - mk57_gap
mk57_block_x1 = pyr_x0 - 40  # clear of the Mk32 mounts flanking the pyramid's fwd end
mk57_block_x0 = mk57_block_x1 - mk57_block_w
ld_hb = half_beam(ld_t)
mk57_boxes = {}
for side in (-1, 1):
    outer_y = PLAN_Y + side * (ld_hb - 4)
    inner_y = outer_y - side * mk57_block_h
    y0, y1 = min(outer_y, inner_y), max(outer_y, inner_y)
    for row in range(mk57_n):
        ry0 = y0 + row * (mk57_mod_w + mk57_gap)
        quad_modules(mk57_block_x0, ry0, mk57_block_x0 + mk57_block_w, ry0 + mk57_mod_w,
                     n_modules=1, fill=MISSILE_DECK_FILL, gap=mk57_gap)
    mk57_boxes[side] = (mk57_block_x0, y0, mk57_block_x0 + mk57_block_w, y1)

mack_box = deck_rect(MACK, 0.40, MACK_FILL)
mack_x0, mack_y0, mack_x1, mack_y1 = mack_box
mack_inset_x = (mack_x1 - mack_x0) * 0.24
mack_top_hb = (mack_y1 - mack_y0) / 2 * 0.45
draw.rectangle([mack_x0 + mack_inset_x, PLAN_Y - mack_top_hb, mack_x1 - mack_inset_x, PLAN_Y + mack_top_hb],
               outline=HULL_LINE, width=2)

# EHF/SHF/UHF SATCOM radomes, clustered on the mack roof -- the ship's
# tallest mast, with the clearest all-around sky view.
mack_cx = (mack_x0 + mack_x1) / 2
ehf_pt = (mack_cx - 12, PLAN_Y - 8)
shf_pt = (mack_cx + 12, PLAN_Y - 8)
uhf_pt = (mack_cx, PLAN_Y + 10)
radome_plan(*ehf_pt, 6)
radome_plan(*shf_pt, 6)
radome_plan(*uhf_pt, 6)

# Surface-search radar, aft mount -- on the mack, below the SATCOM cluster.
mack_radar_pt = (mack_cx, PLAN_Y - 30)
surface_radar_plan(*mack_radar_pt)

# UNREP kingposts (P/S), inward-canted, in the gap between midships and
# the fwd superstructure. Shown foreshortened from directly above: a
# line from the hull-edge base to a top point pulled in toward the
# centerline, plus a short yard hint near the top.
kp_t = 0.567
kp_cx = hull_x(kp_t)
kp_hb = half_beam(kp_t)
kingpost_tops = {}
for side in (-1, 1):
    kp_base_y = PLAN_Y + side * (kp_hb - 10)
    kp_top_y = PLAN_Y + side * (kp_hb - 10) * 0.3
    draw.line([(kp_cx, kp_base_y), (kp_cx, kp_top_y)], fill=(150, 160, 172), width=3)
    draw.ellipse([kp_cx - 3, kp_base_y - 3, kp_cx + 3, kp_base_y + 3], fill=SUPER_FILL, outline=HULL_LINE)
    draw.line([(kp_cx - 10, kp_top_y), (kp_cx + 10, kp_top_y)], fill=(150, 160, 172), width=2)

# Twin .50 cal MG (P/S), next to the kingposts.
tw50_kp_cx = kp_cx + 18
for side in (-1, 1):
    twin50_plan(tw50_kp_cx, PLAN_Y + side * (kp_hb - 10), angle_deg=90 if side > 0 else 270)
    kingpost_tops[side] = (kp_cx, kp_top_y)

# Forward superstructure: a stretched octagon (long, shallow corner
# cuts) spanning the full beam.
ocx = hull_x((FWD_OCT[0] + FWD_OCT[1]) / 2)
o_hw = (hull_x(FWD_OCT[1]) - hull_x(FWD_OCT[0])) / 2
o_hh = half_beam((FWD_OCT[0] + FWD_OCT[1]) / 2) * 0.93
k = 0.22
oct_pts = [
    (ocx - o_hw * (1 - k), PLAN_Y - o_hh), (ocx + o_hw * (1 - k), PLAN_Y - o_hh),
    (ocx + o_hw, PLAN_Y - o_hh * (1 - k)), (ocx + o_hw, PLAN_Y + o_hh * (1 - k)),
    (ocx + o_hw * (1 - k), PLAN_Y + o_hh), (ocx - o_hw * (1 - k), PLAN_Y + o_hh),
    (ocx - o_hw, PLAN_Y + o_hh * (1 - k)), (ocx - o_hw, PLAN_Y - o_hh * (1 - k)),
]
draw.polygon(oct_pts, fill=OCT_FILL, outline=HULL_LINE)

# SPY-6 AESA panels on the octagon's 4 diagonal (corner-cut) faces.
spy6_edges = [(oct_pts[1], oct_pts[2]), (oct_pts[3], oct_pts[4]),
              (oct_pts[5], oct_pts[6]), (oct_pts[7], oct_pts[0])]
for p0, p1 in spy6_edges:
    edge_panel(p0, p1, (ocx, PLAN_Y))

# Small projecting platform on the fwd (bow-facing) face, like the
# forward CIWS platform on the Arleigh Burke class.
plat_hw = 20
plat_depth = 16
plat_x0 = ocx + o_hw
draw.rectangle([plat_x0, PLAN_Y - plat_hw, plat_x0 + plat_depth, PLAN_Y + plat_hw],
               fill=SUPER_FILL, outline=HULL_LINE)

# 500 kW laser mount, on the fwd platform.
laser_plat_cx = plat_x0 + plat_depth / 2
laser_plan(laser_plat_cx, PLAN_Y, angle_deg=0)

# Octagonal stealth mast (LPD-17 AEM/S-style composite structure),
# somewhat forward of center on the fwd superstructure's roof, w/ an
# SPQ-9B horizon/periscope-detection radar mounted atop it.
mast_cx = ocx + 0.35 * o_hw
mast_hw, mast_hh = 24, 26
mk_k = 0.3
mast_pts = [
    (mast_cx - mast_hw * (1 - mk_k), PLAN_Y - mast_hh), (mast_cx + mast_hw * (1 - mk_k), PLAN_Y - mast_hh),
    (mast_cx + mast_hw, PLAN_Y - mast_hh * (1 - mk_k)), (mast_cx + mast_hw, PLAN_Y + mast_hh * (1 - mk_k)),
    (mast_cx + mast_hw * (1 - mk_k), PLAN_Y + mast_hh), (mast_cx - mast_hw * (1 - mk_k), PLAN_Y + mast_hh),
    (mast_cx - mast_hw, PLAN_Y + mast_hh * (1 - mk_k)), (mast_cx - mast_hw, PLAN_Y - mast_hh * (1 - mk_k)),
]
draw.polygon(mast_pts, fill=(46, 50, 58), outline=HULL_LINE)
draw.ellipse([mast_cx - 6, PLAN_Y - 6, mast_cx + 6, PLAN_Y + 6], fill=(30, 34, 42), outline=HULL_LINE)

# Surface-search radar, fwd mount -- on the mast's aft face.
mast_radar_pt = (mast_cx - 40, PLAN_Y)
surface_radar_plan(*mast_radar_pt)

# 2x AN/SLQ-32(V)7 EW arrays, mounted flush on the mast's port/stbd faces.
for side in (-1, 1):
    yA, yB = PLAN_Y + side * (mast_hh - 3), PLAN_Y + side * (mast_hh + 3)
    draw.rectangle([mast_cx - 7, min(yA, yB), mast_cx + 7, max(yA, yB)],
                   fill=(35, 55, 70), outline=HULL_LINE)

# 2x Phalanx CIWS flanking the mast (P/S), facing fwd.
ciws_mast_y_off = mast_hh + 18
for side in (-1, 1):
    ciws_plan(mast_cx, PLAN_Y + side * ciws_mast_y_off, angle_deg=0)

# RAM (Mk49) trainable box launcher, fwd edge of the fwd superstructure roof.
ram_fwd_cx = ocx + 0.8 * o_hw
ram_launcher_plan(ram_fwd_cx, PLAN_Y)

# 8x Nulka decoy launchers, along the roof's port/stbd edges (4 each side).
nulka_y = o_hh - 6
nulka_xs = [ocx - 87.2 + f * (2 * 87.2) for f in (0.12, 0.37, 0.62, 0.87)]
nulka_boxes = []
for side in (-1, 1):
    for nx in nulka_xs:
        deck_box_launcher(nx, PLAN_Y + side * nulka_y, angle_deg=90, w=8, l=11, fill=(66, 72, 84))
        nulka_boxes.append((nx, PLAN_Y + side * nulka_y))

# 2x Mk 36 SRBOC chaff/decoy launchers (P/S), aft portion of the roof, inboard of the Nulka row.
srboc_boxes = {}
for side in (-1, 1):
    sx, sy = ocx - 75, PLAN_Y + side * (o_hh - 30)
    deck_box_launcher(sx, sy, angle_deg=90, w=12, l=16, fill=(72, 78, 90), tube_dots=(2, 3))
    srboc_boxes[side] = (sx, sy)

# New forward 64-cell Mk41 VLS, real-scale, between the (shortened,
# aft-shifted) fwd superstructure and the gun position reserved ahead of it.
fwd_vls_cx = hull_x((FWD_VLS64[0] + FWD_VLS64[1]) / 2)
fwd_mk41_x0, fwd_mk41_x1 = fwd_vls_cx - mk41_size / 2, fwd_vls_cx + mk41_size / 2
cell_grid(fwd_mk41_x0, PLAN_Y - mk41_size / 2, fwd_mk41_x1, PLAN_Y + mk41_size / 2,
          rows=8, cols=8, fill=MISSILE_DECK_FILL, pad=3)

# Mk57 flanking the fwd Mk41 complex, along the deck periphery: 2x 1x4
# modules (P/S) = 16 cells total.
fwd_mk57_mod_len = 4 * MK57_CELL_PX
fwd_mk57_gap = 6
fwd_mk57_block_w = 2 * fwd_mk57_mod_len + fwd_mk57_gap
fwd_mk57_block_x0 = fwd_vls_cx - fwd_mk57_block_w / 2
fwd_hb = half_beam((FWD_VLS64[0] + FWD_VLS64[1]) / 2)
fwd_mk57_boxes = {}
for side in (-1, 1):
    y_center = PLAN_Y + side * (fwd_hb - MK57_CELL_PX / 2 - 6)
    y0, y1 = y_center - MK57_CELL_PX / 2, y_center + MK57_CELL_PX / 2
    quad_modules(fwd_mk57_block_x0, y0, fwd_mk57_block_x0 + fwd_mk57_block_w, y1,
                 n_modules=2, fill=MISSILE_DECK_FILL, gap=fwd_mk57_gap)
    fwd_mk57_boxes[side] = (fwd_mk57_block_x0, y0, fwd_mk57_block_x0 + fwd_mk57_block_w, y1)

# Mk 142 8"/65 (203 mm) main gun, twin barrel, true-scale, forward of
# the fwd VLS complex -- boxy, angular turret on a barbette (ref: USS
# Hull's Mk 71 trials mount, redesignated Mk 142 for this class),
# enlarged and lengthened for the twin 65-caliber mount.
GUN_BARREL_PX = 43.33 * FT_PX   # 203 mm / 65 calibers
gun_len_px, gun_wid_px = 27 * FT_PX, 24 * FT_PX
barbette_r_px = 13 * FT_PX
BARREL_SEP_PX = 6.5 * FT_PX   # twin-barrel centerline spacing
gun_rear_x = fwd_mk41_x1 + 30
gun_front_x = gun_rear_x + gun_len_px
gun_cx = (gun_rear_x + gun_front_x) / 2
draw.ellipse([gun_cx - barbette_r_px, PLAN_Y - barbette_r_px, gun_cx + barbette_r_px, PLAN_Y + barbette_r_px],
             fill=(72, 78, 90), outline=HULL_LINE)
gun_pts = [
    (gun_rear_x, PLAN_Y - gun_wid_px * 0.42), (gun_rear_x + 8, PLAN_Y - gun_wid_px / 2),
    (gun_cx + 6, PLAN_Y - gun_wid_px / 2), (gun_front_x, PLAN_Y - gun_wid_px * 0.28),
    (gun_front_x, PLAN_Y + gun_wid_px * 0.28), (gun_cx + 6, PLAN_Y + gun_wid_px / 2),
    (gun_rear_x + 8, PLAN_Y + gun_wid_px / 2), (gun_rear_x, PLAN_Y + gun_wid_px * 0.42),
]
draw.polygon(gun_pts, fill=(80, 86, 98), outline=HULL_LINE)
barrel_tip_x = gun_front_x + GUN_BARREL_PX
for off in (-BARREL_SEP_PX / 2, BARREL_SEP_PX / 2):
    draw.line([(gun_front_x, PLAN_Y + off), (barrel_tip_x, PLAN_Y + off)], fill=(180, 184, 190), width=5)

# Forecastle (2 pairs) -- the aft pair (twin .50 cal) sits aft of the
# fwd Mk57 VLS complex, clear of both the VLS footprint and the Mk
# 142's train circle; the fwd pair (foremost mounts on the ship,
# upgraded to Mk 38 25mm stabilized RWS) sits well forward of the
# muzzle, also clear of the train circle.
for side in (-1, 1):
    twin50_plan(fwd_mk57_block_x0 - 20, PLAN_Y + side * 90, angle_deg=90 if side > 0 else 270)
    mk38_plan(barrel_tip_x + 15, PLAN_Y + side * 68, angle_deg=90 if side > 0 else 270)

dim_line((STERN_X, PLAN_Y + BEAM + 320), (BOW_X, PLAN_Y + BEAM + 320),
         f"{LOA_FT} ft ({round(LOA_FT * 0.3048)} m) LOA")
max_beam_t = 0.352  # pulled in tight against the aft VLS superstructure to clear the enlarged LD-VLS
dim_line((hull_x(max_beam_t), PLAN_Y - half_beam(max_beam_t)), (hull_x(max_beam_t), PLAN_Y + half_beam(max_beam_t)),
          f"{BEAM_FT} ft beam")

ABOVE_TIERS = [PLAN_Y - (130 + 40 * i) for i in range(5)]  # matches len(above_entries): no tier wrap, so no item can land close enough to the hull edge to clip it
BELOW_TIERS = [PLAN_Y + (120 + 40 * i) for i in range(7)]

# Forward cluster de-crowded: half stay above (auto-tiered) and half
# move below the ship (near their lower/starboard-side instance, for a
# short leader line); two of the above items are pinned manually with
# an x-offset from their point, giving angled (not just vertical)
# leaders instead of stacking straight up in a single column.
above_entries = [
    ((fd_box[0] + 20, fd_box[1]), "FLIGHT DECK", "markings + example MH-60R"),
    ((mk41_x0 + 15, PLAN_Y - mk41_size / 2), "MK41 VLS", "Primary armament"),
    ((ld_x0, ld_y0), "LD-VLS", "16-cell, large-diameter"),
    ((laser_plat_cx, PLAN_Y - 11), "500 kW LASER", "x2: fwd platform + fwd hangar roof"),
    ((fwd_mk41_x0 + 15, PLAN_Y - mk41_size / 2), "MK41 VLS", "Primary armament"),
]
place_tiered(above_entries, ABOVE_TIERS)

leader_label((mast_cx, PLAN_Y - ciws_mast_y_off), (mast_cx - 95, PLAN_Y - 175),
             "PHALANX CIWS", "20mm PD gun")
leader_label((ram_fwd_cx, PLAN_Y - 13), (ram_fwd_cx + 115, PLAN_Y - 210),
             "RIM-116 RAM", "missile CIWS")
leader_label((mast_cx, PLAN_Y - 6), (mast_cx - 40, PLAN_Y - 340),
             "SPQ-9B", "horizon/periscope search radar")

# Mk 142 gun label -- placed below the ship (clear of the turret/barrel
# itself) rather than above it, and still clear of the specs/loadout
# panels regardless of x.
leader_label((gun_cx, PLAN_Y + gun_wid_px / 2), (min(gun_cx, W - 140), PLAN_Y + 190),
             'MK 142 8" GUN', "203 mm/65, twin barrel, true-scale")

below_entries = [
    ((hangar_box[0] + 20, hangar_box[3]), "HANGAR", None),
    ((ram_hangar_cx, PLAN_Y + 13), "RIM-116 RAM", "missile CIWS"),
    ((ciws_hangar_cx, PLAN_Y + hang_hb * 0.6), "PHALANX CIWS", "20mm PD gun"),
    (rhib_boxes[1], "RHIB DAVITS", "x2 (P/S), flanking hangar"),
    ((mk57_boxes[1][0] - 10, mk57_boxes[1][3]), "MK57 VLS", "Peripheral VLS for SR/MR AAW"),
    ((gun76_positions[(1, "aft")][0], gun76_positions[(1, "aft")][1] + 8), "76mm STRALES",
     "Defensive battery, x4 (2 P/S) flanking midships"),
    ((kingpost_tops[1][0], PLAN_Y + (kp_hb - 10)), "UNREP KINGPOSTS", "STREAM cargo/fuel transfer"),
    (uhf_pt, "SATCOM RADOMES", "EHF/SHF/UHF, mack-mounted"),
    ((srboc_boxes[1][0], srboc_boxes[1][1] + 10), "MK 36 SRBOC", "x2 (P/S), fwd superstructure roof"),
    ((pyr_x0 - 4, PLAN_Y + torp_y_off), "MK32 SVTT", "triple torpedo tubes (P/S), typ."),
    ((gun76_aft_x + (gun76_fwd_x - gun76_aft_x) / 2, PLAN_Y + gun76_y + 8), "TWIN .50 CAL RWS",
     "x6, stabilized: midships, kingposts, aft forecastle"),
    ((fantail_cx, PLAN_Y + 78 + 8), "MK 38 25mm", "x4: fantail, fwd forecastle (P/S), stabilized"),
    ((nulka_boxes[6][0], nulka_boxes[6][1]), "NULKA", "Active decoy"),
    ((mast_cx, PLAN_Y + (mast_hh + 3)), "AN/SLQ-32(V)7", "x2 (P/S), mast-mounted"),
    (((spy6_edges[1][0][0] + spy6_edges[1][1][0]) / 2, spy6_edges[1][1][1]), "SPY-6 PANELS", "AESA, 4 diagonal faces"),
    (mack_radar_pt, "SURFACE SEARCH RADAR", "x2: mast + mack"),
]
place_tiered(below_entries, BELOW_TIERS)

# ---------------------------------------------------------------------------
# Profile / side elevation
# ---------------------------------------------------------------------------
PROFILE_Y = 1230
draw.text((40, PROFILE_Y), "PROFILE / SIDE ELEVATION", font=f_section, fill=TEXT_WHITE)

DECK_Y = PROFILE_Y + 420
KEEL_Y = DECK_Y + 95
WATERLINE_Y = KEEL_Y - 22

# Three-zone stem (ref: Flight III Burke drydock photo, DDG-125): the
# deck rakes sharply forward; that rake tapers back to near-vertical
# approaching the waterline (the hull "tucks in" there); then the bulb
# projects forward again below the waterline -- past the tucked vertical
# point, but not as far forward as the raked deck edge above it.
STEM_P0 = (BOW_X - 260, KEEL_Y)          # end of flat keel
BULB_SHOULDER = (BOW_X - 190, KEEL_Y + 15)
BULB_BOTTOM = (BOW_X - 110, KEEL_Y + 45)  # deepest, roundest point of the bulb
VERT_POINT = (BOW_X - 45, WATERLINE_Y - 10)  # tucked-in, near-vertical point
DECK_POINT = (BOW_X + 35, DECK_Y - 30)    # deck edge -- the overall fwd-most point

# Bulb's nose: a swept arc (not a single point) so the fwd-most tip of
# the bulb is a rounded nose rather than a sharp cusp, sitting low.
NOSE_CENTER = (BOW_X - 30, WATERLINE_Y + 38)
NOSE_R = 24
nose_arc = []
angle = 115
while angle >= -115:
    rad = math.radians(angle)
    nose_arc.append((NOSE_CENTER[0] + NOSE_R * math.cos(rad), NOSE_CENTER[1] + NOSE_R * math.sin(rad)))
    angle -= 10

keel_pts = []
x = STERN_X + 60
while x < STEM_P0[0]:
    keel_pts.append((x, KEEL_Y))
    x += 20
keel_pts += eased_segment(STEM_P0, BULB_SHOULDER)
keel_pts += eased_segment(BULB_SHOULDER, BULB_BOTTOM)
keel_pts += eased_segment(BULB_BOTTOM, nose_arc[0])
keel_pts += nose_arc
keel_pts += eased_segment(nose_arc[-1], VERT_POINT)
keel_pts += eased_segment(VERT_POINT, DECK_POINT)

hull_side = [
    (STERN_X, DECK_Y),
    (STERN_X, DECK_Y + 50),
] + keel_pts + [
    (BOW_X - 55, DECK_Y - 5),
    (STERN_X + 45, DECK_Y - 5),
]
draw.polygon(hull_side, fill=HULL_FILL, outline=HULL_LINE)

# Hull number, painted at the standard USN position: well forward, just
# aft of where the bow begins to curve, on the flat hull side.
draw.text((BOW_X - 180, DECK_Y + 28), "74", font=f_hull_number, fill=(210, 214, 220), anchor="mm")

draw.line([(STERN_X - 20, WATERLINE_Y), (BOW_X + 20, WATERLINE_Y)], fill=WATERLINE, width=3)
draw.text((BOW_X + 30, WATERLINE_Y), "DWL", font=f_dim, fill=WATERLINE, anchor="lm")

# Flight deck (flush -- just the deck-edge line, no height) w/ the
# example MH-60R silhouette, visible in profile too: tapered nose,
# boxy cabin on gear struts, tail boom rising to a canted tail-rotor
# pylon w/ a stabilizer, and a rotor mast/disc hint on top.
fd_px0, fd_px1 = hull_x(FLIGHT_DECK[0]), hull_x(FLIGHT_DECK[1])
draw.line([(fd_px0, DECK_Y - 5), (fd_px1, DECK_Y - 5)], fill=(160, 168, 180), width=2)

# Mk 38 25mm RWS -- one representative icon (P/S pairs are at the
# fantail and fwd forecastle), on the fantail.
mk38_profile(hull_x(fantail_t), DECK_Y - 5)

heli_p_cx = (fd_px0 + fd_px1) / 2
heli_p_base = DECK_Y - 5
heli_gear_h = 3 * FT_PX
heli_body_h = 11 * FT_PX
heli_body_len = 32 * FT_PX
heli_p_bottom = heli_p_base - heli_gear_h
heli_p_top = heli_p_bottom - heli_body_h
heli_p_nose = heli_p_cx + heli_body_len / 2
heli_p_tail = heli_p_cx - heli_body_len / 2
for gx in (heli_p_cx - heli_body_len * 0.15, heli_p_cx + heli_body_len * 0.2):
    draw.line([(gx, heli_p_base), (gx, heli_p_bottom)], fill=(150, 160, 172), width=2)
draw.polygon([
    (heli_p_nose, (heli_p_top + heli_p_bottom) / 2),
    (heli_p_cx + heli_body_len * 0.25, heli_p_top),
    (heli_p_tail + 10, heli_p_top + 3),
    (heli_p_tail + 10, heli_p_bottom),
    (heli_p_cx + heli_body_len * 0.25, heli_p_bottom),
], fill=(60, 66, 78), outline=(150, 160, 172))
heli_p_tailtip_x = heli_p_tail - heli_body_len * 0.35
heli_p_tailtip_y = heli_p_top - 10
draw.line([(heli_p_tail + 10, (heli_p_top + heli_p_bottom) / 2), (heli_p_tailtip_x, heli_p_tailtip_y)],
          fill=(60, 66, 78), width=5)
draw.line([(heli_p_tailtip_x - 6, heli_p_tailtip_y + 4), (heli_p_tailtip_x + 6, heli_p_tailtip_y + 4)],
          fill=(150, 160, 172), width=2)
draw.ellipse([heli_p_tailtip_x - 5, heli_p_tailtip_y - 5, heli_p_tailtip_x + 5, heli_p_tailtip_y + 5],
             outline=(150, 160, 172), width=1)
heli_mast_top = heli_p_top - 10
draw.line([(heli_p_cx, heli_p_top), (heli_p_cx, heli_mast_top)], fill=(150, 160, 172), width=2)
draw.line([(heli_p_cx - rotor_r, heli_mast_top), (heli_p_cx + rotor_r, heli_mast_top)], fill=(150, 160, 172), width=1)

# Hangar
hang_x0, hang_x1 = hull_x(HANGAR[0]), hull_x(HANGAR[1])
hang_top = DECK_Y - 55
draw.rectangle([hang_x0, hang_top, hang_x1, DECK_Y - 5], fill=SUPER_FILL, outline=HULL_LINE)

# RAM (Mk49) trainable box launcher, at the aft end of the hangar roof.
ram_launcher_profile(ram_hangar_cx, hang_top)

# Phalanx CIWS on the hangar roof (one representative icon for the P/S
# pair -- profile can't show the beam separation), facing aft.
ciws_profile(ciws_hangar_cx, hang_top, facing=-1)

# 500 kW laser mount, fwd end of the hangar roof.
laser_profile(laser_hangar_cx, hang_top)

# RHIB davit, on the hangar's deck edge (one representative icon for
# the P/S pair).
rhib_davit_profile(hang_cx, DECK_Y - 5)

# Aft VLS superstructure -- raised to hangar height. Mk41 + Mk57 hatches
# are nearly flush with the roof (real VLS hatches sit low, not proud of
# the deck), shown as thin strips right at the roofline.
vls_x0, vls_x1 = hull_x(AFT_VLS[0]), hull_x(AFT_VLS[1])
vls_top = DECK_Y - 55
draw.rectangle([vls_x0, vls_top, vls_x1, DECK_Y - 5], fill=SUPER_FILL, outline=HULL_LINE)
mk41_hatch_y0, mk41_hatch_y1 = vls_top - 4, vls_top + 2
cell_grid((vls_x0 + vls_x1) / 2 - mk41_size / 2, mk41_hatch_y0, (vls_x0 + vls_x1) / 2 + mk41_size / 2, mk41_hatch_y1,
          rows=1, cols=8, fill=MISSILE_DECK_FILL, pad=1)

# Mk57 flush hatches flanking it, tucked into the roof margins fore and aft.
amk57_hint_w = 14
amk57_strip_y0, amk57_strip_y1 = vls_top - 4, vls_top + 2
amk57_hint_x0 = vls_x0 + 3
quad_modules(amk57_hint_x0, amk57_strip_y0, amk57_hint_x0 + amk57_hint_w, amk57_strip_y1,
             n_modules=1, fill=MISSILE_DECK_FILL, gap=mk57_gap)
quad_modules(vls_x1 - 3 - amk57_hint_w, amk57_strip_y0, vls_x1 - 3, amk57_strip_y1,
             n_modules=1, fill=MISSILE_DECK_FILL, gap=mk57_gap)

# LD-VLS -- low deck hint, nearly flush w/ the deck, 16-cell
# (larger pitch than Mk41/Mk57) -- and the Mk57 that now flanks it,
# both at the outer deck edge.
ld_top = DECK_Y - 11
cell_grid(ld_x0, ld_top, ld_x1, DECK_Y - 5, rows=1, cols=8, fill=MISSILE_DECK_FILL, pad=1)
mk57_strip_y0, mk57_strip_y1 = DECK_Y - 5, DECK_Y + 10
quad_modules(mk57_block_x0, mk57_strip_y0, mk57_block_x0 + mk57_block_w, mk57_strip_y1,
             n_modules=mk57_n, fill=MISSILE_DECK_FILL, gap=mk57_gap)

# Midships pyramid (shallow incline -- less sharply inclined walls than
# before, same height but a much smaller inset) + mack (steeper taper
# on top of it)
mid_x0, mid_x1 = hull_x(MIDSHIPS[0]), hull_x(MIDSHIPS[1])
pyr_top_y = DECK_Y - 95
pyr_inset = (mid_x1 - mid_x0) * 0.09
draw.polygon([
    (mid_x0, DECK_Y - 5), (mid_x1, DECK_Y - 5),
    (mid_x1 - pyr_inset, pyr_top_y), (mid_x0 + pyr_inset, pyr_top_y),
], fill=PYRAMID_FILL, outline=HULL_LINE)

# 76mm STRALES -- aft AND fwd representative icons (both are 2 P/S
# pairs flanking midships along its length) -- + twin .50 cal (one
# representative icon, a P/S pair flanking midships).
gun76_profile(mid_x0 + 40, DECK_Y - 5, facing=-1)
gun76_profile(mid_x1 - 40, DECK_Y - 5, facing=1)
twin50_profile((mid_x0 + mid_x1) / 2, DECK_Y - 5)

mack_x0, mack_x1 = hull_x(MACK[0]), hull_x(MACK[1])
mack_top_y = pyr_top_y - 65
mack_inset = (mack_x1 - mack_x0) * 0.30  # steeper taper than the pyramid below
draw.polygon([
    (mack_x0, pyr_top_y), (mack_x1, pyr_top_y),
    (mack_x1 - mack_inset, mack_top_y), (mack_x0 + mack_inset, mack_top_y),
], fill=MACK_FILL, outline=HULL_LINE)

# EHF/SHF/UHF SATCOM radomes, clustered on the mack's flat top.
mack_top_cx = (mack_x0 + mack_x1) / 2
radome_profile(mack_top_cx - 9, mack_top_y, 3.5)
radome_profile(mack_top_cx, mack_top_y, 3.5)
radome_profile(mack_top_cx + 9, mack_top_y, 3.5)

# Surface-search radar, aft mount -- on the mack, below the SATCOM cluster.
surface_radar_profile(mack_top_cx, mack_top_y + 12, height=8)

# UNREP kingposts, in the gap between midships and the fwd superstructure
# -- one representative icon (profile can't show the P/S beam
# separation), w/ a yard hint near the top.
kp_base_y = DECK_Y - 5
kp_height = 40
kp_top_y = kp_base_y - kp_height
draw.line([(kp_cx, kp_base_y), (kp_cx, kp_top_y)], fill=(150, 160, 172), width=3)
kp_yard_y = kp_top_y + 10
draw.line([(kp_cx - 16, kp_yard_y), (kp_cx + 16, kp_yard_y)], fill=(150, 160, 172), width=2)

# Forward octagonal superstructure -- redrawn as a simple trapezoid whose
# walls cant inward at a shallow angle (a small inset relative to its
# height), rather than vertical walls + a faceted top.
oct_x0, oct_x1 = hull_x(FWD_OCT[0]), hull_x(FWD_OCT[1])
oct_top_y = DECK_Y - 125
oct_inset = (oct_x1 - oct_x0) * 0.09
draw.polygon([
    (oct_x0, DECK_Y - 5), (oct_x1, DECK_Y - 5),
    (oct_x1 - oct_inset, oct_top_y), (oct_x0 + oct_inset, oct_top_y),
], fill=OCT_FILL, outline=HULL_LINE)

# Small projecting platform on the fwd face, like the fwd CIWS platform
# on the Arleigh Burke class -- a step-out ledge partway up the slope.
plat_f = 0.45
plat_px = oct_x1 - oct_inset * plat_f
plat_py = (DECK_Y - 5) - plat_f * ((DECK_Y - 5) - oct_top_y)
plat_p_depth, plat_p_h = 14, 8
draw.rectangle([plat_px, plat_py - plat_p_h, plat_px + plat_p_depth, plat_py], fill=SUPER_FILL, outline=HULL_LINE)

# 500 kW laser mount, on the fwd platform.
laser_profile(plat_px + plat_p_depth / 2, plat_py - plat_p_h)

# Phalanx CIWS flanking the mast (one representative icon), facing fwd.
ciws_profile(mast_cx - 45, oct_top_y, facing=1)

# 2x Nulka + Mk 36 SRBOC (one representative icon each) along the roof.
deck_box_launcher(oct_x0 + 18, oct_top_y - 4, angle_deg=0, w=8, l=11, fill=(66, 72, 84))
deck_box_launcher(oct_x0 + 40, oct_top_y - 5, angle_deg=0, w=12, l=16, fill=(72, 78, 90), tube_dots=(2, 3))

# Octagonal stealth mast (LPD-17 AEM/S-style), somewhat fwd of center,
# w/ an SPQ-9B radar on a short pedestal atop it, and an AN/SLQ-32(V)7
# EW array panel on its side (one representative icon for the P/S pair).
mast_x0, mast_x1 = mast_cx - mast_hw, mast_cx + mast_hw
mast_top_y = oct_top_y - 55
mast_inset = (mast_x1 - mast_x0) * 0.06
draw.polygon([
    (mast_x0, oct_top_y), (mast_x1, oct_top_y),
    (mast_x1 - mast_inset, mast_top_y), (mast_x0 + mast_inset, mast_top_y),
], fill=(46, 50, 58), outline=HULL_LINE)
slq32_y0 = mast_top_y + (oct_top_y - mast_top_y) * 0.15
draw.rectangle([mast_x0 + 2, slq32_y0, mast_x0 + 8, slq32_y0 + 16], fill=(35, 55, 70), outline=HULL_LINE)
spq_top_y = mast_top_y - 10
draw.line([(mast_cx, mast_top_y), (mast_cx, spq_top_y)], fill=HULL_LINE, width=3)
draw.rectangle([mast_cx - 2, spq_top_y - 14, mast_cx + 2, spq_top_y], fill=(200, 204, 210), outline=HULL_LINE)

# Surface-search radar, fwd mount -- bracketed to the mast, opposite the SLQ-32.
surface_radar_profile(mast_x1 - 3, mast_top_y + 14, height=10)

# RAM (Mk49) trainable box launcher, fwd edge of the fwd superstructure roof.
ram_launcher_profile(ram_fwd_cx, oct_top_y)

# New forward 64-cell Mk41 VLS -- low deck box, real-scale, flush
fwd_vls_x0, fwd_vls_x1 = hull_x(FWD_VLS64[0]), hull_x(FWD_VLS64[1])
fwd_vls_top = DECK_Y - 11
cell_grid((fwd_vls_x0 + fwd_vls_x1) / 2 - mk41_size / 2, fwd_vls_top,
          (fwd_vls_x0 + fwd_vls_x1) / 2 + mk41_size / 2, DECK_Y - 5,
          rows=1, cols=8, fill=MISSILE_DECK_FILL, pad=1)

# Mk 142 gun -- barbette drum + boxy turret w/ sloped front glacis, twin
# long thin barrels (shown as slightly offset parallel lines, since a
# true side-by-side twin mount is superimposed in profile) roughly at
# trunnion height.
gun_base_y = DECK_Y - 5
barbette_h = 9 * FT_PX
turret_h = 13 * FT_PX
barbette_top_y = gun_base_y - barbette_h
turret_top_y = barbette_top_y - turret_h
barrel_y = barbette_top_y - turret_h * 0.42
gun_rear_xp = fwd_vls_x1 + 30
gun_front_xp = gun_rear_xp + gun_len_px
draw.rectangle([gun_rear_xp - 6, barbette_top_y, gun_front_xp + 6, gun_base_y],
               fill=(72, 78, 90), outline=HULL_LINE)
draw.polygon([
    (gun_rear_xp, barbette_top_y), (gun_rear_xp, turret_top_y),
    (gun_front_xp - 12, turret_top_y), (gun_front_xp, barrel_y),
    (gun_front_xp, barbette_top_y),
], fill=(80, 86, 98), outline=HULL_LINE)
barrel_tip_xp = gun_front_xp + GUN_BARREL_PX
for boff in (-3, 3):
    draw.line([(gun_front_xp, barrel_y + boff), (barrel_tip_xp, barrel_y + boff)], fill=(180, 184, 190), width=4)

dim_line((STERN_X, DECK_Y + 145), (BOW_X, DECK_Y + 145), f"{LOA_FT} ft ({round(LOA_FT * 0.3048)} m) LOA")
dim_line((STERN_X + 95, WATERLINE_Y), (STERN_X + 95, KEEL_Y),
         f"~{DRAFT_FT} ft ({round(DRAFT_FT * 0.3048)} m) draft, indicative")

profile_above = [
    (((hang_x0 + hang_x1) / 2, hang_top), "HANGAR", None),
    ((hang_cx, DECK_Y - 5 - 16), "RHIB DAVITS", "x2 (P/S)"),
    (((vls_x0 + vls_x1) / 2, mk41_hatch_y0), "MK41 VLS", "Primary armament"),
    (((fwd_vls_x0 + fwd_vls_x1) / 2, fwd_vls_top), "MK41 VLS", "Primary armament"),
    (((ld_x0 + ld_x1) / 2, ld_top), "LD-VLS", "16-cell, large-diameter"),
    ((gun_front_xp, barrel_y), 'MK 142 8" GUN', "203 mm/65, twin barrel"),
    ((ram_fwd_cx, oct_top_y - 24), "RIM-116 RAM", "missile CIWS"),
    ((ram_hangar_cx, hang_top - 24), "RIM-116 RAM", "missile CIWS"),
    ((mast_cx - 45, oct_top_y - 20), "PHALANX CIWS", "20mm PD gun"),
    ((ciws_hangar_cx, hang_top - 20), "PHALANX CIWS", "20mm PD gun"),
    ((kp_cx, kp_top_y), "UNREP KINGPOSTS", "STREAM cargo/fuel transfer"),
    ((plat_px + plat_p_depth / 2, plat_py - plat_p_h - 16), "500 kW LASER", "x2: fwd platform + fwd hangar roof"),
    ((mid_x0 + 40, DECK_Y - 5 - 16), "76mm STRALES", "Defensive battery, x4 (2 P/S)"),
    ((oct_x0 + 18, oct_top_y - 10), "NULKA", "Active decoy"),
    ((oct_x0 + 40, oct_top_y - 15), "MK 36 SRBOC", "x2 (P/S)"),
    ((mast_x0 + 5, slq32_y0), "AN/SLQ-32(V)7", "x2 (P/S), mast-mounted"),
    (((mid_x0 + mid_x1) / 2, DECK_Y - 5 - 8), "TWIN .50 CAL RWS", "x6, stabilized (P/S)"),
    ((hull_x(fantail_t), DECK_Y - 5 - 8), "MK 38 25mm", "x4, stabilized (P/S)"),
    ((mast_cx, spq_top_y - 14), "SPQ-9B", "horizon/periscope search radar"),
    ((mack_top_cx, mack_top_y), "SATCOM RADOMES", "EHF/SHF/UHF, mack-mounted"),
    ((mast_x1 - 3, mast_top_y + 14 - 10), "SURFACE SEARCH RADAR", "x2: mast + mack"),
]
place_tiered(profile_above, [mack_top_y - (25 + 40 * i) for i in range(7)])

# ---------------------------------------------------------------------------
# Specifications + guided-weapon loadout insets
# ---------------------------------------------------------------------------
total_mk41 = 64 + 64
total_mk57 = 8 + 16 + 16  # LD-VLS outer-edge + aft Mk41 + fwd Mk41 (hangar-flanking removed for RHIB davits)
total_ld = 16

# Both insets moved to the left side (above the flight deck/hangar,
# below the "PLAN VIEW" header) for more room -- the plan view's own
# "above" labels don't start until y=510 in this x-range, and the
# hull's own deck edge doesn't reach up this far either, so there's
# clearance to place them side by side instead of squeezed into a
# single narrow stacked column on the right.
spec_panel = (40, 158, 470, 458)
draw.rectangle(spec_panel, outline=DIM_LINE, width=2)
draw.text((spec_panel[0] + 16, spec_panel[1] + 14), "SPECIFICATIONS", font=f_panel_head, fill=TEXT_WHITE)
spec_rows = [
    ("Length / Beam", f"{LOA_FT} ft ({round(LOA_FT * 0.3048)} m) / {BEAM_FT} ft ({round(BEAM_FT * 0.3048)} m)"),
    ("Draft", f"~{DRAFT_FT} ft ({round(DRAFT_FT * 0.3048)} m), indicative"),
    ("Displacement", "~20,500 t full load (est.)"),
    ("Speed", "30+ knots (est.)"),
    ("Main gun", "1 x Mk 142 8\"/65 (203 mm), twin barrel"),
    ("VLS", f"{total_mk41} Mk41 + {total_mk57} Mk57 + {total_ld} LD-VLS ({total_mk41 + total_mk57 + total_ld})"),
    ("Sonar", "SQS-53 bow-mounted, TB-37 towed array"),
    ("Point defense", "RAM, 76mm gun, Phalanx + softkill"),
    ("Electronic Warfare", "SLQ-32(V)7, chaff, flares, Nulka, Nixie"),
    ("DEW", "2x 500kW laser"),
    ("Propulsion", "IEP, 8 gas turbines, 4 shafts"),
]
ry = spec_panel[1] + 45
for k, v in spec_rows:
    draw.text((spec_panel[0] + 16, ry), k, font=f_panel_row_sm, fill=TEXT_DIM)
    draw.text((spec_panel[0] + 150, ry), v, font=f_panel_row_sm, fill=TEXT_WHITE)
    ry += 22

loadout_panel = (490, 158, 920, 447)
draw.rectangle(loadout_panel, outline=DIM_LINE, width=2)
draw.text((loadout_panel[0] + 16, loadout_panel[1] + 14), "GUIDED-WEAPON LOADOUT (VLS)", font=f_panel_head, fill=TEXT_WHITE)
loadout_rows = [
    ("ESSM", "SR anti-air, quad-pack per cell"),
    ("SM-2", "MR anti-air, twin-pack in Mk 57 cell"),
    ("SM-6", "LR anti-air, dual-role"),
    ("SM-3", "BMD, exo-atmospheric intercept"),
    ("Tomahawk", "Land-attack / anti-ship"),
    ("LRASM", "Long-range anti-ship"),
    ("LCBM", "Land-attack"),
    ("VL-ASROC", "ASW rocket"),
    ("Mk57 cell", "Larger dia., peripheral, blast-vented"),
    ("LD-VLS cell", "Large-dia. tube, strike/hypersonic"),
    ("DART", "76/203mm guided sub-cal. round"),
    ("VULCANO", "76/203mm long-range guided round"),
]
ry = loadout_panel[1] + 45
for k, v in loadout_rows:
    draw.text((loadout_panel[0] + 16, ry), "• " + k, font=f_panel_row_sm, fill=(120, 150, 200))
    draw.text((loadout_panel[0] + 165, ry), v, font=f_panel_row_sm, fill=TEXT_WHITE)
    ry += 19

out_path = "new_cruiser.png"
img.save(out_path)
print("saved", out_path, img.size)
