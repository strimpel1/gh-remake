"""thumbnail.png for episode 5, in the look of episode 1's: a real game frame, a dark teal band, an orange box.   Run: python make_thumbnail.py"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
INK, ORANGE, MINT = (11, 42, 48), (255, 90, 31), (196, 227, 217)


def font(size, mono=False):
    for name in (["consolab.ttf", "courbd.ttf"] if mono else ["ariblk.ttf", "arialbd.ttf"]):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


game = Image.open(HERE / "assets/shots/a_frozen_game.png").convert("RGB").crop((0, 39, 1585, 931))   # the client area, ammo at 95
img = game.resize((1920, round(892 * 1920 / 1585)), Image.LANCZOS).crop((0, 0, 1920, 1080))
band = Image.new("RGBA", (1920, 500), INK + (225,))
img.paste(band, (0, 0), band)
d = ImageDraw.Draw(img)
d.text((80, 60), "2,253 RESULTS", font=font(116), fill="white")
d.text((80, 220), "DOWN TO", font=font(84), fill=MINT)
d.rectangle((105, 385, 1165, 585), fill=INK)
d.rectangle((90, 365, 1150, 565), fill=ORANGE)
d.text((620, 465), "1 ADDRESS", font=font(150, mono=True), fill="white", anchor="mm")
d.rectangle((1255, 95, 1865, 195), fill=INK)
d.rectangle((1240, 80, 1850, 180), fill=ORANGE)
d.text((1262, 100), "GAME HACKING #5", font=font(54), fill="white")
k = 1920 / 1585                                         # the magazine counter in the frame
x, y, w, h = 478 * k, (855 - 39) * k, 195 * k, 65 * k
for i in range(8):
    d.rectangle((x - 14 - i, y - 14 - i, x + w + 14 + i, min(y + h + 14, 1070) + i), outline=ORANGE)
img.save(HERE / "thumbnail.png")
print(img.size)
