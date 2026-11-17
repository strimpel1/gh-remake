"""Episode 5 capture driver: runs a short list of real mouse/keyboard actions on Cheat Engine's own window and on the
practice target (AssaultCube offline, or scanme.exe), optionally while recording a screen rectangle.

    python ep05_cap.py run  "front ce ;; setval 20 ;; click btnNewScan ;; waitscan ;; found"
    python ep05_cap.py take name x y w h "<actions>"      # the same, recorded to lab/shots/ep05/name.mp4

Actions (separated by " ;; "):
    pause S | front ce|game|con|<title> | setval TEXT [control] | click CONTROL [dx dy] | dbl CONTROL [dx dy] | at X Y [double|right]
    keys "<pywinauto keys>" | fire N | lua <code> | waitscan | found | info | shot NAME <title> | combo CONTROL N [shot-name-while-open]
Cheat Engine must have been started with lab/ce/start_ce.py lab/ce/ep05.CT (the Lua command channel).
Hold the screen lock (lab/lock.py) while this runs.
"""
import os
import subprocess
import sys
import time

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, "..", "videos", "tools"))
import capture  # noqa: E402
import win32api  # noqa: E402
from pywinauto import mouse  # noqa: E402
from pywinauto.keyboard import send_keys  # noqa: E402

RAW = os.path.join(D, "shots", "ep05")
os.makedirs(RAW, exist_ok=True)
CMD, OUT = os.path.join(D, "ce", "cmd.lua"), os.path.join(D, "ce", "cmd.lua.out")
CONTROLS = ["scanvalue", "scanvalue2", "scantype", "VarType", "btnNewScan", "btnNextScan", "foundcountlabel", "Foundlist3", "sbOpenProcess",
            "btnAddAddressManually", "btnMemoryView", "cbFastScan", "cbWritable", "ProcessLabel", "UndoScan", "Panel5", "Panel1"]


def lua(code, wait=20):
    if os.path.exists(OUT):
        os.remove(OUT)
    with open(CMD + ".tmp", "w", encoding="utf-8") as f:
        f.write(code)
    os.replace(CMD + ".tmp", CMD)
    t0 = time.time()
    while time.time() - t0 < wait:
        time.sleep(0.1)
        if os.path.exists(OUT):
            time.sleep(0.1)
            return open(OUT, encoding="utf-8", errors="replace").read()
    return "no answer"


def crect(name):
    """Screen rectangle of a control of Cheat Engine's main form (x, y, w, h)."""
    r = lua(f"local c=getMainForm().{name} local x,y=c.clientToScreen(0,0) return string.format('%d %d %d %d',x,y,c.Width,c.Height)")
    if not r.startswith("true"):
        sys.exit(f"{name}: {r}")
    return [int(v) for v in r.split()[1:5]]


def ce_hwnd():
    hits = [h for h, t in capture.windows() if t.startswith("Cheat Engine") and capture.rect(h)[2] > 300]
    return hits[0]


def glide(x, y, t=0.35, steps=20):
    cx, cy = win32api.GetCursorPos()
    for i in range(1, steps + 1):
        k = i / steps
        k = k * k * (3 - 2 * k)
        win32api.SetCursorPos((int(cx + (x - cx) * k), int(cy + (y - cy) * k)))
        time.sleep(t / steps)


def click(x, y, double=False, button="left"):
    glide(x, y)
    time.sleep(0.15)
    if double:
        mouse.double_click(coords=(x, y))
    else:
        mouse.click(button=button, coords=(x, y))
    time.sleep(0.25)


def target(name, a):
    x, y, w, h = crect(name)
    if len(a) >= 2:
        return x + int(a[0]), y + int(a[1])
    return x + w // 2, y + h // 2


def found():
    return lua("return getMainForm().foundcountlabel.Caption").replace("true ", "")


