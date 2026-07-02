from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/home/claude/fonts"
DISPLAY_BOLD = f"{FONT_DIR}/PlayfairDisplay-Bold.ttf"
DISPLAY_BLACK = f"{FONT_DIR}/PlayfairDisplay-Black.ttf"
BODY = f"{FONT_DIR}/HKGrotesk-Regular.ttf"
BODY_SEMI = f"{FONT_DIR}/HKGrotesk-SemiBold.ttf"

ACCENT = (211, 47, 47)  # #d32f2f

W, H = 1320, 360
SCALE = 2  # render at 2x then downsample for crisp edges

def make_banner(path, bg, fg, muted, accent=ACCENT):
    img = Image.new("RGBA", (W * SCALE, H * SCALE), bg)
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(DISPLAY_BLACK, 92 * SCALE)
    tagline_font = ImageFont.truetype(BODY_SEMI, 30 * SCALE)
    meta_font = ImageFont.truetype(BODY, 26 * SCALE)

    cx = (W * SCALE) // 2

    # Title
    title = "AYAAN GOSWAMI"
    tw = draw.textlength(title, font=title_font)
    ty = 78 * SCALE
    draw.text((cx - tw / 2, ty), title, font=title_font, fill=fg)

    # Ornamental rule: line - diamond - line
    rule_y = ty + 128 * SCALE
    diamond_half = 7 * SCALE
    line_gap = 18 * SCALE
    line_len = 170 * SCALE
    draw.line(
        [(cx - diamond_half - line_gap - line_len, rule_y),
         (cx - diamond_half - line_gap, rule_y)],
        fill=accent, width=int(2 * SCALE)
    )
    draw.line(
        [(cx + diamond_half + line_gap, rule_y),
         (cx + diamond_half + line_gap + line_len, rule_y)],
        fill=accent, width=int(2 * SCALE)
    )
    draw.polygon(
        [(cx, rule_y - diamond_half), (cx + diamond_half, rule_y),
         (cx, rule_y + diamond_half), (cx - diamond_half, rule_y)],
        fill=accent
    )

    # Tagline
    tagline = "AAsSPIRING ENGINEER & DATA SCIENTIST".replace("AAsS", "")
    tagline = "ASPIRING ENGINEER  ·  DATA SCIENTIST  ·  TECHNOLOGY FOR SOCIAL IMPACT"
    tag_font = tagline_font
    tw2 = draw.textlength(tagline, font=tag_font)
    tag_y = rule_y + 34 * SCALE
    draw.text((cx - tw2 / 2, tag_y), tagline, font=tag_font, fill=muted)

    # Meta line
    meta = "CARNEGIE VANGUARD HIGH SCHOOL   ·   HOUSTON, TX"
    mw = draw.textlength(meta, font=meta_font)
    meta_y = tag_y + 54 * SCALE
    draw.text((cx - mw / 2, meta_y), meta, font=meta_font, fill=accent)

    img = img.resize((W, H), Image.LANCZOS)
    img.save(path)

# Light theme: bg #fdfdfd, fg #1a1a1a, muted #55555a
make_banner("/home/claude/hero-light.png", (253, 253, 253, 255), (26, 26, 26, 255), (85, 85, 90, 255))

# Dark theme: bg #0b0b0b, fg #f5f5f5, muted #a8a8ad
make_banner("/home/claude/hero-dark.png", (11, 11, 11, 255), (245, 245, 245, 255), (168, 168, 173, 255))

print("done")
