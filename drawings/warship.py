"""Generic 750 ft / 25,000 t missile cruiser, Burke-family hull shape.

Plan view (aft -> fwd, t = 0 -> 1):
  flight deck | full-beam hangar, shorter run (real-scale Mk41 x64 on the
  centerline + real-scale Mk57 x12 P/S built into its flanks) | gap |
  midships superstructure (truncated pyramid, GT intakes, moved aft,
  topped in profile by a mack w/ twin funnels) | 32-cell Mk41 VLS complex |
  full-beam octagonal superstructure (SPY-6 on diagonal faces, small
  funnel on the after edge) | 16-cell large-dia VLS (Mk57 x8 P/S flanking)
  | twin 203mm/65 gunhouse (compact, elongated-octagon Mk71-style) |
  angled hurricane bow w/ bulbous bow + sonar dome merged in

All shapes are plain polygons keyed off the same t-position, so plan and
profile stay aligned. Move a boundary, get a different ship.
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 2000, 2050

BG = (10, 21, 38)
HULL_FILL = (66, 74, 88)
HULL_LINE = (150, 160, 172)
SUPERSTRUCTURE_FILL = (110, 118, 132)
PYRAMID_FILL = (100, 108, 122)
OCTAGON_FILL = (96, 104, 120)
GUNHOUSE_FILL = (58, 64, 74)
TURRET_FILL = (150, 60, 55)
RAM_FILL = (170, 85, 60)
VLS_FILL = (72, 96, 150)
VLS16_FILL = (86, 78, 150)
RADAR_FILL = (60, 150, 150)
TEXT_WHITE = (232, 236, 240)
TEXT_DIM = (140, 152, 168)
LEADER = (150, 160, 172)
WATERLINE = (176, 48, 48)
PANEL_LINE = (70, 90, 120)

FONT_DIR = "/System/Library/Fonts/Supplemental/"
f_title = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 40)
f_subtitle = ImageFont.truetype(FONT_DIR + "Arial.ttf", 20)
f_section = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 22)
f_label = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 15)
f_label_sub = ImageFont.truetype(FONT_DIR + "Arial.ttf", 13)
f_panel_head = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 16)
f_panel_row = ImageFont.truetype(FONT_DIR + "Arial.ttf", 15)
f_hull_no = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 46)
f_hull_name = ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", 26)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)


def leader_label(point, text_xy, text, sub=None, anchor="ma"):
    draw.line([point, text_xy], fill=LEADER, width=1)
    r = 2.5
    draw.ellipse([point[0] - r, point[1] - r, point[0] + r, point[1] + r], fill=TEXT_WHITE)
    draw.text(text_xy, text, font=f_label, fill=TEXT_WHITE, anchor=anchor)
    if sub:
        sub_anchor = "m" + anchor[1] if anchor[0] == "m" else anchor
        draw.text((text_xy[0], text_xy[1] + 20), sub, font=f_label_sub, fill=TEXT_DIM, anchor=sub_anchor)


def place_tiered(entries, tiers, clamp=(110, W - 110)):
    entries = sorted(entries, key=lambda e: e[0][0])
    for i, (point, text, sub) in enumerate(entries):
        tier_y = tiers[i % len(tiers)]
        x = min(max(point[0], clamp[0]), clamp[1])
        leader_label(point, (x, tier_y), text, sub, anchor="ma")


def hatch_rect(x0, y0, x1, y1, fill=None, spacing=10):
    if fill:
        draw.rectangle([x0, y0, x1, y1], fill=fill, outline=HULL_LINE)
    else:
        draw.rectangle([x0, y0, x1, y1], outline=HULL_LINE)
    x = x0 - (y1 - y0)
    while x < x1:
        p0 = (max(x, x0), y0)
        p1 = (min(x + (y1 - y0), x1), y1)
        if p0[0] < p1[0]:
            draw.line([p0, p1], fill=HULL_LINE, width=1)
        x += spacing


def cell_grid(x0, y0, x1, y1, rows, cols, fill, pad=8):
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=HULL_LINE)
    ix0, iy0, ix1, iy1 = x0 + pad, y0 + pad, x1 - pad, y1 - pad
    cw, ch = (ix1 - ix0) / cols, (iy1 - iy0) / rows
    for r in range(rows):
        for c in range(cols):
            cx0, cy0 = ix0 + c * cw + 2, iy0 + r * ch + 2
            draw.rectangle([cx0, cy0, cx0 + cw - 4, cy0 + ch - 4], outline=BG, width=1)


def quad_modules(x0, y0, x1, y1, n_modules, fill, gap=6, cells_per_module=4):
    """Mk57/PVLS look: separate multi-cell modules (1x4 in-line) w/ gaps
    between them, vs. the dense uniform Mk41 strongback grid."""
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


def ram_launcher(cx, cy, angle_deg, r=15):
    """21-cell trainable RAM launcher: rotary-drum housing (radial spokes
    hint at the packed cells) plus an angled train/aim indicator."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RAM_FILL, outline=HULL_LINE)
    for a in range(0, 360, 30):
        rad = math.radians(a)
        x0, y0 = cx + 5 * math.cos(rad), cy + 5 * math.sin(rad)
        x1, y1 = cx + r * 0.8 * math.cos(rad), cy + r * 0.8 * math.sin(rad)
        draw.line([(x0, y0), (x1, y1)], fill=HULL_LINE, width=1)
    rad = math.radians(angle_deg)
    tip = (cx + (r + 20) * math.cos(rad), cy + (r + 20) * math.sin(rad))
    draw.line([(cx, cy), tip], fill=(210, 210, 215), width=3)


