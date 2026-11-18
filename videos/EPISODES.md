# Game Hacking from Scratch: how an episode is made

The long YouTube series of this repo. One folder per episode: `videos/epNN-<slug>/`. Episodes 1 and 2 are the reference:
read `ep01-bytes-behind-the-health-bar/build.py` and `ep02-why-the-address-changes/build.py` before writing a new one.

## The format the owner chose

- **One continuous video, 7 to 9 minutes.** No lesson title cards, no chapter cards, no mini-game, no recap of "lesson 1.2".
  One short title scene after the cold open, then straight teaching, scene after scene, each one carrying the thought on.
- **Clear and straightforward.** One idea per scene, 8 to 20 seconds of narration per scene, about 30 to 40 scenes.
- **Real captures wherever one is possible:** the open-source game running offline, the real tool attached to it, the
  real output of a small program written for the episode. Diagrams (cells, cards, tiles) explain; captures prove.
- **Every episode ends with** a recap scene, a practice scene (a program the viewer compiles, or a task in the practice
  game) and a "next time" scene that teases the next episode by its real title.
- The look is the kit's: pale teal paper, dark teal ink, orange accents. Do not restyle it.

## The season

| # | Folder | Title on YouTube | Site lessons it merges | Teases next as |
|---|---|---|---|---|
| 1 | `ep01-bytes-behind-the-health-bar` | What 100 Health Really Looks Like in Memory | 1.1, 1.2 | Why the Address Changes |
| 2 | `ep02-why-the-address-changes` | Why the Health Address Changes Every Restart | 1.3, 1.4 | Read One Line of Assembly |
| 3 | `ep03-read-one-line-of-assembly` | The One Line of Assembly That Takes Your Ammo | 1.5 reading assembly, 1.7 stack and calling conventions | Inside the Files |
| 4 | `ep04-inside-the-files` | 9999 Gold With a Hex Editor, and What Is Inside an EXE | 1.6 hex editing files, 1.8 PE, processes and WinAPI | Your First Memory Scan |
| 5 | `ep05-your-first-memory-scan` | How to Find a Value in a Game's Memory with Cheat Engine | 2.1 first scan, 2.2 scan types and unknown values | Finding the Pointer |
| 6 | `ep06-finding-the-pointer` | How to Find a Pointer in a Game You Have Never Seen | 2.3 finding pointers, 2.4 cheat tables and hotkeys | Changing the Code |
| 7 | `ep07-changing-the-code` | (write it) | 2.5 code injection and scripts, 2.6 shared code and structures | Scripts That Survive an Update |
| 8 | `ep08-scripts-that-survive-an-update` | (write it) | 2.7 floats and multipliers, 2.8 AOB and updating scripts | (end of the Cheat Engine track: tease external trainers in general terms) |

The lesson texts are in `site/_source/01-foundations/` and `site/_source/02-cheat-engine/` (Hebrew). Use them for what to
cover and in what order; write the English narration fresh. An episode may assume everything earlier episodes taught, and
nothing else. Titles follow the pattern `"<Concrete promise or question> (Game Hacking from Scratch #N)"`.

## The one rule of the series (never break it)

Practice only on open-source games played **offline** and on programs written for the episode. Never an online game,
never other players, nothing about getting past an anti-cheat. Episode 1 says this out loud; later episodes show it by
example. If a lesson's source text goes beyond that, leave that part out.

## Steps

1. **Script and captures together.** Decide the scenes, then capture exactly what each one needs (see `lab/README.md`).
   Verify every number against the live process (`lab/peek.py`) or the program's real output before it goes on screen.
2. **Practice program** in `videos/epNN-*/lab/`: small, compiles with MSVC
   (`python -c "import subprocess;print(subprocess.run(['cmd','/c',r'D:\AI\cpp-course\probes\win\build.bat','file.cpp'],capture_output=True,text=True).stdout)"`
   run in that folder), output saved next to it as `<name>.out.txt`. `.exe` files are gitignored.
3. **Scaffold:** copy `AGENTS.md`, `CLAUDE.md`, `hyperframes.json`, `package.json`, `meta.json` from `ep02-*` and replace the
   episode name in the last two. Captures go in `assets/shots/` (PNG) and `assets/clips/` (MP4).
