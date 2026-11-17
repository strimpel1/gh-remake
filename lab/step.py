"""Single-step the game while it is stopped in Cheat Engine's debugger, then screenshot the Memory Viewer and print the stack.
    python step.py over|into <name>
"""
import os
import subprocess
import sys
import time

d = os.path.dirname(os.path.abspath(__file__))
how = {"over": "miDebugStepOver", "into": "miDebugStep", "run": "miDebugRun"}[sys.argv[1]]
run = lambda *a: print(subprocess.run([sys.executable, *a], capture_output=True, text=True).stdout.strip())
run(os.path.join(d, "ce", "ce.py"), f"getMemoryViewForm().{how}.doClick() return 1")
time.sleep(1.0)
run(os.path.join(d, "ce", "lua.py"), os.path.join(d, "ce", "ep03_stack.lua"))
run(os.path.join(d, "gshot.py"), "Memory Viewer", sys.argv[2], "--nofront")
