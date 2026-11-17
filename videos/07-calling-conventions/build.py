"""Video 7: Where Do the Arguments Go? (the stack and calling conventions).  Run: python build.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, bar, build, card, cells, tile, txt  # noqa: E402,F401

scenes = [
    Scene("hook", "You found a function in the game. To understand it, or to call it yourself, "
                  "you need to know one thing: where do its arguments go?",
          body=card("@p-f", 190, 250, 900, 160, "call 0x00405000", 70, "on")
          + card("@p-a1", 190, 500, 270, 130, "arg 1", 50) + card("@p-a2", 505, 500, 270, 130, "arg 2", 50)
          + card("@p-a3", 820, 500, 270, 130, "arg 3", 50)
          + txt("@p-q", 190, 760, '<span class="@p-acc">where do they go?</span>', "h", fs=110),
          js="""
    land("#@p-a1", <<understand>>);
    land("#@p-a2", <<call>>);
    land("#@p-a3", <<need>>);
    wipe("#@p-q", <<where>>, 0.6);
"""),

    Scene("stack", "In thirty-two bit code, they go on the stack. Pushed right to left, "
                   "so the first argument ends up on top.",
          body=txt("@p-lh", 190, 150, "the caller", "m")
          + card("@p-c3", 190, 240, 620, 120, "push 3", 56) + card("@p-c2", 190, 390, 620, 120, "push 2", 56)
          + card("@p-c1", 190, 540, 620, 120, "push 1", 56) + card("@p-cc", 190, 690, 620, 120, "call add", 56, "on")
          + txt("@p-rh", 1090, 150, "the stack", "m")
          + card("@p-s1", 1090, 240, 560, 120, "1 &nbsp;(first)", 52, "on")
          + card("@p-s2", 1090, 390, 560, 120, "2", 52, "soft") + card("@p-s3", 1090, 540, 560, 120, "3", 52, "soft")
          + txt("@p-top", 1090, 700, "top of the stack is up here", "m", fs=44),
          js="""
    blurIn(["#@p-lh", "#@p-rh"], <<stack-0.4>>);
    land("#@p-c3", <<pushed>>);
    land("#@p-s3", <<pushed+0.15>>);
    land("#@p-c2", <<right>>);
    land("#@p-s2", <<right+0.15>>);
    land("#@p-c1", <<left>>);
    land("#@p-s1", <<first>>);
    land("#@p-cc", <<ends>>);
    blurIn("#@p-top", <<so>>);
"""),

    Scene("frame", "Inside the function, E B P plus eight is the first argument. Plus twelve is the second. "
                   "And E B P minus four is a local variable.",
          body=card("@p-r0", 260, 130, 520, 120, "[ebp+0xC]", 54) + txt("@p-d0", 860, 160, "second argument", "m")
          + card("@p-r1", 260, 280, 520, 120, "[ebp+8]", 54, "on") + txt("@p-d1", 860, 310, "first argument", "m")
          + card("@p-r2", 260, 430, 520, 120, "[ebp+4]", 54, "soft") + txt("@p-d2", 860, 460, "return address", "m")
          + card("@p-r3", 260, 580, 520, 120, "[ebp]", 54, "soft") + txt("@p-d3", 860, 610, "saved ebp", "m")
          + card("@p-r4", 260, 730, 520, 120, "[ebp-4]", 54) + txt("@p-d4", 860, 760, "local variable", "m")
          + txt("@p-c", 260, 890, "plus is an argument, minus is a local", "m", fs=46),
          js="""
    each(["#@p-r2", "#@p-d2", "#@p-r3", "#@p-d3"], <<inside>>, 0.1, 1.1);
    land("#@p-r1", <<eight-0.3>>);
    blurIn("#@p-d1", <<first>>);
    land("#@p-r0", <<twelve-0.3>>);
    blurIn("#@p-d0", <<second>>);
    land("#@p-r4", <<minus-0.3>>);
    blurIn("#@p-d4", <<local>>);
    blurIn("#@p-c", <<minus>>);