def act(line):
    a = line.strip().split(" ")
    op, a = a[0], a[1:]
    if op == "pause":
        time.sleep(float(a[0]))
    elif op == "front":
        t = " ".join(a)
        h = ce_hwnd() if t == "ce" else capture.find({"game": "AssaultCube", "con": "Scan Me"}.get(t, t))
        capture.front(h)
    elif op == "setval":
        x, y = target(a[1] if len(a) > 1 else "scanvalue", [])
        click(x, y)
        send_keys("^a", pause=0.05)
        time.sleep(0.2)
        send_keys(a[0], pause=0.12)
        time.sleep(0.3)
    elif op == "click":
        click(*target(a[0], a[1:]))
    elif op == "dbl":
        click(*target(a[0], a[1:]), double=True)
    elif op == "at":
        click(int(a[0]), int(a[1]), double="double" in a, button="right" if "right" in a else "left")
    elif op == "keys":
        send_keys(" ".join(a).strip('"'), pause=0.1)
    elif op == "combo":            # open a combo box with the mouse, then pick item N with the keyboard (Home, N x Down, Enter)
        click(*target(a[0], []))
        time.sleep(0.8)
        send_keys("{HOME}" + "{DOWN}" * int(a[1]), pause=0.12)
        time.sleep(0.6)
        if len(a) > 2:
            capture.grab(*capture.rect(ce_hwnd()), os.path.join(RAW, a[2] + ".png"))
        send_keys("{ENTER}")
        time.sleep(0.4)
    elif op == "fire":
        g = capture.find("AssaultCube")
        capture.front(g)
        x, y, w, h = capture.rect(g)
        p = (x + w // 2, y + h // 2 - 100)
        for _ in range(int(a[0])):
            mouse.press(coords=p)
            time.sleep(0.05)
            mouse.release(coords=p)
            time.sleep(float(a[1]) if len(a) > 1 else 0.9)
    elif op == "lua":
        print("lua:", lua(" ".join(a)))
    elif op == "waitscan":
        last, same, t0 = None, 0, time.time()
        time.sleep(0.4)
        while time.time() - t0 < 90 and same < 3:
            r = lua("local f=getMainForm() return f.foundcountlabel.Caption..'/'..tostring(f.btnNewScan.Enabled)")
            same = same + 1 if (r == last and r.endswith("true")) else 0
            last = r
            time.sleep(0.2)
        print("found:", last)
    elif op == "found":
        print("found:", found())
    elif op == "info":
        for n in CONTROLS:
            print(n, lua(f"local c=getMainForm().{n} local x,y=c.clientToScreen(0,0) return string.format('%d %d %d %d %s',x,y,c.Width,c.Height,tostring(c.Visible))"))
        print("ce window", capture.rect(ce_hwnd()))
    elif op == "shot":
        t = " ".join(a[1:])
        h = ce_hwnd() if t == "ce" else capture.find({"game": "AssaultCube", "con": "Scan Me"}.get(t, t))
        capture.grab(*capture.rect(h), os.path.join(RAW, a[0] + ".png"))
    elif op == "area":
        capture.grab(*map(int, a[1:5]), os.path.join(RAW, a[0] + ".png"))
    else:
        sys.exit(f"unknown action {op}")


def run(script):
    for line in script.split(";;"):
        if line.strip():
            act(line)


def take(name, x, y, w, h, script):
    out = os.path.join(RAW, name + ".mp4")
    rec = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "gdigrab", "-framerate", "30", "-offset_x", str(x), "-offset_y", str(y),
                            "-video_size", f"{w // 2 * 2}x{h // 2 * 2}", "-i", "desktop", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
                            "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    time.sleep(1.5)
    t0 = time.time()
    try:
        run(script)
    finally:
        print(f"{name}: actions took {time.time() - t0:.1f}s")
        try:
            rec.communicate(b"q", timeout=20)
        except Exception:
            rec.kill()
    print(out)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        run(sys.argv[2])
    elif sys.argv[1] == "take":
        take(sys.argv[2], *map(int, sys.argv[3:7]), sys.argv[7])
