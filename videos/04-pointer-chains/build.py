"""Video 4: Follow the Pointers (pointer chains).  Run: python build.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, bar, build, card, cells, tile, txt  # noqa: E402,F401

INK = "#0B2A30"

scenes = [
    Scene("hook", "Your player moves to a new address on every run. Yet the game always finds it. How?",
          body=txt("@p-t", 190, 100, "a new address on every run", "h", fs=84)
          + tile("@p-p1", 250, 330, 340, 130, "player", 52) + txt("@p-a1", 250, 490, "0x0A3F2000", "m")
          + tile("@p-p2", 820, 470, 340, 130, "player", 52) + txt("@p-a2", 820, 630, "0x0B71C400", "m")
          + tile("@p-p3", 1340, 300, 340, 130, "player", 52) + txt("@p-a3", 1340, 460, "0x09E60800", "m")
          + txt("@p-q", 190, 820, '<span class="@p-acc">how does the game find it?</span>', "h", fs=90),
          js="""
    each(["#@p-p2", "#@p-a2"], <<new>>, 0.15);
    each(["#@p-p3", "#@p-a3"], <<every>>, 0.15);
    wipe("#@p-q", <<yet>>, 0.7);
"""),

    Scene("pointer", "It keeps a note in a fixed place: a pointer. A pointer is just a number, "
                     "and that number is an address.",
          body=txt("@p-l", 190, 210, "a fixed place", "m")
          + card("@p-s", 190, 300, 700, 130, "game.exe + 0x18AC00", 46, "soft")
          + card("@p-v", 190, 460, 700, 130, "0x0A3F2000", 60)
          + bar("@p-b", 890, 519, 210)
          + tile("@p-pl", 1100, 420, 560, 210, "player", 84)
          + txt("@p-at", 1100, 670, "at 0x0A3F2000", "m")
          + txt("@p-c", 0, 830, "a pointer is a number that is an address", "h", fs=70, w=1920, align="center"),
          js="""
    land("#@p-s", <<note>>);
    blurIn("#@p-l", <<fixed>>);
    land("#@p-v", <<number>>);
    wipe("#@p-b", <<address-0.5>>, 0.3);
    land("#@p-pl", <<address>>);
    blurIn("#@p-at", <<address+0.2>>);
    blurIn("#@p-c", <<pointer#2>>);
"""),

    Scene("struct", "Read the note, and you are standing at the start of the player. "
                    "Health sits a fixed distance in: offset E C.",
          body=txt("@p-h", 260, 150, "Player, starting at 0x0A3F2000", "m")
          + card("@p-f0", 260, 250, 700, 110, "+0x00 &nbsp; ...", 50)
          + card("@p-f1", 260, 380, 700, 110, "+0x04 &nbsp; ...", 50)
          + card("@p-f2", 260, 510, 700, 110, "+0xEC &nbsp; health = 100", 46, "on")
          + card("@p-f3", 260, 640, 700, 110, "+0xF0 &nbsp; armor", 50)
          + txt("@p-o", 1060, 440, '<span class="@p-acc">offset 0xEC</span>', "h", fs=110)
          + txt("@p-d", 1060, 590, "a fixed distance<br>from the start", "m"),
          js="""
    blurIn("#@p-h", <<start>>);
    each(["#@p-f0", "#@p-f1", "#@p-f3"], <<player>>, 0.12);
    land("#@p-f2", <<health>>);
    blurIn("#@p-d", <<fixed>>);
    land("#@p-o", <<offset>>);
"""),

    Scene("recipe", "So the recipe is: read the pointer, then add the offset. In that order.",
          body=txt("@p-f", 0, 300, '[game.exe + 0x18AC00] <span class="@p-acc">+ 0xEC</span>', "m", fs=100, color=INK, w=1920, align="center")
          + txt("@p-s1", 520, 520, "1. read the pointer", "m", fs=64)
          + txt("@p-s2", 520, 630, "2. add the offset", "m", fs=64)
          + txt("@p-c", 0, 820, '<span class="@p-acc">in that order</span>', "h", fs=90, w=1920, align="center"),
          js="""
    land("#@p-f", <<recipe>>, 1.15);
    blurIn("#@p-s1", <<read>>);
    blurIn("#@p-s2", <<add>>);
    wipe("#@p-c", <<order-0.4>>, 0.5);
"""),

    Scene("mistake", "Add first and read second, and you land somewhere else entirely. That is the classic mistake.",
          body=txt("@p-gl", 288, 180, "read, then add", "m")
          + txt("@p-g", 288, 260, '[game.exe + 0x18AC00] <span class="@p-acc">+ 0xEC</span>', "m", fs=80, color=INK)
          + txt("@p-bl", 288, 520, "add, then read: somewhere else", "m")
          + txt("@p-b", 288, 600, "[game.exe + 0x18AC00 + 0xEC]", "m", fs=80, color="#6A9188")
          + bar("@p-x", 270, 642, 1390, 14)
          + txt("@p-c", 0, 830, "the classic mistake", "h", fs=90, w=1920, align="center"),
          js="""
    blurIn("#@p-b", <<add>>);
    blurIn("#@p-bl", <<somewhere>>);
    wipe("#@p-x", <<classic-0.3>>, 0.35);
    wipe("#@p-c", <<classic>>, 0.5);
"""),

    Scene("chain", "Real games chain several. Player points to weapon, weapon points to ammo. Read, add, repeat.",
          body=card("@p-c1", 190, 380, 400, 160, "Player", 60)
          + txt("@p-o1", 600, 300, "+0x364", "m", fs=46) + bar("@p-b1", 590, 454, 170)
          + card("@p-c2", 760, 380, 400, 160, "Weapon", 60)
          + txt("@p-o2", 1178, 300, "+0x14", "m", fs=46) + bar("@p-b2", 1160, 454, 170)
          + card("@p-c3", 1330, 380, 400, 160, "Ammo: 20", 56, "on")
          + txt("@p-f", 0, 650, "[[game.exe + 0x18AC00] + 0x364] + 0x14", "m", fs=60, color=INK, w=1920, align="center")
          + txt("@p-r", 0, 820, "read, add, repeat", "h", fs=90, w=1920, align="center"),
          js="""
    land("#@p-c1", <<player>>);
    wipe("#@p-b1", <<points>>, 0.25);
    blurIn("#@p-o1", <<points>>);
    land("#@p-c2", <<weapon>>);
    wipe("#@p-b2", <<points#2>>, 0.25);
    blurIn("#@p-o2", <<points#2>>);
    land("#@p-c3", <<ammo>>);
    blurIn("#@p-f", <<read-0.6>>);
    wipe("#@p-r", <<read>>, 0.8);
"""),

    Scene("null", "If a link holds zero, stop. There is no player yet, and reading address zero crashes.",
          body=card("@p-s", 190, 250, 700, 130, "game.exe + 0x18AC00", 46, "soft")
          + card("@p-v", 190, 410, 700, 130, "0x00000000", 60, "on")
          + bar("@p-b", 890, 469, 210)
          + card("@p-n", 1100, 380, 560, 190, "no player yet", 52, "soft")
          + txt("@p-st", 190, 640, '<span class="@p-acc">stop.</span>', "h", fs=150)
          + txt("@p-m", 190, 850, "reading address 0 crashes the program", "m"),
          js="""
    land("#@p-v", <<zero>>);
    land("#@p-st", <<stop>>);
    wipe("#@p-b", <<no-0.3>>, 0.25);
    blurIn("#@p-n", <<no>>);
    blurIn("#@p-m", <<reading>>);
"""),

    Scene("claim", "A pointer chain is the path the game itself walks. Walk it the same way.",
          body=card("@p-c1", 192, 200, 300, 110, "base", 46, "soft") + bar("@p-b1", 492, 249, 80)
          + card("@p-c2", 572, 200, 300, 110, "+ offset", 46) + bar("@p-b2", 872, 249, 80)
          + card("@p-c3", 952, 200, 300, 110, "value", 46, "on")
          + txt("@p-a", 192, 400, "A pointer chain is the<br>path the game walks.", "h", fs=110)
          + txt("@p-c", 192, 680, '<span class="@p-acc">Walk it the same way.</span>', "h", fs=110),
          js="""
    each(["#@p-c1", "#@p-b1", "#@p-c2", "#@p-b2", "#@p-c3"], 0.3, 0.1, 1.1);
    wipe("#@p-a", <<pointer>>, 0.9);
    wipe("#@p-c", <<walk-0.2>>, 0.6);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Follow the Pointers")
