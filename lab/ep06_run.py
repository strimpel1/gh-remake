"""Episode 6 capture session, in stages (each stage prints what it found; look at the shots between stages).

    python ep06_run.py game            # start (or restart) the practice game, close its menu, put it at the top left
    python ep06_run.py ce [table]      # start Cheat Engine with lab/ce/ep06.CT (or another table), lay out its window, attach
    python ep06_run.py <stage>         # s1 menu writes hex1 pick access hex2 addptr proof psdlg psrun table hotkey hkclip save rescan loaded
    python ep06_run.py stop            # close the game and Cheat Engine

Everything it drives is Cheat Engine's own window, attached to our own offline AssaultCube process.
Hold the screen lock (lab/lock.py acquire screen ep06) while this runs.
"""
import ctypes
import json
import os
import struct
import subprocess
import sys
import time
from ctypes import wintypes

import ep06_cap as e
import win32con
import win32gui

D = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(e.RAW, "state.json")
CEX = 1600            # Cheat Engine's main window: left edge (the game is 1585 wide at the left)
SAVED = os.path.join(D, "ce", "ep06_assaultcube.CT")
PTR = os.path.join(D, "ptr")


def st(**kw):
    d = json.load(open(STATE)) if os.path.exists(STATE) else {}
    if kw:
        d.update(kw)
        json.dump(d, open(STATE, "w"), indent=1)
    return d


def truth():
    """(player, magazine address, magazine, health) read straight from the game."""
    k = ctypes.windll.kernel32
    pid = int(subprocess.check_output('tasklist /FI "IMAGENAME eq ac_client.exe" /FO CSV /NH', shell=True).decode().split(",")[1].strip('"'))
    h = k.OpenProcess(0x0410, False, pid)

    def u32(a):
        b = ctypes.create_string_buffer(4)
        k.ReadProcessMemory(h, ctypes.c_void_p(a), b, 4, None)
        return struct.unpack("<I", b.raw)[0]
    p = u32(0x400000 + 0x17E0A8)
    w = u32(p + 0x364)
    return {"player": "%08X" % p, "weapon": "%08X" % w, "weapon_slot": "%08X" % (p + 0x364), "ammo_addr": "%08X" % (p + 0x140),
            "ammo_via_weapon": "%08X" % u32(w + 0x14), "mag": u32(p + 0x140), "health": u32(p + 0xEC), "health_addr": "%08X" % (p + 0xEC)}


def game():
    subprocess.run(["taskkill", "/F", "/IM", "ac_client.exe"], capture_output=True)
    time.sleep(1.5)
    subprocess.Popen([r"C:\Program Files\Git\bin\bash.exe", os.path.join(D, "run_ac.sh")])
    for _ in range(40):
        time.sleep(0.5)
        if any("AssaultCube" in t for _, t in e.capture.windows()):
            break
    time.sleep(7)
    g = e.hwnd("game")
    e.capture.front(g)
    e.keys("{ESC}")
    time.sleep(0.8)
    win32gui.MoveWindow(g, -9, 0, 1602, 940, True)
    time.sleep(0.5)
    print("game", e.capture.rect(g), truth())


def yes_prompt():
    for _ in range(60):
        time.sleep(0.5)
        hits = [h for h, t in e.capture.windows() if "Execute this lua script" in t]
        if hits:
            break
    else:
        sys.exit("no Lua prompt")
    kids = []
    win32gui.EnumChildWindows(hits[0], lambda h, _: kids.append(h) or True, None)
    for k in kids:
        if win32gui.GetWindowText(k).replace("&", "") == "Yes":
            win32gui.PostMessage(k, win32con.BM_CLICK, 0, 0)
            return
    sys.exit("no Yes button")


def layout():
    e.prelude()
    print(e.lua(f"local f=getMainForm() f.Left={CEX} f.Top=0 f.Width=940 f.Height=1000 f.Foundlist3.Columns[0].Width=210 return 1"))


def ce(table=None):
    env = dict(os.environ, __COMPAT_LAYER="RunAsInvoker")
    subprocess.Popen([r"C:\Program Files\Cheat Engine\cheatengine-x86_64.exe", table or os.path.join(D, "ce", "ep06.CT")], env=env)
    yes_prompt()
    time.sleep(2.5)
    layout()
    print(e.lua("openProcess('ac_client.exe') return getOpenedProcessID()"))
    time.sleep(1)
    print("ce", e.capture.rect(e.hwnd("ce")))


