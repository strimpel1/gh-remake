"""A tiny lock so two producers never capture the screen at the same time.

    python lab/lock.py acquire screen ep03     # waits (up to 90 min) until the screen is free, then takes it
    python lab/lock.py release screen ep03
    python lab/lock.py status

A lock older than 45 minutes is treated as abandoned and taken over (its game and Cheat Engine are closed first).
"""
import json
import subprocess
import sys
import time
from pathlib import Path

D = Path(__file__).resolve().parent / "locks"
STALE, WAIT = 45 * 60, 90 * 60


def main():
    D.mkdir(exist_ok=True)
    cmd = sys.argv[1]
    if cmd == "status":
        for f in D.glob("*.lock"):
            d = json.loads(f.read_text())
            print(f.stem, d["owner"], f"{int(time.time() - d['t'])}s")
        return
    f, owner = D / f"{sys.argv[2]}.lock", sys.argv[3]
    if cmd == "release":
        if f.exists() and json.loads(f.read_text())["owner"] == owner:
            f.unlink()
        print("released")
        return
    t0 = time.time()
    while True:
        try:
            with open(f, "x") as fh:
                fh.write(json.dumps({"owner": owner, "t": time.time()}))
            print("acquired")
            return
        except FileExistsError:
            try:
                d = json.loads(f.read_text())
            except Exception:
                d = {"owner": "?", "t": 0}
            if d["owner"] == owner:
                f.write_text(json.dumps({"owner": owner, "t": time.time()}))
                print("acquired (already yours)")
                return
            if time.time() - d["t"] > STALE:
                for exe in ("ac_client.exe", "cheatengine-x86_64.exe"):
                    subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True)
                f.unlink(missing_ok=True)
                continue
            if time.time() - t0 > WAIT:
                sys.exit(f"screen still held by {d['owner']}")
            time.sleep(20)


if __name__ == "__main__":
    main()
