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