def ram_launcher_side(cx, base_y, angle_deg, r=12):
    """Profile-view RAM mount: drum on a short pedestal, angled up."""
    top_y = base_y - r * 1.6
    draw.line([(cx, base_y), (cx, top_y)], fill=HULL_LINE, width=4)
    draw.ellipse([cx - r, top_y - r, cx + r, top_y + r], fill=RAM_FILL, outline=HULL_LINE)
    rad = math.radians(angle_deg)
    tip = (cx + (r + 18) * math.cos(rad), top_y + (r + 18) * math.sin(rad))
    draw.line([(cx, top_y), tip], fill=(210, 210, 215), width=3)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
draw.text((40, 30), "CG-74  DENVER-CLASS HEAVY CRUISER", font=f_title, fill=TEXT_WHITE)
draw.text((40, 78), "General arrangement — plan & profile · 750 ft (229 m) · editable template", font=f_subtitle, fill=TEXT_DIM)
draw.line([(40, 108), (1180, 108)], fill=PANEL_LINE, width=2)

panel = (1330, 30, 1960, 300)
draw.rectangle(panel, outline=PANEL_LINE, width=2)
draw.text((panel[0] + 16, panel[1] + 14), "PRINCIPAL CHARACTERISTICS", font=f_panel_head, fill=TEXT_WHITE)
stats = [
    ("Length / Beam", "750 ft (229 m) / 98 ft (30 m)"),
    ("Displacement", "~25,000 t full load"),
    ("Speed", "30+ knots"),
    ("Hull form", "Burke-family, hurricane bow, ogive plan, transom stern"),
    ("Bow", "Bulbous bow (sonar dome), extended fwd, container-ship style"),
    ("Main gun", "1 x twin 203 mm/65, 43.3 ft barrels, Mk 71-style"),
    ("VLS", "96 Mk41 (64 hangar + 32 amidships) + 56 Mk57 (P/S) + 16 large-dia"),
    ("Radar", "SPY-6, full-beam octagonal deckhouse, diagonal faces"),
    ("Aviation", "Flight deck aft + full-beam hangar"),
    ("Propulsion", "6x gas turbine, 2 electric motors on 2 shafts"),
]
ry = panel[1] + 48
for k, v in stats:
    draw.text((panel[0] + 16, ry), k, font=f_panel_row, fill=TEXT_DIM)
    draw.text((panel[0] + 190, ry), v, font=f_panel_row, fill=TEXT_WHITE)
    ry += 22

# ---------------------------------------------------------------------------
# Shared hull geometry (plan + profile keyed off the same t axis)
# ---------------------------------------------------------------------------
STERN_X, BOW_X = 150, 1830
BEAM = 95


def hull_x(t):
    return STERN_X + t * (BOW_X - STERN_X)


# Tangent-ogive bow: a true circular-arc nose (like a shell/bullet profile)
# tangent to the parallel hull at t=0.85, coming to a point at t=1.0.
BOW_START_T = 0.85
OGIVE_L = (1.0 - BOW_START_T) * (BOW_X - STERN_X)
OGIVE_R = BEAM
OGIVE_RHO = (OGIVE_R ** 2 + OGIVE_L ** 2) / (2 * OGIVE_R)

# From the end of the ogive (t=0.85, full beam) aft to the stern, the hull
# tapers gently inward instead of running parallel -- a subtle wedge, not
# a hard narrowing. STERN_TAPER is the fraction of full beam at t=0.03.
STERN_TAPER = 0.93


def half_beam(t):
    """Long raked (hurricane-bow) entry -- no flare bump, tangent-ogive
    taper to the stem for a shell-like plan-view point."""
    if t < 0.03:
        base = BEAM * STERN_TAPER
        return base * (0.85 + 0.15 * (t / 0.03))
    if t < BOW_START_T:
        frac = (t - 0.03) / (BOW_START_T - 0.03)
        smooth = frac * frac * (3 - 2 * frac)
        return BEAM * STERN_TAPER + smooth * BEAM * (1 - STERN_TAPER)
    d = min((t - BOW_START_T) * (BOW_X - STERN_X), OGIVE_L)
    return math.sqrt(max(OGIVE_RHO ** 2 - d ** 2, 0)) + OGIVE_R - OGIVE_RHO