def attach():
    e.prelude()
    print(e.lua("openProcess('ac_client.exe') return getOpenedProcessID()"))
    time.sleep(1.5)


def both(name):
    """Screenshots of the game and of Cheat Engine's main window, a moment apart."""
    e.shot(name + "_ce", "ce")
    e.shot(name + "_game", "game")


def list_row(i):
    """Screen position of row i of the address list (the tree under the scan area)."""
    x, y, w, h = [int(v) for v in e.val("return E6R(getAddressList())").split()]
    return x + 330, y + 24 + 12 + 24 * i


def s1():
    """Run 1: one row, the magazine's address in this run (what a scan like episode 5's ends with)."""
    t = truth()
    st(run1=t)
    print(e.lua(f"""local al=getAddressList() local mr=al.createMemoryRecord() mr.Description='ammo (from the scan)' mr.Address='{t["ammo_addr"]}'
      mr.Type=vtDword return mr.Address"""))
    time.sleep(1)
    both("a0")


def menu():
    """The real right-click menu of the row."""
    e.front("ce")
    x, y = list_row(0)
    e.click(x, y, button="right")
    time.sleep(0.6)
    pops = []
    win32gui.EnumWindows(lambda h, _: pops.append(h) if win32gui.GetClassName(h) == "#32768" and win32gui.IsWindowVisible(h) else True, None)
    for p in pops:
        r = win32gui.GetWindowRect(p)
        print("popup", r)
        e.area("a_menu", r[0], r[1], r[2] - r[0], r[3] - r[1])
    e.shot("a_menu_ce", "ce")
    e.keys("{ESC}")


def found_window(kind, name, rec_fire=0, pick=None, row=0):
    """Open "Find out what writes to / accesses this address" on address-list row `row`, optionally fire while recording,
    select one instruction, screenshot the window and its More information dialog. Returns the details text."""
    item = {"writes": "Setbreakpoint1", "accesses": "Findoutwhataccessesthisaddress1"}[kind]
    print(e.lua(f"""local al=getAddressList() al.SelectedRecord=al[{row}] if not debug_isDebugging() then debugProcess() end
      createTimer(400,function() getMainForm().{item}.doClick() end) return 1"""))
    time.sleep(2.0)
    print(e.lua(f"local d=E6F('opcodes') d.Left={CEX} d.Top=30 return d.Caption"))
    time.sleep(0.5)
    e.shot(name + "_empty", "opcodes", True)
    if rec_fire:
        with e.Rec(name + "_fire", 0, 0, 2540, 940):
            e.fire(1, 1.2)              # the first click only gives the game the mouse
            e.fire(rec_fire, 1.4)
            time.sleep(1.0)
    else:
        time.sleep(2.5)
    n = int(e.val("return E6F('opcodes').FoundCodeList.Items.Count"))
    rows = e.val("""local l=E6F('opcodes').FoundCodeList local s='' for i=0,l.Items.Count-1 do s=s..i..' | '..l.Items[i].Caption..' | '..l.Items[i].SubItems[0]..'\\n' end return s""")
    print(n, "rows\n" + rows)
    i = 0
    if pick:
        for ln in rows.splitlines():
            if pick in ln:
                i = int(ln.split(" | ")[0])
                break
    # a real click on the row, so the details pane fills in the way it does for the viewer
    x, y, w, h = e.crect("opcodes", "FoundCodeList")
    e.front("opcodes")
    e.click(x + 300, y + 24 + 12 + 24 * i)
    time.sleep(0.8)
    e.shot(name, "opcodes")
    info = e.val("return E6F('opcodes').mInfo.Lines.Text")
    open(os.path.join(e.RAW, name + ".txt"), "w").write(rows + "\n" + info)
    print(info)
    e.cclick("opcodes", "btnExtraInfo")
    time.sleep(1.0)
    print(e.lua("local d=E6F('Extra info') d.Left=980 d.Top=120 return 1"))
    time.sleep(0.5)
    e.shot(name + "_extra", "Extra info", True)
    print(e.lua("E6F('Extra info').close() return 1"))
    time.sleep(0.3)
    e.cclick("opcodes", "btnOK")          # Stop
    time.sleep(0.6)
    e.shot(name + "_stopped", "opcodes")
    e.cclick("opcodes", "btnOK")          # Close
    time.sleep(0.5)
    return info


