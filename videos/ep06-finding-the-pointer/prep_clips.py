"""Cut the two raw recordings of episode 6 (lab/shots/ep06) into one clip per window. Run once: python prep_clips.py"""
import subprocess
from pathlib import Path

RAW = Path(__file__).resolve().parents[2] / "lab" / "shots" / "ep06"
OUT = Path(__file__).resolve().parent / "assets" / "clips"
CUTS = {  # name: (source, x, y, w, h)
    "fire_game": ("a_w_fire", 0, 0, 1582, 930),
    "fire_found": ("a_w_fire", 1608, 30, 922, 872),
    "hk_game": ("c_hk_clip", 0, 0, 1582, 930),
    "hk_list": ("c_hk_clip", 1608, 616, 942, 210),
}
for name, (src, x, y, w, h) in CUTS.items():
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(RAW / f"{src}.mp4"), "-vf", f"crop={w}:{h}:{x}:{y}", "-r", "30",
                    "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-an", str(OUT / f"{name}.mp4")], check=True)
    print(name)
