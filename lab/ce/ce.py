"""Run Lua inside the lab Cheat Engine (the table polls lab/ce/cmd.lua): python ce.py "<lua>" """
import os, sys, time
d = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(d, "cmd.lua.out")
if os.path.exists(out): os.remove(out)
open(os.path.join(d, "cmd.tmp"), "w").write(sys.argv[1]); os.replace(os.path.join(d, "cmd.tmp"), os.path.join(d, "cmd.lua"))
for _ in range(40):
    time.sleep(0.25)
    if os.path.exists(out): print(open(out).read()); break
else: print("no answer")
