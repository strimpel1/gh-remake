"""Drive any window by title: clicks at window-relative pixels, key presses, then an optional screenshot.

    python win.py "ImHex" click 1490 856            # left click at (x, y) inside the window's visible frame
    python win.py "ImHex" keys "0F27" 0.15          # pywinauto send_keys syntax, optional pause per key
    python win.py "ImHex" shot out.png              # same as capture.py shot
Several actions can be chained:  python win.py "ImHex" click 400 300 keys "^s" shot out.png
"""
import sys
import time

sys.path.insert(0, r"D:\AI\gh-remake\videos\tools")
import capture  # noqa: E402
from pywinauto import mouse  # noqa: E402
from pywinauto.keyboard import send_keys  # noqa: E402

h = capture.find(sys.argv[1])
capture.front(h)
a = sys.argv[2:]
while a:
    cmd = a.pop(0)
    if cmd in ("click", "dclick", "rclick"):
        x, y = int(a.pop(0)), int(a.pop(0))
        wx, wy, _, _ = capture.rect(h)
        pos = (wx + x, wy + y)
        mouse.move(coords=pos)
        time.sleep(0.15)
        if cmd == "click":
            mouse.click(coords=pos)
        elif cmd == "dclick":
            mouse.double_click(coords=pos)
        else:
            mouse.right_click(coords=pos)
        time.sleep(0.6)
    elif cmd == "keys":
        k = a.pop(0)
        pause = 0.08
        if a and a[0].replace(".", "").isdigit():
            pause = float(a.pop(0))
        send_keys(k, pause=pause, with_spaces=True)
        time.sleep(0.5)
    elif cmd == "move":
        x, y = int(a.pop(0)), int(a.pop(0))
        wx, wy, _, _ = capture.rect(h)
        mouse.move(coords=(wx + x, wy + y))
        time.sleep(0.3)
    elif cmd == "sleep":
        time.sleep(float(a.pop(0)))
    elif cmd == "shot":
        capture.grab(*capture.rect(h), a.pop(0))