# t-range boundaries, aft -> fwd. Real-world scale for VLS cell pitch.
FT_PX = (BOW_X - STERN_X) / 750.0
MK41_CELL_PX = 5.3 * FT_PX     # Mk41: ~5.3 ft module pitch
MK57_CELL_PX = 6.3 * FT_PX     # Mk57/PVLS: larger peripheral quad-pack cell
GUN_BARREL_PX = 43.3 * FT_PX   # 203mm/65 bore x 65 calibers = 43.3 ft

FLIGHT_DECK = (0.00, 0.14)
HANGAR = (0.15, 0.32)       # full beam, shorter than before
PYRAMID = (0.385, 0.483)    # moved aft, adjoining the hangar; lengthened
OCTAGON = (0.54, 0.68)      # broadened to full beam
VLS16 = (0.71, 0.77)
GUNHOUSE = (0.805, 0.855)  # shifted fwd to make room for the widened Mk57 blocks

# ---------------------------------------------------------------------------
# Plan view
# ---------------------------------------------------------------------------
draw.text((40, 150), "PLAN VIEW", font=f_section, fill=TEXT_WHITE)
PLAN_Y = 650


def hull_point(t, side):
    return (hull_x(t), PLAN_Y + side * half_beam(t))


N = 70
top_edge = [hull_point(i / N, -1) for i in range(N + 1)]
bottom_edge = [hull_point(i / N, 1) for i in range(N + 1)]
draw.polygon(top_edge + list(reversed(bottom_edge)), fill=HULL_FILL, outline=HULL_LINE)

# Flight deck marking (helo spot)
fd_x = hull_x(0.075)
draw.ellipse([fd_x - 45, PLAN_Y - 45, fd_x + 45, PLAN_Y + 45], outline=(210, 210, 60), width=3)
draw.line([(fd_x - 45, PLAN_Y), (fd_x + 45, PLAN_Y)], fill=(210, 210, 60), width=3)
draw.line([(fd_x, PLAN_Y - 45), (fd_x, PLAN_Y + 45)], fill=(210, 210, 60), width=3)

# Hangar block: now full beam, shorter length. Mk41 (64-cell, real-scale)
# set into the roof on the centerline; Mk57 (12-cell/side, real-scale
# 1x4 in-line modules) built into the hangar's outer flanks.
hx0, hx1 = hull_x(HANGAR[0]), hull_x(HANGAR[1])
h_t_center = (HANGAR[0] + HANGAR[1]) / 2
h_hb = half_beam(h_t_center) * 0.95
draw.rectangle([hx0, PLAN_Y - h_hb, hx1, PLAN_Y + h_hb], fill=SUPERSTRUCTURE_FILL, outline=HULL_LINE)

h_cx = hull_x(h_t_center)
mk41_size = 8 * MK41_CELL_PX
# Pushed forward, near the hangar's forward edge (vs. centered) -- close
# to the gap/pyramid side of the aft superstructure.
mk41_x1 = hx1 - 18
mk41_x0 = mk41_x1 - mk41_size
mk41_hb = mk41_size / 2
cell_grid(mk41_x0, PLAN_Y - mk41_hb, mk41_x1, PLAN_Y + mk41_hb, rows=8, cols=8, fill=VLS_FILL, pad=3)

MK57_HANGAR_MODULES = 4  # was 3; one more 1x4 module added each side
mk57_w = MK57_HANGAR_MODULES * (4 * MK57_CELL_PX) + (MK57_HANGAR_MODULES - 1) * 6
mk57_h = MK57_CELL_PX
mk57_x0, mk57_x1 = h_cx - mk57_w / 2, h_cx + mk57_w / 2
mk57_boxes = {}
for side in (-1, 1):
    y_center = PLAN_Y + side * (h_hb - mk57_h / 2 - 6)
    y0, y1 = y_center - mk57_h / 2, y_center + mk57_h / 2
    quad_modules(mk57_x0, y0, mk57_x1, y1, n_modules=MK57_HANGAR_MODULES, fill=VLS_FILL)
    mk57_boxes[side] = (mk57_x0, y0, mk57_x1, y1)

# 21-cell trainable RAM launcher, angled, on the hangar's after edge
ram_hangar_x, ram_hangar_y = hx0 + 20, PLAN_Y
ram_launcher(ram_hangar_x, ram_hangar_y, 200)

