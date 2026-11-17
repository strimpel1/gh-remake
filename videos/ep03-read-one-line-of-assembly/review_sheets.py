"""Review helper: tile the latest HyperFrames snapshot frames 2x2 into .hyperframes/review/sheet-NN.jpg (960x540 per frame)."""
import sys
from pathlib import Path

from PIL import Image

root = Path(__file__).resolve().parent / ".hyperframes"
snap = max((root / "artifacts" / "snapshots").iterdir(), key=lambda p: p.stat().st_mtime)
frames = sorted(snap.glob("frame-*.png"), key=lambda p: int(p.name.split("-")[1]))
out = root / "review"
out.mkdir(exist_ok=True)
for old in out.glob("sheet-*.jpg"):
    old.unlink()
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
for i in range(0, len(frames), n):
    sheet = Image.new("RGB", (1920, 1080 if n == 4 else 540))
    for k, f in enumerate(frames[i:i + n]):
        sheet.paste(Image.open(f).convert("RGB").resize((960, 540), Image.LANCZOS), ((k % 2) * 960, (k // 2) * 540))
    sheet.save(out / f"sheet-{i // n + 1:02d}.jpg", quality=90)
    print(out / f"sheet-{i // n + 1:02d}.jpg", [f.name for f in frames[i:i + n]])
