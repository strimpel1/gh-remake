"""Find capture dropouts in screen recordings: a frame that is blank (almost one flat colour) or that differs strongly
from both neighbours while the neighbours match each other.

    python lab/blank_frames.py videos/ep03-*/assets/clips/*.mp4      # prints frame indexes; exit code 1 if any

Checked at the clip's full frame rate: half-second samples miss a one-frame dropout.
"""
import glob
import subprocess
import sys

import numpy as np

W, H = 160, 90


def frames(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H}", "-fps_mode", "passthrough",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)


def scan(path):
    f = frames(path)
    bad = []
    for i in range(len(f)):
        flat = f[i].std() < 3 and (f[i].mean() > 245 or f[i].mean() < 5)
        spike = False
        if 0 < i < len(f) - 1:
            a, b, c = np.abs(f[i] - f[i - 1]).mean(), np.abs(f[i] - f[i + 1]).mean(), np.abs(f[i + 1] - f[i - 1]).mean()
            spike = a > 40 and b > 40 and c < 6
        if flat or spike:
            bad.append(i)
    return len(f), bad


def main():
    paths = [p for a in sys.argv[1:] for p in glob.glob(a)]
    any_bad = False
    for p in paths:
        if "_fit" in p:
            continue
        n, bad = scan(p)
        print(f"{p}: {n} frames, bad {bad}")
        any_bad |= bool(bad)
    sys.exit(1 if any_bad else 0)


if __name__ == "__main__":
    main()
