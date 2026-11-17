"""Record a screen rectangle while firing single shots in the game: python rec_region.py out.mp4 x y w h shots
Both windows must already be placed inside the rectangle and visible. Look at the result before using it."""
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "videos", "tools"))
import capture  # noqa: E402
from pywinauto import mouse  # noqa: E402

out, (rx, ry, rw, rh, shots) = sys.argv[1], map(int, sys.argv[2:7])
for t in sys.argv[7:]:
    capture.front(capture.find(t))
g = capture.find("AssaultCube")
capture.front(g)
x, y, w, h = capture.rect(g)
p = (x + w // 2, y + h // 2 - 100)
dur = 2.0 + shots * 1.5 + 1.5
rec = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "gdigrab", "-framerate", "30", "-offset_x", str(rx), "-offset_y", str(ry),
                        "-video_size", f"{rw // 2 * 2}x{rh // 2 * 2}", "-t", str(dur), "-i", "desktop", "-c:v", "libx264", "-crf", "14",
                        "-pix_fmt", "yuv420p", out])
time.sleep(2.0 + 0.8)
for _ in range(shots):
    mouse.press(coords=p)
    time.sleep(0.03)
    mouse.release(coords=p)
    time.sleep(1.5)
rec.wait()
print(out, dur)