4. **`build.py`** with `videos/tools/kit.py`: `Scene(id, narration, body=..., js=...)`. `<<word>>` in js is the moment that word
   is spoken. `python build.py` voices it (Azure, cached) and writes the HyperFrames project and `SCRIPT.md`.
   Do not edit `kit.py` for one episode; put episode-specific helpers in its `build.py`.
5. **Check:** `npm run check` must end with `Check passed` and 0 errors. Then
   `npx --yes hyperframes@0.9.61 snapshot --at <times>` and look at a frame from **every** scene. Fix overflow, overlap
   and anything unreadable.
6. **Render:** `npm run render` (about 7 minutes). Then measure the mp4 (see "Before you call it done").
7. **`YOUTUBE.md`** like episode 1's: title, description (what the episode shows, "IN THIS EPISODE" bullets, practice
   link, tools with links, the one rule, chapters with timestamps taken from `SCRIPT.md`), tags. No `<` or `>` anywhere.
8. **`thumbnail.png`** (1920x1080): same look as `ep01-*/thumbnail.png`. Its text says the half of the idea the title
   does not say.

## Captures

- Everything is in `lab/README.md`: starting the game, Cheat Engine without elevation, the Lua command channel,
  screenshots and recordings by window, and the verified AssaultCube 1.3.0.2 offsets. Add what you verify to that file.
- The screen is shared. Take the lock before any capture session and release it after:
  `python lab/lock.py acquire screen <your-episode>` ... `python lab/lock.py release screen <your-episode>`.
  Close the game and Cheat Engine before you release it.
- Crop every capture to the tool's own window and **look at it** before use. Nothing else on the desktop may appear.
- Bots: starting a bot match from the command line has not worked reliably. If a scene needs the health to drop and you
  cannot get bots, use the ammo counter (firing) as the changing value, and say so.

## Rules learned in review (the reviewer checks these)

- **Never an empty screen under narration.** The kit moves each scene's first element to 0.3 s and its first real visual
  to 1 s, but check the render anyway.
- **Every number on screen is real and from one consistent run.** If two captures show different values (ammo 20, then
  12), the narration says why.
- **A claim about this game is captured or it is cut.** "Before the match the pointer is zero" needs a capture; otherwise
  say it as a general rule ("in many games ...").
- **An example of "this address dies" must be an address that really changed** between captured runs.
- **A bracket formula is evaluated by hand:** one read per bracket pair, against the chain drawn above it.
- **Value ranges match signedness** (a `char` is not "0 to 255" on MSVC).
- **"From the description" means the link exists.** The practice program must be pushed before the episode is queued.
- **Narration matches the picture:** if the tool updates a moment after the game, say so; do not say "at the same moment".
- **The practice task can be checked** with the program as shipped.
- **The description promises only what the video teaches.**
- A code card that shortens the real file says so.
- **An element added in a fix gets an id nothing else in the scene uses** (helpers like `chain()` already take ids such as
  `@p-c2`). The kit now stops the build on duplicate ids. After any fix, look at frames of the scene you touched.
- **Keep text out of the bottom 80 px** (nothing below y = 1000): YouTube's progress bar covers that strip.
- **"The last lines of the function" are the real last lines.** Search the saved disassembly for every `ret`: a function
  can return early.
- **A count on screen ("N functions in all") is counted from the saved output with a script**, never by eye.
- A tag or label never covers text inside a capture.
- Hex and addresses are spelled for the voice the way episodes 1 and 2 do it ("zero zero eight nine, seven eight six C").

## Before you call it done

- `Check passed`, 0 errors.
- A frame from every scene looked at.
- No bare-background stretch of 1 s or more in the mp4, no heading-only stretch of 2 s or more.
- Mean volume around -19 dB (`ffmpeg -i x.mp4 -af volumedetect -vn -f null -`).
- `SCRIPT.md`, `YOUTUBE.md` (chapters from the final `SCRIPT.md`), `thumbnail.png`, `lab/` program and output all present.
- Game and Cheat Engine closed, screen lock released.

## Publishing (not the producer's job)

Studio project `game-hacking` (`D:\AI\studio\projects\game-hacking.json`), autopilot kind `gh` (Thursdays 16:00):
`studio.py package game-hacking <ep> --thumbnail <png>`, then `autopilot.py add game-hacking <ep> --kind gh`. The
reviewer agent gives the verdict; a remake is fixed in `build.py`, re-rendered, re-packaged and resubmitted.