"""),

    Scene("cleanup", "Who cleans the stack afterwards? In the C convention, the caller does: "
                     "you see an add to E S P right after the call. In the Windows convention, the function does: "
                     "it ends with a return that pops its own arguments.",
          body=txt("@p-t", 190, 90, "who cleans up?", "h", fs=90)
          + txt("@p-lh", 190, 260, "cdecl: the caller", "m")
          + card("@p-l1", 190, 350, 640, 120, "call add", 54) + card("@p-l2", 190, 500, 640, 120, "add esp, 8", 54, "on")
          + txt("@p-lm", 190, 660, "plain C functions", "m", fs=44)
          + txt("@p-rh", 1010, 260, "stdcall: the function", "m")
          + card("@p-r1", 1010, 350, 640, 120, "call Add", 54) + card("@p-r2", 1010, 500, 640, 120, "ret 8", 54, "on")
          + txt("@p-rm", 1010, 660, "the whole Windows API", "m", fs=44),
          js="""
    wipe("#@p-t", <<cleans-0.3>>, 0.5);
    blurIn("#@p-lh", <<caller>>);
    land("#@p-l1", <<caller+0.3>>);
    land("#@p-l2", <<add>>);
    blurIn("#@p-lm", <<after>>);
    blurIn("#@p-rh", <<windows>>);
    land("#@p-r1", <<function>>);
    land("#@p-r2", <<return>>);
    blurIn("#@p-rm", <<pops>>);
"""),

    Scene("thiscall", "C plus plus methods add one more thing: the object itself travels in E C X. "
                      "Find what loads E C X before a call, and you have found the player.",
          body=card("@p-a", 190, 260, 900, 140, "mov ecx, [player]", 60, "on")
          + card("@p-b", 190, 430, 900, 140, "call Player::TakeDamage", 52)
          + tile("@p-k", 1200, 290, 520, 250, "ecx = this", 64)
          + txt("@p-c", 190, 700, "ecx is the object", "h", fs=110)
          + txt("@p-m", 190, 840, "a free pointer to the player, no scanning needed", "m", fs=46),
          js="""
    land("#@p-b", <<methods>>);
    land("#@p-k", <<object>>);
    land("#@p-a", <<travels>>);
    wipe("#@p-c", <<find>>, 0.6);
    blurIn("#@p-m", <<before>>);
"""),

    Scene("x64", "Sixty-four bit Windows has one rule for everyone. The first four arguments ride in registers: "
                 "R C X, R D X, R eight and R nine. The result comes back in R A X.",
          body=txt("@p-t", 190, 100, "64-bit Windows: one rule", "h", fs=90)
          + card("@p-c0", 190, 330, 330, 150, "rcx", 70) + txt("@p-m0", 190, 500, "arg 1", "m")
          + card("@p-c1", 580, 330, 330, 150, "rdx", 70) + txt("@p-m1", 580, 500, "arg 2", "m")
          + card("@p-c2", 970, 330, 330, 150, "r8", 70) + txt("@p-m2", 970, 500, "arg 3", "m")
          + card("@p-c3", 1360, 330, 330, 150, "r9", 70) + txt("@p-m3", 1360, 500, "arg 4", "m")
          + tile("@p-r", 190, 670, 520, 180, "rax", 90) + txt("@p-rm", 770, 730, "the result", "m"),
          js="""
    wipe("#@p-t", <<rule-0.6>>, 0.6);
    each(["#@p-m0", "#@p-m1", "#@p-m2", "#@p-m3"], <<four>>, 0.1, 1.1);
    each(["#@p-c0", "#@p-c1", "#@p-c2", "#@p-c3"], <<registers+0.5>>, 0.55);
    land("#@p-r", <<result>>);
    blurIn("#@p-rm", <<back>>);
    tl.fromTo("#@p-r", { scale: 1 }, { scale: 1.06, duration: 0.2, ease: "power2.out", yoyo: true, repeat: 1 }, <<end-0.3>>);
"""),

    Scene("claim", "Stack or registers. Once you know where the arguments go, you can read any call.",
          body=card("@p-a1", 192, 200, 330, 110, "the stack", 46, "soft") + card("@p-a2", 560, 200, 330, 110, "registers", 46)
          + txt("@p-a", 192, 400, "Know where the<br>arguments go.", "h", fs=118)
          + txt("@p-c", 192, 690, '<span class="@p-acc">Then you can read any call.</span>', "h", fs=96),
          js="""
    each(["#@p-a1", "#@p-a2"], <<stack>>, 0.5);
    wipe("#@p-a", <<once>>, 0.8);
    wipe("#@p-c", <<read-0.3>>, 0.7);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Where Do the Arguments Go?")