# Midships superstructure: truncated pyramid (base + inset top) w/ GT intakes
px0, px1 = hull_x(PYRAMID[0]), hull_x(PYRAMID[1])
p_hb_base = half_beam((PYRAMID[0] + PYRAMID[1]) / 2) * 0.62
draw.rectangle([px0, PLAN_Y - p_hb_base, px1, PLAN_Y + p_hb_base], fill=PYRAMID_FILL, outline=HULL_LINE)
p_hb_top = p_hb_base * 0.6
inset = (px1 - px0) * 0.14
draw.rectangle([px0 + inset, PLAN_Y - p_hb_top, px1 - inset, PLAN_Y + p_hb_top], outline=HULL_LINE, width=2)
for side in (-1, 1):
    iy0 = PLAN_Y + side * p_hb_base * 0.55
    iy1 = PLAN_Y + side * p_hb_base * 0.95
    hatch_rect(px0 + 6, min(iy0, iy1), px1 - 6, max(iy0, iy1), spacing=9)

# 32-cell Mk41 VLS complex, real-scale, dropped into the gap between the
# midships pyramid and the forward octagon
vls32_x0_gap, vls32_x1_gap = px1, hull_x(OCTAGON[0])
vls32_cx = (vls32_x0_gap + vls32_x1_gap) / 2
vls32_w = 4 * MK41_CELL_PX
vls32_h = 8 * MK41_CELL_PX
vls32_x0, vls32_x1 = vls32_cx - vls32_w / 2, vls32_cx + vls32_w / 2
vls32_hb = vls32_h / 2
cell_grid(vls32_x0, PLAN_Y - vls32_hb, vls32_x1, PLAN_Y + vls32_hb, rows=8, cols=4, fill=VLS_FILL, pad=3)

# Octagonal forward superstructure w/ SPY-6 on diagonal faces
ocx = hull_x((OCTAGON[0] + OCTAGON[1]) / 2)
o_hw = (hull_x(OCTAGON[1]) - hull_x(OCTAGON[0])) / 2
o_hh = half_beam((OCTAGON[0] + OCTAGON[1]) / 2) * 0.95
k = 0.42
oct_pts = [
    (ocx - o_hw * (1 - k), PLAN_Y - o_hh),
    (ocx + o_hw * (1 - k), PLAN_Y - o_hh),
    (ocx + o_hw, PLAN_Y - o_hh * (1 - k)),
    (ocx + o_hw, PLAN_Y + o_hh * (1 - k)),
    (ocx + o_hw * (1 - k), PLAN_Y + o_hh),
    (ocx - o_hw * (1 - k), PLAN_Y + o_hh),
    (ocx - o_hw, PLAN_Y + o_hh * (1 - k)),
    (ocx - o_hw, PLAN_Y - o_hh * (1 - k)),
]
draw.polygon(oct_pts, fill=OCTAGON_FILL, outline=HULL_LINE)
diagonal_edges = [(0, 7), (1, 2), (5, 6), (3, 4)]
for a, b in diagonal_edges:
    draw.line([oct_pts[a], oct_pts[b]], fill=RADAR_FILL, width=6)

# Small funnel on the octagon's after (aft-facing) edge
oct_funnel_x = ocx - o_hw + 32
oct_funnel_w, oct_funnel_h = 26, 22
draw.rectangle([
    oct_funnel_x - oct_funnel_w / 2, PLAN_Y - oct_funnel_h / 2,
    oct_funnel_x + oct_funnel_w / 2, PLAN_Y + oct_funnel_h / 2,
], fill=(55, 60, 70), outline=HULL_LINE)

# Octagonal stealth mast footprint, centered between the funnel and the
# octagon's forward edge (San Antonio/AEM-S style enclosed composite mast)
sm_plan_cx = (oct_funnel_x + (ocx + o_hw)) / 2
sm_hw, sm_hh, sm_k = 20, 16, 0.35
sm_plan_pts = [
    (sm_plan_cx - sm_hw * (1 - sm_k), PLAN_Y - sm_hh), (sm_plan_cx + sm_hw * (1 - sm_k), PLAN_Y - sm_hh),
    (sm_plan_cx + sm_hw, PLAN_Y - sm_hh * (1 - sm_k)), (sm_plan_cx + sm_hw, PLAN_Y + sm_hh * (1 - sm_k)),
    (sm_plan_cx + sm_hw * (1 - sm_k), PLAN_Y + sm_hh), (sm_plan_cx - sm_hw * (1 - sm_k), PLAN_Y + sm_hh),
    (sm_plan_cx - sm_hw, PLAN_Y + sm_hh * (1 - sm_k)), (sm_plan_cx - sm_hw, PLAN_Y - sm_hh * (1 - sm_k)),
]
draw.polygon(sm_plan_pts, fill=(40, 44, 52), outline=HULL_LINE)

# 21-cell trainable RAM launcher, angled, on the octagon's forward edge
ram_oct_x, ram_oct_y = ocx + o_hw - 16, PLAN_Y
ram_launcher(ram_oct_x, ram_oct_y, -20)