def reg(info, r):
    for ln in info.splitlines():
        if ln.startswith(r + "="):
            return ln.split("=")[1].strip()


def writes():
    info = found_window("writes", "a_w", rec_fire=3)
    st(esi=reg(info, "ESI"), truth_after_fire=truth())
    print("ESI", reg(info, "ESI"), truth())


def hexscan(value, name):
    e.front("ce")
    if "New" in e.val("return getMainForm().btnNewScan.Caption"):
        e.cclick("main", "btnNewScan")
        time.sleep(0.6)
    if e.val("return tostring(getMainForm().cbHexadecimal.Checked)") != "true":
        e.cclick("main", "cbHexadecimal", 10, 12)
    e.cclick("main", "scanvalue")
    e.keys("^a")
    e.keys(value, 0.07)
    e.shot(name + "_typed", "ce")
    e.cclick("main", "btnNewScan")
    time.sleep(3.5)
    rows = e.val("""local l=getMainForm().Foundlist3 local s='' for i=0,math.min(l.Items.Count,120)-1 do s=s..i..' '..l.Items[i].Caption..'\\n' end return s""")
    print("found", e.val("return getMainForm().foundcountlabel.Caption"))
    print(rows)
    open(os.path.join(e.RAW, name + ".txt"), "w").write(rows)
    e.cclick("main", "foundcountlabel")          # park the mouse away from the list
    e.shot(name, "ce")
    return rows


def hex1():
    hexscan(st()["esi"], "a_hex1")


def pick():
    """Double-click the result that is the player's current-weapon slot, so it lands in the address list."""
    rows = open(os.path.join(e.RAW, "a_hex1.txt")).read().splitlines()
    slot = truth()["weapon_slot"]
    i = [int(r.split()[0]) for r in rows if r.split()[1].upper() == slot][0]
    x, y, w, h = e.crect("main", "Foundlist3")
    print("row", i, slot)
    e.click(x + 60, y + 24 + 10 + 21 * i)
    time.sleep(0.4)
    e.shot("a_hex1_sel", "ce")
    e.click(x + 60, y + 24 + 10 + 21 * i, double=True)
    time.sleep(0.6)
    print(e.lua("local al=getAddressList() local s='' for i=0,al.Count-1 do s=s..al[i].Description..' '..al[i].Address..' | ' end return s"))
    print(e.lua("local al=getAddressList() al[1].Description='holds the weapon address' return 1"))
    time.sleep(0.5)
    e.shot("a_hex1_added", "ce")


def access():
    info = found_window("accesses", "a_a", pick="[esi+00000364]", row=1)
    st(access_info=info)
    print(truth())


def hex2():
    t = truth()
    rows = hexscan(t["player"], "a_hex2")
    i = [int(r.split()[0]) for r in rows.splitlines() if "17E0A8" in r]
    print("green row", i)
    if i and i[0] > 15:
        print(e.lua(f"local l=getMainForm().Foundlist3 l.Items[{min(i[0] + 8, len(rows.splitlines()) - 1)}].makeVisible(false) return 1"))
        time.sleep(0.5)
        e.shot("a_hex2", "ce")


def addptr():
    e.front("ce")
    e.cclick("main", "btnAddAddressManually")
    time.sleep(1.0)
    print(e.lua("local d=E6F('Add address') d.Left=960 d.Top=260 d.Width=600 return 1"))
    time.sleep(0.5)
    x, y, w, h = e.capture.rect(e.hwnd("Add address"))
    e.front("Add address")
    e.click(x + 200, y + 122)
    e.keys("^a")
    e.keys("ammo (pointer)", 0.04)
    e.cclick("Add address", "cbPointer", 10, 12)
    time.sleep(0.5)
    e.shot("a_ptr1", "Add address")
    e.click(x + 200, y + 298)
    e.keys('"ac_client.exe"{+}17E0A8', 0.04)
    e.shot("a_ptr2", "Add address")
    e.click(x + 75, y + 331)
    e.click(x + 75, y + 331 + 30)
    time.sleep(0.4)
    for row, off in ((326, "364"), (296, "14"), (266, "0")):
        e.click(x + 190, y + row)
        e.keys("^a")
        e.keys(off, 0.08)
        time.sleep(0.4)
        e.shot("a_ptr_" + off, "Add address")
    e.click(x + 200, y + 74)           # leave the offset boxes so the last one is applied
    time.sleep(0.8)
    e.shot("a_ptr3", "Add address")
    e.cclick("Add address", "btnOk")
    time.sleep(0.8)
    print(e.lua("local al=getAddressList() local s='' for i=0,al.Count-1 do s=s..al[i].Description..' '..al[i].Address..' '..tostring(al[i].Value)..' | ' end return s"))
    print(e.lua("local al=getAddressList() al[1].destroy() return al.Count"))     # the helper row is not part of the table
    e.cclick("main", "foundcountlabel")
    time.sleep(0.6)
    both("a1")
    print(truth())


