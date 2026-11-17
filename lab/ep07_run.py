"""Episode 7 capture session, in stages (look at the shots between stages). Raw captures: lab/shots/ep07.

    python ep07_run.py setup            # game (no bots) + Cheat Engine, windows laid out, table row for the ammo
    python ep07_run.py <stage> ...      # nop1 nop2 nopclip rest1 rest2 restclip aa1 aa2 aa3 v1 assign jmp toggle v2 chg dis1 ...
    python ep07_cap.py stop

Everything it drives is Cheat Engine's own window, attached to our own offline AssaultCube process.
Hold the screen lock (lab/lock.py acquire screen ep07) while this runs.
"""
import json
import os
import sys
import time

import ep07_cap as c
import ep07_cmd as k
import win32gui

e = c.e
D = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(e.RAW, "state.json")
MVX, MVH = 1600, 520          # Memory Viewer: top right
CEY, CEH = 590, 700           # Cheat Engine's main window: under it
REC = (0, 0, 2552, 1360)      # the recorded rectangle: the game (left) and both Cheat Engine windows (right)
AAF = "TfrmAutoInject"

V1 = """[ENABLE]
alloc(newmem,2048)
label(returnhere)
label(originalcode)
label(exit)

newmem:
  // dec [eax] is not copied here

originalcode:
  lea eax,[esp+1C]

exit:
  jmp returnhere

ac_client.exe+C73EF:
  jmp newmem
  nop
returnhere:

[DISABLE]
dealloc(newmem)
ac_client.exe+C73EF:
  db FF 08 8D 44 24 1C
"""

V2 = V1.replace("""newmem:
  // dec [eax] is not copied here
""", """newmem:
  cmp edi,[ac_client.exe+17E0A8]
  je originalcode
  dec [eax]
""")


def st(**kw):
    d = json.load(open(STATE)) if os.path.exists(STATE) else {}
    if kw:
        d.update(kw)
        json.dump(d, open(STATE, "w"), indent=1)
    return d


def luaf(code, wait=20):
    r = e.lua(code, wait)
    print(r[:1500])
    return r


def mv(top, sel):
    luaf(f"local m=getMemoryViewForm() m.DisassemblerView.TopAddress=0x{top:X} m.DisassemblerView.SelectedAddress=0x{sel:X} return m.DisassemblerView.SelectedAddress")
    time.sleep(0.5)


def layout():
    e.prelude()
    luaf(f"""local f=getMainForm() f.Left={MVX} f.Top={CEY} f.Width=940 f.Height={CEH}
      local m=getMemoryViewForm() m.show() m.Left={MVX} m.Top=0 m.Width=940 m.Height={MVH}
      m.DisassemblerView.TopAddress=0x4C73DA m.DisassemblerView.SelectedAddress=0x4C73EF return 1""")


def setup(bots=None):
    c.game(bots)
    c.ce()
    layout()
    luaf("""local al=getAddressList() local m=al.createMemoryRecord() m.Description='ammo' m.Type=vtDword
      m.Address='"ac_client.exe"+17E0A8' m.OffsetCount=1 m.Offset[0]=0x140 return m.CurrentAddress""")
    time.sleep(1)
    e.shot("s_ce", "ce")
    e.shot("s_mv", "Memory Viewer")
    e.shot("s_game", "game")
    st(run=c.truth())
    print(c.truth())


def sel_row_pos():
    """Screen position of the selected disassembler row (ac_client.exe+C73EF with the top at +C73DA: row 9)."""
    x, y, w, h = e.capture.rect(e.hwnd("Memory Viewer"))
    return x + 420, y + 112 + 22 * 8 + 11


def nop1():
    """The disassembler before the change, and its real right-click menu on the dec line."""
    mv(0x4C73DA, 0x4C73EF)
    e.front("Memory Viewer")
    e.cclick("Memory Viewer", "DisassemblerView", 600, 400)      # park
    mv(0x4C73DA, 0x4C73EF)
    e.shot("n_before", "Memory Viewer")
    x, y = sel_row_pos()
    e.click(x, y, button="right")
    time.sleep(0.7)
    print(c.popup_shot("n_menu"))
    mx, my, mw, mh = e.capture.rect(e.hwnd("Memory Viewer"))
    e.area("n_menu_mv", mx, my, mw + 10, 1300)
    e.keys("{ESC}")