# 16-cell large-diameter VLS
v16_x0, v16_x1 = hull_x(VLS16[0]), hull_x(VLS16[1])
v16_hb = half_beam((VLS16[0] + VLS16[1]) / 2) * 0.5
cell_grid(v16_x0, PLAN_Y - v16_hb, v16_x1, PLAN_Y + v16_hb, rows=4, cols=4, fill=VLS16_FILL, pad=10)

# Mk57 flanking the LD-VLS: 3 modules x 4 cells (1x4, real-scale) each
# side (was 2 -- one more module added per side), pushed outboard to the
# hull edge. Moved aft slightly, into the gap between the octagon and the
# (fwd-shifted) gunhouse, to make room for the extra module.
ld_mk57_w = 3 * (4 * MK57_CELL_PX) + 2 * 6
ld_mk57_h = MK57_CELL_PX
ld_gap_x0 = (ocx + o_hw) + 10
ld_gap_x1 = hull_x(GUNHOUSE[0]) - 10
ld_mk57_x0_base = ld_gap_x0
ld_cx = ld_mk57_x0_base + ld_mk57_w / 2
ld_t = (ld_cx - STERN_X) / (BOW_X - STERN_X)
ld_hb = half_beam(ld_t)
ld_mk57_boxes = {}
for side in (-1, 1):
    y_center = PLAN_Y + side * (ld_hb - ld_mk57_h / 2 - 6)
    x0, x1 = ld_mk57_x0_base, ld_mk57_x0_base + ld_mk57_w
    y0, y1 = y_center - ld_mk57_h / 2, y_center + ld_mk57_h / 2
    quad_modules(x0, y0, x1, y1, n_modules=3, fill=VLS_FILL)
    ld_mk57_boxes[side] = (x0, y0, x1, y1)

# Gunhouse: compact, narrow, boxy Mk 71-style housing (flattened stealth
# facets, short chamfered front) w/ twin 43.3 ft (203mm/65) barrels
gt0, gt1 = GUNHOUSE
g_hb_base = half_beam(gt0) * 0.32
g_hb_tip = half_beam(gt0) * 0.22
gx0 = hull_x(gt0)
gx_shoulder = hull_x(gt0 + (gt1 - gt0) * 0.65)
gx_tip = hull_x(gt1)
# Rear corners angled to match the front, giving an elongated-octagon
# outline instead of a hexagon w/ a flat, square-cornered back.
rc_h, rc_w = g_hb_base * 0.4, 16
gun_pts = [
    (gx0, PLAN_Y - g_hb_base + rc_h), (gx0 + rc_w, PLAN_Y - g_hb_base),
    (gx_shoulder, PLAN_Y - g_hb_base), (gx_tip, PLAN_Y - g_hb_tip),
    (gx_tip, PLAN_Y + g_hb_tip), (gx_shoulder, PLAN_Y + g_hb_base),
    (gx0 + rc_w, PLAN_Y + g_hb_base), (gx0, PLAN_Y + g_hb_base - rc_h),
]
draw.polygon(gun_pts, fill=GUNHOUSE_FILL, outline=HULL_LINE)
barrel_tip = gx_tip + GUN_BARREL_PX
for off in (-6, 6):
    draw.line([(gx_tip, PLAN_Y + off), (barrel_tip, PLAN_Y + off)], fill=(180, 184, 190), width=5)

# Bulbous bow / sonar dome hint -- a slight protrusion visible beyond the
# knife-like plan-view bow point
bow_tip_x = hull_x(1.0)
draw.ellipse([bow_tip_x - 4, PLAN_Y - 9, bow_tip_x + 14, PLAN_Y + 9], fill=HULL_FILL, outline=HULL_LINE)

ABOVE_TIERS = [PLAN_Y - 150, PLAN_Y - 200, PLAN_Y - 250, PLAN_Y - 300, PLAN_Y - 335]
BELOW_TIERS = [PLAN_Y + 110, PLAN_Y + 165, PLAN_Y + 220, PLAN_Y + 275]

above_entries = [
    ((fd_x, PLAN_Y - 45), "FLIGHT DECK", "aft, flush"),
    ((mk41_x0 + 40, PLAN_Y - mk41_hb), "MK41 VLS", "64-cell, real-scale, set in hangar roof"),
    ((px0 + 15, PLAN_Y - p_hb_base * 0.75), "GT INTAKES", "midships pyramid, P/S"),
    ((vls32_x0 + 10, PLAN_Y - vls32_hb), "MK41 VLS", "32-cell, amidships"),
    ((oct_pts[0][0] + 20, oct_pts[0][1]), "SPY-6", "diagonal faces"),
    ((sm_plan_cx, PLAN_Y - sm_hh), "STEALTH MAST", "octagonal, AEM/S-style"),
    ((ram_oct_x, ram_oct_y - 16), "RAM LAUNCHER", "21-cell, trainable, fwd superstructure"),
    ((v16_x0 + 20, PLAN_Y - v16_hb), "16-CELL VLS", "large-diameter, fwd"),
    ((ld_mk57_boxes[-1][0] + 10, ld_mk57_boxes[-1][1]), "MK57 VLS", "12-cell (P/S), flanking LD-VLS"),
]
place_tiered(above_entries, ABOVE_TIERS)

