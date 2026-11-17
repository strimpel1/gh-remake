"""Video 5: Read One Line of Assembly.  Run: python build.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, arena, bar, build, card, cells, tile, txt  # noqa: E402,F401

INK = "#0B2A30"
SPAN = "\n    .@p-m span { display: inline-block; }\n"


def line(y, fs=120):
    """The instruction, 19 characters wide, starting at x=276 when fs=120."""
    return txt("@p-ln", 276, y, '<span id="@p-x1">mov</span> <span id="@p-x2">[ebx+0xEC]</span>, <span id="@p-x3">eax</span>',
               "m", fs=fs, color=INK)


scenes = [
    Scene("hook", "Somewhere in the game, one instruction takes away your health. "
                  "Read that one line, and you understand the whole trick.",
          bg="arena",
          body=arena("100")
          + txt("@p-d", 640, 640, '-25', "h", fs=170)
          + card("@p-q", 1010, 150, 720, 120, "one instruction", 56)
          + card("@p-r", 1010, 310, 720, 120, "? ? ? &nbsp; ? ? ?", 60, "on"),
          js="""
    land("#@p-q", <<instruction-0.3>>);
    land("#@p-d", <<takes>>, 1.6);
    tl.fromTo("#@p-hudn", { scale: 1 }, { scale: 0.92, duration: 0.15, ease: "power2.out", yoyo: true, repeat: 1 }, <<takes>>);
    land("#@p-r", <<read>>);
    tl.fromTo("#@p-r", { rotation: 0 }, { rotation: -3, duration: 0.25, ease: "power2.out" }, <<whole>>);
"""),

    Scene("theline", "Here it is. Move, into the memory at E B X plus E C, the value of E A X.",
          css=SPAN,
          body=line(400) + txt("@p-c", 276, 600, "one line of assembly", "m"),
          js="""
    blurIn("#@p-c", <<here>>);
    blurIn("#@p-x1", <<move>>);
    blurIn("#@p-x2", <<memory>>);
    blurIn("#@p-x3", <<value>>);
"""),

    Scene("order", "Destination comes first, source second. So this line copies E A X into something.",
          css=SPAN,
          body=line(340)
          + bar("@p-b1", 564, 500, 720) + txt("@p-l1", 564, 530, "destination", "m")
          + bar("@p-b2", 1428, 500, 216) + txt("@p-l2", 1428, 530, "source", "m")
          + txt("@p-c", 0, 800, "destination first, source second", "h", fs=80, w=1920, align="center"),
          js="""
    wipe("#@p-b1", <<destination>>, 0.3);
    blurIn("#@p-l1", <<destination>>);
    wipe("#@p-b2", <<source>>, 0.3);
    blurIn("#@p-l2", <<source>>);
    wipe("#@p-c", <<copies-0.3>>, 0.7);
"""),

    Scene("brackets", "Square brackets mean memory. Not the register itself, but the address stored inside it.",
          css=SPAN + "\n    .@p-card { line-height: 1.25 !important; }\n",
          body=line(170)
          + txt("@p-c", 276, 370, '<span class="@p-acc">[ ]</span> means memory', "h", fs=90)
          + txt("@p-reg", 276, 620, "ebx = 0x0A3F2000", "m", fs=60, color=INK)
          + bar("@p-b", 880, 652, 200)
          + tile("@p-mem", 1100, 580, 560, 160, "0x0A3F20EC", 60)
          + txt("@p-n", 276, 800, "the register holds an address; the brackets go there", "m", fs=46),
          js="""
    wipe("#@p-c", <<square>>, 0.5);
    blurIn("#@p-reg", <<register>>);
    wipe("#@p-b", <<address>>, 0.25);
    land("#@p-mem", <<stored>>);
    blurIn("#@p-n", <<not>>);
