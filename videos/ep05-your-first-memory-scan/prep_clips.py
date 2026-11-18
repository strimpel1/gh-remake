"""Cut the raw screen recordings of the capture sessions (lab/shots/ep05, one wide rectangle holding the target window and
Cheat Engine) into per-window clips and stills for build.py. Every crop is exactly one window's own rectangle.
Segments only remove waiting time, and a clip may hold its first frame while the narration sets it up; nothing is sped up.   Run: python prep_clips.py   (or: python prep_clips.py a1c_ce   to cut only the named clips)
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE.parents[1] / "lab" / "shots" / "ep05"
CLIPS, SHOTS = HERE / "assets" / "clips", HERE / "assets" / "shots"
WIN = {"ce": (1618, 0, 888, 932), "game": (9, 0, 1584, 930), "con": (8, 0, 972, 380)}

CUTS = {  # out name: (raw recording, window, [(from, to), ...], seconds to hold the first frame before it starts)
    "a1_ce": ("a1_first", "ce", [(1.0, 11.5)], 0),
    "a1c_ce": ("a1_first", "ce", [(1.0, 11.5)], 4.6),      # cold open: the result appears as the voice says "it answers"
    "a2f_game": ("a2_fire", "game", [(0.0, 8.5)], 0),
    "a2n_ce": ("a2_next", "ce", [(1.0, 11.0)], 0),
    "a3n_ce": ("a3_next", "ce", [(0.8, 9.5)], 0),
    "a3add_ce": ("a3_next", "ce", [(9.0, 17.0)], 0),
    "a4": ("a4_copy", "ce+game", [(1.0, 9.3)], 5.5),
    "a5": ("a5_real", "ce+game", [(0.5, 9.3)], 0),
    "a6": ("a6_fire", "ce+game", [(0.3, 8.7)], 0),
    "a7": ("a7_freeze", "ce+game", [(0.2, 13.9)], 0),
    "c1_ce": ("c1_unknown", "ce", [(3.0, 6.6), (7.0, 14.3), (16.6, 20.5)], 0),
    "c2": ("c2_decr", "ce+con", [(1.5, 4.5), (5.9, 9.2), (9.8, 13.5)], 0),
    "c3": ("c3_unch", "ce+con", [(1.0, 12.0)], 0),
    "c4": ("c4_incr", "ce+con", [(1.5, 3.8), (5.9, 9.0), (9.6, 13.5)], 0),
    "c5": ("c5_write", "ce+con", [(2.0, 11.5)], 0),
    "d1": ("d1_int", "ce+con", [(11.1, 14.3), (17.2, 18.6), (20.0, 25.5)], 4.0),
    "d2": ("d2_float", "ce+con", [(14.3, 17.6), (18.9, 21.0), (27.2, 29.1), (30.2, 32.2), (33.0, 34.6), (38.9, 41.8)], 6.3),
}
FRAMES = {  # still: (raw recording, window, second)
    "game20": ("a1_first", "game", 1.0), "game14": ("a2_next", "game", 1.0), "game10": ("a3_next", "game", 1.0),
    "con_fresh": ("b1_first", "con", 1.0),
}
COPY = ["a_ce_empty", "a_proclist", "a_ce_attached", "a_scan1", "a_scan2", "a_scan3", "a_list", "a_frozen2", "a_frozen_game", "a_restart2",
        "a_restart_game", "b_scan2", "b_copy", "b_real", "b_real_con", "c_dd_open", "c_scan4", "c_w", "c_w_con", "d_scan2", "d_list", "d_con80"]

CLIPS.mkdir(parents=True, exist_ok=True)
SHOTS.mkdir(parents=True, exist_ok=True)
ONLY = sys.argv[1:]
for name, (raw, wins, segs, lead) in CUTS.items():
    if ONLY and name not in ONLY:
        continue
    for win in wins.split("+"):
        out = name if "+" not in wins else f"{name}_{win}"
        x, y, w, h = WIN[win]
        parts = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,crop={w}:{h}:{x}:{y}[v{i}];" for i, (a, b) in enumerate(segs))
        graph = parts + "".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1,tpad=start_mode=clone:start_duration={lead}[o]"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(RAW / f"{raw}.mp4"), "-filter_complex", graph, "-map", "[o]", "-r", "30",
                        "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-an", str(CLIPS / f"{out}.mp4")], check=True)
        print(out, lead + sum(b - a for a, b in segs))
if ONLY:
    sys.exit(0)
for out, (raw, win, t) in FRAMES.items():
    x, y, w, h = WIN[win]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(RAW / f"{raw}.mp4"), "-vf", f"crop={w}:{h}:{x}:{y}", "-frames:v", "1",
                    str(SHOTS / f"{out}.png")], check=True)
for n in COPY:
    shutil.copy(RAW / f"{n}.png", SHOTS / f"{n}.png")
print("done")
