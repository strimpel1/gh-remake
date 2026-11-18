"""Review helper: 2x2 sheets (half-size frames) of the newest snapshot folder -> .hyperframes/review/sheet-N.png"""
import glob, os, sys
from PIL import Image
d = max(glob.glob(".hyperframes/artifacts/snapshots/*/"), key=os.path.getmtime)
fr = sorted(glob.glob(d + "frame-*.png"))
os.makedirs(".hyperframes/review", exist_ok=True)
for k in range(0, len(fr), 4):
    s = Image.new("RGB", (1920, 1080))
    for j, f in enumerate(fr[k:k + 4]):
        s.paste(Image.open(f).convert("RGB").resize((960, 540), Image.LANCZOS), (960 * (j % 2), 540 * (j // 2)))
    s.save(f".hyperframes/review/sheet-{k // 4 + 1}.png")
print(len(fr), "frames")
