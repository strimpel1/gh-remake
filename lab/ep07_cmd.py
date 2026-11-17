"""Type a console command into the practice game with real scan codes (SDL2 ignores keys that carry no scan code):
    python ep07_cmd.py "mode 8; map ac_desert" [seconds to wait] [screenshot name]
The game's console line opens with "/". Do not send ESC first: that opens the main menu.
"""
import ctypes
import sys
import time

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
import ep07_cap as c  # noqa: E402

u = ctypes.windll.user32


def tap(vk, shift=False, hold=0.06):
    sc = u.MapVirtualKeyW(vk, 0)
    if shift:
        u.keybd_event(0x10, 0x2A, 0, 0)
        time.sleep(0.02)
    u.keybd_event(vk, sc, 0, 0)
    time.sleep(hold)
    u.keybd_event(vk, sc, 2, 0)
    if shift:
        time.sleep(0.02)
        u.keybd_event(0x10, 0x2A, 2, 0)
    time.sleep(0.03)


def text(s):
    for ch in s:
        r = u.VkKeyScanW(ord(ch))
        tap(r & 0xFF, bool(r & 0x100))


def cmd(s):
    c.e.front("game")
    time.sleep(0.3)
    text("/")
    time.sleep(0.5)
    text(s)
    time.sleep(0.3)
    tap(0x0D)


if __name__ == "__main__":
    cmd(sys.argv[1])
    time.sleep(float(sys.argv[2]) if len(sys.argv) > 2 else 1)
    if len(sys.argv) > 3:
        c.e.shot(sys.argv[3], "game")
