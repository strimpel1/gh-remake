"""Video 8: What's Inside an EXE (PE files, imports).  Run: python build.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, bar, build, card, cells, tile, txt  # noqa: E402,F401

INK = "#0B2A30"

scenes = [
    Scene("hook", "Double-click a game, and Windows has to answer two questions. Where does this file go in memory? "
                  "And what does it need? Both answers are inside the file.",
          body=tile("@p-g", 190, 300, 620, 300, "game.exe", 90)
          + card("@p-q1", 960, 290, 760, 140, "where does it load?", 50)
          + card("@p-q2", 960, 470, 760, 140, "what does it need?", 50)
          + txt("@p-c", 190, 760, "both answers are inside the file", "h", fs=84),
          js="""
    tl.fromTo("#@p-g", { scale: 1 }, { scale: 0.94, duration: 0.1, ease: "power2.out", yoyo: true, repeat: 3 }, 0.5);
    land("#@p-q1", <<where>>);
    land("#@p-q2", <<what>>);
    wipe("#@p-c", <<both>>, 0.7);
"""),

    Scene("headers", "Every Windows program starts with two letters, M Z. A little further in come the headers: "
                     "a table of contents for the whole file. After them, the sections.",
          body=card("@p-r0", 260, 130, 620, 110, "MZ", 60, "on") + txt("@p-d0", 960, 155, "the first two bytes", "m")
          + card("@p-r1", 260, 270, 620, 150, "PE headers", 56) + txt("@p-d1", 960, 315, "the table of contents", "m")
          + card("@p-r2", 260, 450, 620, 110, "section table", 52) + txt("@p-d2", 960, 475, "one row per section", "m")
          + card("@p-r3", 260, 590, 620, 100, ".text", 50, "soft") + card("@p-r4", 260, 710, 620, 100, ".rdata", 50, "soft")
          + card("@p-r5", 260, 830, 620, 100, ".data", 50, "soft") + txt("@p-d3", 960, 730, "the sections", "m"),
          js="""
    land("#@p-r0", <<letters>>);
    blurIn("#@p-d0", <<letters+0.4>>);
    land("#@p-r1", <<headers>>);
    blurIn("#@p-d1", <<table>>);
    land("#@p-r2", <<contents>>);
    blurIn("#@p-d2", <<contents+0.3>>);
    each(["#@p-r3", "#@p-r4", "#@p-r5"], <<sections-0.3>>, 0.15);
    blurIn("#@p-d3", <<sections>>);
"""),

    Scene("sections", "The sections are the body of the file. Dot text holds the code. Dot data holds the variables. "
                      "Each one gets its own permissions when it is loaded.",
          body=txt("@p-t", 190, 90, "the sections", "h", fs=90)
          + card("@p-n0", 190, 280, 360, 130, ".text", 60) + txt("@p-m0", 610, 315, "the code", "m")
          + card("@p-p0", 1330, 280, 300, 130, "R X", 64, "on")
          + card("@p-n1", 190, 480, 360, 130, ".data", 60) + txt("@p-m1", 610, 515, "the variables", "m")
          + card("@p-p1", 1330, 480, 300, 130, "R W", 64, "on")
          + card("@p-n2", 190, 680, 360, 130, ".rdata", 60) + txt("@p-m2", 610, 715, "constants and imports", "m")
          + card("@p-p2", 1330, 680, 300, 130, "R", 64, "on"),
          js="""
    land("#@p-n0", <<text>>);
    blurIn("#@p-m0", <<code>>);
    land("#@p-n1", <<data>>);
    blurIn("#@p-m1", <<variables>>);
    each(["#@p-n2", "#@p-m2"], <<variables+0.6>>, 0.15);
    each(["#@p-p0", "#@p-p1", "#@p-p2"], <<permissions-0.3>>, 0.2);
