"""Game Hacking from Scratch, episode 4: Inside the Files (hex editing a save file + PE files, processes and the Windows API).

Long-form YouTube episode. Every screenshot and number is real: lab/savegame.cpp and its save.dat opened and edited in ImHex,
dumpbin (MSVC) on savegame.exe, on the practice game's ac_client.exe (read only, never modified) and on Cheat Engine,
lab/loaded.cpp printing its own process, and the memory map captured in episode 2.   Run: python build.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, Shot, bar, build, card, cells, tag, term, tile, txt  # noqa: E402,F401

A = Path(__file__).resolve().parent / "assets"

# ---- geometry of the hex pane in the ImHex screenshots (pixels of the cropped images, all cut at the same origin)
G = dict(off_x=6, off_w=126, b0=160, bw=41, mid=13, a0=838, aw=13.7, r0=58, rh=32)


def hx(name, y=250, rows=None, x=120, w=1680, id="@p-hx"):
    """A hex-pane screenshot. rows=n keeps the column header and the first n rows."""
    from PIL import Image
    W, H = Image.open(A / f"shots/{name}.png").size
    crop = (0, 0, W, G["r0"] + rows * G["rh"] - 1) if rows else None
    return Shot(id, A / f"shots/{name}.png", x, y, w, crop=crop)


def bx(c):
    return G["b0"] + c * G["bw"] + (G["mid"] if c >= 8 else 0)


def mb(s, id, row, c0, c1, pad=6):
    """Mark bytes c0..c1 (inclusive) of a row."""
    return s.mark(id, bx(c0) - 4, G["r0"] + row * G["rh"], bx(c1) - bx(c0) + 32, G["rh"] - 4, pad=pad)


def ma(s, id, row, c0, c1, pad=6):
    """Mark the text column of a row, characters c0..c1."""
    return s.mark(id, round(G["a0"] + c0 * G["aw"]) - 3, G["r0"] + row * G["rh"], round((c1 - c0 + 1) * G["aw"]) + 6, G["rh"] - 4, pad=pad)


def HI(s):
    return f'<span class="hi">{s}</span>'


def DIM(s):
    return f'<span class="dimc">{s}</span>'


STRUCT = ["struct Save {",
          "    char magic[4];    " + DIM("// offset 00: the letters S A V E"),
          "    int  health;      " + DIM("// offset 04: 4 bytes"),
          "    int  gold;        " + DIM("// offset 08: 4 bytes"),
          "    char name[16];    " + DIM("// offset 0C: text"),
          "};                    " + DIM("// 28 bytes in total")]

NEW = ["&gt; savegame new", "wrote save.dat (28 bytes)", "health  " + HI("100"), "gold    " + HI("1000"), "name    " + HI("Hero")]
LOAD = ["&gt; savegame", "loaded save.dat (28 bytes)", "health  100", "gold    " + HI("9999"), "name    Hero"]
BROKEN = ["&gt; savegame", "loaded save.dat (28 bytes)", "health  100", "gold    " + HI("256000"), "name    "]

HEADERS = ["&gt; dumpbin /headers ac_client.exe",
           DIM("FILE HEADER VALUES"),
           "     " + HI("14C") + " machine (x86)",
           "       " + HI("5") + " number of sections",
           DIM("OPTIONAL HEADER VALUES"),
           "   2E5F3 entry point (" + HI("0042E5F3") + ")",
           "  " + HI("400000") + " image base (00400000 to 005B8FFF)"]

SECTIONS = [DIM("SECTION HEADER #1"),
            "   " + HI(".text") + " name",
            "    1000 virtual address (" + HI("00401000") + " to 005247AD)",
            "     400 file pointer to raw data",
            "         " + HI("Execute Read"),
            DIM("SECTION HEADER #2"),
            "  " + HI(".rdata") + " name",
            "  125000 virtual address (" + HI("00525000") + " to 0056A1FB)",
            "         " + HI("Read Only"),
            DIM("SECTION HEADER #3"),
            "   " + HI(".data") + " name",
            "  16B000 virtual address (" + HI("0056B000") + " to 005A49CB)",
            "         " + HI("Read Write")]

FIXED = [DIM("ac_client.exe"), "  400000 image base", "     103 characteristics", "           " + HI("Relocations stripped")]
MOVES = [DIM("savegame.exe"), "  140000000 image base", "       8160 DLL characteristics", "              " + HI("Dynamic base")]

LOADED = ["&gt; loaded.exe",
          "process id        47652",
          "thread id         36512",
          "loaded at         " + HI("7FF7F5070000"),
          "first bytes there " + HI('4D 5A  "MZ"'),
          "modules in this process:",
          "  7FF7F5070000  loaded.exe",
          "  7FFD94360000  ntdll.dll",
          "  7FFD93AF0000  " + HI("KERNEL32.DLL"),
          "  7FFD919B0000  KERNELBASE.dll"]

IMPORTS = ["&gt; dumpbin /imports savegame.exe",
           "    " + HI("KERNEL32.dll"),
           "         E9 " + HI("CreateFileW"),
           "        663 " + HI("WriteFile"),
           "        4AC " + HI("ReadFile"),
           "         A0 CloseHandle",
           DIM("        ... 75 functions in all")]

GAMEIMP = ["&gt; dumpbin /imports ac_client.exe",
           "    " + HI("OPENGL32.dll") + "      4A glDrawElements",
           "    " + HI("OpenAL32.dll") + "      3E alSourcePlay",
           "    " + HI("SDL2.dll") + "          39 SDL_CreateWindow",
           "    " + HI("WS2_32.dll") + "        " + DIM("(by number)"),
           "    " + HI("KERNEL32.dll") + "      CE CreateFileW",
           "    " + HI("USER32.dll") + "       281 MessageBoxA",
           DIM("    ... 13 DLLs in all")]

CEIMP = ["&gt; dumpbin /imports cheatengine-x86_64.exe",
         "    kernel32.dll",
         "          0 " + HI("OpenProcess"),
         "          0 " + HI("ReadProcessMemory"),
         "          0 " + HI("WriteProcessMemory")]

REG = (0, 40, 1284, 390)          # episode 2's memory regions screenshot: header + the module rows


def regions(y=230):
    return Shot("@p-rg", A / "shots/ep02_regions_mod.png", 120, y, 1680, crop=REG)


def byte_row(pfx, y, vals, on=(), size=120, gap=16, x=190):
    return cells(pfx, x, y, vals, size=size, gap=gap, on=on)


scenes = [
    # ------------------------------------------------------------------ cold open
    Scene("cold", "This is the save file of a tiny game. Twenty-eight bytes. And these four bytes are my gold: one thousand.",
          body=txt("@p-t", 120, 96, "a save file: 28 bytes", "h", fs=80) + hx("save_before", 250).html()
          + mb(hx("save_before", 250), "@p-m1", 0, 8, 11)
          + cells("@p-b", 120, 640, ["E8", "03", "00", "00"], size=150, gap=20, on=range(4))
          + txt("@p-kl", 850, 660, "= 1000 gold", "h", fs=100),
          js="""
    land("#@p-m1", <<these>>, 1.3);
    each(".c-@p-b", <<four>>, 0.1);
    blurIn("#@p-kl", <<thousand-0.3>>);
