"""Game Hacking from Scratch, episode 2: Why the Address Changes (virtual memory + pointers and pointer chains).

Long-form YouTube episode. Every screenshot and number is real: AssaultCube 1.3.0.2 (open source) started three times on this
machine, Cheat Engine's memory regions and memory viewer, and three runs of lab/where.cpp.   Run: python build.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, Shot, bar, build, card, cells, tag, term, tile, txt  # noqa: E402,F401

A = Path(__file__).resolve().parent / "assets"
LIST = (0, 596, 902, 150)              # Cheat Engine address list: header + five rows
ROWS = [620, 644, 668, 693, 717]       # top of each row in table_run1.png
LIST3 = (0, 624, 902, 150)             # the run-3 screenshot: its list sits 28 px lower
ROWS3 = [r + 28 for r in ROWS]
MV = (0, 128, 902, 200)


def table(name, y=250, crop=None):
    crop = crop or (LIST3 if name.startswith("ep02") else LIST)
    return Shot("@p-ce", A / f"shots/{name}.png", 120, y, 1680, crop=crop)


def regions(name, crop, y=230):
    return Shot("@p-rg", A / f"shots/{name}.png", 120, y, 1680, crop=crop)


REG_MOD = (0, 40, 1284, 390)
REG_HEAP = (0, 330, 1284, 240)

RUNS = ["0089786C", "00965E7C", "009761DC"]

WHERE = ['<span class="dimc">--- run 1</span>',
         'module base     7FF7D6F10000',
         '&amp;g_player       7FF7D6F32B70  <span class="hi">= base + 22B70</span>',
         'player (heap)   <span class="hi">01C5484C7E40</span>',
         '<span class="dimc">--- run 2</span>',
         'module base     7FF7D6F10000',
         '&amp;g_player       7FF7D6F32B70  <span class="hi">= base + 22B70</span>',
         'player (heap)   <span class="hi">01FE8CB00680</span>',
         '<span class="dimc">--- run 3</span>',
         'module base     7FF7D6F10000',
         '&amp;g_player       7FF7D6F32B70  <span class="hi">= base + 22B70</span>',
         'player (heap)   <span class="hi">01A630C60680</span>']


def chain(y=330):
    """Three boxes: the static pointer, the player, the weapon, and the ammo value."""
    return (card("@p-c0", 120, y, 470, 150, "game+17E0A8", 46, "on") + txt("@p-v0", 120, y + 170, "holds<br>009760F0", "m", fs=40)
            + bar("@p-b0", 590, y + 68, 60, 14)
            + card("@p-c1", 650, y, 380, 150, "player", 54) + txt("@p-v1", 650, y + 170, "+364 holds<br>00967C20", "m", fs=40)
            + bar("@p-b1", 1030, y + 68, 60, 14)
            + card("@p-c2", 1090, y, 380, 150, "weapon", 54) + txt("@p-v2", 1090, y + 170, "+14 holds<br>00976230", "m", fs=40)
            + bar("@p-b2", 1470, y + 68, 60, 14)
            + tile("@p-c3", 1530, y - 10, 270, 170, "20", 110) + txt("@p-v3", 1530, y + 190, "the ammo", "m", fs=40))


scenes = [
    # ------------------------------------------------------------------ cold open
    Scene("cold", "Last episode, we found our player's health at this address. Zero zero eight nine, seven eight six C. One hundred, right there.",
          body=txt("@p-t", 120, 96, "run 1: the health address", "h", fs=80) + table("table_run1").html()
          + table("table_run1").mark("@p-m1", 276, ROWS[0], 130, 24, pad=6) + table("table_run1").mark("@p-m2", 672, ROWS[0], 70, 24, pad=6)
          + tile("@p-k", 120, 640, 760, 170, "0089786C", 110) + txt("@p-kl", 940, 690, "= 100", "h", fs=100),
          js="""
    land("#@p-m1", <<address>>, 1.3);
    land("#@p-k", <<zero>>);
    land("#@p-m2", <<hundred-0.3>>, 1.3); blurIn("#@p-kl", <<hundred>>);
"""),

    Scene("restart", "So I close the game, start it again, and look at the same address. Eight thousand, two hundred ninety-two. "
                     "That is not my health. That is garbage.",
          body=txt("@p-t", 120, 96, "after a restart: the same address", "h", fs=80) + table("ep02_table_run3").html()
          + table("ep02_table_run3").mark("@p-m1", 276, ROWS3[0], 130, 24, pad=6) + table("ep02_table_run3").mark("@p-m2", 672, ROWS3[0], 70, 24, pad=6)
          + tile("@p-k", 120, 640, 760, 170, "0089786C", 110) + txt("@p-kl", 940, 690, '= <span class="@p-acc">8292 ?</span>', "h", fs=100)
          + txt("@p-g", 120, 880, "not my health: garbage", "m", fs=60),
          js="""
    wipe("#@p-t", <<start-0.3>>, 0.6);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m1", <<same>>, 1.3); land("#@p-k", <<same+0.3>>);
    land("#@p-m2", <<eight>>, 1.3); blurIn("#@p-kl", <<eight+0.2>>);
    blurIn("#@p-g", <<garbage-0.3>>);
