"""Video 6: Edit a Save File, Byte by Byte (hex editing).  Run: python build.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from kit import Scene, bar, build, card, cells, tile, txt  # noqa: E402,F401

INK = "#0B2A30"
SPAN = "\n    .@p-m span { display: inline-block; }\n    .@p-of { color: #6A9188; }\n"


def rows(y):
    """Three hex-editor rows, 8 bytes each. Columns at fs=56: offset x=180, bytes x=516, text x=1356."""
    data = [
        ("00000000", '<span id="@p-g1">53 41 56 45</span> 01 00 00 00', "SAVE...."),
        ("00000008", '<span id="@p-g2">64 00 00 00</span> <span id="@p-g3">E8 03 00 00</span>', "d...&egrave;..."),
        ("00000010", "42 6F 62 00 00 00 00 00", "Bob....."),
    ]
    out = ""
    for i, (off, by, tx) in enumerate(data):
        out += txt(f"@p-r{i}", 180, y + i * 96,
                   f'<span class="@p-of">{off}</span>&nbsp;&nbsp;{by}&nbsp;&nbsp;<span class="@p-of">{tx}</span>',
                   "m", fs=56, color=INK)
    return out


HI = '{ backgroundColor: "#FF5A1F", color: "#ffffff", duration: 0.25, ease: "power2.out" }'

scenes = [
    Scene("hook", "A save file is just bytes on disk. No debugger, no running game. "
                  "Open it in a hex editor, and your gold is sitting right there.",
          css=SPAN,
          body=txt("@p-t", 180, 150, "save.dat", "h", fs=96) + rows(330)
          + txt("@p-c", 180, 720, '<span class="@p-acc">your gold: 1000</span>', "h", fs=110),
          js=f"""
    wipe("#@p-r0", <<bytes>>, 0.4);
    wipe("#@p-r1", <<debugger>>, 0.4);
    wipe("#@p-r2", <<running>>, 0.4);
    tl.fromTo("#@p-t", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.2, ease: "power2.out", yoyo: true, repeat: 1 }}, <<open>>);
    tl.to("#@p-g3", {HI}, <<gold>>);
    land("#@p-c", <<gold+0.2>>);
"""),

    Scene("columns", "Three columns. The offset: how far from the start. The bytes. And the same bytes as text.",
          css=SPAN,
          body=rows(250)
          + bar("@p-b1", 180, 560, 269) + txt("@p-l1", 180, 590, "offset", "m")
          + bar("@p-b2", 516, 560, 773) + txt("@p-l2", 516, 590, "the bytes, in hex", "m")
          + bar("@p-b3", 1356, 560, 269) + txt("@p-l3", 1356, 590, "as text", "m")
          + txt("@p-c", 180, 780, "how far from the start of the file", "m"),
          js="""
    wipe("#@p-b1", <<offset>>, 0.3);
    blurIn("#@p-l1", <<offset>>);
    blurIn("#@p-c", <<far>>);
    wipe("#@p-b2", <<bytes>>, 0.4);
    blurIn("#@p-l2", <<bytes>>);
    wipe("#@p-b3", <<text>>, 0.3);
    blurIn("#@p-l3", <<text>>);
"""),

    Scene("read", "Read it like memory. The letters S A V E. Then one hundred, as a whole number. "
                  "Then E eight, zero three: one thousand gold.",
          css=SPAN,
          body=rows(200)
          + card("@p-c1", 180, 600, 420, 140, "SAVE", 64) + txt("@p-m1", 180, 770, "a text marker", "m", fs=44)
          + card("@p-c2", 690, 600, 420, 140, "100", 64) + txt("@p-m2", 690, 770, "health, 4 bytes", "m", fs=44)
          + card("@p-c3", 1200, 600, 420, 140, "1000", 64, "on") + txt("@p-m3", 1200, 770, "gold, small end first", "m", fs=44),
          js=f"""
    tl.to("#@p-g1", {{ backgroundColor: "#0B2A30", color: "#ffffff", duration: 0.25 }}, <<letters>>);
    each(["#@p-c1", "#@p-m1"], <<letters+0.3>>, 0.15);
    tl.to("#@p-g2", {{ backgroundColor: "#0B2A30", color: "#ffffff", duration: 0.25 }}, <<hundred-0.4>>);
    each(["#@p-c2", "#@p-m2"], <<hundred>>, 0.15);
    tl.to("#@p-g3", {HI}, <<eight>>);
    each(["#@p-c3", "#@p-m3"], <<thousand>>, 0.15);
