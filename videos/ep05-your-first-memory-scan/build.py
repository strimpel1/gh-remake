"""Game Hacking from Scratch, episode 5: Your First Memory Scan (first scan + scan types and unknown values).

Long-form YouTube episode. Every screenshot and recording is real: Cheat Engine 7.7 driven through its own window, attached to
AssaultCube 1.3.0.2 (open source, single player, offline) and to lab/scanme.cpp, the practice program of this episode.
All numbers come from those two capture sessions (prep_clips.py cuts the recordings).   Run: python build.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, Shot, bar, build, card, cells, fit_clip, tag, term, tile, txt  # noqa: E402,F401

A = Path(__file__).resolve().parent / "assets"
CE, GAME, CON = (888, 932), (1584, 930), (972, 380)      # the three windows, in pixels
SCANC = (0, 105, 888, 470)       # Cheat Engine: Found, the result list, the scan controls
BOTH = (0, 105, 888, 600)        # the same plus the top of the address list
LISTC = (0, 612, 888, 92)        # the address list: header and two rows
GH = (0, 480, 800, 450)          # the game: lower left, with the health and ammo counters
GB = (0, 560, 1584, 370)         # the game: the whole bottom band
BARS = (0, 150, 972, 88)         # scanme: the health bar and the energy line
AMMO = (478, 855, 195, 65)       # the magazine counter in the game window


def shot(id, name, x, y, w, crop=None):
    return Shot(id, A / f"shots/{name}.png", x, y, w, crop=crop)


def clip(id, name, x, y, w, crop, size, start=0.0):
    """A recording in a frame: returns (Shot for marks, media function for Scene)."""
    s = Shot(id, A / f"clips/{name}.mp4", x, y, w, crop=crop, size=size)

    def media(dur):
        p = fit_clip(A / f"clips/{name}.mp4", dur, start)
        s.path, s.src = p, f"assets/clips/{p.name}"
        return s.video(0, dur)
    return s, media


def both(*media):
    return lambda dur: "".join(m(dur) for m in media)


def found(text, y=640, x=1160, w=700):
    return tile("@p-f", x, y, w, 140, text, 76)


def scan_scene(name, start=0.0):
    """Cheat Engine's scan area on the left (recording), room for the target on the right."""
    return clip("@p-ce", name, 80, 180, 1040, SCANC, CE, start)


def list_game(ce_name, game_name, start=0.0):
    """Address list on top, the game's bottom band below: two recordings of the same moment."""
    c, cm = clip("@p-ce", ce_name, 80, 150, 1760, LISTC, CE, start)
    g, gm = clip("@p-g", game_name, 80, 390, 1760, GB, GAME, start)
    return c, g, both(cm, gm)


def con_scene(ce_name, con_name, crop=SCANC, w=1040):
    """scanme's bar strip on top, Cheat Engine below."""
    k, km = clip("@p-k", con_name, 80, 150, w, BARS, CON)
    c, cm = clip("@p-ce", ce_name, 80, 290, w, crop, CE)
    return k, c, both(km, cm)


g20 = shot("@p-g", "game20", 1160, 180, 700, GH)
g14 = shot("@p-g", "game14", 1160, 180, 700, GH)
g10 = shot("@p-g", "game10", 1160, 180, 700, GH)

cold_ce, cold_m = clip("@p-ce", "a1_ce", 80, 110, 1100, SCANC, CE)
cold_g = shot("@p-g", "game20", 1220, 110, 620, GH)
first_ce, first_m = scan_scene("a1_ce", 1.3)
fire_g, fire_m = clip("@p-g", "a2f_game", 80, 180, 1000, GH, GAME)
next_ce, next_m = scan_scene("a2n_ce")
again_ce, again_m = scan_scene("a3n_ce")
add_ce, add_m = clip("@p-ce", "a3add_ce", 80, 150, 900, BOTH, CE)
copy_c, copy_g, copy_m = list_game("a4_ce", "a4_game")
real_c, real_g, real_m = list_game("a5_ce", "a5_game")
shoot_c, shoot_g, shoot_m = list_game("a6_ce", "a6_game")
frz_c, frz_g, frz_m = list_game("a7_ce", "a7_game")
unk_ce, unk_m = scan_scene("c1_ce")
dec_k, dec_c, dec_m = con_scene("c2_ce", "c2_con")
unc_k, unc_c, unc_m = con_scene("c3_ce", "c3_con")
inc_k, inc_c, inc_m = con_scene("c4_ce", "c4_con")
wr_k, wr_c, wr_m = con_scene("c5_ce", "c5_con", BOTH, 900)
int_k, int_c, int_m = con_scene("d1_ce", "d1_con")
flt_k, flt_c, flt_m = con_scene("d2_ce", "d2_con", BOTH, 900)

tour = shot("@p-ce", "a_scan1", 80, 150, 760)
ctrl = shot("@p-ce", "a_ce_attached", 80, 210, 1150, (405, 170, 480, 125))
btns = shot("@p-ce", "a_scan2", 80, 230, 1300, (405, 122, 480, 46))
dd = shot("@p-ce", "c_dd_open", 80, 160, 1000, (405, 225, 480, 260))
frozen = shot("@p-ce", "a_frozen2", 80, 150, 1760, LISTC)
dead_c = shot("@p-ce", "a_restart2", 80, 150, 1760, LISTC)
dead_g = shot("@p-g", "a_restart_game", 80, 390, 1760, (0, 560, 1585, 371))
con = shot("@p-k", "con_fresh", 80, 190, 1100)
con_p = shot("@p-k", "con_fresh", 80, 250, 860)
att0 = shot("@p-a0", "a_ce_empty", 80, 190, 1100, (0, 0, 888, 132))
att1 = shot("@p-a1", "a_proclist", 1300, 190, 400, (0, 0, 292, 500))
att2 = shot("@p-a2", "a_ce_attached", 80, 470, 1100, (0, 0, 888, 132))