def nop2():
    """Replace with code that does nothing: the name dialog, then the changed bytes."""
    luaf("createTimer(300,function() getMemoryViewForm().miReplacewithnops.doClick() end) return 1")
    time.sleep(1.5)
    luaf("local d=E6F('Code:') d.Left=1800 d.Top=300 return 1")
    time.sleep(0.4)
    e.shot("n_dlg", "Code:", True)
    h = e.capture.find("Code:")
    x, y, w, hh = e.capture.rect(h)
    e.click(x + 150, y + 97)
    time.sleep(0.8)
    mv(0x4C73DA, 0x4C73EF)
    e.cclick("Memory Viewer", "DisassemblerView", 600, 400)
    mv(0x4C73DA, 0x4C73EF)
    e.shot("n_after", "Memory Viewer")
    print(c.truth())


def clip(name, clicks, pre=None, gap=1.1):
    e.front("game")
    time.sleep(0.5)
    e.fire(1, 0.8)                     # the first click only gives the game the mouse
    print("before", c.truth()["mag"])
    with e.Rec(name, *REC):
        time.sleep(1.5)
        if pre:
            pre()
        e.fire(clicks, gap)
        time.sleep(1.5)
    print("after", c.truth())


def reload():
    e.front("game")
    time.sleep(0.4)
    e.fire(1, 0.5)
    k.tap(0x52, hold=0.08)
    time.sleep(3.0)
    print(c.truth())


def nopclip():
    clip("n_fire", 5)


def rest1():
    """The code list (Advanced Options) with the entry, and its real right-click menu."""
    luaf("""local f for i=0,getFormCount()-1 do if getForm(i).ClassName=='TAdvancedOptions' then f=getForm(i) end end
      f.show() f.Left=100 f.Top=960 f.Width=700 f.Height=300 local lv=f.lvCodelist lv.ItemIndex=0 lv.Selected=lv.Items[0] return 1""")
    time.sleep(0.6)
    e.shot("r_list", "Code list", True)
    x, y, w, h = e.capture.rect(e.hwnd("Code list"))
    e.click(x + 120, y + 138, button="right")
    time.sleep(0.7)
    print(c.popup_shot("r_menu"))
    e.area("r_menu_win", x, y, w + 250, h + 300)
    e.keys("{ESC}")


def rest2():
    luaf("""local f for i=0,getFormCount()-1 do if getForm(i).ClassName=='TAdvancedOptions' then f=getForm(i) end end
      local lv=f.lvCodelist lv.ItemIndex=0 lv.Selected=lv.Items[0] f.miRestoreWithOriginal.doClick() f.hide() return 1""")
    time.sleep(0.8)
    mv(0x4C73DA, 0x4C73EF)
    e.shot("r_after", "Memory Viewer", True)
    print(c.truth())


def restclip():
    clip("r_fire", 3)


def aa1():
    """Tools > Auto Assemble on the selected line: the empty window and its Template menu."""
    mv(0x4C73DA, 0x4C73EF)
    luaf("createTimer(300,function() getMemoryViewForm().AutoInject1.doClick() end) return 1")
    time.sleep(1.5)
    luaf(f"local f=E6F('{AAF}') E7AA=f f.Left=300 f.Top=60 f.Width=900 f.Height=860 return f.Caption")
    time.sleep(0.5)
    e.shot("a_empty", "Auto assemble", True)
    x, y, w, h = e.capture.rect(e.hwnd("Auto assemble"))
    e.click(x + 126, y + 50)
    time.sleep(0.7)
    print(c.popup_shot("a_tmenu"))
    e.area("a_tmenu_win", x, y, w, h)
    e.keys("{ESC}")
    time.sleep(0.3)
    e.keys("{ESC}")


def aa2():
    luaf("E7AA.CheatTablecompliantcodee1.doClick() return 1")
    time.sleep(0.6)
    e.shot("a_frame", "Auto assemble", True)
    luaf("createTimer(300,function() E7AA.Codeinjection1.doClick() end) return 1")
    time.sleep(1.5)
    luaf("local d=E6F('Code inject template') d.Left=420 d.Top=420 return 1")
    time.sleep(0.4)
    e.shot("a_dlg", "Code inject template", True)
    x, y, w, h = e.capture.rect(e.capture.find("Code inject template"))
    e.click(x + 505, y + 113)
    time.sleep(1.0)
    e.cclick(AAF, "btnExecute", 300, -200)       # park the mouse in the editor's empty area
    e.shot("a_template", "Auto assemble")
    t = e.val("return E7AA.Assemblescreen.Lines.Text")
    open(os.path.join(e.RAW, "a_template.txt"), "w", encoding="utf-8").write(t)
    print(t)


