"""Record the game + Cheat Engine side by side while firing single shots (real ammo counter and real memory rows change together)."""
import subprocess, sys, time
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "videos", "tools")); import capture
from pywinauto import mouse
out, shots = sys.argv[1], int(sys.argv[2])
ce = [h for h, t in capture.windows() if t == "Cheat Engine" and capture.rect(h)[2] > 0][0]
capture.front(ce); g = capture.find("AssaultCube"); capture.front(g)
x, y, w, h = capture.rect(g)
mouse.click(coords=(x + w // 2, y + h // 2 - 100)); time.sleep(1.5)        # focus the game (fires once)
dur = 2.5 + shots * 1.6 + 1.5
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "gdigrab", "-framerate", "30", "-offset_x", "0", "-offset_y", "0",
                      "-video_size", "2504x964", "-t", str(dur), "-i", "desktop", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", out])
time.sleep(2.5 + 0.8)
for _ in range(shots):
    mouse.press(coords=(x + w // 2, y + h // 2 - 100)); time.sleep(0.03); mouse.release(coords=(x + w // 2, y + h // 2 - 100)); time.sleep(1.6)
p.wait(); print(out, dur)
