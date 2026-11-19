# Draws branding/icon.png (1024x1024 app icon). Run: uv run --with pillow python branding/make_icon.py branding/icon.png /tmp/icon_preview.png
import sys
from PIL import Image, ImageDraw, ImageFilter
N = 1024; SS = 4; W = N * SS
DARK = (42, 33, 26); DARK2 = (70, 50, 36)
RUST = (154, 74, 42); CREAM = (247, 241, 230); GOLD = (214, 160, 92)

# background: dark warm radial glow
bg = Image.new("RGB", (W, W), DARK)
glow = Image.new("L", (W, W), 0)
ImageDraw.Draw(glow).ellipse([W*0.05, W*-0.05, W*0.95, W*0.85], fill=255)
glow = glow.filter(ImageFilter.GaussianBlur(W * 0.12))
bg = Image.composite(Image.new("RGB", (W, W), DARK2), bg, glow)

def card(angle, fill, box, radius, shadow=True):
    layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if shadow:
        sh = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        x0, y0, x1, y1 = box
        ImageDraw.Draw(sh).rounded_rectangle([x0 + W*0.012, y0 + W*0.02, x1 + W*0.012, y1 + W*0.02], radius, fill=(0, 0, 0, 120))
        sh = sh.filter(ImageFilter.GaussianBlur(W * 0.018)).rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
        layer = Image.alpha_composite(layer, sh); d = ImageDraw.Draw(layer)
    c = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle(box, radius, fill=fill)
    c = c.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
    return Image.alpha_composite(layer, c)

img = bg.convert("RGBA")
cw, ch = W * 0.46, W * 0.575          # 4:5 card, like the feed posts
cx, cy = W / 2 + W * 0.035, W / 2 + W * 0.01
box = [cx - cw/2, cy - ch/2, cx + cw/2, cy + ch/2]
r = W * 0.05
img = Image.alpha_composite(img, card(-12, GOLD + (255,), [b + o for b, o in zip(box, (-W*0.07, -W*0.02, -W*0.07, -W*0.02))], r))
img = Image.alpha_composite(img, card(-4, RUST + (255,), [b + o for b, o in zip(box, (-W*0.03, -W*0.01, -W*0.03, -W*0.01))], r))
img = Image.alpha_composite(img, card(5, CREAM + (255,), box, r))

# upward arrow on the front card (rotated with it)
a = Image.new("RGBA", (W, W), (0, 0, 0, 0)); d = ImageDraw.Draw(a)
s = W * 0.0011
shaft_w, head_w, head_h, total = 70*s, 190*s, 120*s, 300*s
top = cy - total/2 - W*0.01
d.polygon([(cx, top), (cx - head_w/2, top + head_h), (cx + head_w/2, top + head_h)], fill=RUST + (255,))
d.rounded_rectangle([cx - shaft_w/2, top + head_h * 0.5, cx + shaft_w/2, top + total], 14*s, fill=RUST + (255,))
# base line: "upload" tray
d.rounded_rectangle([cx - 150*s, top + total + 45*s, cx + 150*s, top + total + 45*s + 34*s], 17*s, fill=RUST + (255,))
a = a.rotate(5, resample=Image.BICUBIC, center=(cx, cy))
img = Image.alpha_composite(img, a)

out = img.convert("RGB").resize((N, N), Image.LANCZOS)
out.save(sys.argv[1], optimize=True)
# small-size preview: 1024, 192, 64 side by side on white
pv = Image.new("RGB", (1024 + 192 + 64 + 80, 1024), (255, 255, 255))
pv.paste(out, (0, 0)); pv.paste(out.resize((192, 192), Image.LANCZOS), (1024 + 30, 0)); pv.paste(out.resize((64, 64), Image.LANCZOS), (1024 + 192 + 55, 0))
pv.save(sys.argv[2])
