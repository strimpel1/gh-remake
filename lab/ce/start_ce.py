"""Open a table in Cheat Engine without elevation and accept its Lua prompt: python start_ce.py ep01.CT"""
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "videos", "tools"))
import capture  # noqa: E402
from pywinauto import mouse  # noqa: E402

env = dict(os.environ, __COMPAT_LAYER="RunAsInvoker")
subprocess.Popen([r"C:\Program Files\Cheat Engine\cheatengine-x86_64.exe", os.path.abspath(sys.argv[1])], env=env)
for _ in range(40):
    time.sleep(0.5)
    if any("Execute this lua script" in t for _, t in capture.windows()):
        break
h = capture.find("Execute this lua script")
capture.front(h)
x, y, w, hh = capture.rect(h)
mouse.click(coords=(x + int(w * 0.42), y + int(hh * 0.88)))
time.sleep(2)