"""),

    Scene("cold2", "I type over two of them, load the save, and now I have nine thousand, nine hundred ninety-nine. "
                   "The game was not even running.",
          body=txt("@p-t", 120, 96, "two bytes later", "h", fs=80) + hx("save_after", 250).html()
          + mb(hx("save_after", 250), "@p-m1", 0, 8, 9)
          + term("@p-o", 120, 590, 900, LOAD, fs=44)
          + txt("@p-kl", 1100, 700, 'gold: <span class="@p-acc">9999</span>', "h", fs=100)
          + txt("@p-g", 1100, 840, "edited on disk,<br>game closed", "m", fs=50),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-hx", 0.2, 1.03, 0.5);
    land("#@p-m1", <<two>>, 1.3);
    land("#@p-o", <<load-0.2>>, 1.03, 0.4);
    blurIn("#@p-kl", <<nine>>);
    blurIn("#@p-g", <<running-0.6>>);
"""),

    Scene("hook", "A file on disk is just bytes: the same bytes we have been reading in memory. Today we open two files: "
                  "a save file, and an executable.",
          body=txt("@p-a", 192, 220, "A file is", "h", fs=130) + txt("@p-b", 192, 380, 'just <span class="@p-acc">bytes</span>.', "h", fs=130)
          + card("@p-c", 192, 660, 620, 170, "save.dat", 70, "on") + card("@p-d", 900, 660, 620, 170, "game.exe", 70, "on")
          + txt("@p-e", 192, 890, "today: we open both", "m", fs=60),
          js="""
    wipe("#@p-a", <<file-0.2>>, 0.5);
    wipe("#@p-b", <<just-0.2>>, 0.6);
    land("#@p-c", <<save>>); land("#@p-d", <<executable-0.5>>);
    blurIn("#@p-e", <<today>>);
"""),

    Scene("title", "This is Game Hacking from Scratch. Episode four: inside the files.",
          body=txt("@p-s", 192, 250, "GAME HACKING FROM SCRATCH", "m", fs=64)
          + txt("@p-a", 192, 360, "Inside", "h", fs=150) + txt("@p-b", 192, 520, 'the <span class="@p-acc">Files</span>', "h", fs=150)
          + tile("@p-e", 192, 760, 420, 130, "EPISODE 4", 60),
          js="""
    blurIn("#@p-s", <<game>>);
    wipe("#@p-a", <<inside-0.3>>, 0.6);
    wipe("#@p-b", <<files-0.3>>, 0.6);
    land("#@p-e", <<episode>>);
"""),

    # ------------------------------------------------------------------ part 1: the save file
    Scene("code", "Here is our game: one small C plus plus program. Its whole state is one structure: four letters, "
                  "the health, the gold, and a name of up to sixteen characters. Twenty-eight bytes.",
          body=txt("@p-t", 120, 80, "savegame.cpp: the whole game state", "h", fs=76)
          + term("@p-o", 120, 230, 1680, STRUCT, fs=46, lh=1.6)
          + tag("@p-g1", 120, 770, "an excerpt: the full file is in the description", 40)
          + txt("@p-c", 120, 900, "4 + 4 + 4 + 16 = 28 bytes", "m", fs=60),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", <<program-0.6>>, 1.03, 0.5);
    tl.fromTo(["#@p-o-l1"], { opacity: 0.35 }, { opacity: 1, duration: 0.3 }, <<four>>);
    tl.fromTo(["#@p-o-l2"], { opacity: 0.35 }, { opacity: 1, duration: 0.3 }, <<health>>);
    tl.fromTo(["#@p-o-l3"], { opacity: 0.35 }, { opacity: 1, duration: 0.3 }, <<gold>>);
    tl.fromTo(["#@p-o-l4"], { opacity: 0.35 }, { opacity: 1, duration: 0.3 }, <<name>>);
    land("#@p-g1", <<structure>>);
    blurIn("#@p-c", <<twenty-eight-0.2>>);
"""),

    Scene("new", "Run it with the word new, and it writes those twenty-eight bytes into a file called save dot dat. "
                 "Health, one hundred. Gold, one thousand. Name, Hero.",
          body=txt("@p-t", 120, 96, "a fresh save", "h", fs=90)
          + term("@p-o", 120, 280, 1000, NEW, fs=56, lh=1.6)
          + card("@p-f", 1260, 400, 480, 200, "save.dat", 70, "on") + txt("@p-fl", 1260, 640, "28 bytes on disk", "m", fs=50),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", <<run-0.2>>, 1.03, 0.5);
    tl.fromTo(["#@p-o-l1"], { opacity: 0 }, { opacity: 1, duration: 0.25 }, <<writes>>);
    land("#@p-f", <<file>>); blurIn("#@p-fl", <<save>>);
    tl.fromTo(["#@p-o-l2"], { opacity: 0 }, { opacity: 1, duration: 0.25 }, <<health>>);
    tl.fromTo(["#@p-o-l3"], { opacity: 0 }, { opacity: 1, duration: 0.25 }, <<gold>>);
    tl.fromTo(["#@p-o-l4"], { opacity: 0 }, { opacity: 1, duration: 0.25 }, <<name>>);
"""),

    Scene("editor", "Now I open that file in a hex editor. This one is Im Hex: free, and open source.",
          body=txt("@p-t", 120, 96, "save.dat in a hex editor", "h", fs=80) + Shot("@p-hx", A / "shots/save_window.png", 120, 230, 1680, crop=(0, 0, 2460, 1130)).html()
          + tag("@p-g1", 1180, 110, "ImHex: free, open source", 40),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-hx", 0.2, 1.03, 0.5);
    land("#@p-g1", <<im>>);
"""),

    Scene("columns", "It looks just like the memory viewer from episode one. On the left, the offset: the distance from the start of the file. "
                     "The second row starts at offset ten in hex: sixteen bytes in. In the middle, the bytes, "
                     "sixteen in a row. And on the right, the same bytes as text.",
          body=txt("@p-t", 120, 96, "three columns", "h", fs=80) + hx("save_before", 250).html()
          + hx("save_before", 250).mark("@p-m1", G["off_x"], G["r0"], G["off_w"], 2 * G["rh"] - 4, pad=4)
          + hx("save_before", 250).mark("@p-m2", bx(0) - 6, G["r0"], bx(15) + 36 - bx(0), 2 * G["rh"] - 4, pad=4)
          + hx("save_before", 250).mark("@p-m3", G["a0"] - 6, G["r0"], 232, 2 * G["rh"] - 4, pad=4)
          + tag("@p-g1", 120, 620, "offset") + tag("@p-g2", 640, 620, "the bytes, 16 per row") + tag("@p-g3", 1380, 620, "as text")
          + txt("@p-c", 120, 800, 'offset = <span class="@p-acc">distance from the start of the file</span>', "m", fs=56)
          + txt("@p-d", 120, 900, "row 2 starts at offset 10 (hex) = 16 bytes in", "m", fs=50),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-hx", 0.2, 1.03, 0.5);
    land("#@p-m1", <<left>>, 1.05); land("#@p-g1", <<offset>>);
    blurIn("#@p-c", <<distance>>); blurIn("#@p-d", <<second>>);
    land("#@p-m2", <<middle>>, 1.05); land("#@p-g2", <<bytes>>);
    land("#@p-m3", <<right>>, 1.05); land("#@p-g3", <<text>>);
"""),

    Scene("fields", "Now read it. Five three, four one, five six, four five: the letters "
                    "of the word SAVE. Six four, and three zeros: one hundred, the health. E eight, zero three, and two zeros: one thousand, "
                    "the gold, lowest byte first. And then the name: Hero.",
          body=txt("@p-t", 190, 70, "reading the save file", "h", fs=80)
          + byte_row("@p-a", 220, ["53", "41", "56", "45"]) + txt("@p-al", 800, 250, '"SAVE"', "h", fs=70) + txt("@p-ao", 1250, 262, "offset 00", "m", fs=46)
          + byte_row("@p-b", 430, ["64", "00", "00", "00"]) + txt("@p-bl", 800, 460, "100 health", "h", fs=70) + txt("@p-bo", 1250, 472, "offset 04", "m", fs=46)
          + byte_row("@p-c", 640, ["E8", "03", "00", "00"], on=range(4)) + txt("@p-cl", 800, 670, "1000 gold", "h", fs=70) + txt("@p-co", 1250, 682, "offset 08", "m", fs=46)
          + byte_row("@p-d", 850, ["48", "65", "72", "6F"]) + txt("@p-dl", 800, 880, '"Hero"', "h", fs=70) + txt("@p-do", 1250, 892, "offset 0C", "m", fs=46),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    each(".c-@p-a", <<five>>, 0.45); blurIn("#@p-al", <<letters>>); blurIn("#@p-ao", <<letters+0.3>>);
    each(".c-@p-b", <<six>>, 0.12); blurIn("#@p-bl", <<hundred-0.3>>); blurIn("#@p-bo", <<health>>);
    each(".c-@p-c", <<eight>>, 0.3); blurIn("#@p-cl", <<thousand-0.3>>); blurIn("#@p-co", <<gold>>);
    each(".c-@p-d", <<name-0.2>>, 0.08); blurIn("#@p-dl", <<hero-0.2>>); blurIn("#@p-do", <<hero>>);
"""),

    Scene("map", "So the file is the structure, byte for byte. The letters at offset zero. Health at offset four. Gold at offset eight. "
                 "The name at offset C. No labels in there. Only the values, in order.",
          body=txt("@p-t", 190, 100, "the file is the structure", "h", fs=90)
          + card("@p-f0", 190, 400, 220, 170, "SAVE", 50) + card("@p-f1", 410, 400, 220, 170, "health", 44) + card("@p-f2", 630, 400, 220, 170, "gold", 50, "on")
          + card("@p-f3", 850, 400, 880, 170, "name", 50, "soft")
          + "".join(txt(f"@p-o{i}", x, 320, o, "m", fs=50) for i, (x, o) in enumerate(((190, "00"), (410, "04"), (630, "08"), (850, "0C"))))
          + "".join(txt(f"@p-z{i}", x, 600, o, "m", fs=40, color="#6A9188") for i, (x, o) in enumerate(((190, "4 bytes"), (410, "4 bytes"), (630, "4 bytes"), (850, "16 bytes"))))
          + txt("@p-c", 190, 760, "no labels in the file", "m", fs=60)
          + txt("@p-d", 190, 860, 'only the <span class="@p-acc">values, in order</span>', "h", fs=76),
          js="""
    wipe("#@p-t", <<file-0.2>>, 0.6);
    land("#@p-f0", <<letters>>, 1.1); blurIn("#@p-o0", <<zero>>); blurIn("#@p-z0", <<zero>>);
    land("#@p-f1", <<health>>, 1.1); blurIn("#@p-o1", <<four>>); blurIn("#@p-z1", <<four>>);
    land("#@p-f2", <<gold>>, 1.1); blurIn("#@p-o2", <<eight>>); blurIn("#@p-z2", <<eight>>);
    land("#@p-f3", <<name>>, 1.05); blurIn("#@p-o3", <<c>>); blurIn("#@p-z3", <<c>>);
    blurIn("#@p-c", <<labels>>);
    wipe("#@p-d", <<only-0.2>>, 0.6);
"""),

    Scene("plan", "I want nine thousand, nine hundred ninety-nine gold. In hex, that is two seven zero F. "
                  "Stored little endian, in four bytes: zero F, two seven, zero zero, zero zero.",
          body=txt("@p-t", 190, 100, "the plan: 9999 gold", "h", fs=90)
          + tile("@p-a", 190, 320, 420, 170, "9999", 100) + txt("@p-eq", 660, 340, "=", "h", fs=100) + card("@p-h", 780, 330, 520, 150, "0x270F", 84)
          + cells("@p-b", 190, 620, ["0F", "27", "00", "00"], size=170, gap=24, on=(0, 1))
          + txt("@p-l", 1010, 660, "little endian:<br>lowest byte first", "m", fs=54),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-a", <<nine>>);
    blurIn("#@p-eq", <<hex-0.2>>); land("#@p-h", <<two>>);
    blurIn("#@p-l", <<little>>);
    land("#@p-b0", <<zero#2>>); land("#@p-b1", <<two#2>>); land("#@p-b2", <<zero#3>>); land("#@p-b3", <<zero#5>>);
"""),

    Scene("edit", "First I copy the file: always keep a backup. Then, in the editor, I click the byte at offset eight, and type over it. "
                  "E eight becomes zero F. Zero three becomes two seven. And I save the file.",
          body=txt("@p-t", 120, 80, "typing over the gold", "h", fs=80)
          + txt("@p-l1", 120, 200, "before", "m", fs=44) + hx("save_before", 260, id="@p-h1").html()
          + mb(hx("save_before", 260, id="@p-h1"), "@p-m1", 0, 8, 9)
          + txt("@p-l2", 120, 560, "after", "m", fs=44) + hx("save_after", 620, id="@p-h2").html()
          + mb(hx("save_after", 620, id="@p-h2"), "@p-m2", 0, 8, 9)
          + tag("@p-g1", 1000, 100, "backup first: copy save.dat save.bak", 36)
          + txt("@p-c", 120, 950, "E8 03 00 00 &nbsp;&rarr;&nbsp; 0F 27 00 00", "m", fs=56, color="#E8490F")
          + txt("@p-n", 1180, 880, "red in ImHex = changed,<br>not saved yet", "m", fs=38, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-h1", 0.2, 1.03, 0.5); blurIn("#@p-l1", 0.3); land("#@p-g1", <<copy>>);
    land("#@p-m1", <<offset>>, 1.3);
    blurIn("#@p-l2", <<becomes-0.3>>); land("#@p-h2", <<becomes-0.3>>, 1.03, 0.4);
    land("#@p-m2", <<becomes>>, 1.3);
    blurIn("#@p-c", <<becomes#2>>); blurIn("#@p-n", <<becomes#2+0.5>>);
"""),

    Scene("load", "Now run the game again, without the word new, so it loads the file. Gold: nine thousand, nine hundred ninety-nine. "
                  "The program simply believes the bytes it finds.",
          body=txt("@p-t", 120, 96, "loading the edited save", "h", fs=90)
          + term("@p-o", 120, 280, 1000, LOAD, fs=56, lh=1.6)
          + tile("@p-k", 1220, 380, 520, 190, "9999", 120) + txt("@p-kl", 1220, 610, "was 1000", "m", fs=54)
          + txt("@p-c", 120, 880, 'a program <span class="@p-acc">believes the bytes it finds</span>', "h", fs=64),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", <<run-0.2>>, 1.03, 0.5);
    tl.fromTo(["#@p-o-l1", "#@p-o-l2", "#@p-o-l3", "#@p-o-l4"], { opacity: 0 }, { opacity: 1, duration: 0.25, stagger: 0.1 }, <<loads-0.3>>);
    land("#@p-k", <<nine>>); blurIn("#@p-kl", <<ninety-nine>>);
    wipe("#@p-c", <<simply-0.3>>, 0.7);
"""),

    Scene("insert", "One rule: type over bytes, never insert them. The program expects the gold at offset eight. "
                    "In a copy, I inserted a single zero byte in front of it. Everything slid one place. "
                    "The gold became two hundred fifty-six thousand, and the name is gone.",
          body=txt("@p-t", 120, 70, "type over, never insert", "h", fs=84)
          + txt("@p-l1", 120, 215, "offset 08 &darr;", "m", fs=40, color="#6A9188")
          + cells("@p-a", 120, 280, ["E8", "03", "00", "00", "48", "65", "72", "6F"], size=110, gap=14, on=range(4))
          + cells("@p-b", 120, 450, ["00", "E8", "03", "00", "00", "48", "65", "72"], size=110, gap=14, on=(1, 2, 3, 4))
          + txt("@p-bl", 1150, 470, "one byte inserted:<br>everything slides", "m", fs=44)
          + term("@p-o", 120, 640, 900, BROKEN, fs=44)
          + txt("@p-c", 1100, 760, '00 E8 03 00<br>= <span class="@p-acc">256000</span>', "m", fs=60),
          js="""
    wipe("#@p-t", <<rule-0.2>>, 0.6);
    each(".c-@p-a", <<type>>, 0.05); blurIn("#@p-l1", <<expects>>);
    each(".c-@p-b", <<inserted-0.3>>, 0.05); blurIn("#@p-bl", <<everything-0.2>>);
    land("#@p-o", <<slid-0.3>>, 1.03, 0.4);
    blurIn("#@p-c", <<became>>);
"""),

    Scene("guards", "Real games add obstacles. Many store a checksum: a number calculated from the whole file. Change one byte, "
                    "and the game calls the save corrupted. Others compress or encrypt their saves: you see no readable text, only noise.",
          body=txt("@p-t", 190, 100, "what real save files add", "h", fs=90)
          + card("@p-a", 190, 320, 520, 150, "checksum", 60, "on") + txt("@p-al", 770, 330, "a number calculated from the file:<br>edit a byte, and it no longer matches", "m", fs=44)
          + card("@p-b", 190, 540, 520, 150, "compression", 56, "on") + txt("@p-bl", 770, 580, "the bytes are packed", "m", fs=44)
          + card("@p-c", 190, 760, 520, 150, "encryption", 56, "on") + txt("@p-cl", 770, 800, "the bytes are scrambled", "m", fs=44)
          + txt("@p-d", 190, 960, "no readable text, only noise? packed or scrambled", "m", fs=44, color="#E8490F"),
          js="""
    wipe("#@p-t", <<real-0.2>>, 0.6);
    land("#@p-a", <<checksum-0.2>>); blurIn("#@p-al", <<calculated-0.2>>);
    land("#@p-b", <<compress-0.2>>); blurIn("#@p-bl", <<compress>>);
    land("#@p-c", <<encrypt-0.2>>); blurIn("#@p-cl", <<encrypt>>);
    blurIn("#@p-d", <<noise-0.4>>);
"""),

    # ------------------------------------------------------------------ part 2: the EXE
    Scene("mz", "The program is a file too. Here is savegame dot E X E, in the hex editor. "
                "The first two bytes: four D, five A. The letters M Z. Every E X E and every D L L on Windows starts with them. "
                "And just below, a message: this program cannot be run in DOS mode.",
          body=txt("@p-t", 120, 80, "savegame.exe is a file too", "h", fs=80) + hx("exe_head", 220, rows=8).html()
          + mb(hx("exe_head", 220, rows=8), "@p-m1", 0, 0, 1)
          + ma(hx("exe_head", 220, rows=8), "@p-m2", 0, 0, 1)
          + hx("exe_head", 220, rows=8).mark("@p-m3", G["a0"] - 6, G["r0"] + 4 * G["rh"], 232, 4 * G["rh"] - 4, pad=4)
          + tile("@p-k", 120, 800, 360, 170, "4D 5A", 80) + txt("@p-kl", 540, 830, '= "MZ"', "h", fs=90)
          + txt("@p-c", 1000, 830, "every EXE and DLL<br>starts with MZ", "m", fs=50),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-hx", <<here-0.3>>, 1.03, 0.5);
    land("#@p-m1", <<first>>, 1.3); land("#@p-k", <<four>>);
    land("#@p-m2", <<letters-0.2>>, 1.3); blurIn("#@p-kl", <<letters>>);
    blurIn("#@p-c", <<every>>);
    land("#@p-m3", <<message-0.2>>, 1.05);
"""),

    Scene("pe", "The format is called P E: portable executable. Think of it as a table of contents. It tells Windows which parts "
                "of the file to load, where each part goes in memory, and where to start running.",
          body=txt("@p-t", 190, 80, "the PE format", "h", fs=96)
          + card("@p-a", 190, 250, 760, 100, 'DOS header: "MZ"', 44, "soft")
          + card("@p-b", 190, 370, 760, 100, 'PE header: "PE"', 44, "on")
          + card("@p-c", 190, 490, 760, 100, "section table", 44, "on")
          + card("@p-d", 190, 610, 760, 100, ".text &nbsp; code", 44)
          + card("@p-e", 190, 730, 760, 100, ".rdata &nbsp; constants", 44)
          + card("@p-f", 190, 850, 760, 100, ".data &nbsp; globals", 44)
          + txt("@p-x", 1040, 280, "PE = Portable<br>Executable", "h", fs=64)
          + txt("@p-y", 1040, 520, "what to load", "m", fs=54) + txt("@p-z", 1040, 620, "where it goes in memory", "m", fs=54)
          + txt("@p-w", 1040, 720, "where to start running", "m", fs=54),
          js="""
    wipe("#@p-t", <<format-0.2>>, 0.6);
    each(["#@p-a", "#@p-b", "#@p-c", "#@p-d", "#@p-e", "#@p-f"], <<called>>, 0.15, 1.1);
    blurIn("#@p-x", <<portable>>);
    blurIn("#@p-y", <<which>>); blurIn("#@p-z", <<where>>); blurIn("#@p-w", <<start>>);
"""),

    Scene("pesig", "At offset three C, the file says where its real header begins: F eight. Go to offset F eight, and there it is. "
                   "Five zero, four five. The letters P E.",
          body=txt("@p-t", 120, 60, "from MZ to PE", "h", fs=76) + hx("exe_head", 170, x=360, w=1200).html()
          + mb(hx("exe_head", 170, x=360, w=1200), "@p-m1", 3, 12, 12)
          + mb(hx("exe_head", 170, x=360, w=1200), "@p-m2", 15, 8, 9)
          + ma(hx("exe_head", 170, x=360, w=1200), "@p-m3", 15, 8, 9)
          + tag("@p-g1", 1600, 310, "offset 3C:<br>F8", 40) + tag("@p-g2", 1600, 730, 'offset F8:<br>50 45 "PE"', 36),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-hx", 0.2, 1.03, 0.5);
    land("#@p-m1", <<three>>, 1.5); land("#@p-g1", <<begins>>);
    land("#@p-m2", <<go>>, 1.5); land("#@p-m3", <<letters>>, 1.5); land("#@p-g2", <<five>>);
"""),

    Scene("dumpbin", "Nobody reads those headers by hand. Dump bin, a tool that comes with Visual Studio, prints them. "
                     "Here it is on our practice game. We only read that file.",
          body=txt("@p-t", 120, 80, "dumpbin reads the headers for us", "h", fs=76)
          + term("@p-o", 120, 230, 1300, HEADERS, fs=44, lh=1.55)
          + tag("@p-g1", 1470, 240, "real output,<br>shortened", 36)
          + txt("@p-c", 120, 850, "ac_client.exe: read only, never modified", "m", fs=54),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", <<dump-0.3>>, 1.03, 0.5);
    land("#@p-g1", <<prints>>);
    blurIn("#@p-c", <<only>>);
""", exit=False),

    Scene("headers", "Machine: x eighty-six, so a thirty-two bit program. Five sections. An entry point: the address of the first instruction "
                     "that will run. And the image base: four hundred thousand, in hex.",
          body=txt("@p-t", 120, 80, "dumpbin reads the headers for us", "h", fs=76)
          + term("@p-o", 120, 230, 1300, HEADERS, fs=44, lh=1.55)
          + tag("@p-g1", 1470, 240, "real output,<br>shortened", 36)
          + tag("@p-a", 1100, 366, "32-bit") + tag("@p-b", 1100, 434, "5 sections")
          + tag("@p-c", 1300, 570, "first instruction") + tag("@p-d", 1300, 640, "image base")
          + txt("@p-e", 120, 850, 'image base: <span class="@p-acc">00400000</span>', "h", fs=84),
          js="""
    land("#@p-a", <<machine>>); land("#@p-b", <<five>>); land("#@p-c", <<entry>>); land("#@p-d", <<image>>);
    wipe("#@p-e", <<four-0.2>>, 0.6);
""", enter=False),

    Scene("base", "You have seen that number. In episode two, Cheat Engine's memory map showed the game's "
                  "module starting exactly there. The image base is the address the file asks to be loaded at.",
          body=txt("@p-t", 120, 96, "episode 2: the memory map", "h", fs=80) + regions().html()
          + regions().mark("@p-m0", 4, 138, 1250, 24, pad=5)
          + tile("@p-k", 120, 780, 620, 170, "00400000", 96) + txt("@p-c", 800, 800, "image base = the address<br>the file asks for", "m", fs=54),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-rg", 0.2, 1.03, 0.5);
    land("#@p-k", <<number>>);
    land("#@p-m0", <<module>>, 1.05);
    blurIn("#@p-c", <<image>>);
"""),

    Scene("sections", "Next, the section table. Dot text is the code: execute and read. Dot R data holds constants: read only. "
                      "Dot data holds the global variables: read and write. Each has a virtual address: where it goes in memory.",
          body=txt("@p-t", 120, 50, "the section table", "h", fs=72)
          + term("@p-o", 120, 160, 1180, SECTIONS, fs=36, lh=1.5)
          + tag("@p-a", 1360, 260, "code") + tag("@p-b", 1360, 530, "constants") + tag("@p-c", 1360, 750, "globals")
          + txt("@p-n", 1360, 900, "dumpbin /headers<br>ac_client.exe,<br>shortened", "m", fs=32, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", 0.3, 1.03, 0.5); blurIn("#@p-n", 0.6);
    tl.fromTo(["#@p-o-l5", "#@p-o-l6", "#@p-o-l7", "#@p-o-l8", "#@p-o-l9", "#@p-o-l10", "#@p-o-l11", "#@p-o-l12"], { opacity: 0.25 }, { opacity: 0.25, duration: 0.01 }, 0.3);
    land("#@p-a", <<code>>);
    tl.to(["#@p-o-l5", "#@p-o-l6", "#@p-o-l7", "#@p-o-l8"], { opacity: 1, duration: 0.3 }, <<r-0.3>>); land("#@p-b", <<constants>>);
    tl.to(["#@p-o-l9", "#@p-o-l10", "#@p-o-l11", "#@p-o-l12"], { opacity: 1, duration: 0.3 }, <<data#2-0.3>>); land("#@p-c", <<global>>);
    tl.fromTo(["#@p-o-l2", "#@p-o-l7", "#@p-o-l11"], { scale: 1 }, { scale: 1.03, transformOrigin: "left center", duration: 0.25, yoyo: true, repeat: 1 }, <<virtual>>);
"""),

    Scene("match", "Now compare that with the memory map. Four zero one thousand: execute and read. Five two five thousand: read. "
                   "Five six B thousand: read and write. The map from episode two is this table, loaded into memory.",
          body=txt("@p-t", 120, 96, "the same three, in the running game", "h", fs=76) + regions().html()
          + regions().mark("@p-m1", 4, 162, 1250, 24, pad=5)
          + regions().mark("@p-m2", 4, 186, 1250, 24, pad=5)
          + regions().mark("@p-m3", 4, 210, 1250, 24, pad=5)
          + tag("@p-g1", 120, 780, ".text 00401000") + tag("@p-g2", 700, 780, ".rdata 00525000") + tag("@p-g3", 1300, 780, ".data 0056B000")
          + txt("@p-c", 120, 910, 'the memory map <span class="@p-acc">is the section table, loaded</span>', "h", fs=60),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-rg", 0.2, 1.03, 0.5);
    land("#@p-m1", <<four>>, 1.05); land("#@p-g1", <<execute>>);
    land("#@p-m2", <<five>>, 1.05); land("#@p-g2", <<read#2>>);
    land("#@p-m3", <<five#3>>, 1.05); land("#@p-g3", <<read#3>>);
    wipe("#@p-c", <<map#2-0.2>>, 0.7);
"""),

    Scene("pointer", "And remember the pointer to our player, at game plus one seven E zero A eight? That offset falls inside dot data. "
                     "It is a global variable, exactly as we said.",
          body=txt("@p-t", 190, 100, "where the player pointer lives", "h", fs=84)
          + card("@p-s", 190, 400, 1540, 190, "", 40, "soft") + txt("@p-sl", 230, 420, ".data", "h", fs=70)
          + txt("@p-lo", 190, 620, "16B000", "m", fs=54) + txt("@p-hi", 1530, 620, "1A49CB", "m", fs=54)
          + tile("@p-k", 520, 420, 420, 150, "17E0A8", 70) + txt("@p-kl", 520, 300, "ac_client.exe + 17E0A8", "m", fs=50)
          + txt("@p-c", 190, 800, 'inside .data = <span class="@p-acc">a global variable</span>', "h", fs=76),
          js="""
    wipe("#@p-t", <<pointer-0.3>>, 0.6);
    land("#@p-s", 0.9, 1.03); blurIn("#@p-sl", 1.0); blurIn("#@p-lo", 1.1); blurIn("#@p-hi", 1.1);
    blurIn("#@p-kl", <<game>>); land("#@p-k", <<inside>>);
    wipe("#@p-c", <<global-0.3>>, 0.7);
"""),

    Scene("fileoff", "One trap. In the file, dot text begins at offset four hundred. In memory, one thousand past the base. "
                     "So a byte's position in the file is not its address in memory.",
          body=txt("@p-t", 190, 100, "file offset is not memory address", "h", fs=80)
          + card("@p-a", 190, 320, 700, 130, "in the file", 54, "soft") + card("@p-b", 1030, 320, 700, 130, "in memory", 54, "soft")
          + tile("@p-c", 190, 500, 700, 170, "00000400", 90) + tile("@p-d", 1030, 500, 700, 170, "00401000", 90)
          + txt("@p-cl", 190, 710, ".text: file pointer<br>to raw data", "m", fs=46) + txt("@p-dl", 1030, 710, ".text: virtual address<br>(base + 1000)", "m", fs=46)
          + txt("@p-e", 190, 900, "debuggers and patch tools convert with the section table", "m", fs=46, color="#E8490F"),
          js="""
    wipe("#@p-t", <<trap-0.2>>, 0.6);
    land("#@p-a", <<file>>); land("#@p-c", <<four>>); blurIn("#@p-cl", <<four+0.2>>);
    land("#@p-b", <<memory>>); land("#@p-d", <<thousand-0.2>>); blurIn("#@p-dl", <<thousand>>);
    blurIn("#@p-e", <<position>>);
"""),

    Scene("aslr", "One more line. The game's header says: relocations stripped. It cannot be moved, so it loads "
                  "at four hundred thousand every time. My own program says: dynamic base. Windows may move it. "
                  "That is the A S L R from episode two, decided right here in the file.",
          body=txt("@p-t", 120, 96, "can the module move? the file decides", "h", fs=72)
          + term("@p-o", 120, 260, 800, FIXED, fs=40, lh=1.6) + term("@p-q", 1000, 260, 800, MOVES, fs=40, lh=1.6)
          + tag("@p-g1", 120, 620, "always at 00400000") + tag("@p-g2", 1000, 620, "Windows may move it")
          + txt("@p-c", 120, 800, 'ASLR is a <span class="@p-acc">flag in the header</span>', "h", fs=80)
          + txt("@p-n", 120, 920, "dumpbin /headers, shortened", "m", fs=36, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", <<game's-0.3>>, 1.03, 0.5); blurIn("#@p-n", <<game's>>);
    land("#@p-g1", <<four>>);
    land("#@p-q", <<own-0.3>>, 1.03, 0.5); land("#@p-g2", <<may>>);
    wipe("#@p-c", <<decided-0.3>>, 0.7);
"""),

    Scene("process", "So what happens when you start an E X E? Windows creates a process: a private address space. It maps the sections "
                     "of the file into it. And it starts a thread at the entry point. The process is the container. The thread is what actually runs.",
          body=txt("@p-t", 190, 90, "from file to process", "h", fs=90)
          + card("@p-f", 190, 300, 420, 420, "", 40, "soft") + txt("@p-fl", 190, 740, "game.exe on disk", "m", fs=44)
          + card("@p-f1", 230, 340, 340, 100, ".text", 44) + card("@p-f2", 230, 460, 340, 100, ".rdata", 44) + card("@p-f3", 230, 580, 340, 100, ".data", 44)
          + bar("@p-b", 610, 505, 190, 14)
          + card("@p-p", 800, 260, 930, 500, "", 40, "soft") + txt("@p-pl", 800, 780, "the process: a private address space", "m", fs=44)
          + card("@p-p1", 850, 310, 380, 100, ".text", 44) + card("@p-p2", 850, 430, 380, 100, ".rdata", 44) + card("@p-p3", 850, 550, 380, 100, ".data", 44)
          + tile("@p-th", 1300, 300, 370, 130, "thread", 54) + txt("@p-tl", 1300, 460, "starts at the<br>entry point", "m", fs=40)
          + txt("@p-c", 190, 900, 'process = container &nbsp; <span class="@p-acc">thread = what runs</span>', "m", fs=56),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-f", 0.8, 1.03); blurIn("#@p-fl", 0.9); each(["#@p-f1", "#@p-f2", "#@p-f3"], 1.0, 0.1, 1.1);
    wipe("#@p-b", <<creates-0.2>>, 0.4); land("#@p-p", <<process>>, 1.03); blurIn("#@p-pl", <<private>>);
    each(["#@p-p1", "#@p-p2", "#@p-p3"], <<maps>>, 0.15, 1.1);
    land("#@p-th", <<thread>>); blurIn("#@p-tl", <<entry>>);
    blurIn("#@p-c", <<container-0.3>>);
"""),

    Scene("loaded", "This small program prints its own process. A process I D. A thread I D. "
                    "The address Windows loaded it at. "
                    "And the first two bytes at that address, in memory: four D, five A. M Z. The file is in there.",
          body=txt("@p-t", 120, 60, "loaded.cpp: a process looks at itself", "h", fs=72)
          + term("@p-o", 120, 180, 1080, LOADED[:5], fs=48, lh=1.6)
          + tag("@p-g0", 1260, 290, "the container, and<br>what runs in it", 38)
          + tag("@p-g1", 1260, 450, "the file asked for<br>140000000", 38)
          + tag("@p-g2", 1260, 610, "the start of the file,<br>in memory", 38)
          + txt("@p-c", 120, 800, 'the EXE file is <span class="@p-acc">mapped into the process</span>', "h", fs=68),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", 0.3, 1.03, 0.5);
    tl.fromTo(["#@p-o-l3", "#@p-o-l4"], { opacity: 0.25 }, { opacity: 0.25, duration: 0.01 }, 0.3);
    land("#@p-g0", <<process#2>>);
    tl.to("#@p-o-l3", { opacity: 1, duration: 0.3 }, <<address>>); land("#@p-g1", <<loaded>>);
    tl.to("#@p-o-l4", { opacity: 1, duration: 0.3 }, <<first>>); land("#@p-g2", <<four>>);
    wipe("#@p-c", <<file-0.4>>, 0.7);
"""),

    Scene("modules", "And it is not alone. The same process holds other modules: system D L Ls, which are P E files too. "
                     "Kernel thirty-two is there because my program asked for it.",
          body=txt("@p-t", 120, 60, "the modules inside one process", "h", fs=76)
          + term("@p-o", 120, 190, 1080, LOADED[5:], fs=48, lh=1.6)
          + tag("@p-g1", 1260, 300, "my EXE", 40) + tag("@p-g2", 1260, 460, "system DLLs:<br>PE files too", 40)
          + txt("@p-c", 120, 760, "module = a PE file loaded into a process", "m", fs=56)
          + txt("@p-d", 120, 880, 'why is kernel32 here? <span class="@p-acc">my program asked</span>', "h", fs=60),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", 0.3, 1.03, 0.5);
    land("#@p-g1", <<alone>>);
    land("#@p-g2", <<system>>); blurIn("#@p-c", <<p>>);
    wipe("#@p-d", <<because-0.4>>, 0.7);
"""),

    Scene("imports", "It asked in its import table: a list, inside the E X E, of the functions it needs from other files. "
                     "My code called F open, F write and F read. Underneath, those became Create File, Write File and Read File, "
                     "from kernel thirty-two.",
          body=txt("@p-t", 120, 60, "the import table", "h", fs=80)
          + term("@p-o", 120, 190, 1050, IMPORTS, fs=44, lh=1.55)
          + card("@p-a", 1260, 250, 520, 110, "fopen", 50, "soft") + card("@p-b", 1260, 400, 520, 110, "fwrite", 50, "soft")
          + card("@p-c", 1260, 550, 520, 110, "fread", 50, "soft")
          + txt("@p-al", 1260, 690, "what my code called", "m", fs=40)
          + txt("@p-d", 120, 850, "import table = the functions this file needs<br>from other files", "m", fs=52),
          js="""
    wipe("#@p-t", <<import-0.2>>, 0.6);
    land("#@p-o", 0.8, 1.03, 0.5);
    blurIn("#@p-d", <<list>>);
    land("#@p-a", <<open>>); land("#@p-b", <<write>>); land("#@p-c", <<read>>); blurIn("#@p-al", <<read+0.2>>);
    tl.fromTo("#@p-o-l2", { scale: 1 }, { scale: 1.05, transformOrigin: "left center", duration: 0.25, yoyo: true, repeat: 1 }, <<create>>);
    tl.fromTo("#@p-o-l3", { scale: 1 }, { scale: 1.05, transformOrigin: "left center", duration: 0.25, yoyo: true, repeat: 1 }, <<write#2>>);
    tl.fromTo("#@p-o-l4", { scale: 1 }, { scale: 1.05, transformOrigin: "left center", duration: 0.25, yoyo: true, repeat: 1 }, <<read#2>>);
"""),

    Scene("api", "This is the Windows A P I. A program cannot touch the disk, the screen or the keyboard by itself. It asks Windows. "
                 "Kernel thirty-two: files, memory, processes. User thirty-two: windows and input.",
          body=txt("@p-t", 190, 100, "the Windows API", "h", fs=100)
          + card("@p-p", 190, 330, 480, 170, "a program", 56, "soft") + bar("@p-b", 670, 408, 170, 14)
          + tile("@p-w", 840, 320, 480, 190, "Windows", 70) + txt("@p-wl", 1380, 350, "disk, screen,<br>keyboard", "m", fs=48)
          + card("@p-k", 190, 640, 560, 140, "kernel32.dll", 54, "on") + txt("@p-kl", 810, 675, "files, memory, processes", "m", fs=52)
          + card("@p-u", 190, 830, 560, 140, "user32.dll", 54, "on") + txt("@p-ul", 810, 865, "windows and input", "m", fs=52),
          js="""
    wipe("#@p-t", <<windows-0.2>>, 0.6);
    land("#@p-p", <<program>>); blurIn("#@p-wl", <<disk>>);
    wipe("#@p-b", <<asks>>, 0.3); land("#@p-w", <<asks+0.2>>);
    land("#@p-k", <<kernel>>); blurIn("#@p-kl", <<files>>);
    land("#@p-u", <<user>>); blurIn("#@p-ul", <<windows#3>>);
"""),

    Scene("gameimp", "Now the game's import table. Open G L: that is how it draws. Open A L: sound. S D L: its window. "
                     "Winsock: the network. An import table is a quick summary of what a program does.",
          body=txt("@p-t", 120, 60, "what the game asks Windows for", "h", fs=76)
          + term("@p-o", 120, 190, 1200, GAMEIMP, fs=42, lh=1.55)
          + tag("@p-a", 1380, 262, "graphics") + tag("@p-b", 1380, 327, "sound") + tag("@p-c", 1380, 392, "the window") + tag("@p-d", 1380, 457, "network")
          + txt("@p-e", 120, 850, 'imports = <span class="@p-acc">a summary of what a program does</span>', "h", fs=60)
          + txt("@p-n", 120, 950, "real output, shortened to one function per DLL", "m", fs=36, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", 0.3, 1.03, 0.5); blurIn("#@p-n", 0.6);
    land("#@p-a", <<draws-0.3>>); land("#@p-b", <<sound>>); land("#@p-c", <<window>>); land("#@p-d", <<network>>);
    wipe("#@p-e", <<summary-0.4>>, 0.7);
"""),

    Scene("ceimp", "And Cheat Engine is a program too. Its own import table: Open Process. Read Process Memory. "
                   "Write Process Memory. Reading a game's memory is a request to Windows.",
          body=txt("@p-t", 120, 60, "Cheat Engine's own imports", "h", fs=80)
          + term("@p-o", 120, 200, 1300, CEIMP, fs=48, lh=1.6)
          + tag("@p-g1", 1470, 215, "real output,<br>shortened", 34)
          + txt("@p-c", 120, 740, "reading another process's memory", "m", fs=56)
          + txt("@p-d", 120, 840, '= <span class="@p-acc">a request to Windows</span>', "h", fs=84),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o", 0.3, 1.03, 0.5); land("#@p-g1", 0.7);
    tl.fromTo(["#@p-o-l2", "#@p-o-l3", "#@p-o-l4"], { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0.3);
    tl.to("#@p-o-l2", { opacity: 1, duration: 0.25 }, <<open>>);
    tl.to("#@p-o-l3", { opacity: 1, duration: 0.25 }, <<read>>);
    tl.to("#@p-o-l4", { opacity: 1, duration: 0.25 }, <<write>>);
    blurIn("#@p-c", <<reading>>);
    wipe("#@p-d", <<request-0.3>>, 0.6);
"""),

    # ------------------------------------------------------------------ outro
    Scene("recap", "Let's recap. A file is bytes at offsets. A save file is often just a structure, "
                   "written to disk. An E X E is a P E file: its image base and its sections become the memory map. "
                   "And a program reaches Windows through its import table.",
          body=txt("@p-t", 190, 90, "recap", "h", fs=110)
          + txt("@p-a", 190, 300, "a file = bytes at offsets", "m", fs=56)
          + txt("@p-b", 190, 470, "a save file = often a structure, written to disk", "m", fs=56)
          + txt("@p-c", 190, 640, "an EXE = a PE file: base + sections = the memory map", "m", fs=52)
          + txt("@p-d", 190, 810, 'import table = <span class="@p-acc">how a program reaches Windows</span>', "m", fs=56),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    wipe("#@p-a", <<file>>, 0.8);
    wipe("#@p-b", <<save>>, 0.8);
    wipe("#@p-c", <<p>>, 0.8);
    wipe("#@p-d", <<reaches-0.5>>, 0.8);
"""),

    Scene("practice", "Your practice. Compile savegame dot C P P from the description, and run it with new. Then, in a hex editor, "
                      "set the health to two hundred fifty-five, and change the name to your own. Load it, and check.",
          body=txt("@p-t", 190, 100, "practice", "h", fs=110)
          + tag("@p-g", 900, 130, "savegame.cpp: link in the description", 36)
          + term("@p-o", 190, 310, 1000, ["&gt; savegame new", "&gt; savegame", "loaded save.dat (28 bytes)", "health  " + HI("255"), "gold    1000", "name    " + HI("(your name)")], fs=40)
          + txt("@p-a", 190, 800, "1. health = 255: which bytes, at which offset?", "m", fs=50)
          + txt("@p-b", 190, 880, "2. your name: type over, up to 15 letters", "m", fs=50)
          + txt("@p-c", 190, 960, "3. load it and check", "m", fs=50),
          js="""
    wipe("#@p-t", <<practice-0.2>>, 0.5);
    land("#@p-g", <<description-0.4>>);
    land("#@p-o", <<run-0.3>>, 1.04, 0.4);
    blurIn("#@p-a", <<health>>);
    blurIn("#@p-b", <<name>>);
    blurIn("#@p-c", <<load>>);
"""),

    Scene("next", "Next time, we attach Cheat Engine to the running game, and find a value while knowing nothing but the number on the screen. "
                  "Your first memory scan. See you there.",
          body=txt("@p-s", 192, 220, "NEXT EPISODE", "m", fs=64)
          + txt("@p-a", 192, 330, "Your First", "h", fs=150) + txt("@p-b", 192, 490, '<span class="@p-acc">Memory Scan</span>', "h", fs=150)
          + card("@p-o", 192, 740, 900, 150, "value: 100 &nbsp; [ First Scan ]", 50, "soft"),
          js="""
    blurIn("#@p-s", <<next>>);
    land("#@p-o", <<number-0.3>>, 1.04, 0.4);
    wipe("#@p-a", <<attach-0.2>>, 0.6); wipe("#@p-b", <<find-0.2>>, 0.5);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Game Hacking from Scratch 4: Inside the Files")