def proof():
    """After a restart of the game: the plain address is dead, the pointer row follows the new player."""
    attach()
    t = truth()
    st(run2=t)
    time.sleep(1.0)
    both("b0")
    print(t, e.lua("local al=getAddressList() local s='' for i=0,al.Count-1 do s=s..al[i].Description..' '..al[i].CurrentAddress..' '..tostring(al[i].Value)..' | ' end return s"))


def psdlg(row=1, level="5"):
    print(e.lua(f"local al=getAddressList() al.SelectedRecord=al[{row}] createTimer(400,function() getMainForm().Pointerscanforthisaddress1.doClick() end) return 1"))
    time.sleep(2.5)
    print(e.forms())
    F = "Pointerscanner scanoptions"
    print(e.lua(f"local s=E6F('{F}') s.Left=300 s.Top=200 return 1"))
    time.sleep(0.4)
    e.front(F)
    x, y, w, h = e.crect(F, "editMaxLevel")
    e.click(x + w // 2, y + h // 2, double=True)
    e.keys("^a" + level)
    e.cclick(F, "Label12")
    e.shot("b_psdlg", F)


def filename(path):
    for _ in range(20):
        time.sleep(0.5)
        if any("Specify the filename" in t or "Save" in t for _, t in e.capture.windows()):
            break
    time.sleep(1.5)
    h = [h for h, t in e.capture.windows() if "Specify the filename" in t or t.startswith("Save")][0]
    e.capture.front(h)
    time.sleep(0.8)
    e.keys("^a")
    e.keys(path, 0.02)
    time.sleep(0.6)
    e.keys("{ENTER}")
    time.sleep(1.0)
    if any("Confirm" in t for _, t in e.capture.windows()):
        e.keys("y")


def ps_wait(name):
    t0 = time.time()
    while time.time() - t0 < 240:
        time.sleep(2)
        r = e.lua("local p=E6F('Tfrmpointerscanner') return p.Caption..' | '..p.Panel1.Caption")
        if "paths" in r:
            break
    print(round(time.time() - t0), r)
    print(e.lua("""local p=E6F('Tfrmpointerscanner') p.Left=100 p.Top=60 p.Width=1200 p.Height=640
      p.lvResults.Columns[0].Width=330 return p.lvResults.Columns.Count"""))
    time.sleep(1.0)
    e.shot(name, "Pointer scan :", True)
    return r


def psrun():
    os.makedirs(PTR, exist_ok=True)
    for f in os.listdir(PTR):
        os.remove(os.path.join(PTR, f))
    e.cclick("Pointerscanner scanoptions", "btnOk")
    filename(os.path.join(PTR, "ep06_ammo.PTR"))
    st(ps=ps_wait("b_psres"))


def table():
    """Run 2: the tidy table: a header, the two ammo pointers and the health next to them."""
    print(e.lua("""local al=getAddressList()
      al[0].Description='ammo: plain address from run 1'
      al[1].Description='ammo (through the weapon)'
      local h=al.createMemoryRecord() h.Description='Player' h.IsGroupHeader=true h.Options='[moAllowManualCollapseAndExpand]'
      local function ptr(name, off)
        local m=al.createMemoryRecord() m.Description=name m.Type=vtDword m.Address='"ac_client.exe"+17E0A8' m.OffsetCount=1 m.Offset[0]=off
        m.appendToEntry(h) return m
      end
      E6AMMO=ptr('ammo', 0x140) ptr('health', 0xEC) ptr('reserve ammo', 0x11C)
      al[1].appendToEntry(h)
      return al.Count"""))
    time.sleep(1.0)
    e.cclick("main", "foundcountlabel")
    both("b_table")
    print(e.lua("local al=getAddressList() local s='' for i=0,al.Count-1 do s=s..al[i].Description..' '..al[i].CurrentAddress..' '..tostring(al[i].Value)..' | ' end return s"))


def hotkey():
    print(e.lua("local al=getAddressList() al.SelectedRecord=E6AMMO or al.getMemoryRecordByDescription('ammo') createTimer(400,function() getMainForm().SetHotkey1.doClick() end) return 1"))
    time.sleep(1.5)
    F = "Set/Change hotkey"
    print(e.lua(f"local d=E6F('{F}') d.Left=700 d.Top=200 return d.Caption"))
    time.sleep(0.4)
    e.front(F)
    e.shot("b_hk0", F)
    e.cclick(F, "btnCreateHotkey")
    time.sleep(0.5)
    e.cclick(F, "cbFreezedirection")
    time.sleep(0.6)
    e.keys("{HOME}{DOWN 5}", 0.1)
    time.sleep(0.4)
    x, y, w, h = e.capture.rect(e.hwnd(F))
    e.area("b_hk_drop", x, y, w, h + 120)
    e.keys("{ENTER}")
    e.cclick(F, "edtFreezeValue")
    e.keys("20", 0.1)
    e.cclick(F, "Button2")               # Clear
    e.cclick(F, "edtHotkey")
    time.sleep(0.3)
    e.keys("{VK_NUMPAD1}")
    time.sleep(0.4)
    e.shot("b_hk1", F)
    e.cclick(F, "btnApply")
    time.sleep(0.5)
    e.shot("b_hk2", F)
    print(e.lua(f"local l=E6F('{F}').ListView1 return l.Items[0].Caption..' | '..l.Items[0].SubItems[0]..' | '..l.Items[0].SubItems[1]"))
    e.cclick(F, "btnOK")
    time.sleep(0.5)


def hkclip(name="b_hk"):
    """Fire a few rounds, press the hotkey: the game's counter jumps back to 20. Game and Cheat Engine in one recording."""
    e.cclick("main", "foundcountlabel")
    e.front("game")
    time.sleep(0.6)
    with e.Rec(name + "_clip", 0, 0, 2552, 1066):
        e.fire(1, 1.0)
        e.fire(4, 1.1)
        print("before", truth()["mag"])
        time.sleep(1.2)
        u = ctypes.windll.user32          # held for a moment: Cheat Engine polls the keyboard for its hotkeys
        u.keybd_event(0x61, 0x4F, 0, 0)
        time.sleep(0.4)
        u.keybd_event(0x61, 0x4F, 2, 0)
        time.sleep(2.0)
        print("after", truth()["mag"])
        e.fire(2, 1.1)
        time.sleep(1.0)
    print(truth())


def save():
    print(e.lua(f"saveTable([[{SAVED}]]) return 1"))
    time.sleep(0.5)
    print(os.path.getsize(SAVED))


def rescan():
    """Run 3: filter the pointer scan with the magazine's new address."""
    attach()
    t = truth()
    st(run3=t)
    time.sleep(1)
    both("c0")
    e.front("Pointer scan :")
    print(e.lua("createTimer(400,function() E6F('Tfrmpointerscanner').Rescanmemory1.doClick() end) return 1"))
    time.sleep(2.0)
    print(e.forms())


def loaded():
    """Run 3: Cheat Engine closed and started again with the saved table."""
    e.lua("closeCE() return 1", 3)
    time.sleep(2)
    subprocess.run(["taskkill", "/F", "/IM", "cheatengine-x86_64.exe"], capture_output=True)
    time.sleep(1)
    ce(SAVED)
    time.sleep(1.5)
    e.cclick("main", "foundcountlabel")
    both("c_loaded")
    print(truth(), e.lua("local al=getAddressList() local s='' for i=0,al.Count-1 do s=s..al[i].Description..' '..al[i].CurrentAddress..' '..tostring(al[i].Value)..' | ' end return s"))


def stop():
    e.lua("closeCE() return 1", 3)
    time.sleep(1)
    for exe in ("ac_client.exe", "cheatengine-x86_64.exe"):
        subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True)
    print("stopped")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        if a.endswith(".CT"):
            continue
        if a == "ce":
            ce(next((x for x in sys.argv if x.endswith(".CT")), None))
        else:
            e.prelude() if a not in ("game", "stop") else None
            globals()[a]()
