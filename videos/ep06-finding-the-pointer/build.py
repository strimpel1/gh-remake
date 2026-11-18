"""Game Hacking from Scratch, episode 6: Finding the Pointer (finding pointers + cheat tables and hotkeys).

Long-form YouTube episode. Every screenshot and recording is real: Cheat Engine 7.7 driven through its own windows, attached to
AssaultCube 1.3.0.2 (open source, single player, offline), over three runs of the game in one session (lab/ep06_run.py):
  run 1  player 009A62B8, weapon 00994BA8, magazine 009A63F8   (the manual search, the pointer entry)
  run 2  player 008D54F8, magazine 008D5638                    (the proof, the pointer scan: 4196 paths)
  run 3  player 00888140, magazine 00888280                    (the rescan: 392 paths, the saved table loaded, the hotkey)
prep_clips.py cuts the two recordings.   Run: python build.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, Shot, bar, build, card, cells, fit_clip, tag, term, tile, txt  # noqa: E402,F401

A = Path(__file__).resolve().parent / "assets"
SCAN = (0, 105, 942, 470)          # Cheat Engine: Found, the result list, the scan controls
HUD = (0, 790, 1583, 141)          # the game: the bottom band with the health and ammo counters
GAME = (1582, 930)                 # the game recordings
ROW = [644, 668, 692, 716, 740, 764]   # top of each address-list row in a Cheat Engine screenshot
ACC = "#E8490F"


def shot(id, name, x, y, w, crop=None):
    return Shot(id, A / f"shots/{name}.png", x, y, w, crop=crop)


def rows(n):
    """Crop of the address list: its header and n rows."""
    return (0, 620, 942, 26 + 24 * n)


def clip(id, name, x, y, w, crop, size, start=0.0):
    """A recording in a frame: returns (Shot for marks, media function for Scene)."""
    s = Shot(id, A / f"clips/{name}.mp4", x, y, w, crop=crop, size=size)

    def media(dur):
        p = fit_clip(A / f"clips/{name}.mp4", dur, start)
        s.path, s.src = p, f"assets/clips/{p.name}"
        return s.video(0, dur)
    return s, media


def held(id, name, x, y, w, crop, size, start, hold):
    """A recording that starts at `start`, holds that first frame for `hold` seconds, then plays (two clips cut alike stay in step)."""
    import subprocess
    s = Shot(id, A / f"clips/{name}.mp4", x, y, w, crop=crop, size=size)

    def media(dur):
        src = A / f"clips/{name}.mp4"
        p = src.with_name(f"{name}_held{int(start * 10)}_{int(hold * 10)}_{int(round(dur * 10))}.mp4")
        if not p.exists() or p.stat().st_mtime < src.stat().st_mtime:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-i", str(src), "-vf",
                            f"tpad=start_mode=clone:start_duration={hold}:stop_mode=clone:stop_duration={dur}", "-t", str(dur), "-r", "30",
                            "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-an", str(p)], check=True)
        s.path, s.src = p, f"assets/clips/{p.name}"
        return s.video(0, dur)
    return s, media


def both(*media):
    return lambda dur: "".join(m(dur) for m in media)


def chain(y=330, show_value="12"):
    """The path found in run 1: static pointer, player, weapon, ammo."""
    return (card("@p-c0", 120, y, 470, 150, "game+17E0A8", 46, "on") + txt("@p-v0", 120, y + 170, "holds<br>009A62B8", "m", fs=40)
            + bar("@p-b0", 590, y + 68, 60, 14)
            + card("@p-c1", 650, y, 380, 150, "player", 54) + txt("@p-v1", 650, y + 170, "+364 holds<br>00994BA8", "m", fs=40)
            + bar("@p-b1", 1030, y + 68, 60, 14)
            + card("@p-c2", 1090, y, 380, 150, "weapon", 54) + txt("@p-v2", 1090, y + 170, "+14 holds<br>009A63F8", "m", fs=40)
            + bar("@p-b2", 1470, y + 68, 60, 14)
            + tile("@p-c3", 1530, y - 10, 270, 170, show_value, 110) + txt("@p-v3", 1530, y + 190, "the ammo", "m", fs=40))


cold = shot("@p-ce", "a0_ce", 120, 250, 1680, rows(1))
dead = shot("@p-ce", "b0_ce", 120, 230, 1680, rows(1))
dead_g = shot("@p-g", "b0_game", 120, 420, 1100, HUD)
menu = shot("@p-ce", "a_menu_ce", 120, 200, 1100, (170, 612, 772, 452))
# The recording from its start: the found-code window opens (empty) at 1.5 s, the line appears at 2.0 s and its count reaches
# 4, 6 and 8 at 4.4, 6.2 and 7.6 s. Held on the empty window for 2.2 s, so the line lands on "One line appears" and 8 on "eight".
fire_g, fire_gm = held("@p-g", "fire_game", 100, 200, 960, None, GAME, 1.5, 2.2)
fire_f, fire_fm = held("@p-f", "fire_found", 1100, 200, 720, (0, 0, 500, 330), (922, 872), 1.5, 2.2)
extra_w = shot("@p-x", "a_w_extra", 120, 200, 1000, (0, 30, 537, 330))
hex1 = shot("@p-ce", "a_hex1", 120, 190, 1680, (0, 105, 942, 217))
hex1b = shot("@p-ce", "a_hex1", 120, 200, 800, (0, 105, 470, 250))
LIST = (0, 105, 470, 250)          # the result list alone: Found, the header, eight rows
pick_a = shot("@p-ce", "a_hex1", 120, 180, 800, LIST)            # nothing selected yet
pick_b = shot("@p-ce2", "a_hex1_sel", 120, 180, 800, LIST)       # the row I double click
al_a = shot("@p-al", "a_hex1_sel", 120, 680, 1680, rows(2))      # the address list before the double click
al_b = shot("@p-al2", "a_hex1_added", 120, 680, 1680, rows(2))   # and after it
acc = shot("@p-f", "a_a", 120, 160, 1062, (0, 0, 560, 432))
extra_a = shot("@p-x", "a_a_extra", 120, 200, 1150, (0, 30, 539, 330))
hex2 = shot("@p-ce", "a_hex2", 120, 175, 800, (0, 105, 450, 452))
hex2v = shot("@p-v", "a_hex2", 1000, 190, 720, (470, 170, 400, 48))
hex2z = shot("@p-ce", "a_hex2", 120, 200, 1000, (0, 425, 470, 100))
ptr = shot("@p-d", "a_ptr_final", 120, 172, 1240, (0, 36, 662, 421))
proof = shot("@p-ce", "b0_ce", 120, 200, 1680, rows(2))
proof_g = shot("@p-g", "b0_game", 120, 460, 1100, HUD)
psdlg = shot("@p-d", "b_psdlg", 120, 190, 1440)
PSR = (0, 62, 850, 276)
psres = shot("@p-r", "b_psres", 120, 200, 1680, PSR)
rsdlg = shot("@p-d", "c_rsdlg", 120, 180, 620, (0, 0, 416, 130))
rescan = shot("@p-r", "c_rescan", 120, 440, 1680, (0, 62, 850, 232))
short = shot("@p-r", "c_rescan", 120, 200, 1680, (0, 62, 850, 132))
table = shot("@p-ce", "c_loaded_ce", 120, 200, 1680, rows(6))
loaded = shot("@p-ce", "c_loaded_ce", 120, 190, 1400, rows(6))
loaded_g = shot("@p-g", "c_loaded_game", 120, 610, 1100, HUD)
hk = shot("@p-d", "b_hk1", 120, 200, 1100, (0, 8, 700, 462))
hk_l, hk_lm = clip("@p-ce", "hk_list", 120, 190, 1500, (0, 0, 942, 186), (942, 210), 3.9)
hk_g, hk_gm = clip("@p-g", "hk_game", 120, 540, 1200, (0, 620, 1582, 310), GAME, 3.9)
con = shot("@p-k", "v_con", 100, 230, 980, (0, 30, 560, 300))

CT = ['&lt;CheatEntry&gt;',
      '  &lt;ID&gt;4&lt;/ID&gt;',
      '  &lt;Description&gt;<span class="hi">"ammo"</span>&lt;/Description&gt;',
      '  &lt;VariableType&gt;4 Bytes&lt;/VariableType&gt;',
      '  &lt;Address&gt;<span class="hi">"ac_client.exe"+17E0A8</span>&lt;/Address&gt;',
      '  &lt;Offsets&gt;',
      '    &lt;Offset&gt;<span class="hi">140</span>&lt;/Offset&gt;',
      '  &lt;/Offsets&gt;',
      '<span class="dimc">  ... the hotkey ...</span>',
      '&lt;/CheatEntry&gt;']

VAULT = ['coins: 486',
         '&gt; t',
         '  module base     7FF7E8010000',
         '  &amp;g_player       7FF7E8033B80  <span class="hi">= vault.exe+23B80</span>',
         '  player (heap)   <span class="hi">02A95AA67C60</span>',
         '  &amp;player-&gt;coins  02A95AA67C74  <span class="hi">= player+14</span>']

scenes = [
    # ------------------------------------------------------------------ cold open
    Scene("cold", "A memory scan, like the one in the last episode, ends here. One address that holds my ammo. "
                  "Zero zero nine A, six three F eight. Twenty rounds.",
          body=txt("@p-t", 120, 96, "run 1: the ammo address", "h", fs=80) + cold.html()
          + cold.mark("@p-m1", 276, ROW[0] + 1, 130, 22, pad=6) + cold.mark("@p-m2", 672, ROW[0] + 1, 60, 22, pad=6)
          + tile("@p-k", 120, 520, 760, 170, "009A63F8", 110) + txt("@p-kl", 940, 570, "= 20", "h", fs=100),
          js="""
    land("#@p-m1", <<address>>, 1.3);
    land("#@p-k", <<zero>>);
    land("#@p-m2", <<twenty-0.3>>, 1.3); blurIn("#@p-kl", <<twenty>>);
