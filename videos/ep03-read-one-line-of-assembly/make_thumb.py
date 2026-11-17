"""thumbnail.png for episode 3 (1920x1080), same look as episodes 1 and 2: a darkened real game frame, big white and
orange words, the real instruction in tiles.   Run: python make_thumb.py"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

D = Path(__file__).resolve().parent
BLACK, MONO = r"C:\Windows\Fonts\ariblk.ttf", r"C:\Windows\Fonts\consolab.ttf"
INK, ORANGE, PAPER = (11, 42, 48), (255, 90, 31), (207, 233, 223)


def font(path, size):
    return ImageFont.truetype(path, size)


bg = Image.open(D / "assets/shots/thumb_game.png").convert("RGB")
bg = bg.crop((0, 39, bg.width, bg.height))                       # drop the window's title bar
s = max(1920 / bg.width, 1080 / bg.height)
bg = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS)
bg = bg.crop(((bg.width - 1920) // 2, bg.height - 1080, (bg.width - 1920) // 2 + 1920, bg.height))
bg = ImageEnhance.Brightness(bg).enhance(0.62)
bg = Image.blend(bg, Image.new("RGB", bg.size, (12, 44, 50)), 0.52)
d = ImageDraw.Draw(bg)


def box(x, y, w, h, fill, text, f, color, shadow=14):
    d.rectangle([x + shadow, y + shadow, x + w + shadow, y + h + shadow], fill=INK)
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=INK, width=10)
    tw = d.textlength(text, font=f)
    b = f.getbbox(text)
    d.text((x + (w - tw) / 2, y + (h - (b[3] - b[1])) / 2 - b[1]), text, font=f, fill=color)


d.text((80, 70), "READ THE", font=font(BLACK, 170), fill=(255, 255, 255))
d.text((80, 260), "GAME'S CODE", font=font(BLACK, 170), fill=ORANGE)

mono = font(MONO, 120)
box(90, 560, 250, 170, PAPER, "FF", mono, INK)
box(370, 560, 250, 170, PAPER, "08", mono, INK)
d.text((670, 580), "=", font=font(BLACK, 110), fill=(255, 255, 255))
box(800, 545, 760, 200, ORANGE, "dec [eax]", font(MONO, 130), (255, 255, 255))
d.text((95, 800), "the line that takes one round", font=font(BLACK, 62), fill=(255, 255, 255))
box(1240, 890, 590, 110, ORANGE, "GAME HACKING #3", font(BLACK, 52), (255, 255, 255), shadow=10)
bg.save(D / "thumbnail.png")
print("thumbnail.png", bg.size)
