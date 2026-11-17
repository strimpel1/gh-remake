"""Game Hacking from Scratch, episode 1: The Bytes Behind the Health Bar (number bases + data types).

Long-form YouTube episode. Every screenshot and recording is real: AssaultCube 1.3.0.2 (open source) running offline,
Cheat Engine attached to it, Windows Calculator, and the output of lab/bytes.cpp.   Run: python build.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, Shot, bar, build, card, cells, fit_clip, tag, term, tile, txt  # noqa: E402,F401

A = Path(__file__).resolve().parent / "assets"
MV = (0, 128, 902, 330)            # memory viewer: the hex pane
LIST = (0, 596, 902, 334)          # Cheat Engine: the address list
ROW = {"health": 620, "health_raw": 644, "health_byte": 668, "health_float": 693, "ammo": 717, "ammo_raw": 741, "reserve": 765,
       "pos": 789, "pos_raw": 813, "pos_int": 837, "name": 861, "name_raw": 885}   # top of each row in ce_table.png


def mv(name="mv_health", y=230, crop=MV):
    return Shot("@p-mv", A / f"shots/{name}.png", 120, y, 1680, crop=crop)


def table(y=250):
    return Shot("@p-ce", A / "shots/ce_table.png", 120, y, 1680, crop=LIST)


def row_mark(s, id, row, x=672, w=160):
    return s.mark(id, x, ROW[row], w, 24, pad=6)


BITS = ["0", "1", "1", "0", "0", "1", "0", "0"]
PLACES = ["128", "64", "32", "16", "8", "4", "2", "1"]
BX, BY, BS, BG = 264, 430, 150, 28          # the bit row: x, y, size, gap


def bit_row(vals=BITS, on=(), y=BY):
    return cells("@p-b", BX, y, vals, size=BS, gap=BG, on=on)


def place_row(y=BY - 90):
    return "".join(txt(f"@p-pv{i}", BX + i * (BS + BG), y, v, "m", fs=50, w=BS, align="center") for i, v in enumerate(PLACES))


ONE = ["0", "0", "1", "0", "0", "0", "0", "0"]

OUT = ["&gt; bytes.exe",
       'int 100         <span class="hi">64 00 00 00</span>',
       'int 1000        <span class="hi">E8 03 00 00</span>',
       'int -1          <span class="hi">FF FF FF FF</span>',
       'float 43.0      <span class="hi">00 00 2C 42</span>']

GAME = (1582, 890)
CEV = (898, 350)


def live_game(still=False):
    s = Shot("@p-g", A / ("shots/live_game.png" if still else "clips/shoot_game.mp4"), 410, 50, 1100, size=GAME)
    return s


def live_ce(still=False):
    return Shot("@p-c", A / ("shots/live_ce.png" if still else "clips/shoot_ce.mp4"), 110, 760, 1700, crop=(0, 124, 898, 50), size=CEV)


def live_media(dur):
    g, c = live_game(), live_ce()
    g.path = fit_clip(A / "clips/shoot_game.mp4", dur, 2.6)
    c.path = fit_clip(A / "clips/shoot_ce.mp4", dur, 2.6)
    g.src, c.src = f"assets/clips/{g.path.name}", f"assets/clips/{c.path.name}"
    return g.video(0, dur) + c.video(0, dur)


hud = Shot("@p-hud", A / "shots/game_hud.png", 210, 96, 1500)
calc = Shot("@p-calc", A / "shots/calc.png", 190, 170, 800, crop=(0, 0, 634, 440))
scan = Shot("@p-scan", A / "shots/ce_table.png", 190, 250, 1100, crop=(410, 125, 492, 168))

scenes = [
    # ------------------------------------------------------------------ cold open
    Scene("cold", "This is AssaultCube, an open-source shooter, running offline on my own machine. Health: one hundred. Ammo: twenty.",
          body=hud.html() + hud.mark("@p-m1", 8, 808, 200, 76) + hud.mark("@p-m2", 476, 808, 196, 76)
          + tag("@p-t1", 250, 720, "health 100") + tag("@p-t2", 700, 720, "ammo 20"),
          js="""
    land("#@p-m1", <<health>>, 1.4); land("#@p-t1", <<health+0.15>>);
    land("#@p-m2", <<ammo>>, 1.4); land("#@p-t2", <<ammo+0.15>>);
"""),

    Scene("memory", "Those numbers live somewhere in the game's memory. And this is what that memory really looks like.",
          body=txt("@p-t", 120, 96, "the game's memory, right now", "h", fs=80) + mv().html(),
          js="""
    wipe("#@p-t", <<memory>>, 0.6);
    land("#@p-mv", <<this>>, 1.05, 0.5);
""", exit=False),

    Scene("promise", "No one hundred anywhere. Just six four, zero zero, zero zero, zero zero. "
                     "By the end of this video, you will read a line like that as easily as the health bar itself.",
          body=txt("@p-t", 120, 96, "the game's memory, right now", "h", fs=80) + mv().html()
          + mv().mark("@p-m", 88, 171, 116, 24) + tag("@p-g", 520, 300, "this is the health")
          + txt("@p-c", 120, 900, 'by the end, you can <span class="@p-acc">read this line</span>', "h", fs=84),
          js="""
    land("#@p-m", <<six>>, 1.5);
    land("#@p-g", <<six+0.5>>);
    wipe("#@p-c", <<read>>, 0.7);