below_entries = [
    ((mk57_boxes[1][0] + 20, mk57_boxes[1][3]), "MK57 VLS", "16-cell (P/S), hangar flanks"),
    ((hx0 + 30, PLAN_Y + h_hb), "HANGAR", "full beam, aft of gap, shorter run"),
    ((ram_hangar_x, ram_hangar_y + 16), "RAM LAUNCHER", "21-cell, trainable, hangar after edge"),
    (((px0 + px1) / 2, PLAN_Y + p_hb_base), "MIDSHIPS SUPERSTRUCTURE", "truncated pyramid"),
    ((ocx, PLAN_Y + o_hh), "OCTAGONAL SUPERSTRUCTURE", "broadened to full beam"),
    ((oct_funnel_x, PLAN_Y + oct_funnel_h / 2), "FUNNEL", "after edge of fwd superstructure"),
    ((gx_shoulder, PLAN_Y + g_hb_base), "MAIN GUN", "twin 203 mm/65, elongated-octagon gunhouse"),
    ((bow_tip_x, PLAN_Y), "BULBOUS BOW / SONAR DOME", "ogive bow"),
]
place_tiered(below_entries, BELOW_TIERS)

# ---------------------------------------------------------------------------
# Profile / side elevation
# ---------------------------------------------------------------------------
PROFILE_HEADER_Y = 980
draw.text((40, PROFILE_HEADER_Y), "PROFILE / SIDE ELEVATION", font=f_section, fill=TEXT_WHITE)

DECK_Y = PROFILE_HEADER_Y + 570
KEEL_Y = DECK_Y + 100
WATERLINE_Y = KEEL_Y - 25

# Angled "hurricane bow": single raked stem line (no flare knuckle) that
# overhangs forward at the top, giving a long knife-like entry. The
# bulbous bow (sonar dome merged in) is its own lobe on the keel that
# extends forward of the stem's own tip -- like a container ship's bulb
# poking out ahead of the flare -- rather than a symmetric bump under it.
STEM_P0 = (BOW_X - 280, KEEL_Y)
STEM_P2 = (BOW_X + 35, DECK_Y - 40)
BULB_PEAK = (BOW_X - 130, KEEL_Y + 22)
BULB_TIP = (BOW_X + 50, WATERLINE_Y + 8)


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


keel_pts = []
x = STERN_X + 80
while x < STEM_P0[0]:
    keel_pts.append((x, KEEL_Y))
    x += 20
keel_pts += eased_segment(STEM_P0, BULB_PEAK)
keel_pts += eased_segment(BULB_PEAK, BULB_TIP)
keel_pts.append(STEM_P2)

hull_side = [
    (STERN_X, DECK_Y),
    (STERN_X, DECK_Y + 60),
] + keel_pts + [
    (BOW_X - 65, DECK_Y - 5),
    (STERN_X + 60, DECK_Y - 5),
]
draw.polygon(hull_side, fill=HULL_FILL, outline=HULL_LINE)

draw.line([(STERN_X - 10, WATERLINE_Y), (BOW_X + 10, WATERLINE_Y)], fill=WATERLINE, width=3)

# Hangar box + Mk41 hatch hint on roof + Mk57 deck-edge hint
hang_top = DECK_Y - 70
draw.rectangle([hx0, hang_top, hx1, DECK_Y - 5], fill=SUPERSTRUCTURE_FILL, outline=HULL_LINE)
hatch_y0, hatch_y1 = hang_top - 14, hang_top
cell_grid(mk41_x0, hatch_y0, mk41_x1, hatch_y1, rows=1, cols=8, fill=VLS_FILL, pad=2)
mk57_strip_y0, mk57_strip_y1 = DECK_Y - 5, DECK_Y + 12
quad_modules(mk57_x0, mk57_strip_y0, mk57_x1, mk57_strip_y1, n_modules=MK57_HANGAR_MODULES, fill=VLS_FILL)

# 21-cell trainable RAM launcher on the hangar's after edge (roof-mounted)
ram_launcher_side(hx0 + 22, hang_top, 220)