scenes = [
    # ------------------------------------------------------------------ cold open
    Scene("cold", "Our game says twenty rounds in the magazine. So I ask Cheat Engine a simple question: where, in this game's memory, "
                  "is the number twenty? And it answers: in two thousand, two hundred and fifty-three places.",
          media=cold_m,
          body=cold_g.html() + cold_g.mark("@p-m1", *AMMO)
          + cold_ce.mark("@p-m2", 0, 110, 130, 20, pad=6)
          + tile("@p-f", 1220, 520, 620, 150, "Found: 2,253", 68)
          + txt("@p-q", 80, 770, "where is the number 20?", "h", fs=96)
          + txt("@p-c", 80, 890, 'in <span class="@p-acc">2,253</span> places', "m", fs=64),
          js="""
    land("#@p-g", 0.2, 1.03, 0.4);
    land("#@p-m1", <<twenty>>, 1.4);
    wipe("#@p-q", <<where-0.2>>, 0.7);
    land("#@p-m2", <<answers>>, 1.4);
    land("#@p-f", <<two>>); blurIn("#@p-c", <<places-0.6>>);
"""),

    Scene("hook", "Two thousand answers is not an answer. So we will cut that list down to a single address, change the number inside it, and watch the game obey.",
          body=txt("@p-t", 190, 110, "2,253 answers is not an answer", "h", fs=88)
          + tile("@p-a", 190, 340, 520, 190, "2,253", 120) + txt("@p-r1", 750, 370, "&rarr;", "h", fs=110)
          + tile("@p-b", 900, 340, 300, 190, "2", 120) + txt("@p-r2", 1240, 370, "&rarr;", "h", fs=110)
          + card("@p-c", 1390, 340, 300, 174, "1", 120, "on")
          + txt("@p-d", 190, 660, "1. cut the list down to one address", "m", fs=58)
          + txt("@p-e", 190, 760, "2. change the number inside it", "m", fs=58)
          + txt("@p-g", 190, 860, '3. <span class="@p-acc">watch the game obey</span>', "m", fs=58),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-a", <<two>>);
    blurIn("#@p-r1", <<cut-0.2>>); land("#@p-b", <<cut>>); blurIn("#@p-r2", <<single-0.3>>); land("#@p-c", <<single>>);
    blurIn("#@p-d", <<cut+0.3>>); blurIn("#@p-e", <<change>>); blurIn("#@p-g", <<watch>>);
"""),

    Scene("title", "This is Game Hacking from Scratch. Episode five: your first memory scan.",
          body=txt("@p-s", 192, 250, "GAME HACKING FROM SCRATCH", "m", fs=64)
          + txt("@p-a", 192, 360, "Your First", "h", fs=150) + txt("@p-b", 192, 520, '<span class="@p-acc">Memory Scan</span>', "h", fs=150)
          + tile("@p-e", 192, 760, 420, 130, "EPISODE 5", 60),
          js="""
    blurIn("#@p-s", <<game>>);
    wipe("#@p-a", <<your-0.3>>, 0.6);
    wipe("#@p-b", <<memory-0.2>>, 0.6);
    land("#@p-e", <<episode>>);
"""),

    Scene("setup", "Until now, I showed you values at addresses I already knew. Today you find them yourself. AssaultCube: open source, single player, offline. And Cheat Engine, a free memory scanner.",
          body=txt("@p-t", 80, 60, "today: find the address yourself", "h", fs=76)
          + shot("@p-g", "game20", 80, 190, 1000).html()
          + card("@p-a", 1140, 190, 700, 120, "AssaultCube", 56, "on") + card("@p-b", 1140, 340, 700, 110, "open source", 50)
          + card("@p-c", 1140, 480, 700, 110, "single player, offline", 46)
          + card("@p-e", 80, 830, 1000, 120, "Cheat Engine: a free memory scanner", 46, "soft"),
          js="""
    wipe("#@p-t", <<find-0.4>>, 0.6);
    land("#@p-g", 0.2, 1.03, 0.5);
    land("#@p-a", <<assaultcube>>); land("#@p-b", <<open>>); land("#@p-c", <<single>>);
    land("#@p-e", <<cheat>>, 1.05);
"""),

    # ------------------------------------------------------------------ attach and the window
    Scene("attach", "Step one: tell Cheat Engine which program to look at. Click the little computer icon, pick the game's process "
                    "from the list, and press Open. The process name appears at the top. We are attached.",
          body=txt("@p-t", 80, 60, "step 1: attach to the game", "h", fs=76)
          + att0.html() + att0.mark("@p-m0", 5, 67, 38, 38, pad=6)
          + att1.html() + att1.mark("@p-m1", 4, 92, 284, 22, pad=4) + att1.mark("@p-m1b", 42, 444, 100, 34, pad=4)
          + att2.html() + att2.mark("@p-m2", 340, 64, 220, 20, pad=6)
          + tag("@p-g0", 80, 390, "1. the computer icon", 36) + tag("@p-g1", 1300, 900, "2. the process, then Open", 34)
          + tag("@p-g2", 80, 670, "3. attached: ac_client.exe", 36)
          + txt("@p-c", 80, 800, "one process at a time:<br>everything we scan is this game's own memory", "m", fs=46),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-a0", 0.2, 1.03, 0.4);
    land("#@p-m0", <<icon-0.6>>, 1.4); land("#@p-g0", <<icon>>);
    land("#@p-a1", <<pick-0.2>>, 1.03, 0.4); land("#@p-m1", <<process>>, 1.1); land("#@p-m1b", <<open-0.2>>, 1.3); land("#@p-g1", <<open>>);
    land("#@p-a2", <<name-0.5>>, 1.03, 0.4); land("#@p-m2", <<name>>, 1.3); land("#@p-g2", <<attached-0.3>>);
    blurIn("#@p-c", <<name>>);
"""),

    Scene("tour", "The window has three parts. On the right, the question: a value, a scan type, and a value type. On the left, the answers: every address that matched. At the bottom, the address list: the ones you decide to keep.",
          body=txt("@p-t", 80, 50, "three parts", "h", fs=76) + tour.html()
          + tour.mark("@p-m1", 398, 172, 486, 122, pad=2) + tour.mark("@p-m2", 2, 110, 390, 462, pad=2) + tour.mark("@p-m3", 2, 616, 884, 284, pad=2)
          + card("@p-a", 900, 180, 940, 130, "the question", 60, "on") + txt("@p-al", 900, 330, "value, scan type, value type", "m", fs=46)
          + card("@p-b", 900, 450, 940, 130, "the answers", 60, "on") + txt("@p-bl", 900, 600, "every address that matched", "m", fs=46)
          + card("@p-c", 900, 720, 940, 130, "the address list", 60, "on") + txt("@p-cl", 900, 870, "the ones you decide to keep", "m", fs=46),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m1", <<right-0.2>>, 1.1); land("#@p-a", <<question>>); blurIn("#@p-al", <<value>>);
    land("#@p-m2", <<left-0.2>>, 1.05); land("#@p-b", <<answers>>); blurIn("#@p-bl", <<every>>);
    land("#@p-m3", <<bottom-0.2>>, 1.05); land("#@p-c", <<list>>); blurIn("#@p-cl", <<keep-0.8>>);
"""),

    Scene("type", "The value type stays on four bytes. Episode one explained why: a whole number like ammo is almost always stored that way. And the scan type stays on exact value.",
          body=txt("@p-t", 80, 60, "which type? which scan?", "h", fs=76) + ctrl.html()
          + ctrl.mark("@p-m1", 408, 261, 306, 28, pad=4) + ctrl.mark("@p-m2", 414, 231, 300, 28, pad=4)
          + card("@p-a", 1290, 210, 550, 130, "ammo: a whole number", 40, "soft")
          + tile("@p-b", 1290, 390, 550, 140, "4 Bytes", 70)
          + tile("@p-c", 80, 620, 700, 140, "Exact Value", 70) + txt("@p-cl", 830, 650, "I know the number: 20", "m", fs=54)
          + txt("@p-d", 80, 850, "episode 1: the type decides how the bytes are read", "m", fs=46, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m1", <<value>>, 1.2); land("#@p-b", <<four>>); blurIn("#@p-d", <<episode>>);
    land("#@p-a", <<whole>>);
    land("#@p-m2", <<scan>>, 1.2); land("#@p-c", <<exact>>); blurIn("#@p-cl", <<scan>>);
"""),

    # ------------------------------------------------------------------ the exact-value scan
    Scene("first", "I type twenty, and press First Scan. Cheat Engine reads all the memory this game can write to, and keeps every address that holds twenty right now. Two thousand, two hundred and fifty-three of them. Twenty is an ordinary number: a menu row, a color, a timer.",
          media=first_m,
          body=txt("@p-t", 80, 60, "first scan: 20", "h", fs=76) + g20.html() + g20.mark("@p-m1", *AMMO)
          + first_ce.mark("@p-m2", 0, 110, 130, 20, pad=6)
          + found("Found: 2,253")
          + txt("@p-c", 80, 800, "every address that holds 20 right now", "m", fs=56)
          + txt("@p-d", 80, 890, "20 is ordinary: a menu row, a color, a timer ...", "m", fs=46, color="#E8490F"),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-g", 0.2, 1.03, 0.4); land("#@p-m1", <<twenty>>, 1.4);
    blurIn("#@p-c", <<keeps>>);
    land("#@p-m2", <<two>>, 1.4); land("#@p-f", <<two+0.2>>);
    blurIn("#@p-d", <<ordinary-0.5>>);
"""),

    Scene("fire", "So I change the value in the game. I fire a few rounds: twenty becomes fourteen. The real ammo address now holds fourteen. Almost all of the others still hold twenty.",
          media=fire_m,
          body=txt("@p-t", 80, 60, "change the value in the game", "h", fs=76) + fire_g.mark("@p-m1", *AMMO)
          + card("@p-a", 1140, 190, 300, 170, "20", 100, "soft") + txt("@p-ar", 1460, 215, "&rarr;", "h", fs=100) + tile("@p-b", 1560, 180, 300, 190, "14", 110)
          + txt("@p-c", 1140, 470, "the real address:<br>now 14", "m", fs=52)
          + txt("@p-d", 1140, 660, "almost all the others:<br>still 20", "m", fs=52, color="#6A9188")
          + txt("@p-e", 80, 860, "automatic fire: each click here costs two rounds", "m", fs=40, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-m1", <<fire>>, 1.4); blurIn("#@p-e", <<fire+0.5>>);
    land("#@p-a", <<twenty>>); blurIn("#@p-ar", <<fourteen-0.3>>); land("#@p-b", <<fourteen>>);
    blurIn("#@p-c", <<real>>); blurIn("#@p-d", <<almost>>);
"""),

    Scene("nextscan", "Now the key move. I type fourteen, and press Next Scan. Next Scan only looks at the addresses already in the list, and keeps the ones that hold fourteen now. From two thousand, two hundred and fifty-three, down to two.",
          media=next_m,
          body=txt("@p-t", 80, 60, "next scan: 14", "h", fs=76) + g14.html() + g14.mark("@p-m1", *AMMO)
          + next_ce.mark("@p-m2", 536, 130, 92, 30, pad=4) + next_ce.mark("@p-m3", 0, 110, 90, 20, pad=6)
          + found("Found: 2")
          + txt("@p-c", 80, 800, "Next Scan filters the list you already have", "m", fs=56)
          + txt("@p-d", 80, 890, '2,253 &rarr; <span class="@p-acc">2</span>', "h", fs=80),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-g", 0.2, 1.03, 0.4); land("#@p-m1", <<fourteen>>, 1.4);
    land("#@p-m2", <<next>>, 1.3);
    blurIn("#@p-c", <<only>>);
    land("#@p-m3", <<down>>, 1.4); land("#@p-f", <<down+0.3>>); wipe("#@p-d", <<from>>, 0.8);
"""),

    Scene("trick", "That is the whole trick of memory scanning. Scan. Change the value in the game. Scan again. "
                   "Every round throws out the addresses that did not follow the game.",
          body=txt("@p-t", 190, 100, "the whole trick", "h", fs=100)
          + card("@p-a", 190, 320, 440, 160, "scan", 70, "on") + bar("@p-b1", 630, 393, 100, 14)
          + card("@p-b", 730, 320, 560, 160, "change the value", 48) + bar("@p-b2", 1290, 393, 100, 14)
          + card("@p-c", 1390, 320, 440, 160, "scan again", 60, "on")
          + txt("@p-l", 190, 540, "&#8635; repeat", "m", fs=56)
          + txt("@p-d", 190, 700, "every round throws out the addresses", "h", fs=66)
          + txt("@p-e", 190, 800, 'that <span class="@p-acc">did not follow the game</span>', "h", fs=66),
          js="""
    wipe("#@p-t", <<whole-0.3>>, 0.6);
    land("#@p-a", <<scan>>); wipe("#@p-b1", <<change-0.2>>, 0.2); land("#@p-b", <<change>>);
    wipe("#@p-b2", <<scan#2-0.2>>, 0.2); land("#@p-c", <<scan#2>>); blurIn("#@p-l", <<again+0.3>>);
    wipe("#@p-d", <<every>>, 0.7); wipe("#@p-e", <<did-0.2>>, 0.7);
"""),

    Scene("again", "One more round. I fire again: ten left. Next Scan for ten. Still two addresses. Both have followed the counter twice, so this list will not get any shorter.",
          media=again_m,
          body=txt("@p-t", 80, 60, "next scan: 10", "h", fs=76) + g10.html() + g10.mark("@p-m1", *AMMO)
          + again_ce.mark("@p-m3", 0, 110, 90, 20, pad=6)
          + found("Found: 2")
          + txt("@p-c", 80, 800, "20 &rarr; 14 &rarr; 10: both addresses followed", "m", fs=56)
          + txt("@p-d", 80, 890, "the list will not get shorter", "m", fs=56, color="#E8490F"),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-g", 0.2, 1.03, 0.4); land("#@p-m1", <<ten>>, 1.4);
    land("#@p-m3", <<still>>, 1.4); land("#@p-f", <<still+0.2>>);
    blurIn("#@p-c", <<both>>); blurIn("#@p-d", <<shorter-0.8>>);
"""),

    Scene("warn", "One warning. After the first scan, that button is called New Scan. Press it by mistake, and the whole list is gone. Filtering is always Next Scan.",
          body=txt("@p-t", 80, 70, "careful: New Scan starts over", "h", fs=80) + btns.html()
          + btns.mark("@p-m1", 434, 130, 92, 30, pad=4) + btns.mark("@p-m2", 536, 130, 92, 30, pad=4)
          + card("@p-a", 80, 480, 800, 150, "New Scan", 70, "soft") + txt("@p-al", 930, 520, "the list is gone", "m", fs=56)
          + tile("@p-b", 80, 700, 800, 170, "Next Scan", 80) + txt("@p-bl", 930, 750, "filters the list", "m", fs=56),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-ce", 0.2, 1.03, 0.5);
    land("#@p-m1", <<button>>, 1.3); land("#@p-a", <<new>>); blurIn("#@p-al", <<gone-0.3>>);
    land("#@p-m2", <<filtering>>, 1.3); land("#@p-b", <<next>>); blurIn("#@p-bl", <<filtering>>);
"""),

    Scene("add", "Two addresses left. I double click each one, and it drops into the address list at the bottom. Remember the first one: zero zero eight one, nine three seven zero.",
          media=add_m,
          body=txt("@p-t", 80, 50, "keep them: the address list", "h", fs=72)
          + add_ce.mark("@p-m1", 2, 645, 760, 48, pad=4)
          + tile("@p-a", 1040, 200, 800, 170, "00819370", 110) + tile("@p-b", 1040, 440, 800, 170, "182C606C", 110)
          + txt("@p-c", 1040, 690, "double click a result:<br>it lands in the list below", "m", fs=48)
          + txt("@p-d", 1040, 850, "both hold 10 right now", "m", fs=48, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    blurIn("#@p-c", <<double>>);
    land("#@p-m1", <<bottom-0.3>>, 1.05);
    land("#@p-a", <<zero>>); land("#@p-b", <<zero+0.6>>);
    blurIn("#@p-d", <<seven>>);
"""),

    Scene("copy", "Which one is the real magazine? Write to each of them, and see which one the game follows. First, the second address: I type ninety-nine. Cheat Engine shows ninety-nine. The game still shows ten. So this one is only a copy.",
          media=copy_m, early=False,
          body=copy_c.mark("@p-m1", 672, 669, 60, 22, pad=4) + copy_g.mark("@p-m2", *AMMO)
          + tag("@p-g1", 1180, 60, "Cheat Engine: the address list", 36) + tag("@p-g2", 80, 840, "the game", 36)
          + txt("@p-c", 420, 850, 'second address = 99, game = 10: <span class="@p-acc">a copy</span>', "h", fs=60),
          js="""
    land("#@p-g1", 0.4); land("#@p-g2", 0.6);
    land("#@p-m1", <<shows>>, 1.4);
    land("#@p-m2", <<still>>, 1.4);
    wipe("#@p-c", <<so-0.2>>, 0.8);
"""),

    Scene("real", "Now the first address. Ninety-nine again. And this time, the counter in the game jumps to ninety-nine. This is the real one.",
          media=real_m, early=False,
          body=real_c.mark("@p-m1", 672, 645, 60, 22, pad=4) + real_g.mark("@p-m2", *AMMO)
          + tag("@p-g1", 1180, 60, "Cheat Engine: the address list", 36) + tag("@p-g2", 80, 840, "the game", 36)
          + txt("@p-c", 420, 850, 'first address = 99, game = 99: <span class="@p-acc">the real one</span>', "h", fs=56),
          js="""
    land("#@p-g1", 0.4); land("#@p-g2", 0.6);
    land("#@p-m1", <<again>>, 1.4);
    land("#@p-m2", <<jumps>>, 1.4);
    wipe("#@p-c", <<jumps+0.5>>, 0.8);
"""),

    Scene("shoot", "And it is not just a picture. I fire, and the game counts down from my number: ninety-seven, ninety-five. And the copy? On the first shot, the game overwrote my ninety-nine.",
          media=shoot_m, early=False,
          body=shoot_c.mark("@p-m1", 672, 669, 60, 22, pad=4) + shoot_g.mark("@p-m2", *AMMO)
          + tag("@p-g1", 1180, 60, "Cheat Engine: the address list", 36) + tag("@p-g2", 80, 840, "the game", 36)
          + txt("@p-c", 420, 850, 'the game uses my number: 99, 97, 95', "h", fs=60),
          js="""
    land("#@p-g1", 0.4); land("#@p-g2", 0.6);
    land("#@p-m2", <<counts>>, 1.4);
    wipe("#@p-c", <<ninety-seven-0.3>>, 0.8);
    land("#@p-m1", <<copy>>, 1.4);
"""),

    Scene("freeze", "One more thing the address list can do. Tick the box in the Active column, and keep firing. The counter flickers, but it returns to ninety-five. Cheat Engine has frozen the value: it writes ninety-five back, again and again, several times a second.",
          media=frz_m, early=False,
          body=frz_c.mark("@p-m1", 8, 645, 26, 22, pad=4) + frz_g.mark("@p-m2", *AMMO)
          + tag("@p-g1", 1180, 60, "Cheat Engine: the address list", 36) + tag("@p-g2", 80, 840, "the game", 36)
          + txt("@p-c", 420, 850, 'freeze = <span class="@p-acc">write it back, again and again</span>', "h", fs=58),
          js="""
    land("#@p-g1", 0.4); land("#@p-g2", 0.6);
    land("#@p-m1", <<tick>>, 1.4);
    wipe("#@p-c", <<writes-0.2>>, 0.8);
    land("#@p-m2", <<counter>>, 1.4);
"""),

    Scene("truth", "But a freeze does not stop the game's code. The game still subtracts. Cheat Engine only puts the old number back afterwards. The copy shows it: it kept counting, down to eighty-seven. The real fix is to change the code. That is episode seven.",
          body=frozen.html() + frozen.mark("@p-m1", 672, 669, 60, 22, pad=4) + frozen.mark("@p-m0", 672, 645, 60, 22, pad=4)
          + txt("@p-t", 80, 400, "a freeze does not stop the game's code", "h", fs=76)
          + card("@p-a", 80, 560, 520, 130, "game: 95 - 1", 50) + bar("@p-b1", 600, 618, 80, 14)
          + card("@p-b", 680, 560, 520, 130, "Cheat Engine: 95", 46, "on") + bar("@p-b2", 1200, 618, 80, 14)
          + card("@p-c", 1280, 560, 520, 130, "game: 95 - 1 ...", 46)
          + txt("@p-d", 80, 760, "the copy kept counting: 87", "m", fs=54)
          + txt("@p-e", 80, 860, 'the real fix: <span class="@p-acc">change the code</span> (episode 7)', "m", fs=54),
          js="""
    land("#@p-ce", 0.2, 1.02, 0.4);
    wipe("#@p-t", <<freeze-0.3>>, 0.7);
    land("#@p-a", <<still>>); wipe("#@p-b1", <<only-0.3>>, 0.2); land("#@p-b", <<only>>); land("#@p-m0", <<old>>, 1.4);
    wipe("#@p-b2", <<afterwards-0.2>>, 0.2); land("#@p-c", <<afterwards>>);
    land("#@p-m1", <<copy>>, 1.4); blurIn("#@p-d", <<eighty-seven-0.4>>);
    blurIn("#@p-e", <<change>>);
"""),

    # ------------------------------------------------------------------ unknown values
    Scene("scanme", "All of that worked because I knew the number. But what about a health bar, with no number at all? AssaultCube prints its health, so for this part I use a tiny practice program I wrote: Scan Me. Gold is a number. Health is only a bar, with nothing to type into the value box.",
          body=txt("@p-t", 80, 60, "scanme.exe: the practice program", "h", fs=76) + con.html()
          + con.mark("@p-m1", 30, 118, 250, 36, pad=4) + con.mark("@p-m2", 30, 156, 570, 36, pad=4)
          + tag("@p-g1", 1220, 290, "gold: a number", 40) + tag("@p-g2", 1220, 400, "health: only a bar", 40)
          + txt("@p-c", 80, 700, "a C++ program of mine, running on my own machine", "m", fs=50)
          + txt("@p-d", 80, 800, 'no number for the health: <span class="@p-acc">nothing to search for</span>', "m", fs=54)
          + txt("@p-e", 80, 900, "source: link in the description", "m", fs=40, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-k", 0.2, 1.03, 0.5);
    blurIn("#@p-c", <<practice>>); blurIn("#@p-e", <<scan-0.2>>);
    land("#@p-m1", <<gold>>, 1.2); land("#@p-g1", <<gold+0.2>>);
    land("#@p-m2", <<health#3>>, 1.2); land("#@p-g2", <<bar#2>>);
    blurIn("#@p-d", <<nothing>>);
"""),

    Scene("behave", "This is what the scan type list is for. You do not search for a value. You search for a behavior. Increased. Decreased. Changed. Unchanged. And when you only know a limit: Bigger than, Smaller than, or Value between.",
          body=txt("@p-t", 80, 50, "search for a behavior", "h", fs=76) + dd.html()
          + dd.mark("@p-m1", 489, 341, 222, 19, pad=2) + dd.mark("@p-m2", 489, 381, 222, 19, pad=2)
          + dd.mark("@p-m3", 489, 421, 222, 19, pad=2) + dd.mark("@p-m4", 489, 441, 222, 19, pad=2)
          + dd.mark("@p-m5", 489, 281, 222, 59, pad=2)
          + card("@p-a", 1140, 180, 700, 120, "Increased", 56, "on") + card("@p-b", 1140, 330, 700, 120, "Decreased", 56, "on")
          + card("@p-c", 1140, 480, 700, 120, "Changed", 56, "on") + card("@p-d", 1140, 630, 700, 120, "Unchanged", 56, "on")
          + txt("@p-e", 80, 780, "compared with the previous scan", "m", fs=50)
          + txt("@p-g", 80, 860, 'only a limit? <span class="@p-acc">Bigger than, Smaller than, Value between</span>', "m", fs=44)
          + txt("@p-f", 80, 940, "the real list, open in Cheat Engine", "m", fs=36, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.6);
    land("#@p-ce", 0.2, 1.03, 0.5); blurIn("#@p-f", 1.2);
    land("#@p-m1", <<increased>>, 1.2); land("#@p-a", <<increased>>);
    land("#@p-m2", <<decreased>>, 1.2); land("#@p-b", <<decreased>>);
    land("#@p-m3", <<changed>>, 1.2); land("#@p-c", <<changed>>);
    land("#@p-m4", <<unchanged>>, 1.2); land("#@p-d", <<unchanged>>);
    blurIn("#@p-e", <<changed>>);
    land("#@p-m5", <<bigger>>, 1.1); blurIn("#@p-g", <<limit-0.3>>);
"""),

    Scene("unknown", "So, a new scan. Value type: float, because a bar is often stored as a fraction. Scan type: unknown initial value. First Scan. Cheat Engine simply remembers everything. Fifty-nine thousand, three hundred and ninety-two candidates.",
          media=unk_m,
          body=txt("@p-t", 80, 60, "first scan: unknown initial value", "h", fs=72)
          + unk_ce.mark("@p-m3", 0, 110, 130, 20, pad=6)
          + card("@p-a", 1160, 190, 700, 120, "Value Type: Float", 46, "on")
          + card("@p-b", 1160, 340, 700, 120, "Unknown initial value", 44, "on")
          + found("Found: 59,392", 500)
          + txt("@p-d", 1160, 690, "no list is shown:<br>too many to draw", "m", fs=44, color="#6A9188")
          + txt("@p-c", 80, 800, "it remembers every value, to compare later", "m", fs=56)
          + txt("@p-e", 80, 890, "float found nothing useful? repeat with 4 Bytes", "m", fs=42, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-a", <<float>>); land("#@p-b", <<unknown>>);
    blurIn("#@p-c", <<remembers>>);
    land("#@p-m3", <<fifty-nine>>, 1.4); land("#@p-f", <<fifty-nine+0.2>>);
    blurIn("#@p-d", <<everything>>); blurIn("#@p-e", <<fraction>>);
"""),

    Scene("decr", "I press H, and take a hit. The bar gets shorter. So I pick Decreased value, and press Next Scan. "
                  "Everything that did not go down is thrown out. Seven left.",
          media=dec_m,
          body=txt("@p-t", 80, 50, "hit, then: Decreased value", "h", fs=72)
          + dec_k.mark("@p-m1", 30, 156, 570, 36, pad=4) + dec_c.mark("@p-m3", 0, 110, 90, 20, pad=6)
          + card("@p-a", 1160, 300, 700, 120, "the bar got shorter", 46, "soft") + card("@p-b", 1160, 450, 700, 120, "Decreased value", 50, "on")
          + found("Found: 7", 640)
          + txt("@p-d", 80, 880, '59,392 &rarr; <span class="@p-acc">7</span>', "h", fs=76),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-m1", <<bar>>, 1.2); land("#@p-a", <<shorter-0.2>>);
    land("#@p-b", <<decreased>>);
    land("#@p-m3", <<seven>>, 1.4); land("#@p-f", <<seven>>); wipe("#@p-d", <<seven+0.2>>, 0.6);
"""),

    Scene("unch", "Now the step most beginners skip. I do nothing. So: Unchanged value, Next Scan. In a busy game, this round removes the most: timers, animations, anything that changes by itself. Here, all seven survive.",
          media=unc_m,
          body=txt("@p-t", 80, 50, "do nothing, then: Unchanged value", "h", fs=72)
          + unc_c.mark("@p-m3", 0, 110, 90, 20, pad=6)
          + card("@p-a", 1160, 300, 700, 120, "I do nothing", 50, "soft") + card("@p-b", 1160, 450, 700, 120, "Unchanged value", 50, "on")
          + found("Found: 7", 640)
          + txt("@p-d", 80, 880, "removes whatever changes by itself", "m", fs=54),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-a", <<nothing>>); land("#@p-b", <<unchanged>>);
    blurIn("#@p-d", <<timers-0.3>>);
    land("#@p-m3", <<seven>>, 1.4); land("#@p-f", <<seven>>);
"""),

    Scene("incr", "I press R, to rest. The bar grows. Increased value, Next Scan. One address left. And look at its value: "
                  "ninety-two point five. That is the number the bar was hiding.",
          media=inc_m,
          body=txt("@p-t", 80, 50, "rest, then: Increased value", "h", fs=72)
          + inc_k.mark("@p-m1", 30, 156, 570, 36, pad=4) + inc_c.mark("@p-m3", 0, 110, 90, 20, pad=6) + inc_c.mark("@p-m4", 116, 157, 60, 20, pad=4)
          + card("@p-a", 1160, 300, 700, 120, "the bar grew", 50, "soft") + card("@p-b", 1160, 450, 700, 120, "Increased value", 50, "on")
          + found("Found: 1", 640)
          + txt("@p-d", 80, 880, 'the number behind the bar: <span class="@p-acc">92.5</span>', "h", fs=64),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-m1", <<bar>>, 1.2); land("#@p-a", <<grows-0.2>>);
    land("#@p-b", <<increased>>);
    land("#@p-m3", <<one>>, 1.4); land("#@p-f", <<one>>);
    land("#@p-m4", <<ninety-two>>, 1.4); wipe("#@p-d", <<ninety-two>>, 0.7);
"""),

    Scene("barwrite", "Same test as before. I add it to the list, write fifty, and the bar drops to exactly half. "
                      "Found, without ever seeing a number.",
          media=wr_m,
          body=txt("@p-t", 80, 50, "the test: write 50", "h", fs=72)
          + wr_k.mark("@p-m1", 30, 156, 570, 36, pad=4) + wr_c.mark("@p-m2", 672, 645, 80, 22, pad=4)
          + tile("@p-a", 1040, 300, 800, 170, "50 = half the bar", 70)
          + txt("@p-c", 1040, 560, "found without<br>ever seeing a number", "h", fs=60)
          + txt("@p-d", 1040, 760, "health is a float<br>from 0 to 100", "m", fs=48, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-m2", <<write>>, 1.3);
    land("#@p-m1", <<half-0.4>>, 1.2); land("#@p-a", <<half>>);
    wipe("#@p-c", <<found>>, 0.7); blurIn("#@p-d", <<found-0.6>>);
"""),

    Scene("rules", "Two rules. After every change, run one round of Unchanged. And do not assume a direction: some games count the damage you took, so a hit makes the value go up. If Decreased empties the list, start over with Changed value.",
          body=txt("@p-t", 190, 90, "two rules for unknown values", "h", fs=84)
          + card("@p-a", 190, 280, 1540, 130, "1. after every change: one round of Unchanged", 48, "on")
          + card("@p-b", 190, 460, 1540, 130, "2. do not assume a direction", 48, "on")
          + card("@p-c", 190, 660, 720, 120, "health left: goes down", 44, "soft") + card("@p-d", 1010, 660, 720, 120, "damage taken: goes up", 44, "soft")
          + txt("@p-e", 190, 860, 'Decreased emptied the list? start over with <span class="@p-acc">Changed value</span>', "m", fs=46),
          js="""
    wipe("#@p-t", <<rules-0.3>>, 0.6);
    land("#@p-a", 0.8, 1.05); land("#@p-b", <<assume-0.4>>, 1.05);
    land("#@p-c", <<direction>>); land("#@p-d", <<damage>>);
    blurIn("#@p-e", <<empties-0.5>>);
"""),

    # ------------------------------------------------------------------ wrong type
    Scene("zero", "Now the other way a scan fails. The program shows energy: eighty-seven. I scan for eighty-seven as four bytes, "
                  "use some energy, and scan for eighty-four. Found: zero. The list is empty.",
          media=int_m,
          body=txt("@p-t", 80, 50, "energy 87, scanned as 4 Bytes", "h", fs=72)
          + int_k.mark("@p-m1", 30, 195, 250, 36, pad=4) + int_c.mark("@p-m3", 0, 110, 90, 20, pad=6)
          + card("@p-a", 1160, 300, 700, 120, "Exact Value, 4 Bytes", 44, "soft")
          + card("@p-b", 1160, 450, 700, 120, "87, then 84", 50, "soft")
          + found("Found: 0", 640)
          + txt("@p-d", 80, 880, 'the list is <span class="@p-acc">empty</span>', "h", fs=70),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-m1", <<energy>>, 1.2); land("#@p-a", <<four>>); land("#@p-b", <<eighty-four-0.3>>);
    land("#@p-m3", <<zero+0.6>>, 1.4); land("#@p-f", <<zero+0.8>>); wipe("#@p-d", <<empty-0.5>>, 0.6);
"""),

    Scene("wrongtype", "The value is there. I asked with the wrong type. This program keeps energy as a float, eighty-four point zero four, and prints only the whole part. As four bytes, those same bytes are a completely different number.",
          body=txt("@p-t", 190, 90, "the value is there: wrong type", "h", fs=84)
          + card("@p-a", 190, 290, 520, 150, "on screen", 54, "soft") + tile("@p-a1", 790, 280, 420, 170, "84", 110)
          + card("@p-b", 190, 510, 520, 150, "in memory (Float)", 42, "soft") + tile("@p-b1", 790, 500, 620, 170, "84.04", 110)
          + card("@p-c", 190, 730, 520, 150, "read as 4 Bytes", 44, "soft") + card("@p-c1", 790, 730, 900, 150, "1118311547", 90)
          + txt("@p-d", 1260, 320, "only the whole part", "m", fs=44),
          js="""
    wipe("#@p-t", <<there-0.3>>, 0.6);
    land("#@p-b", <<float-0.3>>); land("#@p-b1", <<eighty-four>>);
    land("#@p-a", <<prints-0.2>>); land("#@p-a1", <<prints>>); blurIn("#@p-d", <<whole>>);
    land("#@p-c", <<four>>); land("#@p-c1", <<completely-0.3>>);
"""),

    Scene("between", "So: value type float. And because a float is rarely a round number, the scan type is Value between: eighty-four and eighty-five. "
                     "One result. I use some energy again, scan between eighty and eighty-one, and here it is in the address list: eighty point seven four.",
          media=flt_m,
          body=txt("@p-t", 80, 50, "Float + Value between", "h", fs=72)
          + flt_k.mark("@p-m1", 30, 195, 250, 36, pad=4) + flt_c.mark("@p-m2", 672, 645, 110, 22, pad=4)
          + card("@p-a", 1040, 300, 800, 120, "between 84 and 85", 50, "on")
          + card("@p-b", 1040, 450, 800, 120, "between 80 and 81", 50, "on")
          + tile("@p-c", 1040, 620, 800, 170, "80.74", 110)
          + txt("@p-d", 1040, 830, "the screen says 80", "m", fs=48, color="#6A9188"),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    land("#@p-m1", <<float>>, 1.2);
    land("#@p-a", <<between>>); land("#@p-b", <<between#2>>);
    land("#@p-m2", <<here>>, 1.3); land("#@p-c", <<point-0.4>>); blurIn("#@p-d", <<point+0.5>>);
"""),

    Scene("order", "So when a scan finds nothing, change the type. Four bytes first, then float, then the rest. Money and ammo are usually four bytes. Positions and timers, usually floats. A yes or no flag, often a single byte.",
          body=txt("@p-t", 190, 80, "nothing found? change the type", "h", fs=84)
          + card("@p-a", 190, 260, 400, 130, "4 Bytes", 56, "on") + txt("@p-r1", 610, 275, "&rarr;", "h", fs=80)
          + card("@p-b", 720, 260, 400, 130, "Float", 56, "on") + txt("@p-r2", 1140, 275, "&rarr;", "h", fs=80)
          + card("@p-c", 1250, 260, 560, 130, "2 Bytes, Byte, Double", 40)
          + card("@p-d", 190, 480, 760, 120, "money, ammo", 50, "soft") + bar("@p-d1", 950, 534, 110) + card("@p-d2", 1060, 480, 600, 120, "4 Bytes", 54, "on")
          + card("@p-e", 190, 640, 760, 120, "positions, timers", 46, "soft") + bar("@p-e1", 950, 694, 110) + card("@p-e2", 1060, 640, 600, 120, "Float", 54, "on")
          + card("@p-f", 190, 800, 760, 120, "a yes / no flag", 50, "soft") + bar("@p-f1", 950, 854, 110) + card("@p-f2", 1060, 800, 600, 120, "Byte", 54, "on"),
          js="""
    wipe("#@p-t", <<nothing-0.3>>, 0.6);
    land("#@p-a", <<four>>); blurIn("#@p-r1", <<then-0.2>>); land("#@p-b", <<float>>); blurIn("#@p-r2", <<then#2-0.2>>); land("#@p-c", <<rest>>);
    land("#@p-d", <<money>>); wipe("#@p-d1", <<usually-0.2>>, 0.2); land("#@p-d2", <<usually>>);
    land("#@p-e", <<positions>>); wipe("#@p-e1", <<usually#2-0.2>>, 0.2); land("#@p-e2", <<usually#2>>);
    land("#@p-f", <<flag-0.5>>); wipe("#@p-f1", <<often-0.2>>, 0.2); land("#@p-f2", <<single>>);
"""),

    # ------------------------------------------------------------------ the restart
    Scene("restart", "One last thing: the bad news. I close the game, and start it again. The game says twenty. My saved address shows ninety-five, only because the freeze left it there. And the magazine now lives somewhere else: zero zero eight four, six two eight eight.",
          body=dead_c.html() + dead_g.html()
          + dead_c.mark("@p-m1", 672, 645, 60, 22, pad=4) + dead_c.mark("@p-m2", 672, 669, 60, 22, pad=4) + dead_g.mark("@p-m3", *AMMO)
          + tag("@p-g1", 1180, 60, "after a restart: the same list", 36) + tag("@p-g2", 80, 840, "the game", 36)
          + tile("@p-k", 1100, 850, 520, 120, "00846288", 70) + txt("@p-kl", 420, 870, "the magazine, this run:", "h", fs=54),
          js="""
    land("#@p-ce", 0.2, 1.02, 0.4); land("#@p-g", 0.3, 1.02, 0.4); land("#@p-g1", 0.5); land("#@p-g2", 0.7);
    land("#@p-m3", <<twenty>>, 1.4);
    land("#@p-m1", <<ninety-five>>, 1.4);
    land("#@p-m2", <<somewhere>>, 1.4);
    blurIn("#@p-kl", <<magazine-0.2>>); land("#@p-k", <<zero>>);
"""),

    # ------------------------------------------------------------------ recap, practice, next
    Scene("recap", "Let's recap. First Scan. Change the value in the game, Next Scan, and repeat. Test what is left by writing to it. No number? Start from unknown, and filter by behavior. Nothing found? Change the type.",
          body=txt("@p-t", 190, 80, "recap", "h", fs=110)
          + txt("@p-a", 190, 270, "pick the type, First Scan", "m", fs=56)
          + txt("@p-b", 190, 400, "change it in the game, Next Scan, repeat", "m", fs=56)
          + txt("@p-c", 190, 530, "test what is left: write to it", "m", fs=56)
          + txt("@p-d", 190, 660, "no number? Unknown initial value, then behavior", "m", fs=56)
          + txt("@p-e", 190, 790, 'nothing found? <span class="@p-acc">change the type</span>', "m", fs=56),
          js="""
    wipe("#@p-t", 0.3, 0.5);
    wipe("#@p-a", 0.5, 0.8);
    wipe("#@p-b", <<change>>, 0.8);
    wipe("#@p-c", <<test>>, 0.8);
    wipe("#@p-d", <<no>>, 0.8);
    wipe("#@p-e", <<nothing>>, 0.8);
"""),

    Scene("practice", "Your practice. Compile scan me dot C P P from the description. Find the gold: one of the two addresses is a display copy that snaps straight back. Then find the health behind the bar, and set it to exactly half.",
          body=txt("@p-t", 80, 60, "practice", "h", fs=100)
          + tag("@p-g", 760, 90, "scanme.cpp: link in the description", 36)
          + con_p.html()
          + txt("@p-a", 1000, 260, "1. find the gold", "m", fs=54)
          + txt("@p-a2", 1000, 340, "two addresses:<br>which one snaps back?", "m", fs=44, color="#6A9188")
          + txt("@p-b", 1000, 500, "2. find the health<br>behind the bar", "m", fs=54)
          + txt("@p-c", 80, 680, '3. set the bar to exactly half', "m", fs=54)
          + txt("@p-d", 80, 790, "then restart it: do your addresses still work?", "m", fs=50, color="#E8490F"),
          js="""
    wipe("#@p-t", <<practice-0.2>>, 0.5);
    land("#@p-g", <<description-0.4>>);
    land("#@p-k", <<compile-0.3>>, 1.03, 0.4);
    blurIn("#@p-a", <<gold>>); blurIn("#@p-a2", <<two>>);
    blurIn("#@p-b", <<then>>); blurIn("#@p-c", <<set-0.3>>); blurIn("#@p-d", <<set-0.1>>);
"""),

    Scene("next", "Next time. The address we found today dies with every restart, exactly as episode two promised. "
                  "So we go looking for the pointer that survives. Finding the pointer. See you there.",
          body=txt("@p-s", 192, 220, "NEXT EPISODE", "m", fs=64)
          + txt("@p-a", 192, 330, "Finding", "h", fs=150) + txt("@p-b", 192, 490, 'the <span class="@p-acc">Pointer</span>', "h", fs=150)
          + card("@p-x", 192, 740, 520, 130, "00819370", 60, "soft") + bar("@p-x1", 172, 800, 560, 10)
          + txt("@p-ar", 760, 750, "&rarr;", "h", fs=90)
          + card("@p-y", 890, 740, 760, 130, "[game + ?] + 140", 56, "on"),
          js="""
    blurIn("#@p-s", <<next>>);
    land("#@p-x", <<address>>); wipe("#@p-x1", <<dies>>, 0.3);
    blurIn("#@p-ar", <<pointer-0.3>>); land("#@p-y", <<pointer>>);
    wipe("#@p-a", 0.8, 0.6); wipe("#@p-b", 1.1, 0.5);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Game Hacking from Scratch 5: Your First Memory Scan")
