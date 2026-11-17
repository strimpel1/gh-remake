"""Put a finished episode into the channel studio: read its YOUTUBE.md, write the studio project entry, package it.

    python lab/register_episode.py ep03-read-one-line-of-assembly

Queueing (autopilot.py add game-hacking <ep> --kind gh) and pushing the repo are separate, deliberate steps.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROJECT = Path(r"D:\AI\studio\projects\game-hacking.json")
STUDIO = r"D:\AI\.claude\skills\channel-studio\scripts\studio.py"


def main():
    ep = sys.argv[1]
    d = REPO / "videos" / ep
    y = (d / "YOUTUBE.md").read_text(encoding="utf-8")
    title = re.search(r"\*\*Title:\*\*\s*(.+)", y).group(1).strip()
    desc = re.search(r"\*\*Description:\*\*\s*\n(.*?)\n\*\*Tags:\*\*", y, re.S).group(1).strip()
    tags = [t.strip() for t in re.search(r"\*\*Tags:\*\*\s*(.+)", y).group(1).split(",") if t.strip()]
    problems = []
    if "<" in title + desc or ">" in title + desc:
        problems.append("< or > in title/description")
    if len(title) > 100:
        problems.append(f"title is {len(title)} characters")
    if not sorted((d / "renders").glob("*.mp4")):
        problems.append("no render")
    if not (d / "thumbnail.png").exists():
        problems.append("no thumbnail.png")
    for url in re.findall(r"https://github\.com/strimpel1/gh-remake/blob/main/(\S+)", desc):
        if not (REPO / url).exists():
            problems.append(f"description links a file that is not in the repo: {url}")
    if problems:
        sys.exit("NOT registered: " + "; ".join(problems))
    p = json.loads(PROJECT.read_text(encoding="utf-8"))
    e = p["episodes"].setdefault(ep, {})
    e.update(yt_title=title, yt_description=desc, yt_tags=tags, thumbnail=(d / "thumbnail.png").as_posix())
    PROJECT.write_text(json.dumps(p, indent=1, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, STUDIO, "package", "game-hacking", ep], capture_output=True, text=True, encoding="utf-8")
    print(title)
    print((r.stdout or "").strip()[-300:], (r.stderr or "").strip()[-300:])


if __name__ == "__main__":
    main()
