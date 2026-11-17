# Capture lab

Real footage for the long YouTube episodes (`videos/ep*`): the practice game and the tools run on this machine and are
captured window by window. Everything here targets our own offline AssaultCube process.

| Script | What it does |
|---|---|
| `run_ac.sh` | Starts AssaultCube 1.3.0.2 windowed (1280x720) with its own home dir in `lab/ac-home` |
| `ackeys.py` | Sends keys or a console command to the game window |
| `peek.py` | Reads health, ammo and position from the game's memory to verify the offsets a lesson uses |
| `ce/start_ce.py <table.CT>` | Opens a table in Cheat Engine without elevation and accepts its Lua prompt |
| `ce/ce.py "<lua>"` | Runs Lua inside that Cheat Engine (the table polls `ce/cmd.lua`): move windows, set the memory viewer address |
| `rec_shoot.py out.mp4 3` | Records game + Cheat Engine side by side while firing, for "the value changes in both" clips |
| `ep05_cap.py run/take "<actions>"` | Drives Cheat Engine's own window with real mouse and keyboard (control positions come from Lua), optionally while recording a screen rectangle |
| `ep05_con.py` | Starts the episode 5 practice program `scanme.exe` in a classic console window with a large font |
| `ep05_peek.py` | Prints this run's player, health, magazine and reserve addresses, to confirm what a scan found |
| `ep05_events.py <recording>` | Prints when named regions of a raw recording change, to place narration against real events |
| `ce/ep05.CT` | An empty table with only the Lua command channel (no process attached) |
| `../videos/tools/capture.py` | `list`, `shot`, `rec`, `place`, `area`: window screenshots and recordings |

Install the game with `winget install RabidViperProductions.AssaultCube`. AssaultCube 1.3.0.2 offsets used so far
(checked with `peek.py`): local player pointer at `ac_client.exe+17E0A8`; health `+EC`, magazine `+140`, reserve `+11C`,
position x/y/z floats at `+28`, name at `+205`.

Notes:
- Games draw with the GPU, so they are grabbed from the screen: the window is brought to the front first. Always crop a
  recording to the window's own rectangle and look at the result before using it.
- Cheat Engine's manifest asks for elevation; `__COMPAT_LAYER=RunAsInvoker` starts it as the normal user, which is enough
  for a game started by the same user.
- The Windows Calculator ignores synthetic key presses; click its buttons instead.

## Files on disk: hex editor and PE tools (episode 4)

| Script | What it does |
|---|---|
| `win.py "<title>" click x y / dclick x y / keys "..." / shot out.png` | Drives any window by title (chainable); used for ImHex |
| `vc.bat <command>` | Runs a command with the MSVC tools on PATH: `cmd /c labc.bat dumpbin /headers some.exe` |
| `measure.py <mp4>` | Empty-screen runs (4 fps, ink = far from the paper colour and its grid) and mean volume of a render |

ImHex 1.38.1 (`winget install WerWolv.ImHex`, open source, installs unattended to `C:\Program Files\ImHex`):
- First start shows a wizard (Continue, language, "Server Contact": Deny, tutorial: No). After that `imhex.exe <file>` opens the file directly.
- Settings live in `%LOCALAPPDATA%\imhex\config\settings.json` (edit while ImHex is closed). For captures:
  `interface.color` = `Light`, `interface.scaling_factor` = `2.0`, `hex_editor.gray_out_zeros` = `false`,
  `general.auto_load_patterns` = `false`.
- Do not resize it with `capture.py place`: the window rectangle changes but the picture does not follow, and the desktop
  shows through. Use its default size (2460x1240 at scale 2) or click its maximise button.
- It is drawn with the GPU (ImGui): a click needs the mouse to rest on the target first (`win.py` moves, waits, clicks).
- To edit: double-click a byte, type hex digits (the cursor moves on by itself), Esc, Ctrl+S. Changed bytes are red until saved.
- `taskkill /IM imhex-gui.exe` without `/F` does not close it; it restores the open files on the next start.
- Hex pane geometry at scale 2 (pixels from the pane crop at window x=8, y=148): byte column 0 at x=160, pitch 41,
  13 extra before column 8; text column at x=838, 13.7 per character; row 0 at y=58, pitch 32.

Verified with `dumpbin` (MSVC 14.51) on `ac_client.exe` 1.3.0.2, file not modified:
- PE32, machine 14C (x86), 5 sections, image base 00400000, entry point 0042E5F3, size of image 1B9000,
  characteristics 103 = relocations stripped, DLL characteristics 8100 (NX compatible, no Dynamic base).