"""),

    Scene("base", "The headers name a preferred address: the image base. Add an offset from it, called an R V A, "
                  "and you have a real address in memory.",
          body=card("@p-a", 190, 260, 620, 150, "0x00400000", 64) + txt("@p-am", 190, 440, "ImageBase", "m")
          + txt("@p-plus", 850, 280, "+", "h", fs=110)
          + card("@p-b", 960, 260, 420, 150, "0x1530", 64, "on") + txt("@p-bm", 960, 440, "RVA: offset from the base", "m")
          + tile("@p-r", 190, 640, 800, 190, "0x00401530", 90) + txt("@p-rm", 1050, 700, "a real address<br>in memory", "m"),
          js="""
    land("#@p-a", <<preferred>>);
    blurIn("#@p-am", <<base>>);
    blurIn("#@p-plus", <<add>>);
    land("#@p-b", <<offset>>);
    blurIn("#@p-bm", <<called>>);
    land("#@p-r", <<real-0.4>>);
    blurIn("#@p-rm", <<real>>);
"""),

    Scene("imports", "A game does not contain Windows. It only lists the functions it needs, in the import table. "
                     "Windows fills in the real addresses at load time.",
          body=txt("@p-t", 190, 90, "the import table", "h", fs=90)
          + card("@p-n0", 190, 290, 760, 120, "ReadFile", 52) + card("@p-n1", 190, 440, 760, 120, "CreateWindowExA", 52)
          + card("@p-n2", 190, 590, 760, 120, "Direct3DCreate9", 52)
          + bar("@p-b0", 950, 344, 110) + bar("@p-b1", 950, 494, 110) + bar("@p-b2", 950, 644, 110)
          + card("@p-a0", 1060, 290, 620, 120, "0x76A31C20", 52, "on") + card("@p-a1", 1060, 440, 620, 120, "0x75E2B410", 52, "on")
          + card("@p-a2", 1060, 590, 620, 120, "0x6F4C1A90", 52, "on")
          + txt("@p-c", 190, 790, "names in the file, addresses at load time (examples)", "m", fs=40),
          js="""
    wipe("#@p-t", <<import-0.3>>, 0.6);
    each(["#@p-n0", "#@p-n1", "#@p-n2"], <<lists>>, 0.3);
    each(["#@p-b0", "#@p-b1", "#@p-b2"], <<fills>>, 0.15, 1);
    each(["#@p-a0", "#@p-a1", "#@p-a2"], <<fills+0.2>>, 0.25);
    blurIn("#@p-c", <<lists+0.9>>);
"""),

    Scene("tell", "So read the imports, and the file tells on itself. Open process, read process memory, "
                  "write process memory: this program reaches into other programs.",
          body=txt("@p-t", 190, 90, "the imports tell on the file", "h", fs=84)
          + card("@p-n0", 190, 280, 900, 120, "OpenProcess", 54) + card("@p-n1", 190, 430, 900, 120, "ReadProcessMemory", 54)
          + card("@p-n2", 190, 580, 900, 120, "WriteProcessMemory", 54)
          + tile("@p-k", 190, 770, 1300, 160, "reaches into other programs", 60),
          js="""
    wipe("#@p-t", <<tells-0.5>>, 0.6);
    land("#@p-n0", <<open>>);
    land("#@p-n1", <<read#2>>);
    land("#@p-n2", <<write>>);
    land("#@p-k", <<reaches-0.3>>, 1.1);
"""),

    Scene("claim", "An executable is a map of itself. Learn to read the map before you read the code.",
          body=card("@p-a1", 192, 200, 260, 110, "headers", 44, "soft") + card("@p-a2", 480, 200, 260, 110, "sections", 44)
          + card("@p-a3", 768, 200, 260, 110, "imports", 44, "on")
          + txt("@p-a", 192, 400, "An EXE is a map of itself.", "h", fs=110)
          + txt("@p-c", 192, 540, '<span class="@p-acc">Read the map before the code.</span>', "h", fs=96),
          js="""
    each(["#@p-a1", "#@p-a2", "#@p-a3"], 0.3, 0.12);
    wipe("#@p-a", <<executable-0.3>>, 0.8);
    wipe("#@p-c", <<learn>>, 0.8);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "What's Inside an EXE")
