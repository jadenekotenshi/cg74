"""Recreation of the original CG-74 Denver-class missile cruiser reference
diagram (~/Downloads/heavy_cruiser.png): a twin-203mm-turret, octagonal-
bridge cruiser with a dense weapons fit -- distinct from the custom
Burke-family "CG74-new" redesign built elsewhere in this project.

Plan view (aft -> fwd, t = 0 -> 1):
  twin 203mm turret (tier 1, fantail) + Mk57 x24 flanking | VLS x64
  (tier 2) + Mk57 x20 flanking | flight deck (tier 3, raised) w/ helo
  spot | hangar (Coyote UAV roof, 30mm, RAM aft edge) | APKWS x2 P/S |
  VLS x32 amidships | octagonal bridge (SPY-6 diagonal faces, Phalanx,
  lasers, Nulka, SRBOC, .50-cals, kingposts, Mk32 TT) | mast (SPQ-9B,
  SPY-3, Satcom) | 76mm x2 P/S (x2 pairs) | VLS x16 large-dia | twin
  203mm turret (No.1, forward) | bow sonar dome

Output: CG74-new.png (current directory)
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 2650

BG = (10, 21, 38)
HULL_FILL = (66, 74, 88)
HULL_LINE = (150, 160, 172)
DECK_FILL = (92, 100, 114)
SUPER_FILL = (108, 116, 130)
TURRET_FILL = (86, 92, 102)
VLS_FILL = (72, 96, 150)
VLS_LD_FILL = (94, 82, 150)
RAM_FILL = (176, 60, 55)
APKWS_FILL = (190, 100, 60)
SEVENTYSIX_FILL = (176, 96, 60)
PHALANX_FILL = (215, 218, 222)
LASER_FILL = (70, 190, 205)
NULKA_FILL = (140, 150, 85)
SRBOC_FILL = (205, 200, 70)
SLQ32_FILL = (120, 128, 140)
SPY6_FILL = (60, 110, 190)
SPY3_FILL = (60, 150, 150)
COYOTE_FILL = (110, 130, 95)
MG_FILL = (225, 228, 232)
TEXT_WHITE = (232, 236, 240)
TEXT_DIM = (140, 152, 168)
LEADER = (150, 160, 172)
WATERLINE = (176, 48, 48)
PANEL_LINE = (70, 90, 120)

FONT_DIR = "/System/Library/Fonts/Supplemental/"
f_title = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 44)
f_subtitle = ImageFont.truetype(FONT_DIR + "Arial.ttf", 22)
f_section = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 24)
f_label = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 16)
f_label_sub = ImageFont.truetype(FONT_DIR + "Arial.ttf", 14)
f_panel_head = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 18)
f_panel_row = ImageFont.truetype(FONT_DIR + "Arial.ttf", 16)
f_hull_no = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 50)
f_hull_name = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 28)
f_footnote = ImageFont.truetype(FONT_DIR + "Arial.ttf", 15)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)


def leader_label(point, text_xy, text, sub=None, anchor="ma"):
    draw.line([point, text_xy], fill=LEADER, width=1)
    r = 2.5
    draw.ellipse([point[0] - r, point[1] - r, point[0] + r, point[1] + r], fill=TEXT_WHITE)
    draw.text(text_xy, text, font=f_label, fill=TEXT_WHITE, anchor=anchor)
    if sub:
        sub_anchor = "m" + anchor[1] if anchor[0] == "m" else anchor
        draw.text((text_xy[0], text_xy[1] + 21), sub, font=f_label_sub, fill=TEXT_DIM, anchor=sub_anchor)


def place_tiered(entries, tiers, clamp=(120, W - 120)):
    entries = sorted(entries, key=lambda e: e[0][0])
    for i, (point, text, sub) in enumerate(entries):
        tier_y = tiers[i % len(tiers)]
        x = min(max(point[0], clamp[0]), clamp[1])
        leader_label(point, (x, tier_y), text, sub, anchor="ma")


def cell_grid(x0, y0, x1, y1, rows, cols, fill, pad=6, outline=HULL_LINE):
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline)
    ix0, iy0, ix1, iy1 = x0 + pad, y0 + pad, x1 - pad, y1 - pad
    cw, ch = (ix1 - ix0) / cols, (iy1 - iy0) / rows
    for r in range(rows):
        for c in range(cols):
            cx0, cy0 = ix0 + c * cw + 1.5, iy0 + r * ch + 1.5
            draw.rectangle([cx0, cy0, cx0 + cw - 3, cy0 + ch - 3], outline=BG, width=1)


def icon(cx, cy, kind, fill, size=11, outline=HULL_LINE):
    r = size / 2
    if kind == "circle":
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline)
    elif kind == "square":
        draw.rectangle([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline)
    elif kind == "diamond":
        draw.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill, outline=outline)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
draw.text((44, 32), "CG-74  DENVER-CLASS MISSILE CRUISER", font=f_title, fill=TEXT_WHITE)
draw.text((44, 86), "General arrangement — plan & profile · 890 ft (272 m)", font=f_subtitle, fill=TEXT_DIM)
draw.line([(44, 122), (900, 122)], fill=PANEL_LINE, width=2)

# Principal characteristics panel (two label:value columns)
panel = (1610, 34, 2360, 464)
draw.rectangle(panel, outline=PANEL_LINE, width=2)
draw.text((panel[0] + 18, panel[1] + 16), "PRINCIPAL CHARACTERISTICS", font=f_panel_head, fill=TEXT_WHITE)
left_stats = [
    ("Length / Beam", "890 ft (272 m) / 107 ft (33 m)"),
    ("Displacement", "~29,000 t full load"),
    ("Speed", "30+ knots"),
    ("Stern", "3 tiers: 203 / VLS / flight deck"),
    ("Aircraft", "4 MH-60R/S + Coyote UAV"),
    ("VLS", "180: 16 LD, 96 Mk 41, 68 Mk 57"),
    ("Main guns", "2 x twin 203 mm faceted"),
    ("Secondary", "4 x 76 mm STRALES"),
    ("CIWS / RWS", "2 Phalanx, 4x30 mm, 8x twin .50"),
    ("DEW", "2 x 500 kW laser (P/S)"),
]
right_stats = [
    ("Anti-ship", "LRASM, Eagle Strike, MST, SM-6"),
    ("ASW", "VL-ASROC, 2 x Mk32 TT"),
    ("Point def.", "2 x 21-cell RAM"),
    ("APKWS", "2 x trainable 70 mm pod"),
    ("Soft-kill", "8 x Nulka, 4 x Mk36 SRBOC"),
    ("EW", "SLQ-32(V)7, fwd super sides"),
    ("Radar", "4xSPY-6, 4xSPY-3, SPQ-9B"),
    ("Sonar", "SQS-53 hull sonar, towed array"),
    ("Propulsion", "8 GT engines on 4 shafts"),
]
ry = panel[1] + 52
for k, v in left_stats:
    draw.text((panel[0] + 18, ry), k, font=f_panel_row, fill=TEXT_DIM)
    draw.text((panel[0] + 170, ry), v, font=f_panel_row, fill=TEXT_WHITE)
    ry += 23
ry = panel[1] + 52
rx = panel[0] + 430
for k, v in right_stats:
    draw.text((rx, ry), k, font=f_panel_row, fill=TEXT_DIM)
    draw.text((rx + 110, ry), v, font=f_panel_row, fill=TEXT_WHITE)
    ry += 23

# ---------------------------------------------------------------------------
# Shared hull geometry
# ---------------------------------------------------------------------------
STERN_X, BOW_X = 190, 2260
FT_PX = (BOW_X - STERN_X) / 890.0
BEAM = 128


def hull_x(t):
    return STERN_X + t * (BOW_X - STERN_X)


def half_beam(t):
    if t < 0.03:
        return BEAM * (0.90 + 0.10 * (t / 0.03))
    if t < 0.90:
        return BEAM
    tt = (t - 0.90) / 0.10
    bump = math.sin(tt * math.pi) * 0.05 if tt < 0.4 else 0
    smooth = tt * tt * (3 - 2 * tt)
    return BEAM * (1 - smooth) + BEAM * bump * (1 - smooth)


# ---------------------------------------------------------------------------
# Plan view
# ---------------------------------------------------------------------------
draw.text((44, 258), "PLAN VIEW", font=f_section, fill=TEXT_WHITE)
PLAN_Y = 960


def hull_point(t, side):
    return (hull_x(t), PLAN_Y + side * half_beam(t))


N = 80
top_edge = [hull_point(i / N, -1) for i in range(N + 1)]
bottom_edge = [hull_point(i / N, 1) for i in range(N + 1)]
draw.polygon(top_edge + list(reversed(bottom_edge)), fill=HULL_FILL, outline=HULL_LINE)


def turret(t_center, facing):
    x = hull_x(t_center)
    hb = half_beam(t_center)
    rx, ry_ = hb * 0.62, hb * 0.7
    draw.rectangle([x - rx, PLAN_Y - ry_, x + rx, PLAN_Y + ry_], fill=TURRET_FILL, outline=HULL_LINE)
    for off in (-9, 9):
        draw.line([(x, PLAN_Y + off), (x + facing * (rx + 90), PLAN_Y + off)], fill=(205, 208, 212), width=6)
    return (x, PLAN_Y)


def mk57_strip(t_center, t_half_width, beam_frac, rows, cols, side):
    hb = half_beam(t_center)
    y_c = PLAN_Y + side * beam_frac * hb
    y_half = hb * 0.10
    x0, x1 = hull_x(t_center - t_half_width), hull_x(t_center + t_half_width)
    y0, y1 = y_c - y_half, y_c + y_half
    cell_grid(x0, y0, x1, y1, rows=rows, cols=cols, fill=VLS_FILL, pad=2)
    return (x0, y0, x1, y1)


# --- Aft turret + Mk57 x24 flanking ---
aft_turret_pt = turret(0.035, facing=-1)
mk57_aft_top = mk57_strip(0.075, 0.055, 0.62, 1, 8, -1)
mk57_aft_bot = mk57_strip(0.075, 0.055, 0.62, 1, 8, 1)

# --- VLS x64 (tier 2) ---
vls64_x0, vls64_x1 = hull_x(0.115), hull_x(0.16)
vls64_hb = half_beam(0.14) * 0.75
cell_grid(vls64_x0, PLAN_Y - vls64_hb, vls64_x1, PLAN_Y + vls64_hb, rows=8, cols=8, fill=VLS_FILL, pad=5)

# --- Mk57 x20 flanking aft VLS ---
mk57_fwd_top = mk57_strip(0.185, 0.045, 0.62, 1, 7, -1)
mk57_fwd_bot = mk57_strip(0.185, 0.045, 0.62, 1, 7, 1)

# --- Flight deck (tier 3, raised) w/ helo spot ---
fd_x0, fd_x1 = hull_x(0.20), hull_x(0.30)
fd_hb = half_beam(0.25) * 0.92
draw.rectangle([fd_x0, PLAN_Y - fd_hb, fd_x1, PLAN_Y + fd_hb], fill=DECK_FILL, outline=HULL_LINE)
for gx in range(int(fd_x0) + 10, int(fd_x1) - 5, 16):
    draw.line([(gx, PLAN_Y - fd_hb + 6), (gx, PLAN_Y + fd_hb - 6)], fill=(80, 88, 100), width=1)
helo_cx = hull_x(0.245)
draw.ellipse([helo_cx - 42, PLAN_Y - 42, helo_cx + 42, PLAN_Y + 42], outline=(220, 190, 60), width=4)
draw.line([(helo_cx - 42, PLAN_Y), (helo_cx + 42, PLAN_Y)], fill=(220, 190, 60), width=4)
draw.line([(helo_cx, PLAN_Y - 42), (helo_cx, PLAN_Y + 42)], fill=(220, 190, 60), width=4)

# --- Hangar (Coyote UAV roof, 30mm x2, RAM aft edge) ---
hx0, hx1 = hull_x(0.30), hull_x(0.375)
h_hb = half_beam(0.335) * 0.85
draw.rectangle([hx0, PLAN_Y - h_hb, hx1, PLAN_Y + h_hb], fill=SUPER_FILL, outline=HULL_LINE)
coyote_x0, coyote_x1 = hx0 + 12, hx0 + 90
cell_grid(coyote_x0, PLAN_Y - h_hb * 0.75, coyote_x1, PLAN_Y + h_hb * 0.75, rows=4, cols=2, fill=COYOTE_FILL, pad=3)
ram_hangar_pt = (hx0 + 6, PLAN_Y)
icon(*ram_hangar_pt, "diamond", RAM_FILL, size=20)
mm30_hangar_pts = []
for side in (-1, 1):
    p = (hull_x(0.345), PLAN_Y + side * h_hb * 0.85)
    icon(*p, "diamond", SLQ32_FILL, size=14)
    mm30_hangar_pts.append(p)

# --- APKWS x2 (P/S) ---
apkws_pts = []
for side in (-1, 1):
    p = (hull_x(0.39), PLAN_Y + side * half_beam(0.39) * 0.55)
    icon(*p, "square", APKWS_FILL, size=20)
    apkws_pts.append(p)

# --- VLS x32 amidships ---
vls32_x0, vls32_x1 = hull_x(0.40), hull_x(0.465)
vls32_hb = half_beam(0.43) * 0.72
cell_grid(vls32_x0, PLAN_Y - vls32_hb, vls32_x1, PLAN_Y + vls32_hb, rows=6, cols=7, fill=VLS_FILL, pad=5)

# --- SRBOC pair 1 (near hangar/amidships) ---
srboc1_pts = []
for side in (-1, 1):
    p = (hull_x(0.375), PLAN_Y + side * half_beam(0.375) * 0.55)
    icon(*p, "square", SRBOC_FILL, size=12)
    srboc1_pts.append(p)

# --- .50-cal MG (representative marks: fantail, hangar, bridge, fo'c'sle) ---
mg_pts = [
    (hull_x(0.06), PLAN_Y - half_beam(0.06) * 0.85),
    (hull_x(0.33), PLAN_Y - half_beam(0.33) * 0.92),
    (hull_x(0.58), PLAN_Y - half_beam(0.58) * 0.95),
    (hull_x(0.90), PLAN_Y - half_beam(0.90) * 0.7),
]
for p in mg_pts:
    icon(*p, "circle", MG_FILL, size=9)

# --- UNREP kingposts (P/S, canted inboard) ---
kingpost_pts = []
for side in (-1, 1):
    base = (hull_x(0.475), PLAN_Y + side * half_beam(0.475) * 0.75)
    tip = (hull_x(0.475) + 14, PLAN_Y + side * half_beam(0.475) * 0.45)
    draw.line([base, tip], fill=(200, 200, 205), width=4)
    kingpost_pts.append(base)

# --- Octagonal bridge/superstructure w/ SPY-6 diagonal faces ---
ocx = hull_x(0.565)
o_hw = (hull_x(0.66) - hull_x(0.47)) / 2
o_hh = half_beam(0.565) * 0.92
k = 0.38
oct_pts = [
    (ocx - o_hw * (1 - k), PLAN_Y - o_hh), (ocx + o_hw * (1 - k), PLAN_Y - o_hh),
    (ocx + o_hw, PLAN_Y - o_hh * (1 - k)), (ocx + o_hw, PLAN_Y + o_hh * (1 - k)),
    (ocx + o_hw * (1 - k), PLAN_Y + o_hh), (ocx - o_hw * (1 - k), PLAN_Y + o_hh),
    (ocx - o_hw, PLAN_Y + o_hh * (1 - k)), (ocx - o_hw, PLAN_Y - o_hh * (1 - k)),
]
draw.polygon(oct_pts, fill=SUPER_FILL, outline=HULL_LINE)
for a, b in [(0, 7), (1, 2), (5, 6), (3, 4)]:
    draw.line([oct_pts[a], oct_pts[b]], fill=SPY6_FILL, width=7)

# SLQ-32(V)7 EW antenna arrays, fwd super sides (P/S)
slq32_pts = []
for side in (-1, 1):
    p = (ocx - o_hw * 0.72, PLAN_Y + side * o_hh * 0.88)
    draw.rectangle([p[0] - 5, p[1] - 13, p[0] + 5, p[1] + 13], fill=SLQ32_FILL, outline=HULL_LINE)
    slq32_pts.append(p)

# Bridge windows (dark squares)
for side in (-1, 1):
    wx = ocx - o_hw * 0.35
    wy = PLAN_Y + side * o_hh * 0.4
    draw.rectangle([wx - 20, wy - 16, wx + 20, wy + 16], fill=(35, 40, 48), outline=HULL_LINE)

# Phalanx CIWS (roof, inboard of laser)
phalanx_pt = (ocx, PLAN_Y - o_hh * 0.35)
icon(*phalanx_pt, "circle", PHALANX_FILL, size=22)

# Laser x2 (P/S), fwd roof, fwd of MG
laser_pts = []
for side in (-1, 1):
    p = (ocx - o_hw * 0.15, PLAN_Y + side * o_hh * 0.55)
    icon(*p, "circle", LASER_FILL, size=20)
    laser_pts.append(p)

# Nulka x8 on super roof, inboard (two rows of small squares)
nulka_pts = []
for side in (-1, 1):
    for i in range(4):
        p = (ocx + o_hw * 0.05 + i * 20, PLAN_Y + side * o_hh * 0.45)
        icon(*p, "square", NULKA_FILL, size=10)
        if i == 0:
            nulka_pts.append(p)

# SRBOC pair 2 (deckhouse roof)
srboc2_pts = []
for side in (-1, 1):
    p = (ocx - o_hw * 0.35, PLAN_Y + side * o_hh * 0.7)
    icon(*p, "square", SRBOC_FILL, size=12)
    srboc2_pts.append(p)

# Mk32 triple TT, trained fore & aft
mk32_pts = []
for side in (-1, 1):
    p = (hull_x(0.50), PLAN_Y + side * half_beam(0.50) * 0.8)
    icon(*p, "square", (150, 150, 155), size=16)
    mk32_pts.append(p)

# RAM front-face platform
ram_front_pt = (ocx + o_hw + 6, PLAN_Y)
icon(*ram_front_pt, "diamond", RAM_FILL, size=20)

# 30mm x2 fwd, outboard of RAM
mm30_fwd_pts = []
for side in (-1, 1):
    p = (hull_x(0.665), PLAN_Y + side * half_beam(0.665) * 0.6)
    icon(*p, "diamond", SLQ32_FILL, size=14)
    mm30_fwd_pts.append(p)

# --- Mast (SPQ-9B / SPY-3 4-face / Satcom-TACAN-HF) ---
mast_x = hull_x(0.70)
draw.line([(mast_x, PLAN_Y - 30), (mast_x, PLAN_Y + 30)], fill=(220, 220, 224), width=3)
spq9b_pt = (mast_x, PLAN_Y)
icon(*spq9b_pt, "circle", SPY3_FILL, size=13)
satcom_pt = (mast_x + 24, PLAN_Y - 14)
icon(*satcom_pt, "circle", LASER_FILL, size=12)

# --- 76mm x2 (P/S), abaft super / trained astern ---
mm76_aft_pts = []
for side in (-1, 1):
    p = (hull_x(0.60), PLAN_Y + side * half_beam(0.60) * 0.88)
    icon(*p, "square", SEVENTYSIX_FILL, size=18)
    mm76_aft_pts.append(p)

# --- 76mm x2 (P/S), below fwd SPY-6 faces ---
mm76_fwd_pts = []
for side in (-1, 1):
    p = (hull_x(0.735), PLAN_Y + side * half_beam(0.735) * 0.82)
    icon(*p, "square", SEVENTYSIX_FILL, size=18)
    mm76_fwd_pts.append(p)

# --- VLS x16 large-dia, forward ---
vld_x0, vld_x1 = hull_x(0.78), hull_x(0.845)
vld_hb = half_beam(0.81) * 0.62
cell_grid(vld_x0, PLAN_Y - vld_hb, vld_x1, PLAN_Y + vld_hb, rows=4, cols=4, fill=VLS_LD_FILL, pad=8)

# --- Forward turret (No.1) ---
fwd_turret_pt = turret(0.92, facing=1)

# --- Bow sonar dome ---
bow_tip_x = hull_x(1.0)
draw.ellipse([bow_tip_x - 6, PLAN_Y - 10, bow_tip_x + 14, PLAN_Y + 10], fill=HULL_FILL, outline=HULL_LINE)

# ---------------------------------------------------------------------------
# Plan view labels
# ---------------------------------------------------------------------------
ABOVE_TIERS = [PLAN_Y - 160, PLAN_Y - 215, PLAN_Y - 270, PLAN_Y - 325, PLAN_Y - 380, PLAN_Y - 435]
BELOW_TIERS = [PLAN_Y + 150, PLAN_Y + 205, PLAN_Y + 260, PLAN_Y + 315, PLAN_Y + 370, PLAN_Y + 425]

above_entries = [
    (aft_turret_pt, "TWIN 203 MM", "tier 1 — fantail, aft"),
    ((vls64_x0 + 30, PLAN_Y - vls64_hb), "VLS x64", "tier 2"),
    ((fd_x0 + 30, PLAN_Y - fd_hb), "FLIGHT DECK", "tier 3 (raised)"),
    ((coyote_x0 + 20, PLAN_Y - h_hb * 0.75), "COYOTE UAV x2", "8-cell, hangar roof"),
    (apkws_pts[0], "APKWS x2 (P/S)", "trainable 70 mm rocket"),
    ((vls32_x0 + 30, PLAN_Y - vls32_hb), "VLS x32", "amidships"),
    (mm30_hangar_pts[0], "30 MM x2", "outboard of hangar"),
    (srboc2_pts[0], "MK36 SRBOC", "2 pairs (deckhouse roof + hangar)"),
    (oct_pts[0], "SPY-6", "on diagonal faces"),
    (slq32_pts[0], "SLQ-32(V)7", "fwd super sides (P/S)"),
    (nulka_pts[0], "NULKA x8", "on super roof, inboard"),
    (mg_pts[1], ".50-CAL TWIN MG x8", "fantail · hangar · bridge · fo'c'sle"),
    (mm30_fwd_pts[0], "30 MM x2", "fwd, outboard of RAM"),
    (fwd_turret_pt, "TWIN 203 MM", "No.1 — forward"),
]
place_tiered(above_entries, ABOVE_TIERS)

below_entries = [
    (mk57_aft_bot[:2], "MK 57 x24", "flanking the gun"),
    (mk57_fwd_bot[:2], "MK 57 x20", "flanking aft VLS"),
    ((hx0 + 20, PLAN_Y + h_hb), "HANGAR", "fwd of flight deck"),
    ((helo_cx, PLAN_Y + 42), "MH-60R", "on flight deck"),
    (ram_hangar_pt, "RAM", "hangar aft edge"),
    (kingpost_pts[1], "UNREP KINGPOSTS", "P/S, canted inboard"),
    (laser_pts[1], "LASER x2 (P/S)", "fwd roof, fwd of MG"),
    (mk32_pts[1], "MK32 TRIPLE TT", "trained fore & aft"),
    (mm76_aft_pts[1], "76 MM x2 (P/S)", "abaft super, trained astern"),
    (phalanx_pt, "PHALANX CIWS", "on roof, inboard of laser"),
    (spq9b_pt, "SPQ-9B", "atop mast"),
    (satcom_pt, "SPY-3 (4-FACE)", "cardinal, on mast"),
    (ram_front_pt, "RAM", "front-face platform"),
    (mm76_fwd_pts[1], "76 MM x2 (P/S)", "below fwd SPY-6 faces"),
    ((vld_x0 + 20, PLAN_Y + vld_hb), "VLS x16 large-dia", "forward"),
    ((bow_tip_x, PLAN_Y), "BOW SONAR DOME", None),
]
place_tiered(below_entries, BELOW_TIERS)

# ---------------------------------------------------------------------------
# Profile / side elevation
# ---------------------------------------------------------------------------
PROFILE_HEADER_Y = 1500
draw.text((44, PROFILE_HEADER_Y), "PROFILE / SIDE ELEVATION", font=f_section, fill=TEXT_WHITE)

DECK_Y = PROFILE_HEADER_Y + 480
KEEL_Y = DECK_Y + 110
WATERLINE_Y = KEEL_Y - 25

hull_side = [
    (STERN_X, DECK_Y),
    (STERN_X, DECK_Y + 60),
    (STERN_X + 70, KEEL_Y),
    (BOW_X - 260, KEEL_Y),
    (BOW_X - 20, DECK_Y + 25),
    (BOW_X, DECK_Y - 35),
    (BOW_X - 30, DECK_Y - 10),
    (STERN_X + 55, DECK_Y - 10),
]
draw.polygon(hull_side, fill=HULL_FILL, outline=HULL_LINE)
draw.line([(STERN_X - 10, WATERLINE_Y), (BOW_X + 10, WATERLINE_Y)], fill=WATERLINE, width=3)

# Bulbous bow + SQS-53 sonar dome (small bulge on the keel near the bow)
bulb_cx = BOW_X - 70
bulb_box = (bulb_cx - 55, KEEL_Y - 8, bulb_cx + 55, KEEL_Y + 20)
draw.ellipse(bulb_box, fill=HULL_FILL, outline=HULL_LINE)

# Aft turret (profile)
turret_a_x = hull_x(0.035)
draw.rectangle([turret_a_x - 55, DECK_Y - 55, turret_a_x + 55, DECK_Y - 8], fill=TURRET_FILL, outline=HULL_LINE)
draw.line([(turret_a_x, DECK_Y - 32), (turret_a_x - 90, DECK_Y - 32)], fill=(205, 208, 212), width=6)

# Flight deck line + small helo silhouette
helo_profile_x = hull_x(0.24)
draw.rectangle([helo_profile_x - 40, DECK_Y - 34, helo_profile_x + 20, DECK_Y - 10], fill=(70, 78, 90), outline=HULL_LINE)
draw.line([(helo_profile_x - 45, DECK_Y - 26), (helo_profile_x + 25, DECK_Y - 26)], fill=(150, 155, 160), width=3)

# Small pole (kingpost / director) aft of hangar
pole_x = hull_x(0.30)
draw.line([(pole_x, DECK_Y - 10), (pole_x, DECK_Y - 90)], fill=(190, 190, 195), width=4)
icon(pole_x, DECK_Y - 96, "diamond", RAM_FILL, size=16)

# Hangar block w/ louvered front face
hang_x0, hang_x1 = hull_x(0.30), hull_x(0.375)
hang_top = DECK_Y - 75
draw.rectangle([hang_x0, hang_top, hang_x1, DECK_Y - 10], fill=SUPER_FILL, outline=HULL_LINE)
for gx in range(int(hang_x0) + 8, int(hang_x0) + 70, 8):
    draw.line([(gx, hang_top + 6), (gx, DECK_Y - 16)], fill=(75, 82, 94), width=2)

# GT intake grilles (trapezoidal structure)
gt_x0, gt_x1 = hull_x(0.44), hull_x(0.50)
gt_top = DECK_Y - 130
draw.polygon([(gt_x0, DECK_Y - 10), (gt_x1, DECK_Y - 10), (gt_x1 - 15, gt_top), (gt_x0 + 15, gt_top)], fill=(70, 78, 90), outline=HULL_LINE)
for gy in range(int(gt_top) + 15, int(DECK_Y) - 15, 12):
    draw.line([(gt_x0 + 20, gy), (gt_x1 - 20, gy)], fill=(48, 54, 64), width=2)

# Octagonal bridge (SPY-6 octagonal bridge), faceted front
bridge_x0, bridge_x1 = hull_x(0.535), hull_x(0.665)
bridge_top = DECK_Y - 175
draw.polygon([
    (bridge_x0, DECK_Y - 10), (bridge_x1, DECK_Y - 10),
    (bridge_x1, bridge_top + 40), (bridge_x1 - 35, bridge_top),
    (bridge_x0 + 20, bridge_top), (bridge_x0, bridge_top + 55),
], fill=SUPER_FILL, outline=HULL_LINE)

# Roof fittings on bridge: RAM, 30mm pair, Nulka/Phalanx
roof_cx = (bridge_x0 + bridge_x1) / 2
icon(bridge_x1 - 20, bridge_top - 12, "diamond", RAM_FILL, size=18)
for i, side in enumerate((-1, 1)):
    icon(roof_cx + side * 18, bridge_top - 8, "diamond", SLQ32_FILL, size=13)
icon(roof_cx - 45, bridge_top - 6, "circle", PHALANX_FILL, size=18)
icon(roof_cx - 20, bridge_top - 6, "circle", NULKA_FILL, size=13)

# Mast (SPQ-9B atop, SPY-3 4-face, Satcom/TACAN/HF)
mast_px = hull_x(0.685)
mast_top_y = bridge_top - 145
draw.line([(mast_px, bridge_top), (mast_px, mast_top_y)], fill=(210, 210, 215), width=5)
icon(mast_px, mast_top_y, "circle", SPY3_FILL, size=15)
icon(mast_px - 4, mast_top_y + 55, "circle", LASER_FILL, size=16)
for wy in range(int(mast_top_y) + 85, bridge_top - 15, 26):
    draw.line([(mast_px - 18, wy), (mast_px + 18, wy)], fill=(150, 155, 160), width=3)

# Forward turret (No.1) profile
turret_b_x = hull_x(0.92)
draw.rectangle([turret_b_x - 55, DECK_Y - 55, turret_b_x + 55, DECK_Y - 8], fill=TURRET_FILL, outline=HULL_LINE)
draw.line([(turret_b_x, DECK_Y - 32), (turret_b_x + 90, DECK_Y - 32)], fill=(205, 208, 212), width=6)

# 30mm (fwd pair) + RAM (fwd super face) near forward superstructure step
mm30_profile_x = hull_x(0.70)
icon(mm30_profile_x, DECK_Y - 60, "diamond", SLQ32_FILL, size=15)
ram_profile_x = hull_x(0.755)
icon(ram_profile_x, DECK_Y - 30, "diamond", RAM_FILL, size=18)

# SRBOC (roof) + torpedo tubes hint, aft of bridge
srboc_profile_x = hull_x(0.47)
icon(srboc_profile_x, DECK_Y - 20, "square", SRBOC_FILL, size=14)
tt_profile_x = hull_x(0.50)
draw.rectangle([tt_profile_x - 20, DECK_Y - 26, tt_profile_x + 20, DECK_Y - 10], fill=(150, 150, 155), outline=HULL_LINE)

# Single 30mm (aft of hangar)
mm30_single_x = hull_x(0.40)
icon(mm30_single_x, DECK_Y - 40, "diamond", SLQ32_FILL, size=14)

draw.text((hull_x(0.045), DECK_Y - 40), "DENVER", font=f_hull_name, fill=(210, 214, 218))
draw.text((hull_x(0.44), DECK_Y + 55), "CG-74", font=f_hull_name, fill=(200, 204, 210))
draw.text((hull_x(0.86), DECK_Y + 5), "74", font=f_hull_no, fill=(210, 214, 218))

# Connector labels linking plan-view tiers down to the profile (short leaders
# from just under the plan hull to a label row at the top of this section)
tier_link_y = PROFILE_HEADER_Y - 35
for t_pos, txt in ((0.06, "203 mm — tier 1"), (0.14, "VLS — tier 2"), (0.25, "flight deck — tier 3 (MH-60R)")):
    leader_label((hull_x(t_pos), PLAN_Y + half_beam(t_pos) + 15), (hull_x(t_pos), tier_link_y), txt, anchor="ma")

profile_above = [
    ((pole_x, DECK_Y - 96), "30 MM", None),
    ((hang_x0 + 30, hang_top), "HANGAR", None),
    ((gt_x0 + 20, gt_top), "GT INTAKE GRILLES", None),
    ((bridge_x0 + 15, bridge_top + 50), "SPY-6 (OCTAGONAL BRIDGE)", None),
    ((mast_px, mast_top_y), "SPQ-9B ATOP MAST", None),
    ((mast_px - 4, mast_top_y + 55), "SPY-3 (4-FACE)", "cardinal, on mast"),
    ((mast_px, mast_top_y + 100), "SATCOM/TACAN/HF", None),
]
place_tiered(profile_above, [mast_top_y - 30, mast_top_y - 75, mast_top_y - 120, mast_top_y - 165, mast_top_y - 210])

profile_below = [
    ((STERN_X + 15, DECK_Y + 55), "FLARED TRANSOM", None),
    ((mm30_single_x, DECK_Y - 40), "30 MM", None),
    ((srboc_profile_x, DECK_Y - 20), "SRBOC (ROOF)", None),
    ((tt_profile_x, DECK_Y - 26), "TORPEDO TUBES", None),
    ((mm30_profile_x, DECK_Y - 60), "30 MM (FWD PAIR)", None),
    ((ram_profile_x, DECK_Y - 30), "RAM (FWD SUPER FACE)", None),
    ((roof_cx - 20, bridge_top - 6), "NULKA (ROOF) / PHALANX", None),
    ((bulb_cx, bulb_box[3]), "BULBOUS BOW + SQS-53 SONAR DOME", None),
]
place_tiered(profile_below, [DECK_Y + 150, DECK_Y + 200, DECK_Y + 250, DECK_Y + 300, DECK_Y + 350])

# ---------------------------------------------------------------------------
# Missile & guided-munition fit
# ---------------------------------------------------------------------------
mbox = (1740, 1560, 2360, 1860)
draw.rectangle(mbox, outline=PANEL_LINE, width=2)
draw.text((mbox[0] + 18, mbox[1] + 16), "MISSILE & GUIDED-MUNITION FIT", font=f_panel_head, fill=TEXT_WHITE)
missile_left = [
    ("ESSM", "SR anti-air, quad-pack"),
    ("SM-2", "MR dual-role, twin-pack"),
    ("SM-3", "BMD, exo-atmo"),
    ("SM-6", "LR dual-role"),
    ("Tomahawk", "Land-attack, anti-ship"),
    ("LCBM", "land-attack, quad-pack"),
    ("RAM", "Point-defense, trainable"),
]
missile_right = [
    ("LRASM", "anti-ship"),
    ("VL-ASROC", "ASW rocket"),
    ("Eagle Strike", "large-dia AShM"),
    ("APKWS", "70 mm guided rocket"),
    ("DART", "203/76 mm guided"),
    ("VULCANO", "76/203 mm land-attack"),
]
my = mbox[1] + 54
for name, desc in missile_left:
    draw.text((mbox[0] + 16, my), "• " + name, font=f_panel_row, fill=SPY6_FILL)
    draw.text((mbox[0] + 130, my), desc, font=f_panel_row, fill=TEXT_WHITE)
    my += 26
my = mbox[1] + 54
mrx = mbox[0] + 300
for name, desc in missile_right:
    draw.text((mrx, my), "• " + name, font=f_panel_row, fill=SPY6_FILL)
    draw.text((mrx + 120, my), desc, font=f_panel_row, fill=TEXT_WHITE)
    my += 26

# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
legend_y = H - 60
legend_items = [
    ("VLS", VLS_FILL),
    ("SPY-6/SPQ-9B", SPY6_FILL),
    ("SPY-3", SPY3_FILL),
    ("APKWS", APKWS_FILL),
    ("RAM", RAM_FILL),
    ("203 mm", TURRET_FILL),
    ("76 STRALES", SEVENTYSIX_FILL),
    ("Phalanx", PHALANX_FILL),
    ("Laser", LASER_FILL),
    ("Nulka", NULKA_FILL),
    ("SRBOC", SRBOC_FILL),
    ("SLQ-32", SLQ32_FILL),
    ("Coyote", COYOTE_FILL),
    ("MH-60R", (70, 78, 90)),
]
lx = 44
for name, color in legend_items:
    draw.rectangle([lx, legend_y, lx + 24, legend_y + 18], fill=color, outline=HULL_LINE)
    draw.text((lx + 32, legend_y - 1), name, font=f_label_sub, fill=TEXT_DIM)
    lx += 32 + draw.textlength(name, font=f_label_sub) + 36

draw.text((W - 200, H - 30), "not to scale · conceptual", font=f_footnote, fill=TEXT_DIM)

out_path = "CG74-new.png"
img.save(out_path)
print("saved", out_path, img.size)