"""),

    Scene("hook", "Nothing broke. My player simply moved. And yet the game itself never loses it. By the end of this episode, you will know "
                  "how the game finds its player, and how to find it the same way, on every single run.",
          body=txt("@p-a", 192, 240, "Nothing broke.", "h", fs=130)
          + txt("@p-b", 192, 410, 'The player <span class="@p-acc">moved</span>.', "h", fs=130)
          + txt("@p-c", 192, 680, "the game never loses it", "m", fs=64) + txt("@p-d", 192, 780, "so how does it find it?", "m", fs=64),
          js="""
    wipe("#@p-a", <<nothing-0.2>>, 0.5);
    wipe("#@p-b", <<moved-0.4>>, 0.6);
    blurIn("#@p-c", <<never>>);
    blurIn("#@p-d", <<how>>);
"""),

    Scene("title", "This is Game Hacking from Scratch. Episode two: why the address changes.",
          body=txt("@p-s", 192, 250, "GAME HACKING FROM SCRATCH", "m", fs=64)
          + txt("@p-a", 192, 360, "Why the Address", "h", fs=150) + txt("@p-b", 192, 520, '<span class="@p-acc">Changes</span>', "h", fs=150)
          + tile("@p-e", 192, 760, 420, 130, "EPISODE 2", 60),
          js="""
    blurIn("#@p-s", <<game>>);
    wipe("#@p-a", <<why-0.3>>, 0.6);
    wipe("#@p-b", <<changes-0.2>>, 0.6);
    land("#@p-e", <<episode>>);
