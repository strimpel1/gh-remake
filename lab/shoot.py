"""Fire single shots in the practice game: python shoot.py 3   (brings the game to the front and clicks in it)."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "videos", "tools"))
import capture  # noqa: E402
from pywinauto import mouse  # noqa: E402

n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
g = capture.find("AssaultCube")
capture.front(g)
x, y, w, h = capture.rect(g)
p = (x + w // 2, y + h // 2 - 100)
for _ in range(n):
    mouse.press(coords=p)
    time.sleep(0.05)
    mouse.release(coords=p)
    time.sleep(0.9)
