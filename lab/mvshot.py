"""Point Cheat Engine's Memory Viewer disassembler at an address and screenshot the window.
    python mvshot.py <top hex> <selected hex> <name>        -> lab/shots/<name>.png
"""
import os
import subprocess
import sys
import time

d = os.path.dirname(os.path.abspath(__file__))
top, sel, name = sys.argv[1:4]
lua = f"local m=getMemoryViewForm() m.show() m.DisassemblerView.SelectedAddress=0x{sel} m.DisassemblerView.TopAddress=0x{top} return 1"
print(subprocess.run([sys.executable, os.path.join(d, "ce", "ce.py"), lua], capture_output=True, text=True).stdout.strip())
time.sleep(0.6)
subprocess.run([sys.executable, os.path.join(d, "gshot.py"), "Memory Viewer", name])
