from PIL import Image, ImageDraw, ImageFont
import os

FONT_DIR = "/home/claude/fonts"
DISPLAY_BOLD = f"{FONT_DIR}/PlayfairDisplay-Bold.ttf"

ACCENT = (211, 47, 47, 255)  # #d32f2f — visible on both light & dark, so headers need no theme pair
SCALE = 5  # supersample factor for clean serif edges
OUT_MULT = 3  # final native resolution multiplier over "logical" size, for retina sharpness

def make_header(text, filename, size=46, pad_x=6, pad_y=14, underline=True):
    font = ImageFont.truetype(DISPLAY_BOLD, size * SCALE)
    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    W = tw + pad_x * 2 * SCALE
    H = th + pad_y * 2 * SCALE + (14 * SCALE if underline else 0)
    img = Image.new("RGBA", (int(W), int(H)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((pad_x * SCALE - bbox[0], pad_y * SCALE - bbox[1]), text, font=font, fill=ACCENT)
    if underline:
        y = pad_y * SCALE * 2 + th
        draw.line([(pad_x * SCALE, y), (pad_x * SCALE + tw * 0.32, y)], fill=ACCENT, width=int(3 * SCALE))
    final_w = int(W / SCALE * OUT_MULT)
    final_h = int(H / SCALE * OUT_MULT)
    img = img.resize((final_w, final_h), Image.LANCZOS)
    img.save(filename)

def make_divider(filename, width=1100, height=26):
    W, H = width * SCALE, height * SCALE
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cy = H // 2
    dh = 6 * SCALE
    line_gap = 16 * SCALE
    draw.line([(0, cy), (W // 2 - dh - line_gap, cy)], fill=ACCENT, width=int(2 * SCALE))
    draw.line([(W // 2 + dh + line_gap, cy), (W, cy)], fill=ACCENT, width=int(2 * SCALE))
    cx = W // 2
    draw.polygon([(cx, cy - dh), (cx + dh, cy), (cx, cy + dh), (cx - dh, cy)], fill=ACCENT)
    img = img.resize((width * (OUT_MULT // 2 or 1), height * (OUT_MULT // 2 or 1)), Image.LANCZOS)
    img.save(filename)

def make_bullet(filename, size=28):
    S = size * SCALE
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    m = S * 0.22
    draw.polygon([(S/2, m), (S - m, S/2), (S/2, S - m), (m, S/2)], fill=ACCENT)
    out = size * (OUT_MULT // 2 or 1)
    img = img.resize((out, out), Image.LANCZOS)
    img.save(filename)

headers = [
    ("Machine Learning & Research", "hdr-ml.png"),
    ("VEX Robotics", "hdr-robotics.png"),
    ("Other Projects", "hdr-other.png"),
    ("Highlights", "hdr-highlights.png"),
    ("GitHub Activity", "hdr-activity.png"),
    ("GitHub Stats", "hdr-stats.png"),
]

os.makedirs("/home/claude/headers", exist_ok=True)
# clean out any header images from earlier section layouts that no longer apply
for stale in ("hdr-coursework.png", "hdr-beyond.png", "hdr-fullstack.png"):
    stale_path = f"/home/claude/headers/{stale}"
    if os.path.exists(stale_path):
        os.remove(stale_path)

for text, fname in headers:
    make_header(text, f"/home/claude/headers/{fname}")

make_divider("/home/claude/headers/divider.png")
make_bullet("/home/claude/headers/bullet.png")

print("done")