def settext(text, name):
    open(os.path.join(D, "ce", "ep07_script.txt"), "w", encoding="utf-8", newline="\r\n").write(text)
    luaf(r"local f=io.open([[D:\AI\gh-remake\lab\ce\ep07_script.txt]],'r') local s=f:read('*a') f:close() E7AA.Assemblescreen.Lines.Text=s return #s")
    time.sleep(0.6)
    e.shot(name, "Auto assemble", True)


def v1():
    settext(V1, "a_v1")


def assign():
    luaf("createTimer(300,function() E7AA.Assigntocurrentcheattable1.doClick() end) return 1")
    time.sleep(1.5)
    luaf(f"""for i=0,getFormCount()-1 do local f=getForm(i) if f.ClassName=='{AAF}' and f.Visible then f.close() end end
      local al=getAddressList() local m=al[al.Count-1] m.Description='no ammo cost (script)' E7S=m return al.Count""")
    time.sleep(0.8)
    e.cclick("main", "foundcountlabel")
    e.shot("t_off", "ce", True)


def row(i):
    x, y, w, h = [int(v) for v in e.val("return E6R(getAddressList())").split()]
    return x, y + 24 + 12 + 24 * i


def jmp():
    """Tick the script with a real click; the jump in the disassembler and the new memory it leads to."""
    e.front("ce")
    x, y = row(1)
    e.click(x + 21, y)
    time.sleep(0.8)
    e.cclick("main", "foundcountlabel")
    e.shot("t_on", "ce")
    code = c.truth()["code"]
    print(code)
    b = bytes.fromhex(code.replace(" ", ""))
    target = 0x4C73EF + 5 + int.from_bytes(b[4:8], "little")
    st(newmem="%08X" % target, jmp=code)
    mv(0x4C73DA, 0x4C73EF)
    e.shot("j_jmp", "Memory Viewer", True)
    mv(target, target)
    e.shot("j_newmem", "Memory Viewer")
    mv(0x4C73DA, 0x4C73EF)
    print("newmem %08X" % target)
    luaf(f"""local a=0x{target:X} local s='' for i=1,6 do s=s..disassemble(a)..'\\n' a=a+getInstructionSize(a) end return s""")


def off():
    e.front("ce")
    x, y = row(1)
    e.click(x + 21, y)
    time.sleep(0.8)
    e.cclick("main", "foundcountlabel")
    mv(0x4C73DA, 0x4C73EF)
    e.shot("j_off", "Memory Viewer", True)
    print(c.truth())


def toggle():
    """One recording: tick the script, fire (the count stays), untick it, fire (it drops)."""
    x, y = row(1)
    e.front("ce")
    e.cclick("main", "foundcountlabel")
    e.front("game")
    time.sleep(0.5)
    e.fire(1, 0.8)
    print("before", c.truth()["mag"])
    with e.Rec("t_toggle", *REC):
        time.sleep(1.5)
        e.front("ce")
        e.click(x + 21, y)
        time.sleep(1.2)
        print("on", c.truth()["code"][:26], round(time.time(), 1))
        e.fire(1, 0.6)
        e.fire(4, 1.0)
        print("mag after firing with the script on", c.truth()["mag"])
        time.sleep(0.8)
        e.front("ce")
        e.click(x + 21, y)
        time.sleep(1.2)
        print("off", c.truth()["code"][:26])
        e.fire(1, 0.6)
        e.fire(3, 1.0)
        time.sleep(1.5)
    print("after", c.truth())


def edit_v2():
    """Open the script of the table row again (double click on its Value cell opens the editor), put in version 2."""
    luaf("""local al=getAddressList() al.SelectedRecord=E7S createTimer(300,function() getMainForm().Changescript1.doClick() end) return 1""")
    time.sleep(1.5)
    print(e.forms())
    luaf(f"local f=E6F('{AAF}') E7AA=f f.Left=300 f.Top=60 f.Width=900 f.Height=860 return f.Caption")
    settext(V2, "a_v2")