- Sections (RVA / file offset): `.text` 1000 / 400 Execute Read; `.rdata` 125000 / 123C00 Read Only; `.data` 16B000 / 168E00
  Read Write (virtual size 399CC); `_RDATA` 1A5000; `.rsrc` 1A8000. These are the regions 00401000, 00525000 and 0056B000
  in Cheat Engine's memory map (episode 2). The player pointer `ac_client.exe+17E0A8` is inside `.data`.
- It imports from 13 DLLs: libvorbisfile, OpenAL32, zlib1, OPENGL32, SDL2, SDL2_image, WS2_32 (by ordinal), WINMM, dbghelp,
  KERNEL32, USER32 (only MessageBoxA), ADVAPI32, SHELL32.
- `cheatengine-x86_64.exe` imports `OpenProcess`, `ReadProcessMemory` and `WriteProcessMemory` from kernel32.dll.
- A 64-bit console EXE built with `build.bat` (static CRT): image base 140000000, Dynamic base, imports only KERNEL32.dll
  (74 functions for `savegame.exe`, counted by script from `savegame.imports.txt`, among them CreateFileW, ReadFile, WriteFile, CloseHandle); `e_lfanew` (offset 3C) = F8.

## Code: disassembler and debugger captures (episode 3)

| Script | What it does |
|---|---|
| `ce/lua.py script.lua [seconds]` | Runs a Lua *file* in the lab Cheat Engine (same channel as `ce.py`, longer wait) |
| `ce/ep03_watch.lua`, `ce/ep03_dump.lua` | Logs which instructions write to the magazine / health (a Lua breakpoint callback), then prints them with registers |
| `ce/ep03_findwrites.lua`, `ce/ep03_findaccess.lua` | Opens the real "Find out what writes to / accesses this address" window on this run's magazine / health |
| `ce/ep03_selrow.lua` | Selects the first row of that window so its details pane (code around it + registers) fills in |
| `ce/ep03_dis.lua` | Disassembles `EP03_FROM`..`EP03_TO` to `ce/dis.txt` |
| `ce/ep03_stack.lua` | While stopped at a breakpoint: registers and the top of the stack as text |
| `ce/ep03_verify.lua` | Checks that ESI at the ammo write is the player's current weapon |
| `mvshot.py <top> <selected> <name>` | Points the Memory Viewer disassembler at an address and screenshots it |
| `gshot.py "<title>" <name> [--nofront]` | Screenshot of one window into `lab/shots` |
| `shoot.py <n>` | Clicks in the game n times (each click fires one or two rounds) |
| `rec_region.py out.mp4 x y w h shots [titles]` | Records a screen rectangle while firing; crop each window out of it afterwards |

How it works, learned the hard way:
- A fresh game shows a "game account" menu. One `{ESC}` closes it. A second `{ESC}` opens the main menu, and a click then
  lands on "Multiplayer": look at a screenshot before clicking. `ackeys.py cmd` starts with `{ESC}`, so it opens that menu too.
- The first click after another window had the focus only gives the game the mouse; fire once more (or check `peek.py`).
- `start_ce.py`'s click on the Lua prompt can miss when the game holds the mouse. Posting `BM_CLICK` to the dialog's
  "Yes" button (win32gui) always works.
- Menu items by name (Lua): main form `Setbreakpoint1` = "Find out what writes to this address",
  `Findoutwhataccessesthisaddress1` = "Find out what accesses"; Memory Viewer `miDebugRun`, `miDebugStep`, `miDebugStepOver`.
  Call `debugProcess()` first and use a record with a plain address (not a pointer record) so no dialog asks questions.
- Cheat Engine's default debugger here is the VEH debugger (interface 2). Lua `debug_setBreakpoint(addr)` without a
  function stops the game in the GUI (registers pane and "Return Address" pane appear in the Memory Viewer).
  Single-stepping from the command channel (Lua `co_stepover` or the Step menu items) just resumed the game: to look at
  the next instructions, set a breakpoint on each one and Run between them.
- A stopped game keeps its window on top and cannot be moved: move Cheat Engine's windows instead (Lua `.Left/.Top/.Width`).
- The details pane of the found-opcodes window is `mInfo` (set `.Height`), the list is `FoundCodeList`.

Verified in AssaultCube 1.3.0.2 (32-bit, image base 00400000, code addresses are the same on every run):
- The instruction that takes a round when you fire: `ac_client.exe+C73EF` = `FF 08` = `dec [eax]`, preceded by
  `ac_client.exe+C73EC` = `8B 46 14` = `mov eax,[esi+14]`. At that moment ESI = the current weapon = `[player+364]`,
  EAX = `player+140` (the magazine), EDI = the player. Checked in two runs.
- The reload writes the magazine at `ac_client.exe+C8FE4` = `89 02` = `mov [edx],eax`.
- That function starts at `ac_client.exe+C7200` (`sub esp,24 / push ebx / ... / push esi / mov esi,ecx / ... / push edi`)
  and returns with `ret 0004` (thiscall, one stack argument). The return address seen on its stack was `ac_client.exe+7DFFD`.