# Midships pyramid (trapezoid) + intake louver
pyr_top_y = DECK_Y - 175
pyr_inset = (px1 - px0) * 0.22
draw.polygon([
    (px0, DECK_Y - 5), (px1, DECK_Y - 5),
    (px1 - pyr_inset, pyr_top_y), (px0 + pyr_inset, pyr_top_y),
], fill=PYRAMID_FILL, outline=HULL_LINE)
hatch_rect(px0 + 20, DECK_Y - 90, px0 + (px1 - px0) * 0.42, DECK_Y - 25, spacing=9)

# Mack (integrated mast/stack) topped with two funnels, replacing a plain
# comms mast -- pyramidal (tapered) body instead of a plain rectangle
mack_x = (px0 + px1) / 2
mack_top = pyr_top_y - 90
draw.polygon([
    (mack_x - 28, pyr_top_y), (mack_x + 28, pyr_top_y),
    (mack_x + 16, mack_top), (mack_x - 16, mack_top),
], fill=(80, 88, 100), outline=HULL_LINE)
funnel_gap, funnel_w, funnel_top = 6, 16, mack_top - 35
for fx0 in (mack_x - funnel_gap / 2 - funnel_w, mack_x + funnel_gap / 2):
    fx1 = fx0 + funnel_w
    draw.polygon([
        (fx0, mack_top), (fx1, mack_top),
        (fx1 - 3, funnel_top), (fx0 + 3, funnel_top),
    ], fill=(55, 60, 70), outline=HULL_LINE)

# 32-cell Mk41 VLS complex, flush with the deck (clearly sunken into the
# hull rather than a raised deckhouse box) between the pyramid and octagon
vls32_top = DECK_Y - 14
cell_grid(vls32_x0, vls32_top, vls32_x1, DECK_Y - 5, rows=1, cols=8, fill=VLS_FILL, pad=2)

# Octagonal forward superstructure + SPY-6 raked front face
ox0, ox1 = hull_x(OCTAGON[0]), hull_x(OCTAGON[1])
oct_top_y = DECK_Y - 195
oct_inset = (ox1 - ox0) * 0.18
draw.polygon([
    (ox0, DECK_Y - 5), (ox1, DECK_Y - 5),
    (ox1 - oct_inset, oct_top_y), (ox0 + oct_inset, oct_top_y),
], fill=OCTAGON_FILL, outline=HULL_LINE)
spy6_pts = [
    (ox1 - oct_inset * 0.3, oct_top_y + 12),
    (ox1 - 8, DECK_Y - 40),
    (ox1 - 30, DECK_Y - 40),
    (ox1 - oct_inset * 1.1, oct_top_y + 12),
]
draw.polygon(spy6_pts, fill=RADAR_FILL, outline=HULL_LINE)

# 21-cell trainable RAM launcher on the octagon's forward edge (roof-mounted)
ram_launcher_side(ox1 - 55, oct_top_y, -30)

# Small funnel on the octagon's after (aft) edge
oct_funnel_top = oct_top_y - 32
oct_funnel_cx = ox0 + oct_inset + 20
draw.polygon([
    (oct_funnel_cx - 12, oct_top_y), (oct_funnel_cx + 12, oct_top_y),
    (oct_funnel_cx + 9, oct_funnel_top), (oct_funnel_cx - 9, oct_funnel_top),
], fill=(55, 60, 70), outline=HULL_LINE)

# Octagonal enclosed "stealth" mast (San Antonio/AEM-S style composite
# tower), centered between the funnel and the octagon's forward edge
sm_cx = (oct_funnel_cx + ox1) / 2
sm_base_y = oct_top_y
sm_top_y = oct_top_y - 130
sm_base_w, sm_top_w, sm_chamfer = 46, 30, 16
sm_pts = [
    (sm_cx - sm_base_w / 2, sm_base_y), (sm_cx + sm_base_w / 2, sm_base_y),
    (sm_cx + sm_top_w / 2, sm_top_y + sm_chamfer),
    (sm_cx + sm_top_w / 2 - sm_chamfer * 0.6, sm_top_y),
    (sm_cx - sm_top_w / 2 + sm_chamfer * 0.6, sm_top_y),
    (sm_cx - sm_top_w / 2, sm_top_y + sm_chamfer),
]
draw.polygon(sm_pts, fill=(40, 44, 52), outline=HULL_LINE)

# 16-cell VLS deck box + Mk57 (2x 1x4 modules/side) flanking hint
# Lowered -- flush w/ deck, clearly sunken into the hull vs. a raised box
v16_top = DECK_Y - 18
cell_grid(v16_x0, v16_top, v16_x1, DECK_Y - 5, rows=1, cols=4, fill=VLS16_FILL, pad=2)
ld_mk57_strip_y0, ld_mk57_strip_y1 = DECK_Y - 5, DECK_Y + 10
quad_modules(ld_cx - ld_mk57_w / 2, ld_mk57_strip_y0, ld_cx + ld_mk57_w / 2, ld_mk57_strip_y1, n_modules=3, fill=VLS_FILL)

