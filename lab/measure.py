"""Measure a rendered episode for empty-screen stretches and loudness.

    python lab/measure.py videos/ep04-inside-the-files/renders/x.mp4

Samples the video at 4 fps (downscaled to 480x270). A pixel is "ink" when it differs clearly from the paper colour
(228, 242, 236) and from the paper's grid lines; a frame is empty when under 0.15 % of it is ink, and "heading only"
when all its ink sits in the top quarter. Prints every empty run of 1 s or more, every heading-only run of 2 s or
more, and the mean volume.
"""
import subprocess
import sys

import numpy as np

W, H, FPS = 480, 270, 4
PAPER = np.array([228, 242, 236])
f = sys.argv[1]
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(int)
# the grid lines are at most ~150 away from the paper colour (summed over channels); real ink (dark teal, orange, white cards, captures) is further
ink = np.abs(fr - PAPER).sum(3) > 170
frac = ink.reshape(len(fr), -1).mean(1)
low = ink[:, H // 4:, :].reshape(len(fr), -1).mean(1)


def runs(mask, least):
    out, s = [], None
    for i, m in enumerate(list(mask) + [False]):
        if m and s is None:
            s = i
        if not m and s is not None:
            if (i - s) / FPS >= least:
                out.append((s / FPS, i / FPS))
            s = None
    return out


empty = frac < 0.0015
print(f"{len(fr)} frames at {FPS} fps = {len(fr) / FPS:.1f} s; ink fraction min {frac.min():.4f} median {np.median(frac):.3f}")
print("empty runs >= 1 s:", runs(empty, 1.0) or "none")
print("heading-only runs >= 2 s:", runs(~empty & (low < 0.0015), 2.0) or "none")
print("shortest-ink moments:", [(round(i / FPS, 2), round(float(frac[i]), 4)) for i in np.argsort(frac)[:6]])
v = subprocess.run(["ffmpeg", "-i", f, "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
print([ln.split("]")[-1].strip() for ln in v.splitlines() if "mean_volume" in ln or "max_volume" in ln])