- Inside it: a cdecl call at `+C73A7` (4 pushes, one the text "onAttack", then `add esp,10`) and a thiscall at `+C73F9`
  to `ac_client.exe+C9140` (`push ebx` at `+C73E2`, `push eax`, `push ecx`, `mov ecx,esi`; the callee ends with `ret 0C`).
  Stopped at `+C9140`, `[esp]` = `004C73FE`, the address after the call.
- The health is read every frame by `ac_client.exe+5E3EB` = `8B 8B EC000000` = `mov ecx,[ebx+000000EC]` (EBX = the player),
  followed by `cmp ecx,19` / `jng` and `cmp ecx,32` / `jg`; and by `ac_client.exe+61628` = `push [edi+000000EC]`.
  Each was hit 763 times in about 4 seconds (the game ran at about 180 fps). No write to the health was captured (needs damage; `/kill` was not tried to the end).
- MSVC x86 listings are made with `vcvarsamd64_x86.bat` (see `videos/ep03-*/lab/build_both.bat`).

## Verified in episode 5 (Cheat Engine 7.7, driven through its window)

- Main form control names usable from Lua (`getMainForm().<name>`, `clientToScreen(0,0)` gives screen pixels that match
  `capture.rect`): `sbOpenProcess`, `scanvalue`, `scanvalue2` (second box of Value between), `scantype`, `VarType`,
  `btnNewScan` (labelled First Scan, then New Scan), `btnNextScan`, `foundcountlabel`, `Foundlist3`.
- With the window at 888x932 the two first address-list rows are at window y 656 and 680; the Value column is at x 685,
  the Active checkbox at x 21. Double click on a Value opens "Change Value", which appears in the middle of the screen,
  outside Cheat Engine's window.
- Scan type list on a first scan: Exact Value, Bigger than, Smaller than, Value between, Unknown initial value (index 4).
  On a next scan: Exact, Bigger, Smaller, Between, Increased value (4), Increased value by, Decreased value (6),
  Decreased value by, Changed value (8), Unchanged value (9), Ignore value. Value type list: Binary, Byte, 2 Bytes,
  4 Bytes (3), 8 Bytes, Float (5), Double, String, Array of byte, All, Grouped. A combo box opened with a click takes
  Home, Down and Enter.
- Process list: the filter is typed into the list itself and it survives closing the dialog (clear it with Backspace).
  The Processes tab shows `ac_client.exe`; the Applications tab shows window titles. Indexing an empty list from Lua
  opens the Lua Engine error window.
- AssaultCube, one run: Exact Value / 4 Bytes scan for magazine 20 found 2,253; Next Scan 14 left 2; Next Scan 10 left
  the same 2: `player+140` (the real magazine) and one more address outside the player (182C606C in that run). Writing to
  the second one does not change the game, and the game overwrites it on the next shot. Under a freeze of the real one
  the second keeps counting down.
- One click of `fire` with a 0.05 s press spends two rounds (automatic fire).
- After a restart the old magazine address still showed the frozen value, because the freeze was still ticked when the
  game was closed: untick it before closing. The magazine address changed between two runs (00819370, then 00846288).
- `run_ac.sh` did not start a bot match in these sessions (the game came up in an empty TDM map), and typing `/mode` and
  `/map` through `ackeys.py cmd` walked the menu into "multiplayer" instead: do not use it. No way to make the health
  drop was found; episode 5 uses `scanme.exe` for the value without a number.
- `scanme.exe` (64-bit, `videos/ep05-your-first-memory-scan/lab`): gold 250 as 4 Bytes gives 2 addresses after one
  change (the value and its display copy; the copy snaps back within 0.1 s); health as Float, Unknown initial value
  59,392, Decreased 7, Unchanged 7, Increased 1 (value 92.5); energy 87 as 4 Bytes gives 0 after one change, Float with
  Value between finds it (84.04, then 80.74).

## Pointers, pointer scans, tables and hotkeys (episode 6)

| Script | What it does |
|---|---|
| `ep06_cap.py` | Drives *any* Cheat Engine form (not only the main one): `forms`, `comps "<caption or class>"`, `menu`, `lua`, `shot`; as a module `crect(form, control)`, `cclick`, `keys`, `Rec` (records a screen rectangle) |
| `ep06_run.py <stage>` | The whole episode 6 session in stages: `game`, `ce [table.CT]`, `s1 menu writes hex1 pick access hex2 addptr`, restart, `proof psdlg psrun table hotkey hkclip save`, restart, `rescan loaded`, `stop` |
| `ce/ep06.CT` | Empty table with the command channel; `ce/ep06_assaultcube.CT` is the table saved in the episode (pointers + one hotkey) |
| `ce/ep06_watch.lua`, `ce/ep06_dump.lua` | Log which instructions *access* the magazine / health / current-weapon slot (`EP06_WHAT`), then print them |
| `ce/ep06_holders.lua` | Which addresses hold the 4-byte value `EP06_VALUE`, and which of them are static |
| `ce/ep06_vault.lua` | Checks the practice task of episode 6 on `vault.exe` |
| `ptr/` | Pointer scan result files of the episode (`ep06_ammo.PTR`, `ep06_ammo_run3.PTR`) |

