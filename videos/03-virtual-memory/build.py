"""Video 3: Why the Address Changes (virtual memory).  Run: python build.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, bar, build, card, cells, tile, txt  # noqa: E402,F401

scenes = [
    Scene("hook", "Yesterday you found your health at this address. Today you restart the game, "
                  "and the same address holds garbage. Nothing broke. It moved.",
          body=txt("@p-lm", 250, 230, "yesterday", "m")
          + card("@p-la", 250, 320, 640, 130, "0x0A3F2000", 60)
          + txt("@p-lv", 250, 490, "= 100", "h", fs=170)
          + txt("@p-rm", 1030, 230, "today, after a restart", "m")
          + card("@p-ra", 1030, 320, 640, 130, "0x0A3F2000", 60)
          + txt("@p-rv", 1030, 490, '<span class="@p-acc">= ???</span>', "h", fs=170)
          + txt("@p-q", 250, 790, "nothing broke. it moved.", "h", fs=96),
          js="""
    land("#@p-la", <<found>>);
    land("#@p-lv", <<health>>);
    blurIn("#@p-rm", <<today>>);
    land("#@p-ra", <<restart>>);
    land("#@p-rv", <<garbage>>);
    wipe("#@p-q", <<nothing>>, 0.6);
"""),

    Scene("private", "Every process lives in its own private map of memory. "
                     "The same address in two programs is two different places.",
          body=txt("@p-l1", 250, 140, "game.exe", "m")
          + card("@p-m1", 250, 220, 600, 640, "", 40, "soft")
          + card("@p-a1", 320, 400, 460, 110, "0x00401000", 50)
          + txt("@p-c1", 320, 560, "game code", "m")
          + txt("@p-l2", 1070, 140, "notepad.exe", "m")
          + card("@p-m2", 1070, 220, 600, 640, "", 40, "soft")
          + card("@p-a2", 1140, 400, 460, 110, "0x00401000", 50)
          + txt("@p-c2", 1140, 560, "text editor code", "m"),
          js="""
    land("#@p-m1", <<process>>, 1.1);
    blurIn("#@p-l1", <<process>>);
    land("#@p-m2", <<private>>, 1.1);
    blurIn("#@p-l2", <<private>>);
    each(["#@p-a1", "#@p-a2"], <<same>>, 0.25);
    blurIn("#@p-c1", <<two#2>>);
    blurIn("#@p-c2", <<different>>);
"""),

    Scene("regions", "The map has regions. The game's own file, loaded as a module. "
                     "The heap, where it creates things while running. And a stack for every thread.",
          body=card("@p-r0", 260, 150, 620, 150, "game.exe", 60, "on")
          + txt("@p-d0", 980, 190, "the game's own file", "m")
          + card("@p-r1", 260, 330, 620, 130, "DLLs", 56)
          + txt("@p-d1", 980, 365, "more modules", "m")
          + card("@p-r2", 260, 490, 620, 200, "heap", 60, "soft")
          + txt("@p-d2", 980, 555, "things created while running", "m")
          + card("@p-r3", 260, 720, 620, 150, "stack", 60)
          + txt("@p-d3", 980, 760, "one for every thread", "m"),
          js="""
    land("#@p-r0", <<file>>);
    blurIn("#@p-d0", <<module>>);
    land("#@p-r1", <<module+0.6>>);
    blurIn("#@p-d1", <<module+0.8>>);
    land("#@p-r2", <<heap>>);
    blurIn("#@p-d2", <<creates>>);
    land("#@p-r3", <<stack>>);
    blurIn("#@p-d3", <<every>>);
"""),

    Scene("perms", "Each page of memory carries permissions. Code can be read and run, but not written. "
                   "Data can be written, but not run.",
          body=txt("@p-t", 190, 90, "every page has permissions", "h", fs=84)
          + card("@p-n0", 190, 280, 360, 130, ".text", 60) + card("@p-p0", 590, 280, 300, 130, "R X", 64, "on")
          + txt("@p-m0", 950, 315, "code: read and run, never write", "m", fs=46)
          + card("@p-n1", 190, 480, 360, 130, ".data", 60) + card("@p-p1", 590, 480, 300, 130, "R W", 64, "on")
          + txt("@p-m1", 950, 515, "variables: write, never run", "m", fs=46)
          + card("@p-n2", 190, 680, 360, 130, ".rdata", 60) + card("@p-p2", 590, 680, 300, 130, "R", 64, "on")
          + txt("@p-m2", 950, 715, "constants: read only", "m", fs=46),
          js="""
    wipe("#@p-t", <<page>>, 0.5);
    each(["#@p-n0", "#@p-p0"], <<code>>, 0.2);
    blurIn("#@p-m0", <<read>>);
    each(["#@p-n1", "#@p-p1"], <<data>>, 0.2);
    blurIn("#@p-m1", <<data+0.4>>);
    each(["#@p-n2", "#@p-p2"], <<written#2>>, 0.2);
    blurIn("#@p-m2", <<written#2+0.2>>);
"""),

    Scene("heap", "Your player is created on the heap, so it lands somewhere new on every run.",
          body=txt("@p-t", 190, 110, "the heap", "h", fs=84)
          + txt("@p-l1", 190, 345, "run 1", "m")
          + card("@p-h1", 420, 300, 1250, 170, "", 40, "soft")
          + tile("@p-p1", 520, 320, 320, 130, "player", 50)
          + txt("@p-a1", 900, 350, "0x0A3F2000", "m")
          + txt("@p-l2", 190, 645, "run 2", "m")
          + card("@p-h2", 420, 600, 1250, 170, "", 40, "soft")
          + tile("@p-p2", 1300, 620, 320, 130, "player", 50)
          + txt("@p-a2", 920, 650, "0x0B71C400", "m"),
          js="""
    land("#@p-p1", <<player>>);
    blurIn("#@p-a1", <<heap>>);
    land("#@p-p2", <<somewhere>>);
    blurIn("#@p-a2", <<every>>);
"""),

    Scene("aslr", "Even the module moves. Windows loads it at a random base each time. That is A S L R.",
          body=txt("@p-t", 190, 90, "ASLR: a random base on every run", "h", fs=80)
          + txt("@p-l1", 190, 345, "run 1", "m")
          + card("@p-h1", 420, 300, 1250, 170, "", 40, "soft")
          + card("@p-g1", 450, 320, 520, 130, "game.exe", 54, "on")
          + txt("@p-b1", 1010, 350, "base 0x00400000", "m")
          + txt("@p-l2", 190, 645, "run 2", "m")
          + card("@p-h2", 420, 600, 1250, 170, "", 40, "soft")
          + card("@p-g2", 1120, 620, 520, 130, "game.exe", 54, "on")
          + txt("@p-b2", 470, 650, "base 0x00D20000", "m"),
          js="""
    land("#@p-g1", <<module>>);
    blurIn("#@p-b1", <<moves>>);
    land("#@p-g2", <<random>>);
    blurIn("#@p-b2", <<base>>);
    wipe("#@p-t", <<that>>, 0.6);
"""),

    Scene("offset", "But the distance from the start of the module never changes. "
                    "Base plus offset finds the same spot every time.",
          body=txt("@p-r1", 190, 170, "run 1", "m")
          + txt("@p-l1", 190, 250, '0x00400000 + <span class="@p-acc">0x18AC00</span> = 0x0058AC00', "m", fs=70, color="#0B2A30")
          + txt("@p-r2", 190, 420, "run 2", "m")
          + txt("@p-l2", 190, 500, '0x00D20000 + <span class="@p-acc">0x18AC00</span> = 0x00EAAC00', "m", fs=70, color="#0B2A30")
          + tile("@p-k", 400, 730, 1120, 170, "game.exe + 0x18AC00", 76),
          js="""
    blurIn(["#@p-r1", "#@p-l1"], <<distance>>);
    blurIn(["#@p-r2", "#@p-l2"], <<never>>);
    land("#@p-k", <<base>>);
    tl.fromTo("#@p-k", { scale: 1 }, { scale: 1.06, duration: 0.2, ease: "power2.out", yoyo: true, repeat: 1 }, <<every>>);
"""),

    Scene("claim", "Never save an address. Save the module and the offset.",
          body=card("@p-g", 192, 200, 520, 120, "game.exe", 54, "on")
          + txt("@p-o", 760, 225, "+ 0x18AC00", "m", fs=64, color="#0B2A30")
          + txt("@p-a", 192, 400, "Never save an address.", "h", fs=118)
          + txt("@p-c", 192, 540, '<span class="@p-acc">Save the module and the offset.</span>', "h", fs=92),
          js="""
    land("#@p-g", 0.3);
    blurIn("#@p-o", 0.6);
    wipe("#@p-a", <<never>>, 0.5);
    wipe("#@p-c", <<save#2-0.2>>, 0.6);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Why the Address Changes")
