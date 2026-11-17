"""Game Hacking from Scratch, episode 3: Read One Line of Assembly (reading assembly + the stack and calling conventions).

Long-form YouTube episode. Every screenshot and number is real and from one run: AssaultCube 1.3.0.2 (open source, offline) with
Cheat Engine's "find out what writes / accesses this address", its Memory Viewer disassembler and its debugger stopped in the
game's firing code; and the MSVC listings of lab/calls.cpp (calls32.asm = 32-bit, calls.asm = 64-bit).   Run: python build.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, Shot, bar, build, card, cells, fit_clip, tag, term, tile, txt  # noqa: E402,F401

A = Path(__file__).resolve().parent / "assets"
S = lambda name: A / f"shots/{name}.png"  # noqa: E731

# ---- this run (all read from the live process / the stopped debugger) ----
PLAYER, MAG, WEAPON = "00968148", "00968288", "00958080"

# ---- Cheat Engine "found opcodes" windows: list rows and the details pane ----
F_LIST = (0, 38, 556, 56)            # header + first row
F_LIST2 = (0, 38, 556, 80)           # header + two rows
F_PANE = (0, 218, 330, 320)          # the lines around the instruction + the registers
ACC_LIST = (0, 38, 670, 80)
ACC_CODE = (0, 240, 480, 104)

# ---- Memory Viewer disassembler: rows are 22 px, the first one starts at y=112 (y=172 while the debugger is stopped) ----
ROW = lambda k: 112 + 22 * k         # noqa: E731
BROW = lambda k: 172 + 22 * k        # noqa: E731
B_DIS = (0, 128, 740, 352)
B_REG = (750, 60, 212, 205)
REG_Y = {"eax": 89, "ebx": 108, "ecx": 127, "edx": 146, "esi": 165, "edi": 184, "ebp": 203, "esp": 222, "eip": 241}


def dis(name, crop, y=230, w=1680, x=120, id="@p-mv"):
    return Shot(id, S(name), x, y, w, crop=crop)


def brk(name, rows=14):
    d = Shot("@p-mv", S(name), 120, 230, 1150, crop=(0, 128, 740, 44 + 22 * rows))
    r = Shot("@p-rg", S(name), 1310, 230, 490, crop=B_REG)
    return d, r


def hi(s):
    return f'<span class="hi">{s}</span>'


def dimc(s):
    return f'<span class="dimc">{s}</span>'


def a(op, args="", mark=False):
    """One listing line, laid out like the .asm file (tab after the mnemonic)."""
    s = f"    {op:<6}{args}"
    return hi(s) if mark else s


SRC = ["struct Player {",
       "    int id;",
       "    int health;",
       "    int ammo;",
       "    void hit(int damage);",
       "};",
       "",
       "void Player::hit(int damage) {",
       hi("    health = health - damage;"),
       "    if (health &lt;= 0)",
       '        std::puts("dead");',
       "}"]

L22 = [dimc("; Line 22"),
       a("mov", "eax, DWORD PTR _this$[ebp]"),
       a("mov", "ecx, DWORD PTR [eax+4]"),
       a("sub", "ecx, DWORD PTR _damage$[ebp]"),
       a("mov", "edx, DWORD PTR _this$[ebp]"),
       a("mov", "DWORD PTR [edx+4], ecx")]

L23 = [dimc("; Line 23"),
       a("mov", "eax, DWORD PTR _this$[ebp]"),
       a("cmp", "DWORD PTR [eax+4], 0", True),
       a("jg", "SHORT $LN2@hit", True),
       dimc("; Line 24"),
       a("push", "OFFSET $SG6774"),
       a("call", "_puts"),
       a("add", "esp, 4"),
       "$LN2@hit:"]

L29 = [dimc("; Line 29"),
       a("push", "3"),
       a("push", "2"),
       a("push", "1"),
       a("call", "add3"),
       a("add", "esp, 12", True),
       a("mov", "DWORD PTR _s$[ebp], eax")]

ADD3 = [a("push", "ebp"),
        a("mov", "ebp, esp"),
        a("push", "ecx"),
        dimc("; Line 17"),
        a("mov", "eax, DWORD PTR _a$[ebp]"),
        a("add", "eax, DWORD PTR _b$[ebp]"),
        a("add", "eax, DWORD PTR _c$[ebp]"),
        a("mov", "DWORD PTR _sum$[ebp], eax"),
        dimc("; Line 18"),
        a("mov", "eax, DWORD PTR _sum$[ebp]", True)]

L30 = [dimc("; Line 30"),
       a("push", "30"),
       a("lea", "ecx, DWORD PTR _p$[ebp]", True),
       a("call", "Player::hit"),
       "",
       dimc("; Player::hit, its last lines (Line 25)"),
       a("mov", "esp, ebp"),
       a("pop", "ebp"),
       a("ret", "4", True)]

X64 = [dimc("; Line 29"),
       a("mov", "r8d, 3", True),
       a("mov", "edx, 2", True),
       a("mov", "ecx, 1", True),
       a("call", "add3"),
       a("mov", "DWORD PTR s$[rsp], eax"),
       dimc("; Line 30"),
       a("mov", "edx, 30"),
       a("lea", "rcx, QWORD PTR p$[rsp]"),
       a("call", "Player::hit")]

GAME_SIZE, FOUND_SIZE = (1584, 930), (722, 690)
CLIP_FROM = 0.7                      # seconds into the recording where the scene starts


def live_game(still=False):
    return Shot("@p-g", S("game_before") if still else A / "clips/fire_game.mp4", 110, 190, 900, size=None if still else GAME_SIZE)


def live_found(still=False):
    return Shot("@p-c", S("found_12") if still else A / "clips/fire_found.mp4", 1050, 190, 760, crop=(0, 0, 556, 470), size=None if still else FOUND_SIZE)


def live_media(dur):
    g, c = live_game(), live_found()
    g.path = fit_clip(A / "clips/fire_game.mp4", dur, CLIP_FROM)
    c.path = fit_clip(A / "clips/fire_found.mp4", dur, CLIP_FROM)
    g.src, c.src = f"assets/clips/{g.path.name}", f"assets/clips/{c.path.name}"
    return g.video(0, dur) + c.video(0, dur)


def stack_row(i, y, addr, val, label, on=False):
    return (txt(f"@p-sa{i}", 190, y + 26, addr, "m", fs=46)
            + card(f"@p-sv{i}", 520, y, 420, 105, val, 54, "on" if on else "")
            + txt(f"@p-sl{i}", 1000, y + 30, label, "m", fs=40))


cold_game = Shot("@p-g", S("game"), 120, 200, 1100)
found_line = Shot("@p-f", S("found_16"), 120, 220, 1680, crop=F_LIST)
found_pane = Shot("@p-f", S("found_16"), 120, 210, 760, crop=F_PANE)
acc_list = Shot("@p-f", S("acc_health"), 120, 220, 1680, crop=ACC_LIST)
acc_code = Shot("@p-f", S("acc_health"), 120, 220, 1300, crop=ACC_CODE)
mv_dec = dis("mv_sel", (0, 88, 655, 24 + 22 * 9))
mv_this = dis("mv_dec", (0, ROW(7), 655, 22 * 11), y=200)
mv_cdecl = dis("mv_cdecl", (0, 88, 760, 24 + 22 * 9))
mv_top = dis("mv_start", (0, 88, 700, 24 + 22 * 7), y=190, w=1500)
mv_end = dis("mv_start", (0, ROW(29), 700, 22 * 6), y=620, w=1500, id="@p-mv2")
bA, rA = brk("brk_a")
bB, rB = brk("brk_b")
bC = Shot("@p-mv", S("brk_c"), 120, 220, 1100, crop=(0, 128, 740, 44 + 22 * 4))
rC = Shot("@p-rg", S("brk_c"), 1290, 220, 510, crop=B_REG)
retC = Shot("@p-rt", S("brk_c"), 120, 480, 760, crop=(752, 965, 210, 74))

scenes = [
    # ------------------------------------------------------------------ cold open
    Scene("cold", "Every time I fire, this number drops by one. Somewhere in the game's code, one instruction does that. "
                  "Today we find that instruction, and we read it.",
          body=txt("@p-t", 120, 80, "one shot, one round less", "h", fs=80) + cold_game.html()
          + cold_game.mark("@p-m", 478, 856, 196, 62)
          + txt("@p-a", 1290, 300, "who<br>does<br>that?", "h", fs=110)
          + tile("@p-k", 1290, 700, 500, 150, "1 instruction", 50),
          js="""
    land("#@p-g", 0.2, 1.03, 0.5);
    land("#@p-m", <<number-0.3>>, 1.4);
    blurIn("#@p-a", <<somewhere>>);
    land("#@p-k", <<one#2>>);
"""),

    Scene("hook", "Last time, I left you with this line. By the end of this episode, you will read lines like it straight out of a running game, "
                  "and you will know where a function keeps its arguments.",
          body=txt("@p-s", 192, 200, "from the end of episode 2", "m", fs=56)
          + term("@p-o", 192, 310, 1200, ['mov  [ebx+<span class="hi">EC</span>], eax'], fs=88)
          + txt("@p-a", 192, 600, "1. read a line like this", "h", fs=76)
          + txt("@p-b", 192, 720, "2. in a running game", "h", fs=76)
          + txt("@p-c", 192, 840, '3. and find <span class="@p-acc">a function\'s arguments</span>', "h", fs=76),
          js="""
    blurIn("#@p-s", 0.3);
    land("#@p-o", <<line-0.4>>, 1.04, 0.4);
    wipe("#@p-a", <<read-0.2>>, 0.5);
    wipe("#@p-b", <<straight-0.2>>, 0.5);
    wipe("#@p-c", <<function-0.4>>, 0.6);
"""),

    Scene("title", "This is Game Hacking from Scratch. Episode three: read one line of assembly.",
          body=txt("@p-s", 192, 250, "GAME HACKING FROM SCRATCH", "m", fs=64)
          + txt("@p-a", 192, 360, "Read One Line", "h", fs=150) + txt("@p-b", 192, 520, 'of <span class="@p-acc">Assembly</span>', "h", fs=150)
          + tile("@p-e", 192, 760, 420, 130, "EPISODE 3", 60),
          js="""
    blurIn("#@p-s", <<game>>);
    wipe("#@p-a", <<read-0.3>>, 0.6);
    wipe("#@p-b", <<assembly-0.3>>, 0.6);
    land("#@p-e", <<episode>>);
"""),

    # ------------------------------------------------------------------ what assembly is
    Scene("what", "A game on your disk is not C plus plus anymore. The compiler turned it into machine code: bytes that the processor runs. "
                  "Assembly is those same bytes, written as text.",
          body=txt("@p-t", 190, 100, "machine code, written as text", "h", fs=84)
          + card("@p-a", 190, 330, 420, 180, "C++", 80, "soft") + txt("@p-al", 190, 540, "what the<br>programmer wrote", "m", fs=40)
          + bar("@p-b1", 610, 414, 110, 14)
          + cells("@p-c", 720, 330, ["FF", "08"], size=180, gap=24, on=range(2)) + txt("@p-cl", 720, 540, "what the<br>processor runs", "m", fs=40)
          + bar("@p-b2", 1104, 414, 110, 14)
          + term("@p-o", 1214, 340, 440, ["dec [eax]"], fs=64) + txt("@p-ol", 1214, 540, "the same bytes,<br>as text", "m", fs=40)
          + txt("@p-d", 190, 800, 'one line = <span class="@p-acc">one instruction</span>', "h", fs=90),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-a", <<plus-0.3>>); blurIn("#@p-al", <<plus>>);
    wipe("#@p-b1", <<compiler>>, 0.3);
    each(".c-@p-c", <<machine>>, 0.15); blurIn("#@p-cl", <<bytes>>);
    wipe("#@p-b2", <<assembly-0.2>>, 0.3);
    land("#@p-o", <<assembly>>, 1.05, 0.4); blurIn("#@p-ol", <<assembly+0.3>>);
    wipe("#@p-d", <<same>>, 0.6);
"""),

    Scene("src", "Let's start with code we wrote ourselves: calls dot C P P. "
                 "A player, with an I D, health and ammo. And a function, hit, that subtracts damage from the health.",
          body=txt("@p-t", 120, 70, "calls.cpp", "h", fs=80) + tag("@p-g", 620, 86, "part of the file: link in the description", 36)
          + term("@p-o", 120, 210, 1100, SRC, fs=42, lh=1.42)
          + txt("@p-a", 1290, 330, "a player:<br>id, health,<br>ammo", "m", fs=52)
          + txt("@p-b", 1290, 700, 'hit():<br><span class="@p-acc">health goes<br>down</span>', "m", fs=52),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-o", 0.4, 1.03, 0.5);
    land("#@p-g", <<calls>>);
    blurIn("#@p-a", <<player>>);
    blurIn("#@p-b", <<hit>>);
    tl.fromTo("#@p-o-l8", { scale: 1 }, { scale: 1.04, transformOrigin: "left center", duration: 0.25, yoyo: true, repeat: 1 }, <<subtracts>>);
"""),

    Scene("listing", "I compile it with Microsoft's compiler, as thirty-two bit code, like our game, and ask for a listing with slash F A. "
                     "For that one line, health equals health minus damage, the compiler wrote five instructions.",
          body=txt("@p-t", 120, 70, "the compiler's listing", "h", fs=80)
          + term("@p-c", 120, 210, 1100, ["&gt; cl /Od " + hi("/FA") + " calls.cpp"], fs=46)
          + tag("@p-g", 1270, 232, "32-bit build: calls32.asm", 36)
          + card("@p-s", 120, 370, 1100, 110, "health = health - damage;", 50, "soft")
          + term("@p-o", 120, 530, 1100, L22, fs=44, lh=1.45)
          + txt("@p-a", 1290, 640, '1 line of C++<br><span class="@p-acc">5 instructions</span>', "h", fs=62),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-c", <<compile-0.3>>, 1.04, 0.4);
    land("#@p-g", <<thirty-two>>);
    land("#@p-s", <<line-0.3>>, 1.04, 0.4);
    land("#@p-o", <<compiler#2-0.4>>, 1.03, 0.5);
    blurIn("#@p-a", <<five-0.2>>);
"""),

    Scene("regs", "First, the names. E A X, E C X, E D X. These are registers: small, very fast variables inside the processor itself. "
                  "In thirty-two bit code, each one holds four bytes.",
          body=txt("@p-t", 190, 100, "registers: the processor's own variables", "h", fs=76)
          + "".join(card(f"@p-r{i}", 190 + (i % 4) * 300, 300 + (i // 4) * 190, 260, 140, n, 68, "on" if n in ("eax", "ecx", "edx") else "")
                    for i, n in enumerate(["eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp"]))
          + txt("@p-a", 1420, 330, "4 bytes<br>each", "h", fs=80)
          + txt("@p-b", 1420, 560, "(32-bit)", "m", fs=48)
          + txt("@p-c", 190, 730, "memory &rarr; register &rarr; work &rarr; memory", "m", fs=60)
          + txt("@p-d", 190, 850, "and eip: the address of the next instruction", "m", fs=46, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-r0", <<names>>); land("#@p-r2", <<names+0.8>>); land("#@p-r3", <<names+1.6>>);
    each(["#@p-r1", "#@p-r4", "#@p-r5", "#@p-r6", "#@p-r7"], <<registers>>, 0.12);
    blurIn("#@p-a", <<four>>); blurIn("#@p-b", <<thirty-two>>);
    wipe("#@p-c", <<small>>, 1.2);
    blurIn("#@p-d", <<processor>>);
"""),

    Scene("shape", "Every line has the same shape: the instruction, then the destination, then the source. "
                   "M O V, said move, copies the source into the destination.",
          body=txt("@p-t", 190, 100, "instruction &nbsp;destination, source", "h", fs=80)
          + card("@p-a", 190, 340, 330, 190, "mov", 100, "on") + card("@p-b", 580, 340, 330, 190, "ecx", 100)
          + txt("@p-k", 925, 370, ",", "h", fs=110)
          + card("@p-c", 1000, 340, 620, 190, "[eax+4]", 100, "soft")
          + txt("@p-al", 190, 560, "instruction", "m", fs=48, w=330, align="center")
          + txt("@p-bl", 580, 560, "destination", "m", fs=48, w=330, align="center")
          + txt("@p-cl", 1000, 560, "source", "m", fs=48, w=620, align="center")
          + bar("@p-ar", 760, 760, 600, 14) + txt("@p-ah", 700, 706, "&larr;", "h", fs=110)
          + txt("@p-d", 190, 860, 'the value moves <span class="@p-acc">right to left</span>', "h", fs=72),
          js="""
    wipe("#@p-t", <<shape-0.4>>, 0.6);
    land("#@p-a", <<instruction>>); blurIn("#@p-al", <<instruction>>);
    land("#@p-b", <<destination>>); blurIn("#@p-bl", <<destination>>); blurIn("#@p-k", <<destination>>);
    land("#@p-c", <<source>>); blurIn("#@p-cl", <<source>>);
    wipe("#@p-ar", <<copies>>, 0.5); blurIn("#@p-ah", <<copies+0.3>>);
    wipe("#@p-d", <<copies+0.6>>, 0.6);
"""),

    Scene("brackets", "Square brackets mean memory, like last episode. E A X holds the address of the player. "
                  "Four is the offset of health. So the line says: go to player plus four, and read the health into E C X.",
          body=txt("@p-t", 190, 80, "[ ] = memory", "h", fs=90)
          + term("@p-o", 190, 230, 1100, ["mov   ecx, DWORD PTR " + hi("[eax+4]")], fs=52)
          + card("@p-s", 190, 420, 700, 560, "", 40, "soft") + txt("@p-sl", 230, 440, "Player, at the address in eax", "m", fs=32)
          + card("@p-f0", 250, 520, 580, 110, "+0 &nbsp;id", 50) + card("@p-f1", 250, 660, 580, 110, "+4 &nbsp;health", 50, "on")
          + card("@p-f2", 250, 800, 580, 110, "+8 &nbsp;ammo", 50)
          + bar("@p-b", 890, 708, 130, 14) + tile("@p-k", 1020, 640, 300, 150, "ecx", 80)
          + txt("@p-a", 1020, 450, "player + 4<br>= health", "m", fs=54)
          + txt("@p-d", 1020, 860, "DWORD PTR = 4 bytes", "m", fs=48)
          + tag("@p-g", 1020, 960, "offsets 4 and 8: printed by calls.exe", 30),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-o", <<memory-0.3>>, 1.04, 0.4);
    land("#@p-s", <<address-0.5>>, 1.02); blurIn("#@p-sl", <<address>>);
    each(["#@p-f0", "#@p-f2"], <<player>>, 0.15);
    land("#@p-f1", <<offset>>); land("#@p-g", <<offset+0.4>>);
    blurIn("#@p-a", <<plus>>);
    wipe("#@p-b", <<read>>, 0.3); land("#@p-k", <<read+0.2>>);
    blurIn("#@p-d", <<read+0.8>>);
"""),

    Scene("walk", "Now read all five. Get the player's address. Read the health. Subtract the damage. Get the address again. "
                  "And write the result back into health. Read, change, write.",
          body=txt("@p-t", 120, 70, "health = health - damage;", "h", fs=72)
          + term("@p-o", 120, 210, 1060, L22[1:], fs=44, lh=1.9)
          + "".join(tag(f"@p-g{i}", 1240, 240 + i * 84, s, 40) for i, s in enumerate(
              ["eax = the player", "ecx = health", "ecx = ecx - damage", "edx = the player", "health = ecx"]))
          + txt("@p-c", 120, 760, 'read &rarr; change &rarr; <span class="@p-acc">write</span>', "h", fs=100)
          + txt("@p-d", 120, 910, "the pattern behind most of your stats", "m", fs=50),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-o", 0.4, 1.03, 0.5);
    land("#@p-g0", <<get>>); land("#@p-g1", <<read#2>>); land("#@p-g2", <<subtract>>);
    land("#@p-g3", <<get#2>>); land("#@p-g4", <<write>>);
    wipe("#@p-c", <<read#3-0.2>>, 1.2);
    blurIn("#@p-d", <<read#3+0.6>>);
"""),

    # ------------------------------------------------------------------ the real game
    Scene("live1", "Now the real game. I point Cheat Engine at the address of my magazine, and ask: find out what writes to this address. "
                   "I had already fired twelve rounds when this recording starts, so the count says twelve.",
          body=txt("@p-t", 110, 60, "find out what writes to this address", "h", fs=64)
          + live_game(True).html() + live_found(True).html()
          + tag("@p-t1", 110, 740, "AssaultCube, offline") + tag("@p-t2", 1050, 860, "Cheat Engine")
          + live_found(True).mark("@p-m", 4, 66, 50, 24, pad=4)
          + txt("@p-n", 110, 960, "the count: how many times an instruction wrote there", "m", fs=44),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-g", 0.2, 1.03, 0.5); land("#@p-t1", <<game>>);
    land("#@p-c", <<cheat-0.3>>, 1.03, 0.4); land("#@p-t2", <<cheat>>);
    land("#@p-m", <<twelve-0.3>>, 1.4); blurIn("#@p-n", <<count-0.3>>);
""", exit=False),

    Scene("live2", "I fire two rounds. The count goes to fourteen, the magazine is empty, and the game reloads. Two more: sixteen. "
                   "Every shot went through one single instruction. The second line is the reload.",
          media=live_media,
          body=txt("@p-t", 110, 60, "find out what writes to this address", "h", fs=64)
          + tag("@p-t1", 110, 740, "AssaultCube, offline") + tag("@p-t2", 1050, 860, "Cheat Engine")
          + live_game().mark("@p-m1", 476, 856, 200, 62) + live_found().mark("@p-m", 4, 66, 50, 24, pad=4)
          + live_found().mark("@p-m2", 66, 90, 250, 24, pad=4)
          + txt("@p-n", 110, 960, "the count: how many times an instruction wrote there", "m", fs=44),
          js="""
    land("#@p-m1", 0.4, 1.4);
    land("#@p-m2", <<second-0.3>>, 1.3);
""", enter=False, early=False),

    Scene("line", "Here it is. Address zero zero four C, seven three E F. Two bytes: F F, zero eight. "
                  "As text: D E C, short for decrement, brackets, E A X. "
                  "So: subtract one from the number stored at the address in E A X.",
          body=txt("@p-t", 120, 80, "the instruction that takes a round", "h", fs=76) + found_line.html()
          + found_line.mark("@p-m1", 68, 68, 72, 20, pad=5) + found_line.mark("@p-m2", 146, 68, 40, 20, pad=5)
          + found_line.mark("@p-m3", 197, 68, 66, 20, pad=5)
          + card("@p-a", 120, 500, 480, 150, "004C73EF", 70) + txt("@p-al", 120, 700, "its address", "m", fs=46)
          + cells("@p-b", 680, 500, ["FF", "08"], size=150, gap=20, on=range(2)) + txt("@p-bl", 680, 700, "its bytes", "m", fs=46)
          + term("@p-o", 1100, 505, 520, ["dec [eax]"], fs=72) + txt("@p-ol", 1100, 700, "its text", "m", fs=46)
          + txt("@p-d", 120, 850, 'take 1 from <span class="@p-acc">the number at the address in eax</span>', "h", fs=60),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-f", 0.2, 1.03, 0.5);
    land("#@p-m1", <<address-0.3>>, 1.2); land("#@p-a", <<zero>>); blurIn("#@p-al", <<zero>>);
    land("#@p-m2", <<bytes-0.4>>, 1.2); each(".c-@p-b", <<f>>, 0.3); blurIn("#@p-bl", <<f>>);
    land("#@p-m3", <<text-0.3>>, 1.2); land("#@p-o", <<d>>, 1.05, 0.4); blurIn("#@p-ol", <<d>>);
    wipe("#@p-d", <<subtract-0.3>>, 1.0);
"""),

    Scene("regval", "Cheat Engine also saved the registers. E A X held zero zero nine six, eight two eight eight. "
                    "That is exactly my magazine in this run: the player's address, plus one four zero.",
          body=txt("@p-t", 120, 70, "what was in eax?", "h", fs=80) + found_pane.html()
          + found_pane.mark("@p-m1", 6, 362, 112, 20, pad=4) + found_pane.mark("@p-m2", 6, 462, 112, 20, pad=4)
          + txt("@p-al", 960, 230, "eax", "m", fs=56) + tile("@p-a", 960, 310, 760, 170, MAG, 110)
          + txt("@p-eq", 960, 520, "=", "h", fs=90)
          + card("@p-b", 1050, 520, 420, 130, PLAYER, 60) + txt("@p-p", 1490, 545, "+ 140", "h", fs=70)
          + txt("@p-bl", 1050, 670, "the player (edi)", "m", fs=44)
          + txt("@p-d", 960, 800, 'player + 140<br>= <span class="@p-acc">the magazine</span>', "h", fs=64),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-f", 0.2, 1.03, 0.5);
    land("#@p-m1", <<held-0.4>>, 1.2); blurIn("#@p-al", <<held-0.2>>); land("#@p-a", <<held+0.2>>);
    land("#@p-m2", <<player's>>, 1.2); blurIn("#@p-eq", <<player's-0.2>>); land("#@p-b", <<player's+0.2>>); blurIn("#@p-bl", <<player's+0.4>>);
    blurIn("#@p-p", <<plus>>);
    wipe("#@p-d", <<plus+0.6>>, 0.7);
"""),

    Scene("viewer", "Open that address in the disassembler: Cheat Engine's Memory Viewer. Address, bytes, text. "
                  "Now look one line above ours. Move E A X, brackets, E S I plus one four. That is where E A X came from.",
          body=txt("@p-t", 120, 80, "the game's code, in the Memory Viewer", "h", fs=72) + mv_dec.html()
          + mv_dec.mark("@p-m1", 2, ROW(6), 480, 22, pad=4) + mv_dec.mark("@p-m2", 328, ROW(5), 160, 22, pad=4)
          + tag("@p-g1", 120, 835, "address", 36) + tag("@p-g2", 510, 835, "bytes", 36) + tag("@p-g3", 960, 835, "text", 36)
          + txt("@p-n", 120, 915, "ac_client.exe+C73EF = 004C73EF (the module starts at 00400000)", "m", fs=40)
          + txt("@p-d", 120, 975, 'eax = <span class="@p-acc">[esi+14]</span>', "h", fs=60),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-mv", 0.2, 1.03, 0.5);
    land("#@p-m1", <<address-0.2>>, 1.05);
    land("#@p-g1", <<address#2>>); land("#@p-g2", <<bytes>>); land("#@p-g3", <<text>>);
    blurIn("#@p-n", <<text+0.5>>);
    land("#@p-m2", <<above-0.3>>, 1.2);
    wipe("#@p-d", <<came-0.6>>, 0.6);
"""),

    Scene("chain", "Sound familiar? Last episode's chain said: the weapon, plus one four, holds the address of the ammo. "
                   "This is the game's own code walking that chain. E S I is the weapon.",
          body=txt("@p-t", 120, 100, "the game walks its own pointer chain", "h", fs=76)
          + card("@p-c0", 120, 330, 480, 160, "esi", 80, "on") + txt("@p-v0", 120, 510, f"the weapon<br>{WEAPON}", "m", fs=44)
          + bar("@p-b0", 600, 403, 110, 14)
          + card("@p-c1", 710, 330, 480, 160, "[esi+14]", 72) + txt("@p-v1", 710, 510, f"holds<br>{MAG}", "m", fs=44)
          + bar("@p-b1", 1190, 403, 110, 14)
          + tile("@p-c2", 1300, 320, 480, 180, "ammo - 1", 70) + txt("@p-v2", 1300, 530, "dec [eax]", "m", fs=44)
          + term("@p-o", 120, 730, 1000, ["mov   eax, " + hi("[esi+14]"), "dec   " + hi("[eax]")], fs=60, lh=1.5)
          + txt("@p-d", 1190, 780, "read the pointer,<br>then use it", "m", fs=50),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-c0", <<weapon-0.3>>); blurIn("#@p-v0", <<weapon>>);
    wipe("#@p-b0", <<plus-0.2>>, 0.3); land("#@p-c1", <<plus>>); blurIn("#@p-v1", <<holds>>);
    wipe("#@p-b1", <<ammo-0.3>>, 0.3); land("#@p-c2", <<ammo>>); blurIn("#@p-v2", <<ammo+0.3>>);
    land("#@p-o", <<own-0.3>>, 1.04, 0.4);
    blurIn("#@p-d", <<walking>>);
"""),

    Scene("health", "Same question for the health: what reads it? Two instructions, hundreds of times each. "
                  "Look at the first. Move E C X, brackets, E B X plus E C. E B X is the player. E C is the offset of health.",
          body=txt("@p-t", 120, 80, "find out what accesses the health", "h", fs=76) + acc_list.html()
          + acc_list.mark("@p-m0", 4, 66, 50, 48, pad=4) + acc_list.mark("@p-m1", 262, 68, 182, 20, pad=5)
          + term("@p-o", 120, 520, 1000, ["mov   ecx, " + hi("[ebx+EC]")], fs=72)
          + card("@p-a", 120, 730, 520, 130, f"ebx = {PLAYER}", 44) + txt("@p-al", 120, 880, "the player", "m", fs=46)
          + card("@p-b", 700, 730, 420, 130, "+ EC", 60, "on") + txt("@p-bl", 700, 880, "health", "m", fs=46)
          + txt("@p-eq", 1150, 740, "&rarr;", "h", fs=100)
          + card("@p-c", 1290, 730, 500, 130, "ecx = 00000064", 44) + txt("@p-cl", 1290, 880, "= 100", "m", fs=46),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-f", 0.2, 1.03, 0.5);
    land("#@p-m0", <<hundreds-0.3>>, 1.2);
    land("#@p-m1", <<first-0.3>>, 1.2); land("#@p-o", <<move-0.2>>, 1.04, 0.4);
    land("#@p-a", <<player-0.4>>); blurIn("#@p-al", <<player>>);
    land("#@p-b", <<offset-1.0>>); blurIn("#@p-bl", <<offset>>);
    blurIn("#@p-eq", <<offset+0.2>>); land("#@p-c", <<offset+0.3>>); blurIn("#@p-cl", <<offset+0.5>>);
"""),

    Scene("cmp", "Next line. C M P, E C X, one nine: compare the health with hex nineteen, twenty-five. "
                  "Then J N G: jump if not greater. C M P sets flags, the jump reads them. That is what an if looks like in assembly.",
          body=txt("@p-t", 120, 80, "compare, then jump", "h", fs=80) + acc_code.html()
          + acc_code.mark("@p-m1", 6, 302, 250, 20, pad=4) + acc_code.mark("@p-m2", 6, 322, 400, 20, pad=4)
          + card("@p-a", 120, 590, 300, 130, "cmp", 70, "on") + txt("@p-al", 460, 600, "compare: health with 0x19 = 25<br>changes nothing, sets flags", "m", fs=42)
          + card("@p-b", 120, 760, 300, 130, "jng", 70, "on") + txt("@p-bl", 460, 770, "jump if not greater<br>reads the flags", "m", fs=42)
          + tile("@p-k", 1300, 640, 500, 190, "if", 110)
          + txt("@p-d", 120, 940, 'health &lt;= 25 ? <span class="@p-acc">jump</span> : keep going', "m", fs=54),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-f", 0.2, 1.03, 0.5);
    land("#@p-m1", <<c-0.2>>, 1.2); land("#@p-a", <<compare>>); blurIn("#@p-al", <<compare+0.3>>);
    land("#@p-m2", <<j-0.3>>, 1.2); land("#@p-b", <<j>>); blurIn("#@p-bl", <<jump>>);
    blurIn("#@p-d", <<reads>>);
    land("#@p-k", <<looks-0.8>>);
"""),

    Scene("ourif", "Our own program has the same pair: compare health with zero, then J G, jump if greater, right over the call to puts. "
                   "The jump is the opposite of the if: the compiler skips the block when the condition is false.",
          body=txt("@p-t", 120, 60, "the same pair in calls.cpp", "h", fs=72)
          + card("@p-s", 120, 180, 1100, 130, 'if (health &lt;= 0) &nbsp;std::puts("dead");', 44, "soft")
          + term("@p-o", 120, 350, 1100, L23, fs=42, lh=1.42)
          + tag("@p-g1", 1270, 470, "health vs 0") + tag("@p-g2", 1270, 560, "greater? skip the block")
          + txt("@p-d", 1270, 720, 'the jump is<br><span class="@p-acc">the opposite</span><br>of the if', "h", fs=62),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-s", 0.4, 1.03, 0.4);
    land("#@p-o", <<pair-0.3>>, 1.03, 0.5);
    land("#@p-g1", <<compare>>); land("#@p-g2", <<greater>>);
    tl.fromTo(["#@p-o-l5", "#@p-o-l6", "#@p-o-l7"], { opacity: 1 }, { opacity: 0.35, duration: 0.3 }, <<over>>);
    wipe("#@p-d", <<opposite-0.5>>, 0.7);
"""),


    Scene("payoff", "And the line from last time? Same parts, other direction. It writes E A X into the field at E B X plus E C.",
          body=txt("@p-t", 190, 100, "now read it", "h", fs=90)
          + term("@p-o", 190, 260, 1200, ['mov  [ebx+<span class="hi">EC</span>], eax'], fs=88)
          + card("@p-a", 190, 540, 700, 130, "[ebx+EC]", 64, "on") + txt("@p-al", 940, 570, "destination: the field at +EC", "m", fs=48)
          + card("@p-b", 190, 710, 700, 130, "eax", 64) + txt("@p-bl", 940, 740, "source: the new value", "m", fs=48)
          + txt("@p-d", 190, 900, 'a <span class="@p-acc">write</span>: in our game, +EC is health', "h", fs=64),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-o", 0.5, 1.04, 0.4);
    land("#@p-b", <<parts>>); blurIn("#@p-bl", <<parts+0.2>>);
    land("#@p-a", <<direction-0.3>>); blurIn("#@p-al", <<direction>>);
    wipe("#@p-d", <<writes-0.2>>, 0.6);
"""),

    # ------------------------------------------------------------------ the stack
    Scene("stack", "Second half: functions. Code needs scratch space in memory: the stack. "
                  "Push puts a value on top. Pop takes the top value off. And one register, E S P, "
                  "always holds the address of the top.",
          body=txt("@p-t", 190, 100, "the stack", "h", fs=110)
          + card("@p-s0", 190, 760, 560, 120, "older value", 50, "soft") + card("@p-s1", 190, 620, 560, 120, "older value", 50, "soft")
          + card("@p-s2", 190, 480, 560, 120, "pushed value", 50, "on")
          + bar("@p-b", 760, 533, 150, 14) + tile("@p-k", 910, 465, 300, 150, "esp", 80)
          + txt("@p-kl", 1250, 500, "= address of the top", "m", fs=48)
          + card("@p-a", 910, 700, 300, 130, "push", 64) + txt("@p-al", 1250, 735, "put a value on top", "m", fs=48)
          + card("@p-c", 910, 860, 300, 130, "pop", 64) + txt("@p-cl", 1250, 895, "take the top value off", "m", fs=48)
          + txt("@p-n", 190, 910, "scratch space in memory", "m", fs=44),
          js="""
    wipe("#@p-t", <<functions-0.5>>, 0.5);
    each(["#@p-s0", "#@p-s1"], <<scratch-0.3>>, 0.2); blurIn("#@p-n", <<scratch>>);
    land("#@p-a", <<push>>); blurIn("#@p-al", <<push+0.2>>); land("#@p-s2", <<top-0.2>>);
    land("#@p-c", <<pop>>); blurIn("#@p-cl", <<pop+0.2>>);
    wipe("#@p-b", <<register-0.2>>, 0.3); land("#@p-k", <<register>>); blurIn("#@p-kl", <<holds>>);
"""),

    Scene("brka", "Watch it in the game. I put a breakpoint just before two pushes, and fire. "
                  "The game freezes on that line, and Cheat Engine shows every register. E S P is zero zero one A, F D three C.",
          body=txt("@p-t", 120, 80, "the game, stopped at a breakpoint", "h", fs=76) + bA.html() + rA.html()
          + bA.mark("@p-m1", 2, BROW(8), 716, 22, pad=3) + rA.mark("@p-m2", 754, REG_Y["esp"], 150, 19, pad=3)
          + txt("@p-al", 120, 850, "esp, before the pushes", "m", fs=48)
          + tile("@p-a", 120, 920, 700, 130, "001AFD3C", 80)
          + tag("@p-g", 900, 870, "next: push eax, push ecx"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-mv", 0.2, 1.03, 0.5);
    land("#@p-m1", <<freezes-0.3>>, 1.05); land("#@p-g", <<pushes>>);
    land("#@p-rg", <<register-0.6>>, 1.03, 0.4);
    land("#@p-m2", <<zero-0.4>>, 1.3); blurIn("#@p-al", <<zero-0.2>>); land("#@p-a", <<zero>>);
"""),

    Scene("brkb", "I let it run to the call. Two pushes later, E S P is zero zero one A, F D three four. Eight less. "
                  "The stack grows downward: each push subtracts four from E S P.",
          body=txt("@p-t", 120, 80, "two pushes later", "h", fs=76) + bB.html() + rB.html()
          + bB.mark("@p-m1", 2, BROW(8), 716, 44, pad=3) + rB.mark("@p-m2", 754, REG_Y["esp"], 150, 19, pad=3)
          + card("@p-a", 120, 880, 420, 130, "001AFD3C", 60, "soft") + txt("@p-mi", 570, 895, "- 8 =", "h", fs=80)
          + tile("@p-b", 800, 870, 480, 150, "001AFD34", 72)
          + txt("@p-d", 1330, 860, 'push = <span class="@p-acc">esp - 4</span>,<br>then store', "h", fs=56),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-mv", 0.2, 1.03, 0.5); land("#@p-rg", 0.3, 1.03, 0.5);
    land("#@p-m1", <<two-0.2>>, 1.05);
    land("#@p-m2", <<zero-0.4>>, 1.3); land("#@p-a", <<zero-0.2>>); land("#@p-b", <<f>>);
    blurIn("#@p-mi", <<eight>>);
    wipe("#@p-d", <<each-0.2>>, 0.7);
"""),

    Scene("brkc", "Now the call itself. One instruction later, we are inside the function. E S P dropped by four more, and on top of the stack "
                  "sits zero zero four C, seven three F E: the line right after the call. The return address. "
                  "Call pushes it. Ret pops it, and jumps back.",
          body=txt("@p-t", 120, 70, "inside the called function", "h", fs=76) + bC.html() + rC.html() + retC.html()
          + rC.mark("@p-m2", 754, REG_Y["esp"], 150, 19, pad=3) + retC.mark("@p-m3", 756, 993, 140, 22, pad=3)
          + txt("@p-al", 940, 770, "on top of the stack", "m", fs=44) + tile("@p-a", 940, 830, 560, 140, "004C73FE", 80)
          + card("@p-c", 120, 790, 330, 110, "call", 60, "on") + txt("@p-cl", 480, 815, "push return address, jump", "m", fs=30)
          + card("@p-r", 120, 930, 330, 110, "ret", 60, "on") + txt("@p-rl", 480, 955, "pop it, jump back", "m", fs=30)
          + tag("@p-g", 1525, 870, "esp: 001AFD30", 34),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-mv", 0.2, 1.03, 0.5);
    land("#@p-rg", <<dropped-0.8>>, 1.03, 0.4); land("#@p-m2", <<dropped>>, 1.3); land("#@p-g", <<four>>);
    land("#@p-rt", <<top-0.5>>, 1.03, 0.4); land("#@p-m3", <<zero-0.3>>, 1.2);
    blurIn("#@p-al", <<zero-0.2>>); land("#@p-a", <<zero>>);
    land("#@p-c", <<pushes-0.4>>); blurIn("#@p-cl", <<pushes>>);
    land("#@p-r", <<ret>>); blurIn("#@p-rl", <<pops>>);
"""),

    Scene("args", "And those pushes before the call? They are the function's arguments. In thirty-two bit code, arguments go on the stack, "
                  "right above the return address.",
          body=txt("@p-t", 190, 80, "where a function keeps its arguments", "h", fs=72)
          + tag("@p-g", 190, 200, "the same stop: read from the game's stack", 34)
          + txt("@p-e", 30, 320, "esp", "h", fs=56, color="#E8490F")
          + stack_row(0, 290, "001AFD30", "004C73FE", "the return address", True)
          + stack_row(1, 420, "001AFD34", "00000078", "argument: push ecx")
          + stack_row(2, 550, "001AFD38", "001AFD58", "argument: push eax")
          + stack_row(3, 680, "001AFD3C", "0007DEA4", "argument: push ebx (earlier)")
          + txt("@p-d", 190, 840, '32-bit: <span class="@p-acc">arguments are on the stack</span>', "h", fs=72)
          + txt("@p-n", 190, 950, "the function ends with ret 0C: it removes all three itself", "m", fs=44),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-g", 0.5);
    each(["#@p-sv1", "#@p-sv2", "#@p-sv3"], <<pushes-0.3>>, 0.25); each(["#@p-sa1", "#@p-sa2", "#@p-sa3"], <<pushes>>, 0.25, 1);
    each(["#@p-sl1", "#@p-sl2", "#@p-sl3"], <<arguments-0.2>>, 0.25, 1);
    wipe("#@p-d", <<thirty-two-0.3>>, 0.8);
    land("#@p-sv0", <<return-0.3>>); blurIn("#@p-sa0", <<return>>); blurIn("#@p-sl0", <<return>>); blurIn("#@p-e", <<return+0.3>>);
    blurIn("#@p-n", <<stack-0.3>>);
"""),

    Scene("cdecl", "Our own program shows it cleanly. Add three, of one, two, three: push three, push two, push one, call. "
                  "Last argument first. Then add E S P, twelve: the caller throws them away. That is C decl.",
          body=txt("@p-t", 120, 60, "calling add3(1, 2, 3)", "h", fs=72)
          + card("@p-s", 120, 180, 1100, 120, "int s = add3(1, 2, 3);", 48, "soft")
          + term("@p-o", 120, 340, 1100, L29, fs=46, lh=1.45)
          + tag("@p-n", 1270, 200, "names shortened", 32)
          + tag("@p-g1", 1270, 440, "last argument first") + tag("@p-g2", 1270, 690, "caller removes 12 bytes", 36)
          + tile("@p-k", 1270, 840, 420, 150, "cdecl", 80)
          + txt("@p-d", 120, 930, "the caller cleans up the stack", "m", fs=54),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-s", 0.4, 1.03, 0.4); land("#@p-n", 0.8);
    land("#@p-o", <<push-0.4>>, 1.03, 0.5);
    land("#@p-g1", <<last>>);
    land("#@p-g2", <<twelve>>);
    blurIn("#@p-d", <<caller-0.4>>);
    land("#@p-k", <<decl-0.4>>);
"""),

    Scene("inside", "Inside add three, the arguments are read at E B P plus eight, plus twelve, and plus sixteen. "
                    "And the result is left in E A X: that is how a function returns a value.",
          body=txt("@p-t", 120, 60, "inside add3", "h", fs=72)
          + term("@p-o", 120, 190, 1100, ADD3, fs=42, lh=1.42)
          + tag("@p-g0", 1270, 230, "ebp = a fixed anchor", 36)
          + tag("@p-g1", 1270, 440, "_a$ = 8") + tag("@p-g2", 1270, 520, "_b$ = 12") + tag("@p-g3", 1270, 600, "_c$ = 16")
          + txt("@p-gl", 1270, 690, "from the listing:<br>[ebp+8], [ebp+12], [ebp+16]", "m", fs=36)
          + tile("@p-k", 1270, 840, 520, 150, "result: eax", 60),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-o", 0.4, 1.03, 0.5);
    land("#@p-g0", <<inside+0.6>>);
    land("#@p-g1", <<eight>>); land("#@p-g2", <<twelve>>); land("#@p-g3", <<sixteen>>); blurIn("#@p-gl", <<sixteen+0.3>>);
    land("#@p-k", <<result>>);
"""),

    Scene("thisown", "Methods get one twist. For P dot hit of thirty, the thirty is pushed, but the object's address goes into E C X. "
                     "And hit ends with ret four: the function removes its own argument. That is this call.",
          body=txt("@p-t", 120, 60, "calling a method: p.hit(30)", "h", fs=72)
          + term("@p-o", 120, 190, 1100, L30, fs=44, lh=1.45)
          + tag("@p-n", 1270, 100, "names shortened", 32)
          + tag("@p-g1", 1270, 290, "the argument: stack")
          + tag("@p-g2", 1270, 370, "the object: ecx")
          + tag("@p-g3", 1270, 720, "pops 4 extra bytes")
          + tile("@p-k", 1270, 840, 520, 150, "thiscall", 76)
          + txt("@p-d", 120, 880, "lea: compute an address, read nothing", "m", fs=46),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-o", 0.4, 1.03, 0.5); land("#@p-n", 0.9);
    land("#@p-g1", <<pushed>>);
    land("#@p-g2", <<object's>>);
    blurIn("#@p-d", <<goes>>);
    land("#@p-g3", <<ret>>);
    land("#@p-k", <<this-0.2>>);
"""),

    Scene("thisgame", "Now the game again. Push, push, move E C X, E S I, call. Arguments on the stack, "
                  "the object in E C X. This call, in the real game. E C X loaded right before a call usually means: an object.",
          body=txt("@p-t", 120, 70, "the same pattern in the game", "h", fs=76) + mv_this.html()
          + mv_this.mark("@p-m1", 2, ROW(8), 480, 44, pad=3) + mv_this.mark("@p-m2", 2, ROW(10), 480, 22, pad=3)
          + mv_this.mark("@p-m3", 2, ROW(11), 560, 22, pad=3) + mv_this.mark("@p-m4", 2, ROW(17), 480, 22, pad=3)
          + tag("@p-g1", 1330, 265, "arguments") + tag("@p-g2", 1330, 375, "ecx = the weapon") + tag("@p-g4", 1340, 775, "this function: ret 4 too", 34)
          + txt("@p-d", 120, 900, 'ecx loaded before a call = <span class="@p-acc">an object</span>', "h", fs=68),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-mv", 0.2, 1.03, 0.5);
    land("#@p-m1", <<push>>, 1.05); land("#@p-g1", <<arguments>>);
    land("#@p-m2", <<move-0.2>>, 1.05); land("#@p-g2", <<object>>);
    land("#@p-m3", <<call>>, 1.05);
    land("#@p-m4", <<real-0.4>>, 1.05); land("#@p-g4", <<real>>);
    wipe("#@p-d", <<loaded-0.8>>, 0.8);
"""),


    Scene("start", "And the top of the function. It pushes E B X, E S I and E D I to save them, and pops them back before it returns. "
                  "In between: move E S I, E C X. That is why E S I was the weapon all along.",
          body=txt("@p-t", 120, 60, "the first and last lines of the function", "h", fs=68) + mv_top.html() + mv_end.html()
          + mv_top.mark("@p-m1", 328, ROW(1), 130, 22, pad=3) + mv_top.mark("@p-m1b", 328, ROW(3), 130, 22, pad=3)
          + mv_top.mark("@p-m1c", 328, ROW(6), 130, 22, pad=3)
          + mv_top.mark("@p-m3", 328, ROW(4), 150, 22, pad=3)
          + mv_end.mark("@p-m2", 328, ROW(29), 130, 44, pad=3) + mv_end.mark("@p-m2b", 328, ROW(32), 130, 22, pad=3)
          + tag("@p-g1", 1640, 250, "save", 44) + tag("@p-g2", 1640, 690, "restore", 44)
          + txt("@p-d", 120, 960, 'esi = ecx = <span class="@p-acc">the weapon</span>', "h", fs=60),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-mv", 0.2, 1.03, 0.5); land("#@p-mv2", 0.4, 1.03, 0.5);
    each(["#@p-m1", "#@p-m1b", "#@p-m1c"], <<pushes>>, 0.3, 1.2); land("#@p-g1", <<save>>);
    each(["#@p-m2", "#@p-m2b"], <<pops-0.2>>, 0.2, 1.2); land("#@p-g2", <<pops>>);
    land("#@p-m3", <<between>>, 1.3);
    wipe("#@p-d", <<why-0.3>>, 0.7);
"""),

    # ------------------------------------------------------------------ 64-bit
    Scene("x64", "One last thing. Build the same program as sixty-four bit, and the rules change. "
                  "Register names start with R, and hold eight bytes. And the first four arguments skip the stack: "
                  "R C X, R D X, R eight, R nine.",
          body=txt("@p-t", 120, 60, "the same calls, 64-bit", "h", fs=72)
          + term("@p-o", 120, 190, 1000, X64, fs=42, lh=1.42)
          + tag("@p-n", 1180, 100, "calls.asm, names shortened", 32)
          + "".join(card(f"@p-r{i}", 1180 + (i % 2) * 320, 240 + (i // 2) * 250, 280, 140, n, 68, "on")
                    + txt(f"@p-rl{i}", 1180 + (i % 2) * 320, 395 + (i // 2) * 250, s, "m", fs=38, w=280, align="center")
                    for i, (n, s) in enumerate([("rcx", "argument 1"), ("rdx", "argument 2"), ("r8", "argument 3"), ("r9", "argument 4")]))
          + txt("@p-d", 1180, 760, "ecx, edx, r8d =<br>their lower 4 bytes", "m", fs=44)
          + txt("@p-e", 120, 900, 'no pushes: <span class="@p-acc">arguments ride in registers</span>', "h", fs=60),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-o", 0.4, 1.03, 0.5); land("#@p-n", <<sixty-four>>);
    wipe("#@p-e", <<skip-0.4>>, 0.7);
    land("#@p-r0", <<stack+0.5>>); land("#@p-r1", <<stack+1.3>>); land("#@p-r2", <<stack+2.1>>); land("#@p-r3", <<nine-0.3>>);
    each(["#@p-rl0", "#@p-rl1", "#@p-rl2", "#@p-rl3"], <<nine>>, 0.1, 1);
    blurIn("#@p-d", <<stack>>);
"""),

    Scene("worlds", "So, two worlds. Thirty-two bit, like AssaultCube: arguments on the stack, the object in E C X. "
                  "Sixty-four bit Windows: arguments in registers, and the object is simply the first one. "
                  "Always check which world you are in.",
          body=txt("@p-t", 190, 80, "two worlds", "h", fs=96)
          + card("@p-a", 190, 250, 740, 120, "32-bit (AssaultCube)", 48, "on") + card("@p-b", 990, 250, 740, 120, "64-bit Windows", 48, "on")
          + card("@p-a1", 190, 410, 740, 110, "arguments: the stack", 42) + card("@p-b1", 990, 410, 740, 110, "rcx, rdx, r8, r9", 42)
          + card("@p-a2", 190, 550, 740, 110, "object: ecx", 42) + card("@p-b2", 990, 550, 740, 110, "object: rcx (argument 1)", 42)
          + card("@p-a3", 190, 690, 740, 110, "result: eax", 42) + card("@p-b3", 990, 690, 740, 110, "result: rax", 42)
          + txt("@p-d", 190, 880, 'first question: <span class="@p-acc">32 or 64?</span>', "h", fs=80),
          js="""
    wipe("#@p-t", <<two-0.2>>, 0.5);
    land("#@p-a", <<thirty-two-0.2>>);
    land("#@p-a1", <<stack-0.5>>); land("#@p-a2", <<object-0.2>>); land("#@p-a3", <<object+1.0>>);
    land("#@p-b", <<sixty-four-0.2>>);
    land("#@p-b1", <<registers-0.5>>); land("#@p-b2", <<object#2-0.2>>); land("#@p-b3", <<first>>);
    wipe("#@p-d", <<always-0.2>>, 0.7);
"""),


    # ------------------------------------------------------------------ outro
    Scene("recap", "Let's recap. One line: instruction, destination, source. Brackets mean memory, "
                  "so register plus offset is a field of an object. Compare plus jump is an if. "
                  "The stack holds return addresses, and thirty-two bit arguments. "
                  "Today, we changed nothing. We only read.",
          body=txt("@p-t", 190, 80, "recap", "h", fs=110)
          + txt("@p-a", 190, 270, "instruction destination, source", "m", fs=54)
          + txt("@p-b", 190, 400, "[register + offset] = a field of an object", "m", fs=54)
          + txt("@p-c", 190, 530, "cmp + jump = an if", "m", fs=54)
          + txt("@p-d", 190, 660, "the stack: return addresses, and 32-bit arguments", "m", fs=54)
          + txt("@p-e", 190, 790, 'a method\'s object: <span class="@p-acc">ecx</span> (64-bit: rcx)', "m", fs=54)
          + txt("@p-f", 190, 930, "today: read only. changing code comes in episode 7", "m", fs=44, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    wipe("#@p-a", <<instruction-0.3>>, 0.8);
    wipe("#@p-b", <<brackets>>, 0.8);
    wipe("#@p-c", <<compare>>, 0.8);
    wipe("#@p-d", <<stack>>, 0.8);
    wipe("#@p-e", <<arguments+0.5>>, 0.8);
    blurIn("#@p-f", <<today>>);
"""),

    Scene("practice", "Your practice. Compile calls dot C P P from the description with slash F A, and open calls dot A S M. "
                  "Find the instruction that writes the health. Then add an int field above health, and predict the new offset. "
                  "The last line the program prints is your answer key.",
          body=txt("@p-t", 190, 80, "practice", "h", fs=110)
          + tag("@p-g", 900, 110, "calls.cpp: link in the description", 36)
          + term("@p-o", 190, 270, 1300, ["&gt; cl /Od /FA calls.cpp", "&gt; calls.exe", "sum 6  health 70",
                                           "offset of health: " + hi("4") + "   offset of ammo: 8"], fs=46)
          + txt("@p-a", 190, 640, "1. in calls.asm: which line writes the health?", "m", fs=50)
          + txt("@p-b", 190, 740, "2. add an int above health, recompile", "m", fs=50)
          + txt("@p-c", 190, 840, '3. predict the new offset, <span class="@p-acc">then check the last line</span>', "m", fs=50),
          js="""
    wipe("#@p-t", <<practice-0.2>>, 0.5);
    land("#@p-g", <<description-0.4>>);
    land("#@p-o", <<compile-0.3>>, 1.04, 0.4);
    blurIn("#@p-a", <<find>>);
    blurIn("#@p-b", <<add>>);
    blurIn("#@p-c", <<predict>>);
"""),

    Scene("next", "Next time, we leave the running game and open the files on disk: changing a file byte by byte in a hex editor, "
                  "and what is really inside an E X E. See you there.",
          body=txt("@p-s", 192, 220, "NEXT EPISODE", "m", fs=64)
          + txt("@p-a", 192, 330, "Inside", "h", fs=150) + txt("@p-b", 192, 490, 'the <span class="@p-acc">Files</span>', "h", fs=150)
          + cells("@p-c", 192, 740, ["4D", "5A", "90", "00"], size=150, gap=20, on=(0, 1))
          + txt("@p-d", 900, 780, "a hex editor,<br>and an EXE opened up", "m", fs=50),
          js="""
    blurIn("#@p-s", <<next>>);
    wipe("#@p-a", <<files-0.6>>, 0.6); wipe("#@p-b", <<files-0.2>>, 0.5);
    each(".c-@p-c", <<hex-0.3>>, 0.12);
    blurIn("#@p-d", <<inside>>);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Game Hacking from Scratch 3: Read One Line of Assembly")