How it works, learned the hard way:
- On the primary monitor (125 % scaling) Cheat Engine's main window is 1129x1290 by default and hangs over the edge next to the game.
  `getMainForm()` `.Left=1600 .Top=0 .Width=940 .Height=1000` gives a 942x1064 window beside the 1583 wide game.
  New dialogs open on the second monitor: move each one with `.Left/.Top` before the screenshot.
- Forms by class: `TFoundCodeDialog` (find what writes/accesses; `FoundCodeList`, `mInfo`, `btnExtraInfo`, `btnOK` = Stop, then Close),
  `TFormFoundCodeListExtra` ("Extra info" = More information), `TformAddressChange` (Add/Change address; `cbPointer`, `editDescription`, `btnOk`),
  `TfrmPointerScannerSettings` (`editMaxLevel`, `editStructsize` = maximum offset, `btnOk`), `Tfrmpointerscanner` (`Panel1.Caption` = "Pointer paths:N",
  `lvResults`, menu item `Rescanmemory1`), `TfrmRescanPointer` (`edtAddress`, `Button1` = OK), `THotKeyForm` (`btnCreateHotkey`, `edtHotkey`,
  `cbFreezedirection`, `edtFreezeValue`, `btnApply`, `btnOK`). Main form menu items: `Pointerscanforthisaddress1`, `SetHotkey1`, `Address1`.
- A menu item that opens a modal dialog must be clicked from a timer (`createTimer(400, function() ... .doClick() end)`), or the command
  channel never answers. The channel keeps working while the modal dialog is open.
- In the Add address dialog with Pointer ticked (window 600 wide): base box at y=298 with one offset; each "Add Offset" adds a row and moves
  the base down 30 px. Offset rows are 30 px apart; the bottom row is the one nearest the base.
- The hotkey box records every key while it has the focus (a stray Alt from `capture.front` ends up in it): set the action and the value
  first, then click Clear, click the box and press the key last.
- Cheat Engine polls the keyboard for hotkeys: a synthetic key must be held about 0.4 s (`keybd_event` down, wait, up); `send_keys` is too short.
- The file dialog of the pointer scan drops the first typed character if you type at once: wait about 1.5 s, Ctrl+A, then type the path.
- `debug_setBreakpoint` callbacks and the real "Find out what ..." window both work after `debugProcess()`; restarting the game while the
  debugger was attached gave no error, `openProcess("ac_client.exe")` simply attaches to the new process.

Verified in AssaultCube 1.3.0.2 (three runs in one session: player at 009A62B8, 008D54F8, 00888140):
- Nothing reads or writes the magazine through the player with a `+140` offset. Both readers (`ac_client.exe+C7254` `cmp dword ptr [eax],00`,
  `ac_client.exe+C8E9B` `push [eax]`) and the writer (`dec [eax]` at `+C73EF`) get the address from the weapon: `mov eax,[esi+14]`.
  So the path the code walks is `[[[ac_client.exe+17E0A8]+364]+14]+0`, and `weapon+14` points back into the player at `player+140`.
- A hex scan for the weapon's address finds 8 addresses, none static: one on the stack and `player+354, +360, +364, +368, +36C, +370, +374`.
- `player+364` (current weapon) is read on every frame by 15 instructions, all `mov reg,[reg+00000364]`; the first is
  `ac_client.exe+7DFBF` = `8B 9E 64030000` = `mov ebx,[esi+00000364]` with ESI = the player. (A few more appear when firing or reloading.)
- A hex scan for the player's address finds about 41 addresses (the count varies with the stack); three are static:
  `ac_client.exe+17E0A8`, `+18AC00`, `+195404`. The weapon object holds the player too, at `weapon+8`.
- Pointer scan for the magazine address, max level 5, maximum offset 4095, max 3 offsets per node: 4196 paths in about 2 seconds
  (603 with max level 4 in an earlier run); after one restart and Rescan memory: 392. The first three rows both times are the three static
  addresses above with the single offset 140.
- A plain address from run 1 (009A63F8) read 65537 in run 2 and 11358 in run 3.
- `vault.exe` (episode 6 practice, 64-bit, `/Od`): the coins are written by `mov [rcx+14],eax` with RCX = the player; an 8-byte scan for
  the player finds 3 addresses, one static: `vault.exe+23B80`.