def chg(shots=3, name="c_chg"):
    """Find out what addresses this instruction accesses, on the dec line."""
    mv(0x4C73DA, 0x4C73EF)
    luaf("""if not debug_isDebugging() then debugProcess() end
      createTimer(500,function() getMemoryViewForm().Findoutwhataddressesthisinstructionaccesses1.doClick() end) return 1""")
    time.sleep(2.5)
    luaf("local f=E6F('TfrmChangedAddresses') f.Left=100 f.Top=945 f.Width=640 f.Height=360 return f.Caption")
    time.sleep(0.4)
    e.shot(name + "_empty", "Accessed addresses", True)
    if shots:
        e.fire(1, 0.8)
        e.fire(shots, 1.0)
    time.sleep(1.0)
    rows = e.val("""local l=E6F('TfrmChangedAddresses').Changedlist local s='' for i=0,l.Items.Count-1 do
      s=s..l.Items[i].Caption..' | '..l.Items[i].SubItems[0]..' | '..l.Items[i].SubItems[1]..'\\n' end return s""")
    print(rows, c.truth())
    open(os.path.join(e.RAW, name + ".txt"), "w").write(rows)
    e.shot(name, "Accessed addresses", True)


def chg_close():
    luaf("local f=E6F('TfrmChangedAddresses') f.OKButton.doClick() f.close() return 1")


def bots():
    """Same process, a new match: bot team deathmatch on ac_desert, typed into the game's own console."""
    for cmd, wait in (("mode 7", 0.8), ("map ac_desert", 6), ("addnbot 3 RVSF good", 1.0), ("addnbot 4 CLA good", 2.5)):
        k.cmd(cmd)
        time.sleep(wait)
    u = k.u
    u.keybd_event(9, 0x0F, 0, 0)
    time.sleep(0.8)
    e.shot("b_score", "game")
    u.keybd_event(9, 0x0F, 2, 0)
    st(run_bots=c.truth())
    print(c.truth())


def chgshot(name="c_chg"):
    rows = e.val("""local l=E6F('TfrmChangedAddresses').Changedlist local s='' for i=0,l.Items.Count-1 do
      s=s..l.Items[i].Caption..' | '..l.Items[i].SubItems[0]..' | '..l.Items[i].SubItems[1]..'\n' end return s""")
    print(rows, c.truth())
    open(os.path.join(e.RAW, name + ".txt"), "w").write(rows)
    e.shot(name, "Accessed addresses")
    return rows


def regs(i, name):
    """The real "Show register states" window of row i of the accessed-addresses list."""
    luaf(f"""local f=E6F('TfrmChangedAddresses') local l=f.Changedlist l.ItemIndex={i} l.Selected=l.Items[{i}]
      createTimer(300,function() f.Showregisterstates1.doClick() end) return l.Items[{i}].Caption""")
    time.sleep(1.5)
    luaf("local f=E6F('TRegisters') f.Left=800 f.Top=950 return f.Caption")
    time.sleep(0.4)
    e.shot(name, "Registers")
    e.shot(name + "_list", "Accessed addresses")
    luaf("E6F('TRegisters').close() return 1")


LOG = r"""
E7LOG = {} E7N = 0
if not debug_isDebugging() then debugProcess() end
debug_setBreakpoint(0x%X, 1, bptExecute, function()
  E7N = E7N + 1
  local k = string.format("%%08X %%08X", EDI, EAX)
  if not E7LOG[k] then E7LOG[k] = {0, readInteger(EAX)} end
  E7LOG[k][1] = E7LOG[k][1] + 1
  debug_continueFromBreakpoint(co_run)
  return 1
end)
return "watching"
"""
DUMP = r"""
local s = string.format("local player %08X\n", readInteger(0x0057E0A8))
for k, v in pairs(E7LOG or {}) do
  local edi, eax = tonumber(k:sub(1, 8), 16), tonumber(k:sub(10, 17), 16)
  s = s .. k .. string.format("  hits %d  eax-edi=%X  first %d  now %d  name %s\n", v[1], eax - edi, v[2], readInteger(eax), readString(edi + 0x205, 16) or "?")
end
return s .. "total " .. tostring(E7N)
"""


