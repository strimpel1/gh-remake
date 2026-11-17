"""Screen capture for real-tool footage: window screenshots and short recordings.

    python capture.py list                          # visible windows: hwnd, size, title
    python capture.py shot  "AssaultCube" out.png   # screenshot of the first window whose title contains the text
    python capture.py rec   "AssaultCube" out.mp4 8 # record that window's area for 8 seconds (ffmpeg gdigrab, 30 fps)
    python capture.py place "AssaultCube" 0 0 1280 720   # move/resize a window
    python capture.py area  x y w h out.png         # screenshot of a screen rectangle

Windows are brought to the front first, because games draw with the GPU and can only be grabbed from the screen.
"""
import ctypes
import subprocess
import sys
import time
from ctypes import wintypes

import mss
import mss.tools
import win32con
import win32gui

ctypes.windll.shcore.SetProcessDpiAwareness(2)


def windows():
    out = []

    def cb(h, _):
        if win32gui.IsWindowVisible(h) and win32gui.GetWindowText(h):
            out.append((h, win32gui.GetWindowText(h)))

    win32gui.EnumWindows(cb, None)
    return out


def find(title):
    if title.isdigit():
        return int(title)
    hits = [h for h, t in windows() if title.lower() in t.lower()]
    if not hits:
        sys.exit(f'no window with "{title}" in its title')
    return hits[0]


def front(h):
    if win32gui.IsIconic(h):
        win32gui.ShowWindow(h, win32con.SW_RESTORE)
    ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)        # a tap on Alt lets SetForegroundWindow succeed
    ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)
    try:
        win32gui.SetForegroundWindow(h)
    except Exception:
        pass
    time.sleep(0.5)


def rect(h, client=False):
    if client:
        l, t, r, b = win32gui.GetClientRect(h)
        x, y = win32gui.ClientToScreen(h, (0, 0))
        return x, y, r - l, b - t
    r = wintypes.RECT()                                        # the visible frame, without the invisible resize border
    ctypes.windll.dwmapi.DwmGetWindowAttribute(h, 9, ctypes.byref(r), ctypes.sizeof(r))
    return r.left, r.top, r.right - r.left, r.bottom - r.top


def grab(x, y, w, h, out):
    with mss.mss() as s:
        img = s.grab({"left": x, "top": y, "width": w, "height": h})
        mss.tools.to_png(img.rgb, img.size, output=out)
    print(f"{out}  {w}x{h}")


if __name__ == "__main__":
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "list":
        for h, t in windows():
            print(h, rect(h)[2:], t.encode("ascii", "replace").decode())
    elif cmd == "shot":
        h = find(a[0])
        front(h)
        grab(*rect(h, client="--client" in a), a[1])
    elif cmd == "area":
        grab(*map(int, a[:4]), a[4])
    elif cmd == "place":
        h = find(a[0])
        front(h)
        win32gui.MoveWindow(h, *map(int, a[1:5]), True)
    elif cmd == "rec":
        h = find(a[0])
        front(h)
        x, y, w, hh = rect(h, client="--client" in a)
        w, hh = w // 2 * 2, hh // 2 * 2
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "gdigrab", "-framerate", "30", "-offset_x", str(x), "-offset_y", str(y),
                        "-video_size", f"{w}x{hh}", "-t", a[2], "-i", "desktop", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", a[1]],
                       check=True)
        print(f"{a[1]}  {w}x{hh}  {a[2]}s")