"""),

    Scene("compare", "To find a value, save with one thousand gold, then with twelve fifty, and compare the two files. "
                     "The bytes that changed are yours.",
          body=txt("@p-l1", 190, 300, "save 1<br>1000 gold", "m")
          + cells("@p-a", 720, 270, ["E8", "03", "00", "00"], 190, 26, on={0, 1})
          + txt("@p-l2", 190, 560, "save 2<br>1250 gold", "m")
          + cells("@p-b", 720, 530, ["E2", "04", "00", "00"], 190, 26, on={0, 1})
          + txt("@p-c", 0, 820, "what changed is yours", "h", fs=90, w=1920, align="center"),
          js="""
    blurIn("#@p-l1", <<thousand-0.5>>);
    each(".c-@p-a", <<thousand>>, 0.1);
    blurIn("#@p-l2", <<then>>);
    each(".c-@p-b", <<twelve>>, 0.1);
    wipe("#@p-c", <<changed-0.3>>, 0.6);
"""),

    Scene("edit", "Overwrite those four bytes with the biggest number they can hold. Save the file, load the game, "
                  "and you are rich.",
          body=txt("@p-l1", 190, 215, "before", "m")
          + cells("@p-a", 720, 170, ["E8", "03", "00", "00"], 170, 24)
          + txt("@p-l2", 190, 445, "after", "m")
          + cells("@p-b", 720, 400, ["FF", "FF", "FF", "7F"], 170, 24, on={0, 1, 2, 3})
          + txt("@p-n", 0, 650, '<span class="@p-acc">2,147,483,647</span>', "h", fs=180, w=1920, align="center")
          + txt("@p-c", 0, 870, "gold", "m", w=1920, align="center"),
          js="""
    blurIn("#@p-l2", <<overwrite>>);
    each(".c-@p-b", <<overwrite+0.3>>, 0.3);
    dim(".c-@p-a", <<biggest>>, 0.35);
    land("#@p-n", <<load>>, 1.2);
    blurIn("#@p-c", <<rich>>);
"""),

    Scene("traps", "Two traps. Never insert bytes, only overwrite, or everything after them shifts. "
                   "And some games store a checksum, so an edited save looks corrupt.",
          body=txt("@p-t", 190, 100, "two traps", "h", fs=96)
          + card("@p-a", 190, 300, 720, 150, "overwrite, never insert", 46, "on")
          + txt("@p-am", 190, 480, "one extra byte shifts<br>everything after it", "m")
          + card("@p-b", 1010, 300, 720, 150, "checksum", 60, "on")
          + txt("@p-bm", 1010, 480, "the game notices the edit:<br>&quot;save corrupted&quot;", "m"),
          js="""
    land("#@p-a", <<insert-0.5>>);
    blurIn("#@p-am", <<shifts-0.6>>);
    land("#@p-b", <<checksum-0.3>>);
    blurIn("#@p-bm", <<corrupt-0.8>>);
"""),

    Scene("claim", "So back up the file first. And remember: a file is just memory that sits still.",
          body=cells("@p-b", 192, 190, ["E8", "03", "00", "00"], 120, 18, on={0, 1})
          + txt("@p-a", 192, 400, "Back up first.", "h", fs=118)
          + txt("@p-c", 192, 540, '<span class="@p-acc">A file is memory that sits still.</span>', "h", fs=92),
          js="""
    each(".c-@p-b", 0.3, 0.08);
    wipe("#@p-a", <<back>>, 0.5);
    wipe("#@p-c", <<file#2-0.2>>, 0.7);
"""),
]

if __name__ == "__main__":
    build(__file__, scenes, "Edit a Save File, Byte by Byte")
