"""Episode 7 capture helpers (code changes: NOP, Auto Assemble scripts, shared code, structure dissect).

Thin layer over ep06_cap.py (same Lua command channel, same mouse and keyboard helpers); raw captures go to lab/shots/ep07.

    python ep07_cap.py lua "<lua code>"            # run Lua in the lab Cheat Engine, print the answer
    python ep07_cap.py luaf file.lua               # the same from a file
    python ep07_cap.py forms | comps "<form>" | menu "<form>"
    python ep07_cap.py shot "<window title part>" name [--front]
    python ep07_cap.py game [bots]                 # start the practice game from lab/ep07_run_ac.sh, close its menu, place it
    python ep07_cap.py ce                          # start Cheat Engine with lab/ce/ep07.CT, place it, attach to the game
    python ep07_cap.py truth                       # player, magazine, health read straight from the game
    python ep07_cap.py bytes                       # the bytes at ac_client.exe+C73EC..C73FF right now
    python ep07_cap.py restore                     # write the original bytes back at +C73EF (safety net)
    python ep07_cap.py stop                        # close the game and Cheat Engine

Hold the screen lock (lab/lock.py acquire screen ep07) while this runs.
"""
import ctypes
import os
import struct
import subprocess
import sys
import time

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import ep06_cap as e  # noqa: E402
import win32con  # noqa: E402
import win32gui  # noqa: E402

e.RAW = os.path.join(D, "shots", "ep07")
os.makedirs(e.RAW, exist_ok=True)
CEX = 1600
ORIG = "FF 08 8D 44 24 1C"      # filled in from the live process in the first session (see lab/README.md)


def proc():
    k = ctypes.windll.kernel32
    pid = int(subprocess.check_output('tasklist /FI "IMAGENAME eq ac_client.exe" /FO CSV /NH', shell=True).decode().split(",")[1].strip('"'))
    return k, k.OpenProcess(0x0410, False, pid)


def rd(a, n):
    k, h = proc()
    b = ctypes.create_string_buffer(n)
    k.ReadProcessMemory(h, ctypes.c_void_p(a), b, n, None)
    k.CloseHandle(h)
    return b.raw


def u32(a):
    return struct.unpack("<I", rd(a, 4))[0]


def truth():
    p = u32(0x400000 + 0x17E0A8)
    return {"player": "%08X" % p, "mag_addr": "%08X" % (p + 0x140), "mag": u32(p + 0x140), "health": u32(p + 0xEC),
            "reserve": u32(p + 0x11C), "code": rd(0x4C73EC, 20).hex(" ").upper()}


def game(bots=None):
    subprocess.run(["taskkill", "/F", "/IM", "ac_client.exe"], capture_output=True)
    time.sleep(1.5)
    args = [r"C:\Program Files\Git\bin\bash.exe", os.path.join(D, "ep07_run_ac.sh")] + (str(bots).split() if bots else [])
    subprocess.Popen(args)
    for _ in range(40):
        time.sleep(0.5)
        if any("AssaultCube" in t for _, t in e.capture.windows()):
            break
    time.sleep(8)
    g = e.hwnd("game")
    e.capture.front(g)
    e.keys("{ESC}")
    time.sleep(0.8)
    win32gui.MoveWindow(g, -9, 0, 1602, 940, True)
    time.sleep(0.5)
    print("game", e.capture.rect(g), truth())


def yes_prompt():
    for _ in range(60):
        time.sleep(0.5)
        hits = [h for h, t in e.capture.windows() if "Execute this lua script" in t]
        if hits:
            break
    else:
        sys.exit("no Lua prompt")
    kids = []
    win32gui.EnumChildWindows(hits[0], lambda h, _: kids.append(h) or True, None)
    for k in kids:
        if win32gui.GetWindowText(k).replace("&", "") == "Yes":
            win32gui.PostMessage(k, win32con.BM_CLICK, 0, 0)
            return
    sys.exit("no Yes button")


def ce(table=None):
    env = dict(os.environ, __COMPAT_LAYER="RunAsInvoker")
    subprocess.Popen([r"C:\Program Files\Cheat Engine\cheatengine-x86_64.exe", table or os.path.join(D, "ce", "ep07.CT")], env=env)
    yes_prompt()
    time.sleep(2.5)
    e.prelude()
    print(e.lua(f"local f=getMainForm() f.Left={CEX} f.Top=0 f.Width=940 f.Height=1000 return 1"))
    print(e.lua("openProcess('ac_client.exe') return getOpenedProcessID()"))
    time.sleep(1)
    print("ce", e.capture.rect(e.hwnd("ce")))


def restore():
    print(e.lua("writeBytes(0x004C73EF, 0xFF, 0x08, 0x8D, 0x44, 0x24, 0x1C) return 1"))
    print(truth()["code"])


def stop():
    try:
        e.lua("closeCE() return 1", 3)
    except Exception:
        pass
    time.sleep(1)
    for exe in ("ac_client.exe", "cheatengine-x86_64.exe"):
        subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True)
    print("stopped")


def popup_shot(name):
    """Screenshot every visible popup menu (class #32768). Returns their rectangles."""
    pops = []
    win32gui.EnumWindows(lambda h, _: pops.append(h) if win32gui.GetClassName(h) == "#32768" and win32gui.IsWindowVisible(h) else True, None)
    out = []
    for i, p in enumerate(pops):
        r = win32gui.GetWindowRect(p)
        out.append(r)
        e.area(name + (str(i) if i else ""), r[0], r[1], r[2] - r[0], r[3] - r[1])
    return out


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "lua":
        print(e.lua(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 20))
    elif c == "luaf":
        print(e.lua(open(sys.argv[2], encoding="utf-8").read(), float(sys.argv[3]) if len(sys.argv) > 3 else 20))
    elif c == "forms":
        e.prelude()
        print(e.forms())
    elif c == "comps":
        e.prelude()
        print(e.comps(sys.argv[2]))
    elif c == "menu":
        e.prelude()
        print(e.val(f"""local f=E6F([[{sys.argv[2]}]]) local s='' for j=0,f.ComponentCount-1 do local c=f.Component[j]
          if c.ClassName=='TMenuItem' then s=s..c.Name..' = '..tostring(c.Caption)..'\\n' end end return s"""))
    elif c == "shot":
        print(e.shot(sys.argv[3], sys.argv[2], "--front" in sys.argv))
    elif c == "game":
        game(sys.argv[2] if len(sys.argv) > 2 else None)
    elif c == "ce":
        ce()
    elif c == "truth":
        print(truth())
    elif c == "bytes":
        print(truth()["code"])
    elif c == "restore":
        restore()
    elif c == "stop":
        stop()


def btn(title, text="OK"):
    """Press a button of a dialog by posting BM_CLICK (works when the game holds the mouse or the focus is elsewhere)."""
    h = e.capture.find(title)
    kids = []
    win32gui.EnumChildWindows(h, lambda k, _: kids.append(k) or True, None)
    for k in kids:
        if win32gui.GetWindowText(k).replace("&", "") == text:
            win32gui.PostMessage(k, win32con.BM_CLICK, 0, 0)
            return True
    return False
