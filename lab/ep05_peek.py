"""Episode 5: the true addresses of this run, to confirm what a scan found (our own offline AssaultCube process).
    python ep05_peek.py            # player, health, magazine, reserve addresses and values
"""
import ctypes
import struct
import subprocess
from ctypes import wintypes

k = ctypes.windll.kernel32
pid = int(subprocess.check_output('tasklist /FI "IMAGENAME eq ac_client.exe" /FO CSV /NH', shell=True).decode().split(",")[1].strip('"'))
h = k.OpenProcess(0x0410, False, pid)
mods = (wintypes.HMODULE * 256)()
need = wintypes.DWORD()
ctypes.windll.psapi.EnumProcessModulesEx(h, mods, ctypes.sizeof(mods), ctypes.byref(need), 3)
base = mods[0] & 0xFFFFFFFF


def rd(a, n):
    b = ctypes.create_string_buffer(n)
    k.ReadProcessMemory(h, ctypes.c_void_p(a), b, n, None)
    return b.raw


u32 = lambda a: struct.unpack("<I", rd(a, 4))[0]
p = u32(base + 0x17E0A8)
print("pid %d  base %08X  player %08X" % (pid, base, p))
for name, off in (("health", 0xEC), ("armor", 0xF0), ("magazine", 0x140), ("reserve", 0x11C)):
    print("%-9s %08X = %d" % (name, p + off, u32(p + off)))