"""),

    Scene("runs", "First, the evidence. I started the game three times, and wrote down where the health was. Three runs. Three different addresses.",
          body=txt("@p-t", 190, 110, "three runs, same game, same machine", "h", fs=80)
          + "".join(card(f"@p-n{i}", 190, 300 + i * 200, 320, 150, f"run {i + 1}", 60, "soft") + bar(f"@p-b{i}", 510, 368 + i * 200, 110, 14)
                    + tile(f"@p-a{i}", 620, 290 + i * 200, 700, 170, a, 100) for i, a in enumerate(RUNS))
          + txt("@p-c", 1400, 520, "real<br>addresses", "m", fs=54),
          js="""
    wipe("#@p-t", <<evidence-0.3>>, 0.6);
    each(["#@p-n0", "#@p-n1", "#@p-n2"], <<three>>, 0.25);
    each(["#@p-b0", "#@p-b1", "#@p-b2"], <<three#2>>, 0.3, 1);
    each(["#@p-a0", "#@p-a1", "#@p-a2"], <<three#2+0.1>>, 0.3);
    blurIn("#@p-c", <<different>>);
"""),

    # ------------------------------------------------------------------ virtual memory
    Scene("space", "To see why, we need the map. Every process gets its own address space. For a thirty-two bit game like this one, "
                   "that is four gigabytes of addresses, from zero, all the way up to F F F F, F F F F.",
          body=txt("@p-t", 190, 110, "every process gets its own map", "h", fs=90)
          + card("@p-box", 190, 330, 1540, 240, "", 40, "soft")
          + txt("@p-lo", 190, 600, "0x00000000", "m", fs=60) + txt("@p-hi", 1350, 600, "0xFFFFFFFF", "m", fs=60)
          + txt("@p-mid", 640, 400, "4 GB of addresses", "h", fs=84)
          + txt("@p-c", 190, 780, "32-bit game = 4-byte addresses", "m", fs=60),
          js="""
    wipe("#@p-t", <<map-0.3>>, 0.6);
    wipe("#@p-box", <<address-0.2>>, 0.8);
    blurIn("#@p-c", <<thirty-two>>);
    blurIn("#@p-mid", <<four>>);
    blurIn("#@p-lo", <<zero>>); blurIn("#@p-hi", <<f>>);
"""),

    Scene("private", "And it is private. The same address in two programs is two completely different places. "
                     "That is why it is called virtual memory.",
          body=txt("@p-t", 190, 110, "the same address, two different places", "h", fs=80)
          + card("@p-p1", 190, 320, 700, 130, "game.exe", 60, "on") + card("@p-p2", 1030, 320, 700, 130, "notepad.exe", 60, "on")
          + card("@p-a1", 190, 500, 700, 130, "0x0089786C", 56) + card("@p-a2", 1030, 500, 700, 130, "0x0089786C", 56)
          + card("@p-v1", 190, 680, 700, 130, "health: 100", 56, "soft") + card("@p-v2", 1030, 680, 700, 130, "a letter of text", 50, "soft")
          + txt("@p-c", 190, 890, '<span class="@p-acc">virtual</span> memory: each process sees only its own', "m", fs=56),
          js="""
    wipe("#@p-t", <<same-0.3>>, 0.6);
    land("#@p-p1", <<private>>); land("#@p-p2", <<private+0.2>>);
    land("#@p-a1", <<address>>); land("#@p-a2", <<address+0.2>>);
    land("#@p-v1", <<different>>); land("#@p-v2", <<different+0.2>>);
    blurIn("#@p-c", <<different+0.6>>);
"""),

    Scene("regions", "This is the real map of our game, in Cheat Engine's memory regions view. Every row is one region: "
                     "where it starts, what you are allowed to do there, and how big it is.",
          body=txt("@p-t", 120, 96, "the game's real memory map", "h", fs=80) + regions("ep02_regions", (0, 40, 1284, 480)).html()
          + regions("ep02_regions", (0, 40, 1284, 480)).mark("@p-m1", 4, 44, 180, 470, pad=4)
          + regions("ep02_regions", (0, 40, 1284, 480)).mark("@p-m2", 616, 44, 250, 470, pad=4)
          + regions("ep02_regions", (0, 40, 1284, 480)).mark("@p-m3", 1010, 44, 110, 470, pad=4)
          + tag("@p-g1", 120, 900, "where it starts") + tag("@p-g2", 870, 900, "what is allowed") + tag("@p-g3", 1420, 900, "how big"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-rg", 0.2, 1.03, 0.5);
    land("#@p-m1", <<starts-0.4>>, 1.05); land("#@p-g1", <<starts>>);
    land("#@p-m2", <<allowed-0.5>>, 1.05); land("#@p-g2", <<allowed>>);
    land("#@p-m3", <<big-0.3>>, 1.05); land("#@p-g3", <<big>>);
"""),

    Scene("module", "Find address four hundred thousand, in hex. This is the game's own file, loaded into memory: its module. "
                    "First the code: execute and read. Then constants: read only. Then global variables: read and write.",
          body=txt("@p-t", 120, 96, "the module: ac_client.exe at 00400000", "h", fs=76) + regions("ep02_regions_mod", REG_MOD).html()
          + regions("ep02_regions_mod", REG_MOD).mark("@p-m0", 4, 138, 1250, 24, pad=5)
          + regions("ep02_regions_mod", REG_MOD).mark("@p-m1", 4, 162, 1250, 24, pad=5)
          + regions("ep02_regions_mod", REG_MOD).mark("@p-m2", 4, 186, 1250, 24, pad=5)
          + regions("ep02_regions_mod", REG_MOD).mark("@p-m3", 4, 210, 1250, 24, pad=5)
          + tag("@p-g1", 120, 780, "code: Execute + Read") + tag("@p-g2", 760, 780, "constants: Read") + tag("@p-g3", 1260, 780, "globals: Read + Write"),
          js="""
    wipe("#@p-t", <<module-0.3>>, 0.6);
    land("#@p-rg", 0.2, 1.03, 0.5);
    land("#@p-m0", <<four>>, 1.05);
    tl.to("#@p-m0", { opacity: 0, duration: 0.3 }, <<first-0.2>>);
    land("#@p-m1", <<code>>, 1.05); land("#@p-g1", <<execute>>);
    land("#@p-m2", <<constants>>, 1.05); land("#@p-g2", <<read#2>>);
    land("#@p-m3", <<global>>, 1.05); land("#@p-g3", <<read#3>>);
"""),

    Scene("perms", "Those permissions are enforced by the processor. Write to a read only page, or try to run data as code, "
                   "and the program crashes with an access violation.",
          body=txt("@p-t", 190, 110, "permissions are enforced", "h", fs=96)
          + card("@p-a", 190, 320, 360, 150, "R X", 80, "on") + txt("@p-al", 610, 360, "code: read and run, never write", "m", fs=54)
          + card("@p-b", 190, 510, 360, 150, "R", 80, "on") + txt("@p-bl", 610, 550, "constants: read only", "m", fs=54)
          + card("@p-c", 190, 700, 360, 150, "R W", 80, "on") + txt("@p-cl", 610, 740, "variables: read and write, never run", "m", fs=54)
          + txt("@p-x", 190, 920, 'break the rule = <span class="@p-acc">access violation</span>', "h", fs=64),
          js="""
    wipe("#@p-t", <<permissions-0.2>>, 0.6);
    each(["#@p-a", "#@p-b", "#@p-c"], <<enforced>>, 0.2);
    blurIn("#@p-bl", <<write>>); blurIn("#@p-cl", <<run>>); blurIn("#@p-al", <<run+0.4>>);
    wipe("#@p-x", <<crashes-0.2>>, 0.7);
"""),

    Scene("heap", "Further down is the heap: private, read and write. This is where a program creates things while it runs. "
                  "Bullets, enemies, and your player.",
          body=txt("@p-t", 120, 96, "the heap: created while the game runs", "h", fs=76) + regions("ep02_regions_heap", REG_HEAP, 250).html()
          + regions("ep02_regions_heap", REG_HEAP, 250).mark("@p-m", 4, 426, 1250, 24, pad=2)
          + card("@p-a", 120, 660, 480, 130, "bullets", 56, "soft") + card("@p-b", 660, 660, 480, 130, "enemies", 56, "soft")
          + card("@p-c", 1200, 660, 480, 130, "your player", 56, "on")
          + txt("@p-n", 120, 860, "our player, this run: 009760F0, inside the region at 00940000", "m", fs=44),
          js="""
    wipe("#@p-t", <<heap-0.3>>, 0.6);
    land("#@p-rg", 0.2, 1.03, 0.5);
    land("#@p-m", <<private>>, 1.05);
    land("#@p-a", <<bullets>>); land("#@p-b", <<enemies>>); land("#@p-c", <<player>>);
    blurIn("#@p-n", <<private+0.5>>);
"""),

    Scene("answer", "And that is the answer. The player object is created on the heap while the game runs. Wherever there is free space "
                    "at that moment, that is where it goes. Different run, different spot.",
          body=txt("@p-t", 190, 110, "why the address changes", "h", fs=96)
          + "".join(txt(f"@p-l{i}", 190, 330 + i * 190, f"run {i + 1}", "m", fs=54) + card(f"@p-h{i}", 420, 300 + i * 190, 1300, 130, "", 40, "soft")
                    + tile(f"@p-p{i}", x, 290 + i * 190, 240, 150, "player", 44) for i, x in enumerate((560, 1180, 860)))
          + txt("@p-c", 190, 900, "new on the heap = wherever there is room", "m", fs=58),
          js="""
    wipe("#@p-t", <<answer-0.3>>, 0.6);
    each(["#@p-h0", "#@p-h1", "#@p-h2"], <<heap-0.3>>, 0.15, 1);
    each(["#@p-l0", "#@p-l1", "#@p-l2"], <<heap>>, 0.15, 1);
    land("#@p-p0", <<free>>); land("#@p-p1", <<different>>); land("#@p-p2", <<different#2>>);
    blurIn("#@p-c", <<wherever>>);
"""),

    Scene("where", "You can watch this with a few lines of C plus plus. This program creates a player on the heap, and prints where things live. "
                   "I ran it three times. The heap address is different every time. But look at the global variable: "
                   "base plus two two B seven zero, on every run.",
          body=txt("@p-t", 120, 60, "where.cpp, three real runs", "h", fs=72)
          + term("@p-o", 120, 180, 1180, WHERE, fs=40, lh=1.45)
          + tag("@p-g1", 1340, 330, "heap: moves", 44) + tag("@p-g2", 1340, 560, "base + 22B70:<br>never moves", 44)
          + txt("@p-n", 1340, 800, "where.exe is 64-bit:<br>longer addresses", "m", fs=38, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", <<program-0.3>>, 1.03, 0.5);
    tl.fromTo(["#@p-o-l4", "#@p-o-l5", "#@p-o-l6", "#@p-o-l7"], { opacity: 0 }, { opacity: 1, duration: 0.3 }, <<three-0.3>>);
    tl.fromTo(["#@p-o-l8", "#@p-o-l9", "#@p-o-l10", "#@p-o-l11"], { opacity: 0 }, { opacity: 1, duration: 0.3 }, <<three+0.3>>);
    land("#@p-g1", <<different>>); blurIn("#@p-n", <<prints>>);
    tl.fromTo(["#@p-o-l3", "#@p-o-l7", "#@p-o-l11"], { scale: 1 }, { scale: 1.04, transformOrigin: "left center", duration: 0.25, yoyo: true, repeat: 1 }, <<different>>);
    land("#@p-g2", <<base>>);
    tl.fromTo(["#@p-o-l2", "#@p-o-l6", "#@p-o-l10"], { scale: 1 }, { scale: 1.04, transformOrigin: "left center", duration: 0.25, yoyo: true, repeat: 1 }, <<base>>);
"""),

    Scene("aslr", "A module has a base address, and everything inside it sits at a fixed offset from that base. Windows is free to move the base, "
                  "usually when the machine restarts. That is A S L R: address space layout randomization. "
                  "But base plus offset always lands on the same variable.",
          body=txt("@p-t", 190, 110, "base + offset", "h", fs=110)
          + card("@p-m", 190, 330, 1100, 170, "", 60, "soft") + txt("@p-mt", 240, 380, "module", "m", fs=60) + tile("@p-v", 800, 320, 300, 190, "variable", 44)
          + bar("@p-bb", 190, 540, 610, 14) + txt("@p-bl", 190, 570, "offset: always the same", "m", fs=50)
          + txt("@p-b1", 190, 250, "base", "m", fs=50)
          + txt("@p-as", 190, 720, 'ASLR: <span class="@p-acc">the base can move</span>', "h", fs=80)
          + txt("@p-c", 190, 850, "the offset inside the module cannot", "m", fs=58),
          js="""
    wipe("#@p-t", <<base-0.2>>, 0.6);
    land("#@p-m", <<module>>, 1.03); blurIn("#@p-mt", <<module>>); blurIn("#@p-b1", <<base>>);
    land("#@p-v", <<everything>>); wipe("#@p-bb", <<fixed-0.2>>, 0.5); blurIn("#@p-bl", <<fixed>>);
    wipe("#@p-as", <<a-0.2>>, 0.6);
    tl.to(["#@p-m", "#@p-mt", "#@p-v", "#@p-bb", "#@p-bl", "#@p-b1"], { x: 380, duration: 0.6, ease: "power2.inOut" }, <<move>>);
    blurIn("#@p-c", <<always>>);
"""),

    Scene("rule", "So here is the first rule of this series. Never save a raw address. Save the module name, and the offset.",
          body=txt("@p-t", 190, 130, "rule 1", "h", fs=110)
          + card("@p-x", 190, 360, 760, 170, "0x0089786C", 84, "soft") + bar("@p-x1", 170, 438, 800, 10) + txt("@p-xl", 1010, 410, "a raw heap address: dies", "m", fs=54)
          + tile("@p-y", 190, 620, 1100, 190, "ac_client.exe + 17E0A8", 76) + txt("@p-yl", 1340, 680, "survives", "m", fs=54),
          js="""
    wipe("#@p-t", <<rule-0.2>>, 0.5);
    land("#@p-x", <<never>>); wipe("#@p-x1", <<raw>>, 0.3); blurIn("#@p-xl", <<raw+0.2>>);
    land("#@p-y", <<module>>); blurIn("#@p-yl", <<offset>>);
"""),

    # ------------------------------------------------------------------ pointers
    Scene("note", "Now, how does the game find a player that keeps moving? It keeps a note. Somewhere in its global data, at a fixed offset, "
                  "it stores the player's current address. That note is called a pointer.",
          body=txt("@p-t", 190, 110, "the game keeps a note", "h", fs=96)
          + card("@p-m", 190, 320, 720, 420, "", 40, "soft") + txt("@p-ml", 190, 760, "the module (fixed place)", "m", fs=48)
          + tile("@p-n", 290, 440, 520, 170, "player is at …", 50)
          + bar("@p-b", 910, 520, 250, 14)
          + card("@p-p", 1160, 430, 560, 190, "the player", 60, "on") + txt("@p-pl", 1160, 640, "on the heap (moves)", "m", fs=48)
          + txt("@p-c", 190, 890, 'that note is a <span class="@p-acc">pointer</span>', "h", fs=80),
          js="""
    wipe("#@p-t", <<note-0.3>>, 0.6);
    land("#@p-p", <<player>>); blurIn("#@p-pl", <<moving>>);
    land("#@p-m", <<global-0.3>>, 1.03); blurIn("#@p-ml", <<fixed>>);
    land("#@p-n", <<stores>>); wipe("#@p-b", <<address>>, 0.4);
    wipe("#@p-c", <<pointer-0.4>>, 0.7);
"""),

    Scene("number", "A pointer is not magic. It is just a number. Four bytes in a thirty-two bit game, eight in a sixty-four bit one. "
                    "And that number happens to be an address.",
          body=txt("@p-t", 190, 110, "a pointer is just a number", "h", fs=96)
          + cells("@p-b", 190, 360, ["F0", "60", "97", "00"], size=190, gap=28, on=range(4))
          + txt("@p-l", 190, 600, "4 bytes (32-bit) &nbsp;/&nbsp; 8 bytes (64-bit)", "m", fs=56)
          + txt("@p-c", 190, 780, 'a number that <span class="@p-acc">is an address</span>', "h", fs=90),
          js="""
    wipe("#@p-t", <<magic-0.5>>, 0.6);
    each(".c-@p-b", <<four>>, 0.1);
    blurIn("#@p-l", <<eight>>);
    wipe("#@p-c", <<happens-0.2>>, 0.7);
"""),

    Scene("real", "Here it is, for real. At the game's base plus one seven E zero A eight, there are four bytes. F zero, six zero, nine seven, "
                  "zero zero. Little endian, remember? Flip them: zero zero nine seven, six zero F zero. That is where my player is, right now.",
          body=txt("@p-t", 120, 96, "the pointer, in the memory viewer", "h", fs=80)
          + Shot("@p-mv", A / "shots/ep02_mv_ptr.png", 120, 230, 1680, crop=MV).html()
          + Shot("@p-mv", A / "shots/ep02_mv_ptr.png", 120, 230, 1680, crop=MV).mark("@p-m", 88, 171, 116, 24)
          + cells("@p-b", 120, 700, ["F0", "60", "97", "00"], size=150, gap=20, on=range(4))
          + txt("@p-ar", 850, 720, "&rarr;", "h", fs=110) + tile("@p-k", 1010, 690, 760, 170, "009760F0", 110)
          + txt("@p-kl", 1010, 890, "my player, this run", "m", fs=54),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-mv", 0.2, 1.03, 0.5);
    land("#@p-m", <<four>>, 1.5);
    land("#@p-b0", <<f>>); land("#@p-b1", <<six>>); land("#@p-b2", <<nine>>); land("#@p-b3", <<zero#3>>);
    blurIn("#@p-ar", <<flip>>); land("#@p-k", <<flip+0.4>>);
    blurIn("#@p-kl", <<player>>);
"""),

    Scene("struct", "The player is a structure: a block of fields in a fixed order. Health is always the same distance from the start: E C. "
                    "Ammo: one four zero. Those offsets were decided when the game was compiled. They never change between runs.",
          body=txt("@p-t", 190, 90, "the player is a structure", "h", fs=90)
          + card("@p-s", 190, 260, 900, 690, "", 40, "soft") + txt("@p-sl", 230, 280, "player, starts at 009760F0", "m", fs=44)
          + card("@p-f0", 250, 380, 780, 110, "+28 &nbsp;position x", 48) + card("@p-f1", 250, 520, 780, 110, "+EC &nbsp;health", 48, "on")
          + card("@p-f2", 250, 660, 780, 110, "+140 &nbsp;ammo", 48, "on") + card("@p-f3", 250, 800, 780, 110, "+205 &nbsp;name", 48)
          + txt("@p-c", 1170, 480, "offsets come<br>from the compiler", "m", fs=54)
          + txt("@p-d", 1170, 680, '<span class="@p-acc">they never change<br>between runs</span>', "h", fs=56),
          js="""
    wipe("#@p-t", <<structure-0.4>>, 0.6);
    land("#@p-s", <<block-0.2>>, 1.02); blurIn("#@p-sl", <<block>>);
    each(["#@p-f0", "#@p-f3"], <<fields>>, 0.15);
    land("#@p-f1", <<health>>); land("#@p-f2", <<ammo>>);
    blurIn("#@p-c", <<compiled-0.5>>);
    blurIn("#@p-d", <<never>>);
"""),

    Scene("recipe", "So the recipe has two steps. Read the pointer. Then add the offset. Zero zero nine seven, six zero F zero, plus E C, "
                    "is zero zero nine seven, six one D C. And at that address: one hundred.",
          body=txt("@p-t", 190, 100, "the recipe: read, then add", "h", fs=90)
          + card("@p-a", 190, 300, 660, 150, "[game+17E0A8]", 54) + txt("@p-al", 900, 340, "1. read the pointer", "m", fs=54)
          + tile("@p-b", 190, 500, 660, 170, "009760F0", 96) + txt("@p-pl", 900, 540, "+ EC &nbsp; 2. add the offset", "m", fs=54)
          + tile("@p-c", 190, 730, 660, 170, "009761DC", 96) + txt("@p-eq", 900, 760, "= ", "h", fs=100) + card("@p-v", 1010, 740, 420, 150, "100", 96, "on"),
          js="""
    wipe("#@p-t", <<recipe-0.2>>, 0.6);
    land("#@p-a", <<read>>); blurIn("#@p-al", <<read+0.2>>);
    land("#@p-b", <<zero>>);
    blurIn("#@p-pl", <<plus>>);
    land("#@p-c", <<is>>);
    blurIn("#@p-eq", <<hundred-0.4>>); land("#@p-v", <<hundred-0.2>>);
"""),

    Scene("ce", "Cheat Engine can do that for us. This row uses the pointer instead of a raw address, and it shows one hundred. "
                "The top two rows are the addresses from the earlier runs. Wrong values. The pointer row survives every restart.",
          body=txt("@p-t", 120, 96, "the same thing in Cheat Engine", "h", fs=80) + table("ep02_table_run3").html()
          + table("ep02_table_run3").mark("@p-m3", 44, ROWS3[3], 740, 24, pad=4)
          + table("ep02_table_run3").mark("@p-m1", 44, ROWS3[0], 740, 48, pad=4)
          + tag("@p-g1", 120, 570, "runs 1 and 2: wrong values") + tag("@p-g2", 800, 570, "through the pointer: 100")
          + txt("@p-c", 120, 700, '"P-&gt;" means: this address came from a pointer', "m", fs=54)
          + txt("@p-d", 120, 830, 'the pointer row <span class="@p-acc">survives every restart</span>', "h", fs=72),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m3", <<row>>, 1.05); land("#@p-g2", <<hundred-0.3>>); blurIn("#@p-c", <<pointer>>);
    land("#@p-m1", <<two>>, 1.05); land("#@p-g1", <<wrong-0.2>>);
    wipe("#@p-d", <<survives-0.5>>, 0.7);
"""),

    Scene("order", "One warning. Order matters. Read first, then add. If you add the offset to the pointer's own address and then read, "
                   "you land somewhere else in the module, and get nonsense.",
          body=txt("@p-t", 190, 100, "order matters", "h", fs=100)
          + card("@p-a", 190, 320, 900, 150, "[game+17E0A8] + EC", 60, "on") + txt("@p-al", 1150, 360, "read, then add", "m", fs=56)
          + txt("@p-ar", 1150, 430, "= the health", "m", fs=56)
          + card("@p-b", 190, 600, 900, 150, "[game+17E0A8 + EC]", 60, "soft") + txt("@p-bl", 1150, 640, "add, then read", "m", fs=56)
          + txt("@p-br", 1150, 710, '<span class="@p-acc">= nonsense</span>', "m", fs=56)
          + txt("@p-c", 190, 870, "the brackets say what gets read", "m", fs=54),
          js="""
    wipe("#@p-t", <<order-0.2>>, 0.5);
    land("#@p-a", <<read>>); blurIn("#@p-al", <<read+0.2>>); blurIn("#@p-ar", <<then>>);
    land("#@p-b", <<add#2>>); blurIn("#@p-bl", <<add#2+0.3>>);
    blurIn("#@p-br", <<nonsense-0.3>>);
    blurIn("#@p-c", <<nonsense+0.2>>);
"""),

    Scene("chain", "Real games chain several of these. In AssaultCube, the player holds a pointer to its current weapon. "
                   "The weapon holds a pointer to its ammo. Read, add, read, add.",
          body=txt("@p-t", 120, 110, "a pointer chain", "h", fs=100)
          + card("@p-c0", 120, 400, 400, 170, "player", 60, "on") + bar("@p-b0", 520, 478, 160, 14)
          + card("@p-c1", 680, 400, 400, 170, "weapon", 60) + bar("@p-b1", 1080, 478, 160, 14)
          + card("@p-c2", 1240, 400, 400, 170, "ammo", 60)
          + txt("@p-l0", 500, 600, "pointer", "m", fs=40, w=200, align="center") + txt("@p-l1", 1060, 600, "pointer", "m", fs=40, w=200, align="center")
          + txt("@p-c", 120, 720, "read, add, read, add", "h", fs=90, color="#E8490F"),
          js="""
    wipe("#@p-t", <<chain-0.2>>, 0.5);
    land("#@p-c0", <<player>>);
    wipe("#@p-b0", <<pointer>>, 0.3); blurIn("#@p-l0", <<pointer>>); land("#@p-c1", <<weapon>>);
    wipe("#@p-b1", <<pointer#2>>, 0.3); blurIn("#@p-l1", <<pointer#2>>); land("#@p-c2", <<ammo>>);
    wipe("#@p-c", <<read>>, 1.6);
"""),

    Scene("chainreal", "With real numbers from this run. Base plus one seven E zero A eight gives the player. Player plus three six four "
                       "gives the weapon. Weapon plus one four gives the address of the ammo. One last read, at that address: twenty.",
          body=txt("@p-t", 120, 110, "the real chain, this run", "h", fs=90) + chain()
,
          js="""
    wipe("#@p-t", <<real-0.3>>, 0.6);
    land("#@p-c0", <<base>>); blurIn("#@p-v0", <<gives>>);
    wipe("#@p-b0", <<gives>>, 0.3); land("#@p-c1", <<player>>);
    blurIn("#@p-v1", <<three>>); wipe("#@p-b1", <<gives#2>>, 0.3); land("#@p-c2", <<weapon>>);
    blurIn("#@p-v2", <<one#2>>); wipe("#@p-b2", <<gives#3>>, 0.3);
    land("#@p-c3", <<twenty>>); blurIn("#@p-v3", <<twenty+0.2>>);
""", exit=False),

    Scene("brackets", "You will see this written with square brackets. A pair of brackets means: read what is stored at this address. "
                      "So the whole chain fits on one line.",
          body=txt("@p-t", 120, 110, "the real chain, this run", "h", fs=90) + chain()
          + term("@p-o", 120, 700, 1680, ['<span class="hi">[[[[</span>ac_client.exe+17E0A8<span class="hi">]</span>+364<span class="hi">]</span>+14<span class="hi">]]</span>  =  20'], fs=62)
          + txt("@p-c2", 1010, 920, "four reads, four pairs", "m", fs=54, color="#E8490F")
          + txt("@p-c", 120, 920, "[ x ] = read what is stored at x", "m", fs=54),
          js="""
    land("#@p-o", <<brackets-0.3>>, 1.03, 0.5);
    blurIn("#@p-c", <<means>>);
    blurIn("#@p-c2", <<whole>>);
""", enter=False),

    Scene("null", "One more thing. A pointer can also hold zero. In many games, before a match starts, there is no player yet. Follow a zero pointer and you read "
                  "address zero, which is never mapped. So every tool, and every program you write, should check for zero, and stop.",
          body=txt("@p-t", 190, 110, "when the pointer is zero", "h", fs=96)
          + card("@p-a", 190, 330, 660, 150, "[a pointer]", 54) + txt("@p-eq", 890, 345, "=", "h", fs=100) + tile("@p-z", 1000, 320, 520, 170, "00000000", 80)
          + txt("@p-l", 190, 560, "nothing to point at yet", "m", fs=56)
          + card("@p-r", 190, 680, 1330, 130, "address 0 is never mapped: reading it crashes", 46, "soft")
          + txt("@p-c", 190, 880, 'zero? <span class="@p-acc">stop.</span>', "h", fs=96),
          js="""
    wipe("#@p-t", <<zero-0.5>>, 0.6);
    land("#@p-a", <<pointer>>); blurIn("#@p-eq", <<zero-0.2>>); land("#@p-z", <<zero>>);
    blurIn("#@p-l", <<zero+0.3>>);
    land("#@p-r", <<never-0.5>>, 1.03);
    wipe("#@p-c", <<check>>, 0.6);
"""),

    Scene("later", "How do you discover a pointer like this, in a game you have never seen? That is a skill of its own, and we will get there "
                   "in the Cheat Engine episodes. Today was about knowing what you are looking for.",
          body=txt("@p-a", 192, 260, "Finding pointers", "h", fs=120) + txt("@p-b", 192, 410, "in a game you have never seen", "h", fs=80)
          + card("@p-x", 192, 640, 1160, 140, "coming: the Cheat Engine episodes", 46, "on")
          + txt("@p-c", 192, 860, "today: know what you are looking for", "m", fs=56),
          js="""
    wipe("#@p-a", <<discover-0.3>>, 0.6); wipe("#@p-b", <<never-0.5>>, 0.6);
    land("#@p-x", <<cheat-0.3>>, 1.05);
    blurIn("#@p-c", <<today>>);
"""),

    Scene("recap", "Let's recap. Every process has its own virtual address space, split into regions with permissions. "
                   "The module sits at a base. The heap moves on every run. A pointer is a number that holds an address. "
                   "And a pointer chain is the path the game itself walks to its own data.",
          body=txt("@p-t", 190, 90, "recap", "h", fs=110)
          + txt("@p-a", 190, 290, "each process: its own address space, in regions", "m", fs=56)
          + txt("@p-b", 190, 430, "module = base + fixed offsets; the heap moves", "m", fs=56)
          + txt("@p-c", 190, 570, "pointer = a number that holds an address", "m", fs=56)
          + txt("@p-d", 190, 710, 'pointer chain = <span class="@p-acc">the path the game itself walks</span>', "m", fs=56),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    wipe("#@p-a", <<every>>, 0.8);
    wipe("#@p-b", <<module>>, 0.8);
    wipe("#@p-c", <<pointer>>, 0.8);
    wipe("#@p-d", <<chain>>, 0.8);
"""),

    Scene("practice", "Your practice. Compile where dot C P P from the description, run it three times, and write down what moves "
                      "and what stays. Then restart your computer, and run it once more.",
          body=txt("@p-t", 190, 100, "practice", "h", fs=110)
          + tag("@p-g", 960, 130, "where.cpp: link in the description", 36)
          + term("@p-o", 190, 320, 1180, ["&gt; where.exe", "module base     ?", "&amp;g_player       ?", "player (heap)   ?", "local (stack)   ?"], fs=48)
          + txt("@p-a", 190, 800, "1. run it three times: what moves?", "m", fs=56)
          + txt("@p-b", 190, 890, "2. reboot, run again: what moved now?", "m", fs=56),
          js="""
    wipe("#@p-t", <<practice-0.2>>, 0.5);
    land("#@p-g", <<description-0.4>>);
    land("#@p-o", <<run-0.3>>, 1.04, 0.4);
    blurIn("#@p-a", <<three>>);
    blurIn("#@p-b", <<restart>>);
"""),

    Scene("next", "Next time, we open the code itself: what one line of assembly says, and where a function keeps its arguments. See you there.",
          body=txt("@p-s", 192, 220, "NEXT EPISODE", "m", fs=64)
          + txt("@p-a", 192, 330, "Read One Line", "h", fs=150) + txt("@p-b", 192, 490, 'of <span class="@p-acc">Assembly</span>', "h", fs=150)
          + term("@p-o", 192, 740, 1000, ['mov  [ebx+<span class="hi">EC</span>], eax'], fs=64),
          js="""
    blurIn("#@p-s", <<next>>);
    wipe("#@p-a", <<code-0.3>>, 0.6); wipe("#@p-b", <<assembly-0.3>>, 0.5);
    land("#@p-o", <<function-0.3>>, 1.04, 0.4);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Game Hacking from Scratch 2: Why the Address Changes")
