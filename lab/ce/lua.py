"""Run a Lua FILE inside the lab Cheat Engine (same channel as ce.py, longer wait): python lua.py script.lua [seconds]"""
import os
import sys
import time

d = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(d, "cmd.lua.out")
if os.path.exists(out):
    os.remove(out)
src = open(sys.argv[1], encoding="utf-8").read()
open(os.path.join(d, "cmd.tmp"), "w", encoding="utf-8").write(src)
os.replace(os.path.join(d, "cmd.tmp"), os.path.join(d, "cmd.lua"))
wait = float(sys.argv[2]) if len(sys.argv) > 2 else 15
t0 = time.time()
while time.time() - t0 < wait:
    time.sleep(0.25)
    if os.path.exists(out):
        time.sleep(0.1)
        print(open(out).read())
        break
else:
    print("no answer")