"""),

    Scene("twofacts", "E B X holds the start of the player. E C is the offset of health. One line just told you both.",
          css=SPAN,
          body=line(170)
          + card("@p-c1", 276, 430, 620, 140, "ebx", 76, "on") + txt("@p-m1", 276, 600, "start of the player", "m")
          + card("@p-c2", 1024, 430, 620, 140, "0xEC", 76, "on") + txt("@p-m2", 1024, 600, "offset of health", "m")
          + txt("@p-c", 0, 800, "one line told you both", "h", fs=84, w=1920, align="center"),
          js="""
    land("#@p-c1", <<holds-0.6>>);
    blurIn("#@p-m1", <<start>>);
    land("#@p-c2", <<offset-0.7>>);
    blurIn("#@p-m2", <<offset>>);
    wipe("#@p-c", <<one>>, 0.6);
"""),

    Scene("three", "Two lines earlier, a subtract: health minus damage. Then this line stores the result.",
          body=card("@p-c1", 190, 230, 900, 130, "mov eax, [ebx+0xEC]", 58) + txt("@p-n1", 1150, 262, "read health", "m")
          + card("@p-c2", 190, 400, 900, 130, "sub eax, edi", 58) + txt("@p-n2", 1150, 432, "subtract the damage", "m")
          + card("@p-c3", 190, 570, 900, 130, "mov [ebx+0xEC], eax", 58, "on") + txt("@p-n3", 1150, 602, "store the result", "m")
          + txt("@p-c", 190, 810, "read, subtract, store", "h", fs=84),
          js="""
    land("#@p-c1", <<two>>);
    blurIn("#@p-n1", <<earlier>>);
    land("#@p-c2", <<subtract>>);
    blurIn("#@p-n2", <<minus>>);
    blurIn("#@p-n3", <<stores>>);
    wipe("#@p-c", <<result-0.4>>, 0.6);
"""),

    Scene("nop", "Replace the store with no-ops, the instruction that does nothing, and health stops dropping. "
                 "Six bytes out, six no-ops in.",
          body=card("@p-ln", 190, 150, 900, 130, "mov [ebx+0xEC], eax", 58)
          + txt("@p-l0", 1150, 182, "6 bytes", "m")
          + cells("@p-o", 190, 370, ["89", "83", "EC", "00", "00", "00"], 150, 20)
          + txt("@p-l1", 1250, 410, "the store", "m")
          + cells("@p-n", 190, 610, ["90"] * 6, 150, 20, on={0, 1, 2, 3, 4, 5})
          + txt("@p-l2", 1250, 630, "six NOPs:<br>do nothing", "m")
          + txt("@p-c", 190, 850, "same length, or the game crashes", "m"),
          js="""
    each(".c-@p-o", 0.5, 0.07);
    blurIn("#@p-l0", 0.9);
    blurIn("#@p-l1", <<store>>);
    each(".c-@p-n", <<store+0.5>>, 0.12);
    blurIn("#@p-l2", <<nothing-0.4>>);
    dim(".c-@p-o", <<stops>>, 0.35);
    blurIn("#@p-c", <<six>>);
"""),

    Scene("careful", "But careful. The same code runs for enemies too. E B X is whoever just got hit.",
          body=txt("@p-t", 190, 110, "careful", "h", fs=110)
          + card("@p-k", 360, 330, 1200, 160, "ebx = whoever got hit", 70, "on")
          + card("@p-a", 360, 560, 560, 130, "the player", 54)
          + card("@p-b", 1000, 560, 560, 130, "or an enemy", 54)
          + txt("@p-c", 0, 800, "the same code runs for everyone", "h", fs=80, w=1920, align="center"),
          js="""
    land("#@p-a", <<same>>);
    land("#@p-b", <<enemies>>);
    land("#@p-k", <<whoever-0.6>>, 1.15);
    wipe("#@p-c", <<whoever>>, 0.7);
"""),

    Scene("claim", "Destination, brackets, offset. Read those three, and you can read the line.",
          css=SPAN,
          body=line(190, 100)
          + txt("@p-a", 192, 420, "Destination, brackets, offset.", "h", fs=100)
          + txt("@p-c", 192, 560, '<span class="@p-acc">Read those, and you can read the line.</span>', "h", fs=78),
          js="""
    blurIn("#@p-ln", 0.3);
    wipe("#@p-a", <<destination>>, 1.6);
    wipe("#@p-c", <<read-0.2>>, 0.8);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Read One Line of Assembly")
