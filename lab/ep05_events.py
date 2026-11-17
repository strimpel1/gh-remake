"""Episode 5: print the moments at which named regions of a raw recording change (to place narration against real events).
    python ep05_events.py a1_first [more names]
"""
import os
import subprocess
import sys

import numpy as np

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots", "ep05")
W, H, FPS = 2520, 940, 10
CE = 1618
REG = {"found": (CE + 0, 108, 130, 20), "value": (CE + 488, 186, 394, 30), "results": (CE + 4, 155, 384, 60), "list": (CE + 4, 644, 860, 50),
       "combo": (CE + 488, 230, 226, 250), "target": (8, 100, 960, 200), "hud": (480, 850, 220, 80), "dialog": (953, 651, 657, 135),
       "buttons": (CE + 434, 130, 200, 30)}

for name in sys.argv[1:]:
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", os.path.join(RAW, name + ".mp4"), "-vf", f"fps={FPS}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True)
    fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W).astype(np.int16)
    print(f"== {name}: {len(fr) / FPS:.1f}s")
    for r, (x, y, w, h) in REG.items():
        ts = [i / FPS for i in range(1, len(fr)) if (np.abs(fr[i, y:y + h, x:x + w] - fr[i - 1, y:y + h, x:x + w]) > 40).mean() > 0.004]
        runs = []
        for t in ts:
            if runs and t - runs[-1][1] < 0.35:
                runs[-1][1] = t
            else:
                runs.append([t, t])
        print(f"  {r:8s}", " ".join(f"{a:.1f}" if a == b else f"{a:.1f}-{b:.1f}" for a, b in runs))
