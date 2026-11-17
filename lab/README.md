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
  (75 functions for `savegame.exe`, among them CreateFileW, ReadFile, WriteFile, CloseHandle); `e_lfanew` (offset 3C) = F8.

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