"""),

    Scene("restart", "Then I close the game, and start it again. The same address now says sixty-five thousand, five hundred and thirty-seven. "
                     "The game says twenty. The address is dead.",
          body=txt("@p-t", 120, 96, "after a restart: the same address", "h", fs=80) + dead.html()
          + dead.mark("@p-m1", 276, ROW[0] + 1, 130, 22, pad=6) + dead.mark("@p-m2", 672, ROW[0] + 1, 80, 22, pad=6)
          + dead_g.html() + dead_g.mark("@p-m3", 478, 855, 195, 65)
          + tile("@p-k", 1300, 440, 500, 150, "65537 ?", 80) + txt("@p-g2", 1300, 630, "the game: 20", "m", fs=54)
          + txt("@p-x", 120, 800, 'this address is <span class="@p-acc">dead</span>', "h", fs=84),
          js="""
    wipe("#@p-t", <<start-0.3>>, 0.6);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m1", <<same>>, 1.3);
    land("#@p-m2", <<sixty-five>>, 1.3); land("#@p-k", <<sixty-five+0.2>>);
    land("#@p-g", <<game-0.4>>, 1.03); land("#@p-m3", <<twenty#1>>, 1.3); blurIn("#@p-g2", <<twenty#1>>);
    wipe("#@p-x", <<dead-0.4>>, 0.6);
"""),

    Scene("hook", "Episode two explained why, and showed you the pointer that fixes it. But I promised that one day you would "
                  "find such a pointer yourself, in a game you have never seen. That day is today.",
          body=txt("@p-a", 192, 220, "Episode 2 showed", "h", fs=110)
          + txt("@p-b", 192, 350, "you the pointer.", "h", fs=110)
          + card("@p-x", 192, 560, 1100, 150, "[ac_client.exe+17E0A8] + 140", 60, "soft")
          + txt("@p-c", 192, 790, 'Today <span class="@p-acc">you find it yourself.</span>', "h", fs=96),
          js="""
    wipe("#@p-a", <<episode-0.2>>, 0.5); wipe("#@p-b", <<explained>>, 0.5);
    land("#@p-x", <<pointer-0.3>>, 1.05);
    wipe("#@p-c", <<find-0.5>>, 0.7);
"""),

    Scene("title", "This is Game Hacking from Scratch. Episode six: finding the pointer.",
          body=txt("@p-s", 192, 250, "GAME HACKING FROM SCRATCH", "m", fs=64)
          + txt("@p-a", 192, 360, "Finding", "h", fs=150) + txt("@p-b", 192, 520, 'the <span class="@p-acc">Pointer</span>', "h", fs=150)
          + tile("@p-e", 192, 760, 420, 130, "EPISODE 6", 60),
          js="""
    blurIn("#@p-s", <<game>>);
    wipe("#@p-a", <<finding-0.3>>, 0.6);
    wipe("#@p-b", <<pointer-0.2>>, 0.6);
    land("#@p-e", <<episode>>);
"""),

    # ------------------------------------------------------------------ the manual way
    Scene("idea", "The idea is simple. The game's own code knows the way to the ammo. Every time I fire, some instruction writes "
                  "the new number. Catch that instruction, and we see where it got the address.",
          body=txt("@p-t", 190, 110, "let the game's code show the way", "h", fs=84)
          + card("@p-a", 190, 360, 520, 170, "an instruction", 50, "soft") + bar("@p-b1", 710, 438, 130, 14)
          + card("@p-b", 840, 360, 520, 170, "an address", 54) + bar("@p-b2", 1360, 438, 130, 14)
          + tile("@p-c", 1490, 350, 270, 190, "20", 110)
          + txt("@p-l1", 190, 560, "writes the new number", "m", fs=44) + txt("@p-l2", 840, 560, "where did it get it?", "m", fs=44, color=ACC)
          + txt("@p-d", 190, 780, "catch the instruction, follow it back", "h", fs=72),
          js="""
    wipe("#@p-t", <<idea-0.3>>, 0.6);
    land("#@p-c", <<ammo>>);
    land("#@p-a", <<instruction>>); blurIn("#@p-l1", <<writes>>); wipe("#@p-b1", <<writes>>, 0.3);
    land("#@p-b", <<number>>); wipe("#@p-b2", <<number>>, 0.3);
    blurIn("#@p-l2", <<where>>);
    wipe("#@p-d", <<catch-0.2>>, 0.7);
"""),

    Scene("menu", "In Cheat Engine, right click the address, and choose: find out what writes to this address. "
                  "Cheat Engine attaches its debugger to the game, our own offline process, and opens an empty window.",
          body=txt("@p-t", 120, 80, "right click the address", "h", fs=80) + menu.html()
          + menu.mark("@p-m", 338, 980, 300, 26, pad=4)
          + tag("@p-g1", 1260, 330, "Find out what<br>writes to this address", 40)
          + txt("@p-n", 1260, 560, "the debugger attaches<br>to our own<br>offline process", "m", fs=44),
          js="""
    wipe("#@p-t", <<right-0.2>>, 0.5);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m", <<find-0.2>>, 1.2); land("#@p-g1", <<find>>);
    blurIn("#@p-n", <<debugger-0.3>>);
"""),

    Scene("fire", "Now I fire. One line appears, and its counter climbs with every burst: two, four, six, eight. "
                  "This is the instruction that takes a round out of my magazine.",
          body=txt("@p-t", 100, 80, "fire, and watch the window", "h", fs=80)
          + fire_g.mark("@p-m1", 478, 855, 195, 65)
          + fire_f.mark("@p-m2", 4, 66, 300, 26, pad=4)
          + tag("@p-g1", 1100, 700, "dec [eax]: take one away", 40),
          media=both(fire_gm, fire_fm),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-m2", <<appears+0.4>>, 1.2); land("#@p-m1", <<burst>>, 1.2);
    land("#@p-g1", <<instruction-0.3>>);
"""),

    Scene("above", "Click More information. The line itself says: subtract one at the address in E A X. Our ammo "
                  "address. Nothing new. But look one line up. Move into E A X, what is stored at E S I plus one four. The game "
                  "fetched our address from memory.",
          body=txt("@p-t", 120, 80, "More information", "h", fs=80) + extra_w.html()
          + extra_w.mark("@p-m1", 8, 128, 262, 26, pad=3) + extra_w.mark("@p-m2", 28, 101, 334, 26, pad=3)
          + extra_w.mark("@p-m3", 8, 256, 164, 24, pad=3)
          + tag("@p-g1", 1170, 300, "EAX = our ammo address", 36)
          + term("@p-o", 1170, 480, 640, ['mov eax,[<span class="hi">esi+14</span>]', 'dec [eax]'], fs=50)
          + txt("@p-n", 1170, 740, "the address was read<br>from memory,<br>at ESI + 14", "m", fs=46),
          js="""
    wipe("#@p-t", <<more-0.3>>, 0.5);
    land("#@p-x", 0.2, 1.03, 0.5);
    land("#@p-m1", <<subtract-0.3>>, 1.1); land("#@p-m3", <<e-0.2>>, 1.2); land("#@p-g1", <<ammo>>);
    tl.to(["#@p-m1", "#@p-m3"], { opacity: 0, duration: 0.3 }, <<look-0.2>>);
    land("#@p-m2", <<up>>, 1.1); land("#@p-o", <<move>>, 1.04);
    blurIn("#@p-n", <<fetched-0.3>>);
"""),

    Scene("esi", "And Cheat Engine shows what was in E S I at that moment. Zero zero nine nine, four B A eight. So an object starts there, "
                 "and at offset one four, it keeps a pointer to our ammo. Episode two gave it a name: the weapon.",
          body=txt("@p-t", 120, 80, "what was in ESI?", "h", fs=80) + extra_w.html()
          + extra_w.mark("@p-m1", 176, 280, 164, 26, pad=3)
          + tile("@p-k", 1170, 220, 640, 150, "00994BA8", 90)
          + card("@p-w", 1170, 440, 640, 130, "the weapon", 56, "on")
          + txt("@p-n", 1170, 610, "+14 holds 009A63F8", "m", fs=46) + bar("@p-b", 1170, 690, 300, 12)
          + txt("@p-n2", 1170, 730, "our ammo address", "m", fs=46, color=ACC),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-m1", <<e-0.2>>, 1.3); land("#@p-k", <<zero>>);
    blurIn("#@p-n", <<offset>>); wipe("#@p-b", <<pointer>>, 0.3); blurIn("#@p-n2", <<ammo>>);
    land("#@p-w", <<weapon-0.3>>);
"""),

    Scene("hex1", "So the question moves up one level. Who holds the weapon's address? A pointer is just a number, so we can scan for it. "
                  "New scan. Tick Hex. Four bytes. Type the address. Eight results.",
          body=txt("@p-t", 120, 80, "scan for the address itself", "h", fs=80) + hex1.html()
          + hex1.mark("@p-m1", 490, 186, 448, 30, pad=4) + hex1.mark("@p-m2", 464, 262, 300, 28, pad=4)
          + hex1.mark("@p-m3", 0, 110, 70, 22, pad=4) + hex1.mark("@p-m4", 4, 155, 440, 166, pad=4)
          + tile("@p-f", 120, 660, 490, 140, "Found: 8", 70)
          + tag("@p-g1", 1000, 640, "Hex + the address", 44) + tag("@p-g2", 1000, 770, "4 Bytes", 44),
          js="""
    wipe("#@p-t", <<who-0.2>>, 0.5);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m1", <<tick-0.2>>, 1.1); land("#@p-g1", <<hex>>);
    land("#@p-m2", <<four>>, 1.1); land("#@p-g2", <<four+0.2>>);
    land("#@p-m3", <<eight-0.3>>, 1.3); land("#@p-m4", <<eight>>, 1.05); land("#@p-f", <<eight>>);
"""),

    Scene("black", "All eight are black. Cheat Engine paints an address green when it is static: inside a module, at the same "
                  "offset on every run. Black is heap or stack, and it will move. We are not at the bottom yet.",
          body=txt("@p-t", 120, 80, "eight results, none of them green", "h", fs=76) + hex1b.html()
          + card("@p-a", 1000, 230, 800, 150, "green = static", 60, "on") + txt("@p-al", 1000, 400, "inside a module:<br>same offset every run", "m", fs=44)
          + card("@p-b", 1000, 570, 800, 150, "black = heap or stack", 54, "soft") + txt("@p-bl", 1000, 740, "it will move", "m", fs=44)
          + txt("@p-c", 120, 880, "not at the bottom yet", "h", fs=72, color=ACC),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-a", <<green-0.3>>); blurIn("#@p-al", <<inside>>);
    land("#@p-b", <<black#2-0.2>>); blurIn("#@p-bl", <<move>>);
    wipe("#@p-c", <<bottom-0.6>>, 0.6);
"""),

    Scene("pick", "So we climb again. Seven of the eight sit close together, right next to our ammo address. Probably one object. "
                  "I double click one of them to add it to the list, and this time I ask: find out what accesses this address.",
          body=txt("@p-t", 120, 70, "one level up", "h", fs=80) + pick_a.html() + pick_b.html() + al_a.html() + al_b.html()
          + pick_a.mark("@p-m1", 4, 176, 440, 148, pad=3) + pick_a.mark("@p-m2", 4, 218, 440, 22, pad=3)
          + al_b.mark("@p-m3", 4, 668, 760, 24, pad=3)
          + tag("@p-g1", 1000, 220, "seven neighbours", 38)
          + txt("@p-n", 1000, 330, "ammo:&nbsp; 009A63F8<br>these: 009A66..", "m", fs=44)
          + tag("@p-g2", 1000, 480, "Find out what<br>accesses this address", 38),
          js="""
    wipe("#@p-t", <<climb-0.3>>, 0.5);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m1", <<seven>>, 1.05); land("#@p-g1", <<seven+0.2>>); blurIn("#@p-n", <<next>>);
    land("#@p-al", 0.3, 1.02, 0.5);
    tl.to("#@p-m1", { opacity: 0, duration: 0.3 }, <<double-0.2>>);
    blurIn("#@p-ce2", <<double>>, 0.15); land("#@p-m2", <<double+0.1>>, 1.1);
    blurIn("#@p-al2", <<add>>, 0.15); land("#@p-m3", <<list>>, 1.05);
    land("#@p-g2", <<find-0.2>>);
"""),

    Scene("access", "No need to fire. The window fills at once, because the game reads this value on every frame. "
                    "Fifteen instructions, and every one of them has the same offset in its brackets: three six four.",
          body=txt("@p-t", 120, 60, "who reads it? everyone", "h", fs=80) + acc.html()
          + acc.mark("@p-m1", 334, 66, 104, 364, pad=3)
          + tile("@p-k", 1280, 260, 520, 170, "+364", 110)
          + txt("@p-n", 1280, 480, "15 instructions,<br>one offset", "m", fs=50)
          + txt("@p-n2", 1280, 660, "read on<br>every frame", "m", fs=44, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    blurIn("#@p-n2", <<frame-0.4>>);
    blurIn("#@p-n", <<fifteen>>);
    land("#@p-m1", <<offset-0.3>>, 1.03); land("#@p-k", <<three>>);
"""),

    Scene("player", "More information on the first one. Move into E B X, what is stored at E S I plus three six four. And E S I is zero zero nine A, "
                    "six two B eight. It holds the weapon, and the ammo sits right inside it. This is the player.",
          body=txt("@p-t", 120, 80, "the next object up", "h", fs=80) + extra_a.html()
          + extra_a.mark("@p-m1", 8, 128, 440, 26, pad=3) + extra_a.mark("@p-m2", 176, 280, 164, 26, pad=3)
          + tile("@p-k", 1320, 220, 490, 150, "009A62B8", 76)
          + card("@p-w", 1320, 440, 490, 130, "the player", 54, "on")
          + txt("@p-n", 1320, 610, "+364 holds<br>00994BA8", "m", fs=46)
          + txt("@p-n2", 1320, 740, "the weapon", "m", fs=46, color=ACC),
          js="""
    wipe("#@p-t", <<more-0.3>>, 0.5);
    land("#@p-x", 0.2, 1.03, 0.5);
    land("#@p-m1", <<move>>, 1.05);
    land("#@p-m2", <<zero-0.4>>, 1.3); land("#@p-k", <<zero>>);
    blurIn("#@p-n", <<holds>>); blurIn("#@p-n2", <<weapon>>);
    land("#@p-w", <<player-0.3>>);
"""),

    Scene("hex2", "Third scan: who holds the player's address? Forty-one results. The red ones are leftovers on the stack, "
                  "already overwritten. But in the middle of the list: three green addresses.",
          body=txt("@p-t", 120, 66, "who holds the player?", "h", fs=80) + hex2.html() + hex2v.html()
          + hex2.mark("@p-m1", 0, 110, 76, 22, pad=4) + hex2.mark("@p-m2", 212, 155, 220, 293, pad=7)
          + hex2.mark("@p-m3", 4, 449, 440, 64, pad=3)
          + tile("@p-f", 1000, 340, 490, 140, "Found: 41", 66)
          + tag("@p-g1", 1000, 570, "red: stack leftovers", 40)
          + tag("@p-g2", 1000, 800, "three green", 48),
          js="""
    wipe("#@p-t", <<who-0.2>>, 0.5);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-v", <<holds>>, 1.03, 0.4);
    land("#@p-m1", <<forty-one-0.2>>, 1.3); land("#@p-f", <<forty-one>>);
    land("#@p-m2", <<red>>, 1.03); land("#@p-g1", <<leftovers-0.3>>);
    tl.to("#@p-m2", { opacity: 0, duration: 0.3 }, <<but>>);
    land("#@p-m3", <<three-0.2>>, 1.05); land("#@p-g2", <<green-0.2>>);
"""),

    Scene("green", "The first one: A C client dot E X E, plus one seven E zero A eight. The same static pointer episode two handed "
                  "you. This time, we found it ourselves.",
          body=txt("@p-t", 120, 80, "green: the static address", "h", fs=80) + hex2z.html()
          + hex2z.mark("@p-m1", 4, 449, 190, 22, pad=3)
          + tile("@p-k", 120, 520, 1240, 190, "ac_client.exe + 17E0A8", 84)
          + txt("@p-n", 120, 780, "same offset in the module, every run", "m", fs=54)
          + txt("@p-c", 120, 880, 'this time <span class="@p-acc">we found it ourselves</span>', "h", fs=68),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-m1", <<first-0.2>>, 1.2); land("#@p-k", <<a>>);
    blurIn("#@p-n", <<static>>);
    wipe("#@p-c", <<this-0.2>>, 0.7);
"""),

    Scene("chain", "So here is the whole path, as the game walks it. The static pointer gives the player. Player plus three six four gives the weapon. "
                   "Weapon plus one four gives the address of the ammo. And there: twelve, what my shots left in the magazine.",
          body=txt("@p-t", 120, 110, "the path we found, in run 1", "h", fs=84) + chain()
          + txt("@p-v4", 1530, 580, "one last read", "m", fs=34, color=ACC)
          + txt("@p-c", 120, 760, "read, add, read, add, read", "h", fs=80, color=ACC),
          js="""
    wipe("#@p-t", <<whole-0.3>>, 0.6);
    land("#@p-c0", <<static>>); blurIn("#@p-v0", <<gives>>);
    wipe("#@p-b0", <<gives>>, 0.3); land("#@p-c1", <<player>>);
    blurIn("#@p-v1", <<three>>); wipe("#@p-b1", <<gives#2>>, 0.3); land("#@p-c2", <<weapon>>);
    blurIn("#@p-v2", <<one>>); wipe("#@p-b2", <<gives#3>>, 0.3);
    land("#@p-c3", <<twelve>>); blurIn("#@p-v3", <<twelve+0.2>>); blurIn("#@p-v4", <<shots>>);
    wipe("#@p-c", <<magazine-0.6>>, 1.0);
"""),

    # ------------------------------------------------------------------ the pointer entry
    Scene("add", "Now tell Cheat Engine. Add Address Manually, and tick Pointer. The base goes in the bottom box: the module name in quotes, plus the offset. "
                 "Then the offsets, from the bottom up. Three six four. One four. And zero, because the ammo sits exactly where the last pointer lands.",
          body=txt("@p-t", 120, 70, "Add Address Manually: Pointer", "h", fs=76) + ptr.html()
          + ptr.mark("@p-m0", 12, 230, 72, 24, pad=3) + ptr.mark("@p-m1", 12, 343, 436, 28, pad=3)
          + ptr.mark("@p-m2", 40, 313, 380, 26, pad=2) + ptr.mark("@p-m3", 40, 283, 380, 26, pad=2) + ptr.mark("@p-m4", 40, 253, 380, 26, pad=2)
          + tag("@p-g1", 1400, 250, "base: at the bottom", 32)
          + txt("@p-n", 1410, 400, "offsets go<br>bottom-up:<br>364, 14, 0", "m", fs=50),
          js="""
    wipe("#@p-t", <<add-0.2>>, 0.5);
    land("#@p-d", 0.2, 1.03, 0.5);
    land("#@p-m0", <<tick>>, 1.2);
    land("#@p-m1", <<base>>, 1.05); land("#@p-g1", <<bottom>>);
    tl.to(["#@p-m0", "#@p-m1"], { opacity: 0, duration: 0.3 }, <<then-0.2>>);
    blurIn("#@p-n", <<offsets>>);
    land("#@p-m2", <<three>>, 1.05); land("#@p-m3", <<one>>, 1.05); land("#@p-m4", <<zero>>, 1.05);
"""),

    Scene("walk", "On the right, Cheat Engine walks the chain while you type. The player. The weapon. And on the top line, "
                  "zero zero nine A, six three F eight: our ammo address, holding twelve.",
          body=txt("@p-t", 120, 70, "Cheat Engine walks the chain live", "h", fs=76) + ptr.html()
          + ptr.mark("@p-m1", 450, 344, 90, 26, pad=3) + ptr.mark("@p-m2", 450, 314, 208, 26, pad=3)
          + ptr.mark("@p-m3", 450, 254, 170, 26, pad=3) + ptr.mark("@p-m4", 14, 60, 316, 28, pad=3)
          + tag("@p-g1", 1410, 250, "= 009A63F8", 44) + tile("@p-k", 1410, 420, 300, 170, "12", 110)
          + txt("@p-n", 1410, 640, "the chain<br>is right", "m", fs=50),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-m1", <<player>>, 1.1); land("#@p-m2", <<weapon>>, 1.05);
    land("#@p-m3", <<top>>, 1.05); land("#@p-g1", <<zero>>);
    land("#@p-m4", <<holding-0.3>>, 1.05); land("#@p-k", <<twelve>>);
    blurIn("#@p-n", <<address-0.2>>);
"""),

    Scene("proof", "Now the test. I close the game, and start it again. The old address: garbage. The pointer row now lands on a different address, "
                   "zero zero eight D, five six three eight, and shows twenty. Exactly what the game says.",
          body=txt("@p-t", 120, 70, "run 2: after a restart", "h", fs=80) + proof.html()
          + proof.mark("@p-m1", 44, ROW[0] + 1, 720, 22, pad=3) + proof.mark("@p-m2", 44, ROW[1] + 1, 720, 22, pad=3)
          + proof_g.html() + proof_g.mark("@p-m3", 478, 855, 195, 65)
          + tag("@p-g1", 1260, 440, "plain address: garbage", 34) + tag("@p-g2", 1260, 560, "pointer: 20", 44)
          + txt("@p-n", 120, 700, '"P-&gt;" = this address came from a pointer', "m", fs=50)
          + txt("@p-c", 120, 830, 'the pointer <span class="@p-acc">survived the restart</span>', "h", fs=76),
          js="""
    wipe("#@p-t", <<test-0.3>>, 0.5);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m1", <<old>>, 1.03); land("#@p-g1", <<garbage-0.2>>);
    land("#@p-m2", <<pointer>>, 1.03); blurIn("#@p-n", <<lands>>); land("#@p-g2", <<twenty-0.2>>);
    land("#@p-g", <<exactly-0.4>>, 1.03); land("#@p-m3", <<exactly>>, 1.2);
    wipe("#@p-c", <<game#2-0.5>>, 0.7);
"""),

    # ------------------------------------------------------------------ the automatic way
    Scene("auto", "That was the manual way. Now the automatic one. Right click the row: Pointer scan for this "
                  "address. It searches for every chain of pointers that ends at our ammo. Two settings matter. Max level: how "
                  "many pointers in a row. I use five. And the maximum offset.",
          body=txt("@p-t", 120, 80, "the automatic way: Pointer scan", "h", fs=76) + psdlg.html()
          + psdlg.mark("@p-m0", 14, 88, 816, 28, pad=3) + psdlg.mark("@p-m1", 425, 302, 212, 30, pad=3) + psdlg.mark("@p-m2", 172, 302, 242, 30, pad=3)
          + tag("@p-g0", 1600, 300, "this run's<br>ammo address", 30)
          + tag("@p-g1", 880, 880, "Max level: 5", 40) + tag("@p-g2", 400, 880, "Maximum offset", 40),
          js="""
    wipe("#@p-t", <<automatic-0.3>>, 0.5);
    land("#@p-d", <<right-0.3>>, 1.03, 0.5);
    land("#@p-m0", <<address-0.3>>, 1.03); land("#@p-g0", <<ammo>>);
    land("#@p-m1", <<max>>, 1.1); land("#@p-g1", <<five-0.3>>);
    land("#@p-m2", <<maximum>>, 1.1); land("#@p-g2", <<maximum+0.2>>);
"""),

    Scene("paths", "A few seconds later: four thousand, one hundred and ninety-six paths. Every one of them lands on the ammo right now. "
                   "And most of them only by accident.",
          body=txt("@p-t", 120, 80, "every path that works right now", "h", fs=76) + psres.html()
          + psres.mark("@p-m1", 535, 70, 130, 22, pad=4)
          + tile("@p-f", 120, 800, 620, 140, "4196 paths", 70)
          + txt("@p-n", 800, 830, "most of them: by accident", "m", fs=54, color=ACC),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-m1", <<four-0.2>>, 1.3); land("#@p-f", <<four>>);
    blurIn("#@p-n", <<accident-0.6>>);
"""),

    Scene("rescan", "The filter is a restart. Start the game again, find the ammo's new address, and choose Rescan memory. "
                    "Every path that no longer lands there is thrown out. Four thousand, one hundred and ninety-six becomes three hundred and ninety-two. "
                    "Repeat until the list is short.",
          body=txt("@p-t", 120, 70, "run 3: Rescan memory", "h", fs=80) + rsdlg.html() + rescan.html()
          + rsdlg.mark("@p-m0", 8, 56, 320, 30, pad=3)
          + rescan.mark("@p-m1", 535, 70, 130, 22, pad=4)
          + card("@p-a", 820, 210, 380, 150, "4196", 80, "soft") + txt("@p-ar", 1230, 225, "&rarr;", "h", fs=100)
          + tile("@p-b", 1380, 200, 420, 170, "392", 110),
          js="""
    wipe("#@p-t", <<filter-0.3>>, 0.5);
    land("#@p-d", 0.2, 1.03, 0.5);
    land("#@p-m0", <<new-0.2>>, 1.05);
    land("#@p-a", <<four-0.2>>);
    land("#@p-r", <<thrown-0.4>>, 1.02, 0.5);
    blurIn("#@p-ar", <<becomes>>); land("#@p-b", <<three>>); land("#@p-m1", <<three>>, 1.3);
"""),

    Scene("short", "Then choose: few offsets, small offsets, and a base inside the game's own module. Look at the first row. "
                  "Our static pointer, and a single offset: one four zero. The player holds the ammo itself, and the weapon only "
                  "points back at it. Both paths are correct.",
          body=txt("@p-t", 120, 80, "which path do you keep?", "h", fs=80) + short.html()
          + short.mark("@p-m1", 4, 126, 420, 24, pad=3)
          + txt("@p-a", 120, 500, "few offsets &nbsp;&middot;&nbsp; small offsets &nbsp;&middot;&nbsp; the game's own module", "m", fs=46)
          + card("@p-x", 120, 620, 1160, 150, "[ac_client.exe+17E0A8] + 140", 60, "on")
          + txt("@p-n", 120, 810, "the player holds the ammo itself;<br>the weapon only points back at it", "m", fs=46),
          js="""
    wipe("#@p-t", <<choose-0.3>>, 0.5);
    land("#@p-r", 0.2, 1.02, 0.5);
    blurIn("#@p-a", <<few>>);
    land("#@p-m1", <<first>>, 1.03);
    land("#@p-x", <<single-0.3>>, 1.04);
    blurIn("#@p-n", <<holds>>);
"""),

    Scene("which", "So which way? The scan is fast, but its paths are guesses until restarts prove them. The manual way is the "
                  "path the code really takes, and it showed us the objects on the way. Start manual. Scan when you are stuck.",
          body=txt("@p-t", 190, 100, "manual or automatic?", "h", fs=90)
          + card("@p-a", 190, 300, 720, 130, "Pointer scan", 56, "soft")
          + txt("@p-a1", 190, 460, "fast", "m", fs=50) + txt("@p-a2", 190, 540, "guesses, until restarts<br>prove them", "m", fs=44)
          + card("@p-b", 1010, 300, 720, 130, "by hand", 56, "on")
          + txt("@p-b1", 1010, 460, "slower", "m", fs=50) + txt("@p-b2", 1010, 540, "the path the code takes;<br>you learn the objects", "m", fs=44)
          + txt("@p-c", 190, 800, 'start manual, <span class="@p-acc">scan when stuck</span>', "h", fs=80),
          js="""
    wipe("#@p-t", <<which-0.2>>, 0.5);
    land("#@p-a", <<scan>>); blurIn("#@p-a1", <<fast>>); blurIn("#@p-a2", <<guesses>>);
    land("#@p-b", <<manual>>); blurIn("#@p-b1", <<manual+0.3>>); blurIn("#@p-b2", <<path>>);
    wipe("#@p-c", <<start-0.2>>, 0.7);
"""),

    # ------------------------------------------------------------------ cheat tables and hotkeys
    Scene("table", "Now keep the work. Double click a description to name a row. Right click, Create Header, to group rows. And "
                  "once you have one pointer into an object, its neighbours are cheap. Copy the row, and change only the last "
                  "offset. E C: the health. One one C: the reserve ammo.",
          body=txt("@p-t", 120, 80, "a table you can read", "h", fs=80) + table.html()
          + table.mark("@p-m1", 44, ROW[1] + 1, 120, 22, pad=3) + table.mark("@p-m2", 62, ROW[3] + 1, 700, 22, pad=3)
          + table.mark("@p-m3", 62, ROW[4] + 1, 700, 22, pad=3)
          + tag("@p-g1", 120, 600, "names") + tag("@p-g2", 420, 600, "a header groups rows")
          + txt("@p-n", 120, 740, "same base, last offset changed:", "m", fs=48)
          + card("@p-a", 120, 830, 400, 120, "+140 ammo", 44, "soft") + card("@p-b", 560, 830, 400, 120, "+EC health", 44, "on")
          + card("@p-c", 1000, 830, 480, 120, "+11C reserve", 44, "on"),
          js="""
    wipe("#@p-t", <<keep-0.2>>, 0.5);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-g1", <<name-0.3>>);
    land("#@p-m1", <<header-0.3>>, 1.1); land("#@p-g2", <<header>>);
    blurIn("#@p-n", <<copy>>); land("#@p-a", <<copy+0.2>>);
    land("#@p-m2", <<e>>, 1.03); land("#@p-b", <<health-0.2>>);
    land("#@p-m3", <<one#3>>, 1.03); land("#@p-c", <<reserve-0.2>>);
"""),

    Scene("ct", "Control S saves the list as a cheat table: a dot C T file. It is plain X M L text. Here is our ammo entry. The "
                  "description. The base. And the offset. Nothing magic.",
          body=txt("@p-t", 120, 70, "the .CT file is plain text", "h", fs=80)
          + term("@p-o", 120, 200, 1220, CT, fs=40, lh=1.5)
          + tag("@p-g1", 1400, 350, "the name", 38) + tag("@p-g2", 1400, 470, "the base", 38) + tag("@p-g3", 1400, 590, "the offset", 38)
          + txt("@p-n", 1400, 720, "one entry of<br>the real file,<br>hotkey part<br>left out", "m", fs=38, color="#6A9188"),
          js="""
    wipe("#@p-t", <<control-0.2>>, 0.5);
    land("#@p-o", <<saves-0.3>>, 1.03, 0.5);
    blurIn("#@p-n", <<entry>>);
    land("#@p-g1", <<description>>); land("#@p-g2", <<base>>); land("#@p-g3", <<offset>>);
"""),

    Scene("load", "Run three. A new game process, and Cheat Engine opened again with the saved table. Every pointer row is alive: "
                  "twenty, one hundred, forty. Only the top row is garbage: the plain address I kept from run one. Only pointer "
                  "rows survive.",
          body=txt("@p-t", 120, 70, "run 3: the saved table, loaded", "h", fs=76) + loaded.html()
          + loaded.mark("@p-m1", 62, ROW[2] + 1, 700, 94, pad=3) + loaded.mark("@p-m2", 44, ROW[0] + 1, 720, 22, pad=3)
          + loaded_g.html()
          + tag("@p-g1", 1260, 640, "pointers: alive", 40) + tag("@p-g2", 1260, 770, "plain address: garbage", 34)
          + txt("@p-c", 120, 870, 'only pointer rows <span class="@p-acc">survive</span>', "h", fs=72),
          js="""
    wipe("#@p-t", <<run-0.2>>, 0.5);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-g", <<new-0.3>>, 1.03);
    land("#@p-m1", <<alive-0.4>>, 1.03); land("#@p-g1", <<alive>>);
    land("#@p-m2", <<top>>, 1.03); land("#@p-g2", <<garbage>>);
    wipe("#@p-c", <<only#2-0.2>>, 0.7);
"""),

    Scene("hotkey", "One last piece: a hotkey. Right click the ammo row, Set hotkeys, Create hotkey. Press the key you want. "
                    "I use one on the numeric keypad. Then pick what it does: toggle freeze, set a value, increase or decrease. Mine says: set value to twenty.",
          body=txt("@p-t", 120, 80, "Set hotkeys", "h", fs=80) + hk.html()
          + hk.mark("@p-m1", 12, 258, 352, 28, pad=3) + hk.mark("@p-m2", 12, 288, 256, 28, pad=3) + hk.mark("@p-m3", 12, 344, 352, 28, pad=3)
          + tag("@p-g1", 1270, 330, "the key", 40) + tag("@p-g2", 1270, 480, "the action", 40) + tag("@p-g3", 1270, 630, "the value: 20", 40),
          js="""
    wipe("#@p-t", <<hotkey-0.2>>, 0.5);
    land("#@p-d", <<right-0.3>>, 1.03, 0.5);
    land("#@p-m1", <<press>>, 1.05); land("#@p-g1", <<numeric-0.3>>);
    land("#@p-m2", <<pick>>, 1.05); land("#@p-g2", <<toggle>>);
    land("#@p-m3", <<mine>>, 1.05); land("#@p-g3", <<twenty-0.3>>);
"""),

    Scene("refill", "Back in the game. I fire: fourteen, twelve, ten. Then one tap on the keypad, and the magazine is back at twenty. "
                    "I fire again, and both ammo rows follow the game. Cheat Engine wrote that twenty through the pointer.",
          body=txt("@p-t", 120, 70, "one key: refill", "h", fs=80)
          + hk_l.mark("@p-m1", 62, 76, 720, 22, pad=3) + hk_l.mark("@p-m2", 62, 148, 720, 22, pad=3)
          + tag("@p-g1", 1380, 620, "numeric 1", 44) + tile("@p-k", 1380, 760, 300, 160, "20", 100),
          media=both(hk_lm, hk_gm),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-g1", <<tap-0.3>>); land("#@p-k", <<twenty-0.2>>);
    land("#@p-m1", <<both-0.3>>, 1.03); land("#@p-m2", <<both-0.1>>, 1.03);
""", early=False),

    # ------------------------------------------------------------------ recap, practice, next
    Scene("recap", "Let's recap. Find out what writes to the address: read the offset and the register. Scan for the register's "
                  "value, in hex. Repeat until an address is green. Add a pointer: base at the bottom, offsets bottom up. Then "
                  "save the table, and give it a key.",
          body=txt("@p-t", 190, 80, "recap", "h", fs=110)
          + txt("@p-a", 190, 270, "what writes? read the offset and the register", "m", fs=54)
          + txt("@p-b", 190, 400, "scan for the register's value, in hex", "m", fs=54)
          + txt("@p-c", 190, 530, 'repeat until an address is <span class="@p-acc">green</span>', "m", fs=54)
          + txt("@p-d", 190, 660, "add a pointer: base at the bottom, offsets bottom-up", "m", fs=54)
          + txt("@p-e", 190, 790, "save the table, give it a key", "m", fs=54),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    wipe("#@p-a", <<find>>, 0.8);
    wipe("#@p-b", <<scan>>, 0.8);
    wipe("#@p-c", <<repeat>>, 0.8);
    wipe("#@p-d", <<add>>, 0.8);
    wipe("#@p-e", <<then>>, 0.8);
"""),

    Scene("practice", "Your practice. Compile vault dot C P P from the description. Find the coins, find what writes to them, and "
                  "scan for the register as eight bytes: this program is sixty-four bit. Add the pointer, save the table, "
                  "restart, and load it. Press T, and the program tells you the truth.",
          body=txt("@p-t", 100, 60, "practice", "h", fs=100)
          + tag("@p-g", 700, 90, "vault.cpp: link in the description", 36)
          + con.html()
          + txt("@p-a", 1140, 240, "1. find the coins", "m", fs=46)
          + txt("@p-b", 1140, 330, "2. what writes to them?", "m", fs=46)
          + txt("@p-c", 1140, 420, "3. scan the register:<br>&nbsp;&nbsp; Hex, 8 Bytes", "m", fs=46)
          + txt("@p-d", 1140, 570, "4. add the pointer", "m", fs=46)
          + txt("@p-e", 100, 810, "5. save the table, restart vault.exe, load it: still the coins?", "m", fs=46)
          + txt("@p-f", 100, 890, "press t: the program tells you the right answer", "m", fs=46, color=ACC),
          js="""
    wipe("#@p-t", <<practice-0.2>>, 0.5);
    land("#@p-g", <<description-0.4>>);
    land("#@p-k", <<compile-0.3>>, 1.03, 0.4);
    blurIn("#@p-a", <<find>>); blurIn("#@p-b", <<writes>>); blurIn("#@p-c", <<eight-0.5>>);
    blurIn("#@p-d", <<add>>); blurIn("#@p-e", <<save>>); blurIn("#@p-f", <<press>>);
"""),

    Scene("next", "One thing has not changed. The game still subtracts a round on every shot. We only write a number back. Next "
                  "time, we change the instruction itself. Changing the code. See you there.",
          body=txt("@p-s", 192, 200, "NEXT EPISODE", "m", fs=64)
          + txt("@p-a", 192, 310, "Changing", "h", fs=150) + txt("@p-b", 192, 470, 'the <span class="@p-acc">Code</span>', "h", fs=150)
          + term("@p-o", 192, 720, 1280, ['ac_client.exe+C73EF   <span class="hi">dec [eax]</span>'], fs=56)
          + txt("@p-n", 192, 900, "the instruction that takes the round", "m", fs=46),
          js="""
    land("#@p-o", <<subtracts-0.4>>, 1.04, 0.4); blurIn("#@p-n", <<subtracts>>);
    blurIn("#@p-s", <<next>>);
    wipe("#@p-a", <<changing-0.3>>, 0.6); wipe("#@p-b", <<changing+0.1>>, 0.5);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Game Hacking from Scratch 6: Finding the Pointer")
