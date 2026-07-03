from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/home/claude/fonts"
DISPLAY_BLACK = f"{FONT_DIR}/PlayfairDisplay-Black.ttf"
BODY = f"{FONT_DIR}/HKGrotesk-Regular.ttf"
BODY_SEMI = f"{FONT_DIR}/HKGrotesk-SemiBold.ttf"

ACCENT = (211, 47, 47, 255)  # #d32f2f — legible on both light and dark, used for the ornament + meta line

# Final output is transparent PNG at 1.2x the old size for extra crispness on retina
# displays, supersampled at a higher factor for cleaner serif edges before downsampling.
W, H = 1584, 432
SCALE = 4

def make_banner(path, fg, muted, accent=ACCENT):
    img = Image.new("RGBA", (W * SCALE, H * SCALE), (0, 0, 0, 0))  # fully transparent canvas
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(DISPLAY_BLACK, 110 * SCALE)
    tagline_font = ImageFont.truetype(BODY_SEMI, 36 * SCALE)
    meta_font = ImageFont.truetype(BODY, 31 * SCALE)

    cx = (W * SCALE) // 2

    title = "AYAAN GOSWAMI"
    tw = draw.textlength(title, font=title_font)
    ty = 94 * SCALE
    draw.text((cx - tw / 2, ty), title, font=title_font, fill=fg)

    rule_y = ty + 154 * SCALE
    diamond_half = 8 * SCALE
    line_gap = 22 * SCALE
    line_len = 204 * SCALE
    draw.line(
        [(cx - diamond_half - line_gap - line_len, rule_y),
         (cx - diamond_half - line_gap, rule_y)],
        fill=accent, width=int(2.4 * SCALE)
    )
    draw.line(
        [(cx + diamond_half + line_gap, rule_y),
         (cx + diamond_half + line_gap + line_len, rule_y)],
        fill=accent, width=int(2.4 * SCALE)
    )
    draw.polygon(
        [(cx, rule_y - diamond_half), (cx + diamond_half, rule_y),
         (cx, rule_y + diamond_half), (cx - diamond_half, rule_y)],
        fill=accent
    )

    tagline = "ASPIRING ENGINEER  ·  DATA SCIENTIST  ·  TECHNOLOGY FOR SOCIAL IMPACT"
    tw2 = draw.textlength(tagline, font=tagline_font)
    tag_y = rule_y + 40 * SCALE
    draw.text((cx - tw2 / 2, tag_y), tagline, font=tagline_font, fill=muted)

    meta = "CARNEGIE VANGUARD HIGH SCHOOL   ·   HOUSTON, TX"
    mw = draw.textlength(meta, font=meta_font)
    meta_y = tag_y + 64 * SCALE
    draw.text((cx - mw / 2, meta_y), meta, font=meta_font, fill=accent)

    img = img.resize((W, H), Image.LANCZOS)
    img.save(path)

# Light-theme text: dark ink title, mid-gray tagline, transparent canvas throughout
make_banner("/home/claude/hero-light.png", (26, 26, 26, 255), (85, 85, 90, 255))

# Dark-theme text: off-white title, light-gray tagline, transparent canvas throughout
make_banner("/home/claude/hero-dark.png", (245, 245, 245, 255), (168, 168, 173, 255))

print("done")
