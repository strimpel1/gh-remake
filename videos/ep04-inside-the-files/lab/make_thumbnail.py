"""Thumbnail for episode 4, in the look of ep01's: a real capture, a dark band, white heading, an orange byte box.
    python make_thumbnail.py   ->  ../thumbnail.png (1920x1080)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

E = Path(__file__).resolve().parents[1]
W, H = 1920, 1080
INK, ORANGE, MINT = (11, 42, 48), (255, 90, 31), (191, 230, 221)


def font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            pass
    raise SystemExit(f"no font among {names}")


HEAD = ["ariblk.ttf", "arialbd.ttf"]
MONO = ["consolab.ttf", "courbd.ttf"]

img = Image.new("RGB", (W, H), (236, 236, 236))
shot = Image.open(E / "assets/shots/exe_head.png").convert("RGB")
s = W / 900                                       # show the left ~900 px of the hex pane, large
big = shot.resize((round(shot.width * s), round(shot.height * s)), Image.LANCZOS)
img.paste(big.crop((0, round(46 * s), W, round(46 * s) + 560)), (0, 540))
d = ImageDraw.Draw(img, "RGBA")
d.rectangle([0, 0, W, 540], fill=INK + (255,))
d.rectangle([0, 540, W, 552], fill=(9, 32, 37, 255))

d.text((80, 30), "EVERY EXE", font=font(HEAD, 150), fill="white")
d.text((80, 200), "STARTS WITH", font=font(HEAD, 84), fill=MINT)

# the byte box
d.rectangle([104, 334, 104 + 760, 334 + 170], fill=(5, 22, 26, 255))
d.rectangle([90, 320, 90 + 760, 320 + 170], fill=ORANGE + (255,))
d.text((90 + 380, 320 + 85), '4D 5A = "MZ"', font=font(MONO, 104), fill="white", anchor="mm")

# episode tag
f = font(HEAD, 50)
t = "GAME HACKING #4"
tw = d.textlength(t, font=f)
d.rectangle([W - 90 - tw - 56 + 12, 78 + 12, W - 90 + 12, 78 + 100 + 12], fill=(9, 32, 37, 255))
d.rectangle([W - 90 - tw - 56, 78, W - 90, 78 + 100], fill=ORANGE + (255,))
d.text((W - 90 - 28 - tw / 2, 78 + 50), t, font=f, fill="white", anchor="mm")

# ring around the real 4D 5A in the capture (row 0 text is at y 63..80, bytes 0-1 at x 160..225 in the source image)
x0, y0 = 156 * s, 540 + (60 - 46) * s
x1, y1 = 229 * s, 540 + (84 - 46) * s
for k in range(8):
    d.rounded_rectangle([x0 - 10 - k, y0 - 10 - k, x1 + 10 + k, y1 + 10 + k], radius=16, outline=ORANGE + (255,))
img.save(E / "thumbnail.png")
print("thumbnail.png", img.size)
