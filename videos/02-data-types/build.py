"""Video 2: Same Bytes, Different Number (data types in memory).  Run: python build.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, arena, bar, build, card, cells, tile, txt  # noqa: E402,F401

B = ["00", "00", "C8", "42"]

scenes = [
    Scene("hook", "You search the game's memory for your health, one hundred. Zero results. "
                  "The number is right there on screen. So where is it?",
          bg="arena",
          body=arena("100")
          + card("@p-q", 1010, 150, 720, 120, "search: 100 &nbsp;(4 Bytes)", 50)
          + card("@p-r", 1010, 310, 720, 120, "0 results", 60, "on"),
          js="""
    land("#@p-q", <<search>>);
    land("#@p-r", <<zero>>);
    tl.fromTo("#@p-hudn", { scale: 1 }, { scale: 1.08, duration: 0.2, ease: "power2.out", yoyo: true, repeat: 1 }, <<screen>>);
    tl.fromTo("#@p-r", { rotation: 0 }, { rotation: -3, duration: 0.25, ease: "power2.out" }, <<where>>);
"""),

    Scene("four", "It is here, in these four bytes. They just don't say one hundred the way you expected.",
          body=txt("@p-t", 475, 250, "your health, as the game stores it", "m")
          + cells("@p-b", 475, 380, B, 220, 30, on={0, 1, 2, 3})
          + txt("@p-u", 475, 680, "4 bytes &middot; no label &middot; no type", "m"),
          js="""
    each(".c-@p-b", <<here>>, 0.15);
    blurIn("#@p-t", <<four>>);
    blurIn("#@p-u", <<they>>);
"""),

    Scene("asint", "Read them as a whole number and you get one billion, one hundred twenty million. "
                   "Nonsense for a health bar.",
          body=cells("@p-b", 564, 150, B, 180, 24, on={0, 1, 2, 3})
          + txt("@p-l", 0, 400, "read as a whole number (4 Bytes)", "m", w=1920, align="center")
          + txt("@p-n", 0, 510, "1,120,403,456", "h", fs=190, w=1920, align="center")
          + txt("@p-c", 0, 790, "nonsense for a health bar", "m", w=1920, align="center"),
          js="""
    blurIn("#@p-l", <<whole>>);
    land("#@p-n", <<billion-0.4>>);
    blurIn("#@p-c", <<nonsense>>);
"""),

    Scene("asfloat", "Read the same four bytes as a float, a number with a decimal point, "
                     "and they say exactly one hundred.",
          body=cells("@p-b", 564, 150, B, 180, 24, on={0, 1, 2, 3})
          + txt("@p-l", 0, 400, "read as a float", "m", w=1920, align="center")
          + txt("@p-n", 0, 500, '<span class="@p-acc">100.0</span>', "h", fs=260, w=1920, align="center")
          + txt("@p-c", 0, 830, "a number with a decimal point", "m", w=1920, align="center"),
          js="""
    blurIn("#@p-l", <<float>>);
    blurIn("#@p-c", <<decimal-0.4>>);
    land("#@p-n", <<exactly>>);
"""),

    Scene("compare", "A whole number one hundred looks completely different: sixty-four, zero, zero, zero. "
                     "Same value on screen, different bytes in memory.",
          body=txt("@p-la", 190, 290, "100 as a<br>whole number", "m")
          + cells("@p-a", 860, 250, ["64", "00", "00", "00"], 170, 22, on={0})
          + txt("@p-lb", 190, 580, "100.0 as a<br>float", "m")
          + cells("@p-b", 860, 540, B, 170, 22, on={2, 3})
          + txt("@p-f", 0, 830, "same number on screen &middot; different bytes", "h", fs=76, w=1920, align="center"),
          js="""
    blurIn("#@p-la", <<whole>>);
    each(".c-@p-a", <<sixty-four>>, 0.4);
    blurIn("#@p-lb", <<same-0.3>>);
    each(".c-@p-b", <<same>>, 0.12);
    blurIn("#@p-f", <<different#2-0.2>>);
"""),

    Scene("endian", "And the bytes run backwards. One thousand is hex three E eight, "
                    "but memory stores the small end first: E eight, zero three.",
          body=txt("@p-t", 0, 150, '1000 = 0x0000<span class="@p-acc">03E8</span>', "h", fs=120, w=1920, align="center")
          + txt("@p-l", 0, 400, "in memory", "m", w=1920, align="center")
          + cells("@p-b", 515, 500, ["E8", "03", "00", "00"], 200, 30, on={0, 1})
          + txt("@p-c", 0, 800, "small end first: little-endian", "m", w=1920, align="center"),
          js="""
    land("#@p-t", <<thousand-0.4>>);
    blurIn("#@p-l", <<memory>>);
    blurIn("#@p-c", <<small>>);
    each(".c-@p-b", <<first+0.4>>, 0.35);
"""),

    Scene("rule", "So when a search finds nothing, change the type. Whole numbers for things you count. "
                  "Floats for things that move.",
          body=txt("@p-t", 190, 90, "no results? change the type.", "h", fs=84)
          + txt("@p-lh", 190, 260, "things you count", "m")
          + card("@p-l0", 190, 350, 520, 100, "ammo") + card("@p-l1", 190, 480, 520, 100, "money")
          + card("@p-l2", 190, 610, 520, 100, "score")
          + tile("@p-lt", 190, 770, 520, 150, "4 Bytes", 76)
          + txt("@p-rh", 1010, 260, "things that move", "m")
          + card("@p-r0", 1010, 350, 520, 100, "position") + card("@p-r1", 1010, 480, 520, 100, "speed")
          + card("@p-r2", 1010, 610, 520, 100, "angle")
          + tile("@p-rt", 1010, 770, 520, 150, "Float", 76),
          js="""
    wipe("#@p-t", <<change-0.3>>, 0.4);
    land("#@p-lt", <<whole>>);
    blurIn("#@p-lh", <<things>>);
    each(["#@p-l0", "#@p-l1", "#@p-l2"], <<things+0.1>>, 0.14);
    land("#@p-rt", <<floats>>);
    blurIn("#@p-rh", <<things#2>>);
    each(["#@p-r0", "#@p-r1", "#@p-r2"], <<things#2+0.1>>, 0.14);
"""),

    Scene("claim", "Memory holds only bytes. The type is how you choose to read them.",
          body=cells("@p-b", 192, 190, B, 120, 18, on={0, 1, 2, 3})
          + txt("@p-a", 192, 400, "Memory holds only bytes.", "h", fs=118)
          + txt("@p-c", 192, 540, '<span class="@p-acc">The type is how you read them.</span>', "h", fs=96),
          js="""
    each(".c-@p-b", 0.3, 0.08);
    wipe("#@p-a", <<memory>>, 0.5);
    wipe("#@p-c", <<type-0.2>>, 0.6);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Same Bytes, Different Number")
