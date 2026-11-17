"""Episode 5: start the practice program scanme.exe in its own classic console window with a large font, at the top left.
    python ep05_con.py            # start it (conhost), font Consolas 30, window at 0,0
"""
import ctypes
import os
import subprocess
import sys
import time
from ctypes import wintypes

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, "..", "videos", "tools"))
import capture  # noqa: E402
import win32gui  # noqa: E402

EXE = os.path.join(D, "..", "videos", "ep05-your-first-memory-scan", "lab", "scanme.exe")


class FONT(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.ULONG), ("nFont", wintypes.DWORD), ("X", wintypes.SHORT), ("Y", wintypes.SHORT),
                ("FontFamily", wintypes.UINT), ("FontWeight", wintypes.UINT), ("FaceName", wintypes.WCHAR * 32)]


p = subprocess.Popen(["conhost.exe", os.path.abspath(EXE)])
time.sleep(2.0)
pid = int(subprocess.check_output('tasklist /FI "IMAGENAME eq scanme.exe" /FO CSV /NH', shell=True).decode().split(",")[1].strip('"'))
k = ctypes.windll.kernel32
k.FreeConsole()
if k.AttachConsole(pid):
    h = k.CreateFileW("CONOUT$", 0xC0000000, 3, None, 3, 0, None)
    f = FONT()
    f.cbSize = ctypes.sizeof(FONT)
    f.Y, f.FontFamily, f.FontWeight, f.FaceName = 30, 54, 400, "Consolas"
    print("font", k.SetCurrentConsoleFontEx(h, False, ctypes.byref(f)))
    k.FreeConsole()
time.sleep(0.5)
w = capture.find("Scan Me")
x, y, ww, hh = capture.rect(w)
win32gui.MoveWindow(w, 0, 0, ww + 14, hh + 7, True)
print("pid", pid, capture.rect(w))