""", enter=False),

    Scene("title", "This is Game Hacking from Scratch. Episode one: the bytes behind the health bar.",
          body=txt("@p-s", 192, 250, "GAME HACKING FROM SCRATCH", "m", fs=64)
          + txt("@p-a", 192, 360, "The Bytes Behind", "h", fs=150) + txt("@p-b", 192, 520, 'the <span class="@p-acc">Health Bar</span>', "h", fs=150)
          + tile("@p-e", 192, 760, 420, 130, "EPISODE 1", 60),
          js="""
    blurIn("#@p-s", <<game>>);
    wipe("#@p-a", <<bytes-0.3>>, 0.6);
    wipe("#@p-b", <<health-0.2>>, 0.6);
    land("#@p-e", <<episode>>);
"""),

    Scene("rules", "One rule for the whole series. We only practice on things we are allowed to touch: open-source games, offline, "
                   "against bots, and programs we wrote ourselves. Never online games. Never other players.",
          body=txt("@p-t", 190, 110, "the one rule", "h", fs=96)
          + card("@p-a", 190, 300, 760, 130, "open-source games", 52, "on") + card("@p-b", 190, 470, 760, 130, "offline, against bots", 52, "on")
          + card("@p-c", 190, 640, 760, 130, "programs we wrote", 52, "on")
          + card("@p-x", 1060, 385, 670, 130, "online games", 52, "soft") + card("@p-y", 1060, 555, 670, 130, "other players", 52, "soft")
          + bar("@p-x1", 1040, 447, 710, 8) + bar("@p-y1", 1040, 617, 710, 8)
          + txt("@p-n", 1060, 300, "never", "h", fs=64, color="#E8490F"),
          js="""
    wipe("#@p-t", <<rule-0.3>>, 0.5);
    land("#@p-a", <<open-source>>); land("#@p-b", <<offline>>); land("#@p-c", <<programs>>);
    blurIn("#@p-n", <<never-0.1>>);
    land("#@p-x", <<never>>); wipe("#@p-x1", <<never+0.35>>, 0.3);
    land("#@p-y", <<never#2>>); wipe("#@p-y1", <<never#2+0.35>>, 0.3);
"""),

    # ------------------------------------------------------------------ bits and bytes
    Scene("byte", "Start with the smallest piece. Memory is a very long row of boxes. Each box is one byte, and every byte has its own address.",
          body=txt("@p-t", 190, 130, "memory = a long row of boxes", "h", fs=90)
          + cells("@p-b", 190, 420, ["64", "00", "00", "00", "00", "00", "00", "00"], size=160, gap=32, on=(0,))
          + "".join(txt(f"@p-a{i}", 190 + i * 192, 610, f"{0x6C + i:02X}", "m", fs=46, w=160, align="center") for i in range(8))
          + txt("@p-l1", 190, 760, "one box = one byte", "m", fs=60) + txt("@p-l2", 190, 850, "the number under it = its address", "m", fs=60),
          js="""
    wipe("#@p-t", <<memory-0.2>>, 0.7);
    each(".c-@p-b", <<row>>, 0.07);
    blurIn("#@p-l1", <<byte>>);
    each(["#@p-a0", "#@p-a1", "#@p-a2", "#@p-a3", "#@p-a4", "#@p-a5", "#@p-a6", "#@p-a7"], <<address-0.5>>, 0.06, 1);
    blurIn("#@p-l2", <<every>>);
"""),

    Scene("bits", "A byte is eight switches, called bits. Each bit is off or on. Zero or one.",
          body=txt("@p-t", BX, 150, "1 byte = 8 bits", "h", fs=110) + bit_row(ONE, on=(2,))
          + txt("@p-l", BX, 700, "each bit: off or on, 0 or 1", "m", fs=64),
          js="""
    wipe("#@p-t", <<eight-0.3>>, 0.6);
    each(".c-@p-b", <<switches>>, 0.08);
    blurIn("#@p-l", <<off>>);
    tl.fromTo("#@p-b2", { scale: 1 }, { scale: 1.12, duration: 0.2, yoyo: true, repeat: 1 }, <<one>>);
""", exit=False),

    Scene("places", "Each bit has a place value, and every place is worth double the one to its right. One, two, four, eight, "
                    "all the way up to one hundred twenty-eight.",
          body=txt("@p-t", BX, 150, "every place is worth double", "h", fs=96) + bit_row(ONE, on=(2,)) + place_row()
          + txt("@p-l", BX, 700, "each place = 2 &times; the one on its right", "m", fs=60),
          js="""
    wipe("#@p-t", <<place-0.3>>, 0.6);
    blurIn("#@p-pv7", <<one>>); blurIn("#@p-pv6", <<two>>); blurIn("#@p-pv5", <<four>>); blurIn("#@p-pv4", <<eight>>);
    each(["#@p-pv3", "#@p-pv2", "#@p-pv1", "#@p-pv0"], <<all>>, 0.25, 1);
    blurIn("#@p-l", <<double>>);
""", enter=False),

    Scene("hundred", "To store one hundred, switch on sixty-four, thirty-two, and four. Add them up: one hundred. "
                     "So in binary, our health is zero one one zero, zero one zero zero.",
          body=txt("@p-t", BX, 150, "health = 100", "h", fs=110) + bit_row(BITS) + place_row()
          + txt("@p-s", BX, 690, '64 + 32 + 4 = <span class="@p-acc">100</span>', "h", fs=100)
          + txt("@p-bn", BX, 850, "binary: 0110 0100", "m", fs=70),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    const on = (i, t) => tl.to("#@p-b" + i, { backgroundColor: "#FF5A1F", color: "#fff", scale: 1.08, duration: 0.2, yoyo: true, repeat: 1 }, t)
      .set("#@p-b" + i, { backgroundColor: "#FF5A1F", color: "#fff" }, t + 0.4);
    on(1, <<sixty-four>>); on(2, <<thirty-two>>); on(5, <<four>>);
    wipe("#@p-s", <<add>>, 0.7);
    blurIn("#@p-bn", <<binary>>);
"""),

    Scene("max", "With all eight bits on, a byte holds two hundred fifty-five. That is the largest number one byte can store.",
          body=txt("@p-t", BX, 150, "all eight bits on", "h", fs=110) + bit_row(["1"] * 8, on=range(8)) + place_row()
          + txt("@p-s", BX, 690, 'one byte: 0 to <span class="@p-acc">255</span>', "h", fs=110),
          js="""
    wipe("#@p-t", <<all-0.2>>, 0.5);
    each(".c-@p-b", <<eight>>, 0.06, 1.2);
    wipe("#@p-s", <<two>>, 0.7);
"""),

    # ------------------------------------------------------------------ hex
    Scene("hexwhy", "Binary is exact, but nobody wants to read eight digits for every byte. So tools use hexadecimal: base sixteen.",
          body=txt("@p-a", 190, 250, "0110 0100", "h", fs=170) + txt("@p-al", 190, 450, "binary: eight digits per byte", "m", fs=56)
          + tile("@p-b", 190, 620, 420, 260, "64", 190) + txt("@p-bl", 680, 660, "hexadecimal:<br>two digits per byte", "m", fs=60)
          + txt("@p-c", 680, 820, "base 16", "h", fs=80, color="#E8490F"),
          js="""
    wipe("#@p-a", <<binary-0.2>>, 0.6);
    blurIn("#@p-al", <<eight>>);
    land("#@p-b", <<hexadecimal-0.3>>);
    blurIn("#@p-bl", <<hexadecimal>>);
    blurIn("#@p-c", <<base>>);
"""),

    Scene("digits", "Hex has sixteen digits. Zero to nine, then A for ten, B for eleven, up to F for fifteen.",
          body=txt("@p-t", 144, 150, "sixteen digits", "h", fs=110)
          + cells("@p-d", 144, 440, list("0123456789ABCDEF"), size=90, gap=12, on=range(10, 16))
          + "".join(txt(f"@p-v{i}", 144 + i * 102, 560, str(i), "m", fs=44, w=90, align="center") for i in range(10, 16))
          + txt("@p-l", 144, 720, "after 9, the letters keep counting", "m", fs=58),
          js="""
    wipe("#@p-t", <<sixteen-0.3>>, 0.6);
    each(["#@p-d0", "#@p-d1", "#@p-d2", "#@p-d3", "#@p-d4", "#@p-d5", "#@p-d6", "#@p-d7", "#@p-d8", "#@p-d9"], <<zero>>, 0.07);
    land("#@p-d10", <<a>>); blurIn("#@p-v10", <<ten>>);
    land("#@p-d11", <<b>>); blurIn("#@p-v11", <<eleven>>);
    each(["#@p-d12", "#@p-d13", "#@p-d14", "#@p-d15"], <<up>>, 0.12);
    each(["#@p-v12", "#@p-v13", "#@p-v14", "#@p-v15"], <<up+0.2>>, 0.12, 1);
    blurIn("#@p-l", <<a+0.3>>);
"""),

    Scene("nibble", "And here is the trick. One hex digit is exactly four bits. So split the byte in half. Zero one one zero is six. "
                    "Zero one zero zero is four. One hundred is hex six four.",
          body=txt("@p-t", 190, 110, "1 hex digit = 4 bits", "h", fs=100)
          + cells("@p-l", 190, 330, ["0", "1", "1", "0"], size=150, gap=24, on=(1, 2))
          + cells("@p-r", 1030, 330, ["0", "1", "0", "0"], size=150, gap=24, on=(1,))
          + tile("@p-h6", 380, 570, 290, 230, "6", 170) + tile("@p-h4", 1220, 570, 290, 230, "4", 170)
          + txt("@p-c", 190, 880, '100 = hex <span class="@p-acc">64</span>', "h", fs=100),
          js="""
    wipe("#@p-t", <<exactly-0.4>>, 0.6);
    each(".c-@p-l", <<split>>, 0.06); each(".c-@p-r", <<split+0.3>>, 0.06);
    land("#@p-h6", <<six>>);
    land("#@p-h4", <<four#2>>);
    wipe("#@p-c", <<hundred>>, 0.7);
"""),

    Scene("calc", "You don't have to trust me. Windows Calculator has a programmer mode. Type one hundred, and it shows the same number "
                  "three ways. Decimal: one hundred. Hex: six four. Binary: zero one one zero, zero one zero zero.",
          body=calc.html() + calc.mark("@p-m2", 10, 306, 180, 34) + calc.mark("@p-m1", 10, 266, 180, 34) + calc.mark("@p-m3", 10, 386, 220, 34)
          + txt("@p-t", 1100, 190, "check it yourself", "h", fs=72)
          + card("@p-a", 1100, 360, 640, 130, "DEC &nbsp;100", 58) + card("@p-b", 1100, 530, 640, 130, "HEX &nbsp;64", 58, "on")
          + card("@p-c", 1100, 700, 640, 130, "BIN &nbsp;0110 0100", 58),
          js="""
    land("#@p-calc", <<calculator-0.2>>, 1.05, 0.5);
    wipe("#@p-t", <<trust>>, 0.5);
    land("#@p-m2", <<decimal>>, 1.4); land("#@p-a", <<decimal+0.1>>);
    land("#@p-m1", <<hex>>, 1.4); land("#@p-b", <<hex+0.1>>);
    land("#@p-m3", <<binary>>, 1.4); land("#@p-c", <<binary+0.1>>);
"""),

    Scene("prefix", "To avoid confusion, hex numbers are written with a zero x in front. Zero x one zero is not ten. It is sixteen. "
                    "And zero x F F is two hundred fifty-five: a full byte in two digits.",
          body=txt("@p-t", 190, 110, 'hex starts with <span class="@p-acc">0x</span>', "h", fs=100)
          + tile("@p-a", 190, 330, 520, 220, "0x10", 130) + txt("@p-ae", 760, 370, "=", "h", fs=130) + card("@p-av", 900, 345, 380, 190, "16", 120)
          + txt("@p-an", 1340, 390, "not ten", "m", fs=60)
          + tile("@p-b", 190, 640, 520, 220, "0xFF", 130) + txt("@p-be", 760, 680, "=", "h", fs=130) + card("@p-bv", 900, 655, 380, 190, "255", 120)
          + txt("@p-bn", 1340, 670, "a full byte,<br>two digits", "m", fs=60),
          js="""
    wipe("#@p-t", <<zero-0.3>>, 0.6);
    land("#@p-a", <<zero#2>>);
    blurIn("#@p-an", <<not>>);
    blurIn("#@p-ae", <<sixteen-0.2>>); land("#@p-av", <<sixteen>>);
    land("#@p-b", <<zero#3>>);
    blurIn("#@p-be", <<two-0.2>>); land("#@p-bv", <<two>>);
    blurIn("#@p-bn", <<full>>);
"""),

    Scene("hexread", "Bigger hex numbers work the same way as decimal, only the places are powers of sixteen. Zero x one F four: "
                     "one times two hundred fifty-six, plus fifteen times sixteen, plus four. Five hundred.",
          body=txt("@p-t", 190, 110, "reading a bigger hex number", "h", fs=84)
          + cells("@p-d", 560, 400, ["1", "F", "4"], size=220, gap=40)
          + txt("@p-p0", 560, 310, "256", "m", fs=60, w=220, align="center") + txt("@p-p1", 820, 310, "16", "m", fs=60, w=220, align="center")
          + txt("@p-p2", 1080, 310, "1", "m", fs=60, w=220, align="center")
          + txt("@p-x", 300, 440, "0x", "h", fs=150)
          + txt("@p-s", 190, 720, "1&times;256 + 15&times;16 + 4", "m", fs=80)
          + txt("@p-r", 190, 850, '= <span class="@p-acc">500</span>', "h", fs=120),
          js="""
    wipe("#@p-t", <<bigger-0.2>>, 0.6);
    each(["#@p-p2", "#@p-p1", "#@p-p0"], <<powers-0.4>>, 0.15, 1);
    blurIn("#@p-x", <<zero>>); each(".c-@p-d", <<zero+0.3>>, 0.25);
    wipe("#@p-s", <<times-0.3>>, 2.2);
    land("#@p-r", <<five>>);
"""),

    Scene("viewer", "This is why every tool in this series shows memory in hex. Two digits, one byte, and the columns line up. "
                    "On the left, the address of each row. In the middle, the bytes. On the right, the same bytes shown as text.",
          body=txt("@p-t", 120, 96, "reading a memory viewer", "h", fs=80) + mv().html()
          + mv().mark("@p-m1", 2, 150, 84, 300) + mv().mark("@p-m2", 90, 150, 716, 300) + mv().mark("@p-m3", 808, 150, 92, 300)
          + tag("@p-g1", 120, 880, "address") + tag("@p-g2", 760, 880, "the bytes") + tag("@p-g3", 1560, 880, "as text"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-mv", 0.2, 1.03, 0.5);
    land("#@p-m1", <<left>>, 1.1); land("#@p-g1", <<address>>);
    tl.to("#@p-m1", { opacity: 0.35, duration: 0.3 }, <<middle>>);
    land("#@p-m2", <<middle>>, 1.05); land("#@p-g2", <<bytes#2-0.1>>);
    tl.to("#@p-m2", { opacity: 0.35, duration: 0.3 }, <<right>>);
    land("#@p-m3", <<right>>, 1.1); land("#@p-g3", <<right+0.25>>);
"""),

    # ------------------------------------------------------------------ sizes
    Scene("bigger", "So one byte tops out at two fifty-five. But ammo, money and score get much bigger than that. "
                    "A program solves it by using several bytes side by side.",
          body=txt("@p-t", 190, 110, "one byte is not enough", "h", fs=100)
          + cells("@p-o", 190, 330, ["FF"], size=180) + txt("@p-ol", 420, 375, "= 255, the limit", "m", fs=64)
          + txt("@p-q", 190, 600, "money: 5000 ?", "m", fs=64)
          + cells("@p-b", 190, 720, ["88", "13", "00", "00"], size=180, gap=24, on=(0, 1))
          + txt("@p-bl", 190, 940, "four bytes, side by side", "m", fs=60),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-o0", <<tops-0.3>>); blurIn("#@p-ol", <<two>>);
    blurIn("#@p-q", <<money>>);
    each(".c-@p-b", <<several>>, 0.12);
    blurIn("#@p-bl", <<side>>);
"""),

    Scene("types", "In C and C plus plus, the type decides how many. A char is one byte. A short is two. An int is four, "
                   "good for about four billion values. A long long is eight.",
          body=txt("@p-t", 190, 80, "the type decides the size", "h", fs=90)
          + "".join(card(f"@p-n{i}", 190, 250 + i * 190, 420, 140, n, 58, "on")
                    + cells(f"@p-c{i}_", 680, 260 + i * 190, ["&nbsp;"] * k, size=120 if k < 8 else 88, gap=14)
                    + txt(f"@p-r{i}", 680 + (k * 134 if k < 8 else 8 * 102) + 30, 285 + i * 190, r, "m", fs=50)
                    for i, (n, k, r) in enumerate([("char", 1, "1 byte: 256 values"), ("short", 2, "2 bytes: 65,536 values"),
                                                   ("int", 4, "4 bytes: ~4 billion"), ("long long", 8, "8 bytes")])),
          js="""
    wipe("#@p-t", <<type-0.3>>, 0.6);
    land("#@p-n0", <<char>>); each(".c-@p-c0_", <<char+0.2>>, 0.05); blurIn("#@p-r0", <<one>>);
    land("#@p-n1", <<short>>); each(".c-@p-c1_", <<short+0.2>>, 0.05); blurIn("#@p-r1", <<two>>);
    land("#@p-n2", <<int>>); each(".c-@p-c2_", <<int+0.2>>, 0.05); blurIn("#@p-r2", <<four>>);
    land("#@p-n3", <<long#2>>); each(".c-@p-c3_", <<long#2+0.2>>, 0.04); blurIn("#@p-r3", <<eight>>);
"""),

    Scene("int100", "The game stores health as a four byte integer. That is why we saw four bytes: six four, then three zeros.",
          body=txt("@p-t", 120, 96, "health is an int: four bytes", "h", fs=80) + mv().html() + mv().mark("@p-m", 88, 171, 116, 24)
          + tile("@p-k", 120, 880, 760, 150, "64 00 00 00", 84) + txt("@p-kl", 930, 920, "= 100, as a 4 byte int", "m", fs=60),
          js="""
    wipe("#@p-t", <<four-0.4>>, 0.6);
    land("#@p-m", <<saw>>, 1.5);
    land("#@p-k", <<six>>); blurIn("#@p-kl", <<three>>);
"""),

    Scene("order", "But look at the order. The six four comes first, and the zeros come after. If you wrote this number on paper, "
                   "it would be the other way round.",
          body=txt("@p-t", 190, 110, "look at the order", "h", fs=100)
          + txt("@p-ml", 190, 290, "in memory", "m", fs=56) + cells("@p-m", 190, 370, ["64", "00", "00", "00"], size=180, gap=24, on=(0,))
          + txt("@p-pl", 190, 640, "on paper", "m", fs=56) + cells("@p-p", 190, 720, ["00", "00", "00", "64"], size=180, gap=24, on=(3,))
          + txt("@p-c", 1080, 560, "backwards?", "h", fs=96, color="#E8490F"),
          js="""
    wipe("#@p-t", <<order-0.3>>, 0.5);
    blurIn("#@p-ml", <<six-0.3>>); each(".c-@p-m", <<six>>, 0.15);
    blurIn("#@p-pl", <<paper-0.4>>); each(".c-@p-p", <<paper>>, 0.1);
    land("#@p-c", <<other>>);
"""),

    Scene("endian", "This is called little endian: the smallest part of the number is stored first. Take one thousand. "
                    "In hex, that is three E eight. In memory, it becomes E eight, zero three, zero zero, zero zero.",
          body=txt("@p-t", 190, 100, 'little endian: <span class="@p-acc">smallest part first</span>', "h", fs=80)
          + txt("@p-v", 190, 270, "1000 = 0x000003E8", "m", fs=70)
          + txt("@p-pl", 190, 420, "the number", "m", fs=50) + cells("@p-p", 560, 380, ["00", "00", "03", "E8"], size=170, gap=24, on=(3,))
          + txt("@p-ml", 190, 740, "in memory", "m", fs=50) + cells("@p-m", 560, 700, ["E8", "03", "00", "00"], size=170, gap=24, on=(0,))
          + txt("@p-a", 1400, 560, "flipped,<br>byte by byte", "m", fs=54),
          js="""
    wipe("#@p-t", <<little-0.2>>, 0.7);
    blurIn("#@p-v", <<thousand-0.3>>);
    blurIn("#@p-pl", <<hex>>); each(".c-@p-p", <<hex+0.2>>, 0.12);
    blurIn("#@p-ml", <<memory>>);
    land("#@p-m0", <<e#2>>); land("#@p-m1", <<three#2-0.3>>); land("#@p-m2", <<zero#2>>); land("#@p-m3", <<zero#4>>);
    blurIn("#@p-a", <<zero#4+0.3>>);
"""),

    Scene("proof", "Here is a tiny C plus plus program that prints the bytes of any value. Int one hundred: six four, zero zero, zero zero, "
                   "zero zero. Int one thousand: E eight, zero three. Exactly as predicted.",
          body=txt("@p-t", 190, 100, "prove it with your own program", "h", fs=80)
          + term("@p-c", 190, 250, 1540, ["template &lt;class T&gt; void dump(const char* label, T value) {",
                                           "    unsigned char bytes[sizeof(T)];",
                                           "    memcpy(bytes, &amp;value, sizeof(T));",
                                           '    for (unsigned char b : bytes) printf("%02X ", b);',
                                           "}"], fs=36)
          + term("@p-o", 190, 610, 1000, OUT[:3], fs=48)
          + txt("@p-k", 1270, 660, "real output,<br>my machine", "m", fs=50)
          + txt("@p-k2", 1270, 830, "code shortened:<br>full file below", "m", fs=40, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-c", <<program-0.4>>, 1.04, 0.5);
    land("#@p-o", <<int-0.5>>, 1.04, 0.4);
    tl.fromTo("#@p-o-l1", { opacity: 0 }, { opacity: 1, duration: 0.25 }, <<int>>);
    tl.fromTo("#@p-o-l2", { opacity: 0 }, { opacity: 1, duration: 0.25 }, <<int#2>>);
    blurIn("#@p-k", <<exactly>>); blurIn("#@p-k2", <<program>>);
"""),

    Scene("negative", "And minus one? Four bytes of F F. A signed integer uses the top half of its range for negative numbers. "
                      "Read those same bytes as unsigned, and you get more than four billion.",
          body=txt("@p-t", 190, 100, "what about -1 ?", "h", fs=100)
          + term("@p-o", 190, 280, 840, [OUT[0], OUT[3]], fs=44)
          + cells("@p-b", 190, 560, ["FF", "FF", "FF", "FF"], size=170, gap=24, on=range(4))
          + card("@p-s", 1080, 480, 660, 140, "signed: -1", 56) + card("@p-u", 1080, 670, 660, 140, "unsigned: 4,294,967,295", 42, "on")
          + txt("@p-c", 190, 860, "same bytes, two readings", "m", fs=60),
          js="""
    wipe("#@p-t", <<minus-0.2>>, 0.5);
    land("#@p-o", <<four-0.3>>, 1.04, 0.4);
    each(".c-@p-b", <<f>>, 0.1);
    land("#@p-s", <<signed>>);
    land("#@p-u", <<unsigned>>);
    blurIn("#@p-c", <<billion>>);
"""),

    # ------------------------------------------------------------------ floats
    Scene("floats", "Not everything is a whole number. Positions, speeds and angles need a decimal point. "
                    "For those, programs use a float: four bytes with a completely different layout.",
          body=txt("@p-t", 190, 110, "numbers with a decimal point", "h", fs=90)
          + card("@p-a", 190, 320, 480, 130, "position", 56, "soft") + card("@p-b", 720, 320, 480, 130, "speed", 56, "soft")
          + card("@p-c", 1250, 320, 480, 130, "angle", 56, "soft")
          + tile("@p-f", 190, 580, 620, 260, "float", 150) + txt("@p-fl", 880, 620, "four bytes,<br>a different layout", "m", fs=64),
          js="""
    wipe("#@p-t", <<whole-0.6>>, 0.7);
    land("#@p-a", <<positions>>); land("#@p-b", <<speeds>>); land("#@p-c", <<angles>>);
    land("#@p-f", <<float>>);
    blurIn("#@p-fl", <<four>>);
"""),

    Scene("layout", "A float splits its thirty-two bits into three parts. One bit for the sign, eight for the exponent, "
                    "and twenty-three for the fraction. It is scientific notation, in binary.",
          body=txt("@p-t", 190, 110, "inside a float: 32 bits", "h", fs=96)
          + card("@p-s", 160, 400, 110, 220, "1", 80, "on") + card("@p-e", 290, 400, 400, 220, "8", 110, "soft") + card("@p-f", 710, 400, 1050, 220, "23", 110)
          + txt("@p-sl", 130, 650, "sign", "m", fs=50) + txt("@p-el", 290, 650, "exponent", "m", fs=50) + txt("@p-fl", 710, 650, "fraction", "m", fs=50)
          + txt("@p-c", 190, 830, "scientific notation, in binary", "h", fs=76, color="#E8490F"),
          js="""
    wipe("#@p-t", <<thirty-two-0.4>>, 0.6);
    land("#@p-s", <<sign-0.5>>); blurIn("#@p-sl", <<sign>>);
    land("#@p-e", <<eight>>); blurIn("#@p-el", <<exponent>>);
    land("#@p-f", <<twenty-three>>); blurIn("#@p-fl", <<fraction>>);
    wipe("#@p-c", <<scientific>>, 0.7);
"""),

    Scene("pos", "Here is my real position in the game, in Cheat Engine. X is forty-three point zero. And its bytes: zero zero, zero zero, "
                 "two C, four two. Nothing in there looks like forty-three.",
          body=txt("@p-t", 120, 96, "my real position, in Cheat Engine", "h", fs=80) + table().html()
          + row_mark(table(), "@p-m1", "pos") + row_mark(table(), "@p-m2", "pos_raw")
          + tag("@p-g1", 120, 930, "float: 43.0", 48) + tag("@p-g2", 560, 930, "bytes: 00 00 2C 42", 48),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m1", <<forty-three>>, 1.3); land("#@p-g1", <<forty-three+0.2>>);
    land("#@p-m2", <<bytes>>, 1.3); land("#@p-g2", <<two>>);
""", exit=False),

    Scene("same", "Now the important part. Read those same four bytes as an integer, and you get one billion, one hundred ten million. "
                  "Same bytes. Different number.",
          body=txt("@p-t", 120, 96, 'same bytes, <span class="@p-acc">different number</span>', "h", fs=80) + table().html()
          + row_mark(table(), "@p-m2", "pos_raw") + row_mark(table(), "@p-m3", "pos_int")
          + tag("@p-g1", 120, 930, "float: 43.0", 48) + tag("@p-g2", 560, 930, "bytes: 00 00 2C 42", 48) + tag("@p-g3", 1190, 930, "int: 1,110,179,840", 48),
          js="""
    blurIn("#@p-t", 0, 0.3);
    land("#@p-m3", <<integer>>, 1.3); land("#@p-g3", <<billion-0.3>>);
    tl.fromTo("#@p-t .@p-acc", { scale: 1 }, { scale: 1.12, transformOrigin: "left center", duration: 0.25, yoyo: true, repeat: 1 }, <<different>>);
""", enter=False),

    Scene("reverse", "It works the other way too. Health is one hundred. Read its bytes as a float, and you get one point four, "
                     "times ten to the minus forty-three. Practically zero.",
          body=txt("@p-t", 120, 96, "and the other way round", "h", fs=80) + table().html()
          + row_mark(table(), "@p-m1", "health") + row_mark(table(), "@p-m2", "health_float")
          + tag("@p-g1", 120, 930, "int: 100", 48) + tag("@p-g2", 520, 930, "same bytes as a float: 1.4 &times; 10<sup>-43</sup>", 48),
          js="""
    wipe("#@p-t", <<other-0.3>>, 0.6);
    land("#@p-m1", <<health>>, 1.3); land("#@p-g1", <<hundred>>);
    land("#@p-m2", <<float>>, 1.3); land("#@p-g2", <<point>>);
"""),

    Scene("lesson", "Memory does not store types. It only stores bytes. The type is a decision made by whoever is reading.",
          body=cells("@p-b", 192, 180, ["00", "00", "2C", "42"], size=170, gap=24)
          + txt("@p-a", 192, 440, "Memory stores bytes.", "h", fs=130)
          + txt("@p-c", 192, 620, '<span class="@p-acc">The reader picks the type.</span>', "h", fs=110)
          + card("@p-x", 1080, 190, 300, 130, "43.0", 60, "on") + card("@p-y", 1420, 190, 390, 130, "1110179840", 46, "soft"),
          js="""
    each(".c-@p-b", 0.3, 0.1);
    wipe("#@p-a", <<only-0.3>>, 0.7);
    land("#@p-x", <<type-0.4>>); land("#@p-y", <<type-0.1>>);
    wipe("#@p-c", <<decision-0.3>>, 0.8);
"""),

    Scene("text", "Even text works this way. My player name is pixel. In memory, it is five bytes: seven zero, six nine, seven eight, "
                  "six five, six C. One number per letter.",
          body=txt("@p-t", 120, 80, "even text is just bytes", "h", fs=80)
          + mv("mv_name", 210, (0, 128, 902, 100)).html() + mv("mv_name", 210, (0, 128, 902, 100)).mark("@p-m1", 88, 171, 146, 24)
          + mv("mv_name", 210, (0, 128, 902, 100)).mark("@p-m2", 808, 171, 52, 24)
          + cells("@p-l", 420, 500, list("pixel"), size=170, gap=40, on=range(5))
          + cells("@p-h", 420, 720, ["70", "69", "78", "65", "6C"], size=170, gap=40)
          + txt("@p-c", 420, 940, "one number per letter (ASCII)", "m", fs=56),
          js="""
    wipe("#@p-t", <<text-0.3>>, 0.6);
    land("#@p-mv", 0.3, 1.03, 0.5);
    each(".c-@p-l", <<pixel>>, 0.08); land("#@p-m2", <<pixel+0.2>>, 1.4);
    land("#@p-m1", <<five>>, 1.4);
    land("#@p-h0", <<seven>>); land("#@p-h1", <<six>>); land("#@p-h2", <<seven#2>>); land("#@p-h3", <<six#2>>); land("#@p-h4", <<six#3>>);
    blurIn("#@p-c", <<letter-0.4>>);
"""),

    # ------------------------------------------------------------------ live
    Scene("live1", "Let's watch it live. On top, the game. I have already fired a few rounds, so the magazine is at twelve. "
                   "Below it, Cheat Engine, an open-source memory scanner, showing the magazine's address and its raw bytes.",
          body=live_game(True).html() + live_ce(True).html()
          + tag("@p-t1", 130, 60, "the game") + tag("@p-t2", 110, 690, "Cheat Engine: the same value in memory"),
          js="""
    land("#@p-g", 0.2, 1.03, 0.5); land("#@p-t1", <<game>>);
    land("#@p-c", <<below-0.2>>, 1.03, 0.4); land("#@p-t2", <<cheat>>);
""", exit=False),

    Scene("live2", "I fire a few rounds. The counter on screen drops, and the bytes in memory drop with it. Cheat Engine re-reads the value "
                   "a few times a second, so it follows a moment behind. The number on your screen is just a picture of those bytes.",
          media=live_media,
          body=live_game().mark("@p-m1", 476, 808, 196, 76) + live_ce().mark("@p-m2", 672, 126, 110, 46, pad=2)
          + tag("@p-t1", 130, 60, "the game") + tag("@p-t2", 110, 690, "Cheat Engine: the same value in memory"),
          js="""
    land("#@p-m1", 0.3, 1.4);
    land("#@p-m2", 0.5, 1.3);
""", enter=False),

    # ------------------------------------------------------------------ why it matters
    Scene("scanner", "This is why every memory scanner asks you for a value type before it searches. Pick four bytes when the game uses a float, "
                     "and you will find nothing, even though the value is right there.",
          body=txt("@p-t", 190, 90, "the scanner asks: which type?", "h", fs=84) + scan.html() + scan.mark("@p-m", 422, 258, 310, 34)
          + card("@p-a", 1360, 300, 420, 130, "4 Bytes", 56, "on") + card("@p-b", 1360, 470, 420, 130, "Float", 56, "soft")
          + txt("@p-c", 190, 760, 'wrong type = <span class="@p-acc">zero results</span>', "h", fs=96)
          + txt("@p-d", 190, 890, "even though the value is right there", "m", fs=56),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-scan", 0.2, 1.03, 0.5);
    land("#@p-m", <<value>>, 1.3);
    land("#@p-a", <<four>>); land("#@p-b", <<float>>);
    wipe("#@p-c", <<nothing-0.3>>, 0.6);
    blurIn("#@p-d", <<even>>);
"""),

    Scene("sheet", "So here is your cheat sheet. Whole numbers like health and ammo: usually four bytes. Anything with a decimal point: float. "
                   "Not sure? Try four bytes first, then float, then the rest.",
          body=txt("@p-t", 190, 100, "your cheat sheet", "h", fs=100)
          + card("@p-a", 190, 300, 760, 140, "health, ammo, money", 50) + bar("@p-a1", 950, 364, 110) + card("@p-a2", 1060, 300, 600, 140, "4 Bytes", 60, "on")
          + card("@p-b", 190, 490, 760, 140, "position, speed, timers", 50) + bar("@p-b1", 950, 554, 110) + card("@p-b2", 1060, 490, 600, 140, "Float", 60, "on")
          + card("@p-c", 190, 680, 760, 140, "not sure?", 50, "soft") + bar("@p-c1", 950, 744, 110)
          + card("@p-c2", 1060, 680, 760, 140, "4 Bytes, Float, the rest", 46, "on"),
          js="""
    wipe("#@p-t", <<cheat-0.2>>, 0.6);
    land("#@p-a", <<whole>>); wipe("#@p-a1", <<usually-0.2>>, 0.2); land("#@p-a2", <<usually>>);
    land("#@p-b", <<anything>>); wipe("#@p-b1", <<float-0.2>>, 0.2); land("#@p-b2", <<float>>);
    land("#@p-c", <<sure>>); wipe("#@p-c1", <<try-0.2>>, 0.2); land("#@p-c2", <<try>>);
"""),

    Scene("recap", "Let's recap. A byte is eight bits, and holds zero to two fifty-five. Hex writes one byte as two digits. "
                   "Bigger numbers use more bytes, stored smallest part first. And the same bytes mean different things, "
                   "depending on the type you read them as.",
          body=txt("@p-t", 190, 90, "recap", "h", fs=110)
          + txt("@p-a", 190, 290, "1 byte = 8 bits = 0 to 255", "m", fs=58)
          + txt("@p-b", 190, 440, "hex: one byte, two digits &nbsp;(100 = 0x64)", "m", fs=58)
          + txt("@p-c", 190, 590, "more bytes for bigger numbers, smallest first", "m", fs=58)
          + txt("@p-d", 190, 740, 'same bytes, another type: <span class="@p-acc">another number</span>', "m", fs=58),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    wipe("#@p-a", <<byte>>, 0.8);
    wipe("#@p-b", <<hex>>, 0.8);
    wipe("#@p-c", <<bigger>>, 0.8);
    wipe("#@p-d", <<same>>, 0.8);
"""),

    Scene("practice", "Your practice for this episode. Compile the little program from the description, and before you run it, "
                      "predict the bytes of the integer three hundred. Then check yourself.",
          body=txt("@p-t", 190, 100, "practice", "h", fs=110)
          + term("@p-o", 190, 320, 1180, ["&gt; bytes.exe", 'int 300         <span class="hi">?? ?? ?? ??</span>'], fs=56)
          + txt("@p-a", 190, 620, "1. write 300 in hex", "m", fs=60) + txt("@p-b", 190, 720, "2. pad it to four bytes", "m", fs=60)
          + txt("@p-c", 190, 820, "3. flip the order, then run it and compare", "m", fs=60)
          + tag("@p-g", 960, 130, "bytes.cpp: link in the description", 36),
          js="""
    wipe("#@p-t", <<practice-0.2>>, 0.5);
    land("#@p-g", <<description-0.4>>);
    land("#@p-o", <<predict-0.3>>, 1.04, 0.4);
    each(["#@p-a", "#@p-b", "#@p-c"], <<three>>, 0.5, 1);
"""),

    Scene("next", "Next time: you find the health address, restart the game, and it is gone. "
                  "Why the address changes, and how pointers lead you back to it. See you there.",
          body=txt("@p-s", 192, 220, "NEXT EPISODE", "m", fs=64)
          + txt("@p-a", 192, 330, "Why the Address", "h", fs=150) + txt("@p-b", 192, 490, '<span class="@p-acc">Changes</span>', "h", fs=150)
          + card("@p-x", 192, 740, 520, 130, "0x0089786C", 56) + txt("@p-ar", 750, 760, "&rarr;", "h", fs=90)
          + card("@p-y", 880, 740, 520, 130, "0x00965E7C ?", 56, "on"),
          js="""
    blurIn("#@p-s", <<next>>);
    wipe("#@p-a", <<why-0.3>>, 0.6); wipe("#@p-b", <<changes-0.2>>, 0.5);
    land("#@p-x", <<find>>); blurIn("#@p-ar", <<restart>>); land("#@p-y", <<gone>>);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Game Hacking from Scratch 1: The Bytes Behind the Health Bar")