def log(addr=0x4C73EF, secs=20, name="log"):
    """Who runs the instruction at addr? EDI (owner), EAX (the address written), hits, value at first hit and now."""
    luaf(LOG % addr)
    time.sleep(secs)
    r = luaf(DUMP)
    luaf(f"debug_removeBreakpoint(0x{addr:X}) return 1")
    open(os.path.join(e.RAW, name + ".txt"), "w").write(r)


def script_on(on=True):
    luaf(f"E7S.Active={'true' if on else 'false'} return tostring(E7S.Active)")
    time.sleep(0.5)
    print(c.truth()["code"])


def v2save():
    """Version 2 is in the editor (edit_v2): press its OK button, the table row keeps the new script."""
    print(e.comps(AAF)[:600])
    e.cclick(AAF, "btnExecute")
    time.sleep(0.8)
    print(e.forms())
    luaf("return E7S.Script")


def dis_open():
    luaf("createTimer(300,function() getMemoryViewForm().miDissectData2.doClick() end) return 1")
    time.sleep(2)
    luaf("local f=E6F('TfrmStructures2') E7D=f f.Left=200 f.Top=60 f.Width=1100 f.Height=800 return f.ColumnCount")
    e.shot("d_empty", "Structure dissect", True)
    luaf(f"local col=E7D.Column[0] col.AddressText='{c.truth()['player']}' return col.AddressText")
    time.sleep(0.5)
    e.shot("d_addr", "Structure dissect")
    x, y, w, h = e.capture.rect(e.hwnd("Structure dissect"))
    e.click(x + 128, y + 50)                  # the Structures menu
    time.sleep(0.6)
    print(c.popup_shot("d_smenu"))
    e.area("d_smenu_win", x, y, 700, 420)
    e.keys("{ESC}")
    time.sleep(0.2)
    e.keys("{ESC}")
    luaf("createTimer(300,function() E7D.Definenewstructure1.doClick() end) return 1")
    time.sleep(1.5)
    e.front("New Structure")
    time.sleep(0.3)
    e.cclick("TfrmStructuresNewStructure", "edtStructName")
    e.keys("^a")
    e.keys("Player", 0.05)
    e.shot("d_new", "New Structure")
    e.cclick("TfrmStructuresNewStructure", "btnOk")
    time.sleep(1.5)
    luaf("local h=E7D.HeaderControl1 h.Sections[0].Width=330 h.Sections[1].Width=300 return h.Sections.Count")
    time.sleep(0.5)
    x, y, w, h = e.capture.rect(e.hwnd("Structure dissect"))
    e.click(x + 900, y + 60)
    e.shot("d_top", "Structure dissect", True)


def dis_scroll(name="d_fields", names=True):
    if names:
        luaf("""local st=E7D.MainStruct local s='' for i=0,st.Count-1 do local el=st.Element[i]
          if el.Offset==0xEC then el.Name='health' s=s..i..' ' end if el.Offset==0x140 then el.Name='magazine' s=s..i..' ' end
          if el.Offset==0x11C then el.Name='reserve ammo' s=s..i..' ' end end return s""")
    x, y, w, h = e.capture.rect(e.hwnd("Structure dissect"))
    e.front("Structure dissect")
    e.click(x + 250, y + 182)
    e.keys("{HOME}", 0.05)
    e.keys("{DOWN 85}", 0.01)
    e.keys("{UP 4}", 0.03)
    time.sleep(0.6)
    e.click(x + 900, y + 60)
    e.shot(name, "Structure dissect")
    print(c.truth())


def dis_bot(addr):
    luaf(f"local col=E7D.addColumn() col.AddressText='{addr}' local h=E7D.HeaderControl1 h.Sections[2].Width=300 return E7D.ColumnCount")
    time.sleep(1.2)
    e.shot("d_two", "Structure dissect", True)
    x, y, w, h = e.capture.rect(e.hwnd("Structure dissect"))
    e.click(x + 250, y + 182)
    e.keys("{HOME}", 0.05)
    time.sleep(0.5)
    e.click(x + 900, y + 60)
    e.shot("d_two_top", "Structure dissect")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        if a == "setup":
            setup()
        elif a == "setupbots":
            setup("bots")
        else:
            e.prelude()
            f, _, arg = a.partition(":")
            globals()[f](*([arg] if arg else []))