# Gunhouse: compact, narrow, boxy Mk 71-style housing, low profile, front
# AND rear corners chamfered (elongated-octagon) down to the 43.3 ft
# (203mm/65) barrels
gun_base_y = DECK_Y - 5
gun_top_y = DECK_Y - 38
gx0p, gx1p = hull_x(GUNHOUSE[0]), hull_x(GUNHOUSE[1])
draw.polygon([
    (gx0p, gun_base_y), (gx0p, gun_top_y + 14), (gx0p + 16, gun_top_y),
    (gx1p - 18, gun_top_y), (gx1p, gun_top_y + 16),
    (gx1p, gun_base_y),
], fill=GUNHOUSE_FILL, outline=HULL_LINE)
barrel_y = gun_top_y + 16
barrel_tip_x = gx1p + GUN_BARREL_PX
for off in (-5, 5):
    draw.line([(gx1p, barrel_y + off), (barrel_tip_x, barrel_y + off)], fill=(180, 184, 190), width=4)

draw.text((hull_x(0.05), DECK_Y + 35), "DENVER", font=f_hull_name, fill=(210, 214, 218))
draw.text((hull_x(0.90), DECK_Y + 10), "74", font=f_hull_no, fill=(210, 214, 218))

profile_above = [
    ((mack_x, funnel_top), "MACK / TWIN FUNNELS", None),
    ((mk41_x0 + 30, hatch_y0), "MK41 VLS — 64-CELL", "real-scale"),
    ((px0 + 40, DECK_Y - 60), "GT INTAKE", None),
    ((vls32_x0 + 10, vls32_top), "MK41 VLS — 32-CELL", "amidships, flush w/ deck"),
    ((spy6_pts[0][0], spy6_pts[0][1]), "SPY-6", "raked face"),
    ((oct_funnel_cx, oct_funnel_top), "FUNNEL", "aft edge, fwd superstructure"),
    ((sm_cx, sm_top_y), "STEALTH MAST", "octagonal, AEM/S-style"),
    ((ox1 - 55, oct_top_y - 19), "RAM LAUNCHER", "21-cell, trainable, fwd superstructure"),
    ((v16_x0 + 20, v16_top), "16-CELL VLS", "lowered, sunken into hull"),
    ((ld_cx, ld_mk57_strip_y0), "MK57 VLS — 12-CELL (P/S)", "flanks LD-VLS"),
]
place_tiered(profile_above, [sm_top_y - 25, sm_top_y - 70, sm_top_y - 115, sm_top_y - 160, sm_top_y - 205, sm_top_y - 250])

profile_below = [
    ((mk57_x0 + 20, mk57_strip_y1), "MK57 VLS — 16-CELL (P/S)", "real-scale"),
    (((hx0 + hx1) / 2, DECK_Y - 5), "HANGAR", "full beam"),
    ((hx0 + 22, hang_top - 19), "RAM LAUNCHER", "21-cell, trainable, hangar after edge"),
    (((px0 + px1) / 2, DECK_Y - 5), "MIDSHIPS SUPERSTRUCTURE", None),
    (((ox0 + ox1) / 2, DECK_Y - 5), "OCTAGONAL SUPERSTRUCTURE", "full beam"),
    (((gx0p + gx1p) / 2, gun_base_y), "MAIN GUN — 203 mm/65 (Mk 71-style)", None),
    ((STERN_X + 10, WATERLINE_Y), "WATERLINE", None),
    (BULB_PEAK, "BULBOUS BOW / SONAR DOME", "extended fwd, container-ship style"),
]
place_tiered(profile_below, [DECK_Y + 150, DECK_Y + 200, DECK_Y + 250, DECK_Y + 300, DECK_Y + 350])

# ---------------------------------------------------------------------------
# Legend
# ---------------------------------------------------------------------------
legend_y = H - 50
legend_items = [
    ("Hull", HULL_FILL),
    ("Hangar / superstructure", SUPERSTRUCTURE_FILL),
    ("Midships pyramid", PYRAMID_FILL),
    ("Octagonal superstructure", OCTAGON_FILL),
    ("Gunhouse", GUNHOUSE_FILL),
    ("Mk41 / Mk57 VLS", VLS_FILL),
    ("16-cell large-dia VLS", VLS16_FILL),
    ("SPY-6 / radar", RADAR_FILL),
    ("RAM launcher", RAM_FILL),
]
lx = 40
for name, color in legend_items:
    draw.rectangle([lx, legend_y, lx + 22, legend_y + 16], fill=color, outline=HULL_LINE)
    draw.text((lx + 30, legend_y - 2), name, font=f_label_sub, fill=TEXT_DIM)
    lx += 30 + draw.textlength(name, font=f_label_sub) + 40

out_path = "drawings/warship.png"
img.save(out_path)
print("saved", out_path, img.size)
