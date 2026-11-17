"""Read values from the practice game (our own offline AssaultCube process) to check the offsets used in the lessons."""
import ctypes, struct, subprocess, sys
from ctypes import wintypes
k = ctypes.windll.kernel32
pid = int(subprocess.check_output('tasklist /FI "IMAGENAME eq ac_client.exe" /FO CSV /NH', shell=True).decode().split(",")[1].strip('"'))
h = k.OpenProcess(0x0410, False, pid)
psapi = ctypes.windll.psapi
mods = (wintypes.HMODULE * 256)(); need = wintypes.DWORD()
psapi.EnumProcessModulesEx(h, mods, ctypes.sizeof(mods), ctypes.byref(need), 3)
base = mods[0] & 0xFFFFFFFF
def rd(a, n):
    b = ctypes.create_string_buffer(n); k.ReadProcessMemory(h, ctypes.c_void_p(a), b, n, None); return b.raw
u32 = lambda a: struct.unpack("<I", rd(a, 4))[0]
print("pid", pid, "base %08X" % base)
for off in (0x17E0A8, 0x18AC00, 0x195404, 0x109B74, 0x10F4F4):
    p = u32(base + off)
    try:
        print("base+%X -> %08X  health %d  mag %d  reserve %d  pos %s" % (off, p, u32(p + 0xEC), u32(p + 0x140), u32(p + 0x11C), struct.unpack("<3f", rd(p + 0x28, 12))))
    except Exception as e:
        print("base+%X -> %08X" % (off, p), e)
