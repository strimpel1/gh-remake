"""One-off: write the animated scene files from the approved storyboard layouts. Outputs are plain HTML, edited by hand afterwards."""
from pathlib import Path

P = Path(r"C:\ai\gh-remake\videos\01-number-bases")
C = P / "compositions"

PAPER_BG = """background-color: #E4F2EC;
      background-image:
        linear-gradient(#9CCFC0 3px, transparent 3px), linear-gradient(90deg, #9CCFC0 3px, transparent 3px),
        linear-gradient(#C4E3D9 1px, transparent 1px), linear-gradient(90deg, #C4E3D9 1px, transparent 1px);
      background-size: 60px 60px, 60px 60px, 20px 20px, 20px 20px;"""

PAPER = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; {PAPER_BG}
      font-family: 'IBM Plex Mono', monospace; color: #0B2A30; }}
    .{{p}}-stage {{ position: absolute; inset: 0; }}
"""

ARENA = """
    #root { position: absolute; inset: 0; overflow: hidden; color: #fff; font-family: 'League Gothic', sans-serif; background: #0E4A55; }
    .{p}-stage { position: absolute; inset: 0; }
    .{p}-cam { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 38%, #2A97A6 0%, #1C7C8A 35%, #0E4A55 100%); }
    .{p}-world { position: absolute; inset: 0; z-index: 0; isolation: isolate; }
    .{p}-wall { position: absolute; left: -200px; right: -200px; top: 330px; height: 150px; background: #0C4650; border-top: 10px solid #093840; }
    .{p}-floorwrap { position: absolute; left: -200px; right: -200px; top: 480px; bottom: 0; overflow: hidden; background: #0F5560; }
    .{p}-floor { position: absolute; inset: 0; width: 100%; height: 100%; }
    .{p}-crate { position: absolute; z-index: 2; background: #E8B04A; border: 10px solid #B9832E; box-shadow: 14px 14px 0 #093840; }
    .{p}-crate::after { content: ""; position: absolute; inset: 0;
      background: linear-gradient(45deg, transparent 47%, #B9832E 47%, #B9832E 53%, transparent 53%); }
    .{p}-cross { position: absolute; left: 960px; top: 470px; width: 0; height: 0; z-index: 4; }
    .{p}-cross i { position: absolute; background: #fff; }
    .{p}-cross i:nth-child(1) { left: -34px; top: -3px; width: 22px; height: 6px; }
    .{p}-cross i:nth-child(2) { left: 12px; top: -3px; width: 22px; height: 6px; }
    .{p}-cross i:nth-child(3) { left: -3px; top: -34px; width: 6px; height: 22px; }
    .{p}-cross i:nth-child(4) { left: -3px; top: 12px; width: 6px; height: 22px; }
    .{p}-hud { position: absolute; left: 192px; bottom: 108px; z-index: 5; }
    .{p}-label { font-size: 64px; letter-spacing: 0.08em; line-height: 1; }
    .{p}-num { font-size: 330px; line-height: 0.86; margin-top: 6px; }
    .{p}-bar { position: relative; margin-top: 18px; width: 560px; height: 46px; border: 8px solid #fff; background: #093840; }
    .{p}-fill { position: absolute; left: 0; top: 0; bottom: 0; background: #FF5A1F;
      background-image: linear-gradient(90deg, transparent 50px, #093840 50px); background-size: 56px 100%; }
"""

ARENA_WORLD = """
        <div id="{p}-world" class="{p}-world" data-layout-allow-overflow>
          <div class="{p}-wall"></div>
          <div class="{p}-floorwrap"><svg class="{p}-floor" viewBox="0 0 2320 600" preserveAspectRatio="none"><rect width="2320" height="600" fill="#14606B"/><g stroke="#0C4650" stroke-width="6"><line x1="1160" y1="-150" x2="-3600" y2="600"/><line x1="1160" y1="-150" x2="-3260" y2="600"/><line x1="1160" y1="-150" x2="-2920" y2="600"/><line x1="1160" y1="-150" x2="-2580" y2="600"/><line x1="1160" y1="-150" x2="-2240" y2="600"/><line x1="1160" y1="-150" x2="-1900" y2="600"/><line x1="1160" y1="-150" x2="-1560" y2="600"/><line x1="1160" y1="-150" x2="-1220" y2="600"/><line x1="1160" y1="-150" x2="-880" y2="600"/><line x1="1160" y1="-150" x2="-540" y2="600"/><line x1="1160" y1="-150" x2="-200" y2="600"/><line x1="1160" y1="-150" x2="140" y2="600"/><line x1="1160" y1="-150" x2="480" y2="600"/><line x1="1160" y1="-150" x2="820" y2="600"/><line x1="1160" y1="-150" x2="1160" y2="600"/><line x1="1160" y1="-150" x2="1500" y2="600"/><line x1="1160" y1="-150" x2="1840" y2="600"/><line x1="1160" y1="-150" x2="2180" y2="600"/><line x1="1160" y1="-150" x2="2520" y2="600"/><line x1="1160" y1="-150" x2="2860" y2="600"/><line x1="1160" y1="-150" x2="3200" y2="600"/><line x1="1160" y1="-150" x2="3540" y2="600"/><line x1="1160" y1="-150" x2="3880" y2="600"/><line x1="1160" y1="-150" x2="4220" y2="600"/><line x1="1160" y1="-150" x2="4560" y2="600"/><line x1="1160" y1="-150" x2="4900" y2="600"/><line x1="1160" y1="-150" x2="5240" y2="600"/><line x1="1160" y1="-150" x2="5580" y2="600"/><line x1="1160" y1="-150" x2="5920" y2="600"/><line x1="0" y1="18" x2="2320" y2="18"/><line x1="0" y1="48" x2="2320" y2="48"/><line x1="0" y1="96" x2="2320" y2="96"/><line x1="0" y1="172" x2="2320" y2="172"/><line x1="0" y1="300" x2="2320" y2="300"/><line x1="0" y1="520" x2="2320" y2="520"/></g></svg></div>
          <div class="{p}-crate" style="left: 1210px; top: 380px; width: 230px; height: 230px"></div>
          <div class="{p}-crate" style="left: 1470px; top: 450px; width: 170px; height: 170px"></div>
          <div class="{p}-crate" style="left: 330px; top: 410px; width: 150px; height: 150px"></div>
        </div>
        <div class="{p}-cross"><i></i><i></i><i></i><i></i></div>"""

TILE = """
    .{p}-cell { position: relative; width: 150px; height: 150px; background: #fff; border: 8px solid #0B2A30;
      box-shadow: 10px 10px 0 #0B2A30; font-size: 110px; font-weight: 700; line-height: 134px; text-align: center; }
    .{p}-cell.on { background: #FF5A1F; color: #fff; }
    .{p}-pv { position: absolute; left: 0; right: 0; top: -66px; font-size: 40px; line-height: 1; color: #2E6B63; font-weight: 700; }
"""

JS_HEAD = """
    const tl = gsap.timeline({ paused: true });
    const blurIn = (sel, t, d = 0.2) =>
      tl.fromTo(sel, { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: d, ease: "power2.out" }, t);
    const blurOut = (sel, t, d = 0.2) => tl.to(sel, { opacity: 0, filter: "blur(8px)", duration: d, ease: "power2.in" }, t);
    const land = (sel, t, from = 1.3, d = 0.35) =>
      tl.fromTo(sel, { opacity: 0, scale: from }, { opacity: 1, scale: 1, duration: d, ease: "expo.out" }, t);
"""


def scene(sid, p, dur, css, body, js):
    (C / f"{sid}.html").write_text(f"""<template>
  <style>{css.replace("{p}", p)}  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
    <div id="{p}-stage" class="clip {p}-stage" data-start="0" data-duration="{dur}">{body}
    </div>
  </div>
  <script>{JS_HEAD}{js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
""", encoding="utf-8")


def cells(p, bits, pv=False, prefix="", extra=""):
    out = []
    for i, b in enumerate(bits):
        place = [8, 4, 2, 1][i % 4]
        pvh = f'<span class="{p}-pv">{place}</span>' if pv else ""
        out.append(f'<div id="{prefix}{i}" class="{p}-cell{" on" if b == "1" else ""}">{pvh}{b}{extra}</div>')
    return "".join(out)


# ---- 1: HUD ----
p = "s1"
scene("hud", p, 8.5, ARENA, f"""
      <div id="s1-cam" class="{p}-cam" data-layout-allow-overflow>{ARENA_WORLD.replace("{p}", p)}
        <div id="s1-hud" class="{p}-hud">
          <div class="{p}-label">HEALTH</div>
          <div id="s1-num" class="{p}-num">100</div>
          <div class="{p}-bar"><div id="s1-fill" class="{p}-fill" style="width: 100%"></div></div>
        </div>
      </div>
      <div id="s1-white" style="position: absolute; inset: 0; background: #fff" data-layout-ignore></div>""", """
    // the world looks around a little, then the camera dives into the stem of the "1"
    tl.fromTo("#s1-world", { x: 60 }, { x: -40, duration: 5.2, ease: "sine.inOut" }, 0);
    tl.fromTo("#s1-fill", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.9, ease: "power2.out" }, 0.25);
    const hp = { v: 0 };
    const num = document.querySelector("#s1-num");
    tl.fromTo(hp, { v: 0 }, { v: 100, duration: 0.9, ease: "power2.out", onUpdate: () => { num.textContent = Math.round(hp.v); } }, 0.25);
    gsap.set("#s1-cam", { transformOrigin: "345px 765px" });
    tl.fromTo("#s1-cam", { scale: 1 }, { scale: 1.35, duration: 2.6, ease: "power2.inOut" }, 5.0);
    tl.to("#s1-cam", { scale: 5, duration: 0.9, ease: "power3.in" }, 7.6);
    // the white of the numeral opens over the frame
    tl.fromTo("#s1-white", { clipPath: "circle(0px at 345px 765px)" }, { clipPath: "circle(2000px at 345px 765px)", duration: 0.5, ease: "power3.in" }, 8.0);
""")

# ---- 2: memory wall ----
p = "s2"
rows = [
    ("00F8A480", "3C 00 00 00 01 00 00 00 9A 99 19 3F 00 00 80 3F"),
    ("00F8A490", "00 00 C8 42 00 00 48 43 00 00 20 41 14 00 00 00"),
    ("00F8A4A0", "28 00 00 00 02 00 01 00 E8 03 00 00 64 00 00 00"),
    ("00F8A4B0", "32 00 00 00 00 00 00 00 42 6F 62 00 00 00 00 00"),
    ("00F8A4C0", "FF FF FF FF 10 27 00 00 00 00 A0 40 01 01 00 00"),
    ("00F8A4D0", "00 20 3F 0A 00 00 00 00 0C 00 00 00 7F 00 00 00"),
    ("00F8A4E0", "05 00 00 00 00 00 7A 44 00 00 00 00 1E 00 00 00"),
]
rh = []
for n, (addr, bs) in enumerate(rows):
    bh = []
    for k, b in enumerate(bs.split()):
        hero = n == 2 and k == 12
        bh.append(f'<span id="s2-hero" class="s2-hero">{b}</span>' if hero else f'<span class="s2-b">{b}</span>')
    rh.append(f'        <div id="s2-row{n}" class="{p}-row"><span class="{p}-addr">{addr}</span>{"".join(bh)}</div>')
scene("wall", p, 9.1, PAPER + """
    .{p}-wall { position: absolute; left: 96px; top: 150px; right: 96px; }
    .{p}-row { display: flex; align-items: center; height: 112px; font-size: 56px; font-weight: 700; color: #0B2A30; }
    .{p}-row span { width: 96px; height: 96px; line-height: 96px; text-align: center; }
    .{p}-row .{p}-addr { width: 330px; text-align: left; color: #2E6B63; margin-right: 30px; }
    .{p}-flash { position: absolute; inset: 0; background: #fff; }
""", f"""
      <div id="s2-wall" class="{p}-wall" data-layout-allow-overflow>
{chr(10).join(rh)}
      </div>
      <div id="s2-flash" class="{p}-flash" data-layout-ignore></div>""", """
    // out of the white of the numeral, rows print one at a time
    tl.fromTo("#s2-flash", { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "power2.out" }, 0);
    for (let i = 0; i < 7; i++) {
      tl.fromTo("#s2-row" + i, { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power1.inOut" }, 1.0 + i * 0.38);
    }
    // everything dims except the byte we follow
    tl.to(".s2-b", { color: "#9DC4BA", duration: 0.5, ease: "power2.inOut" }, 5.8);
    tl.to(".s2-addr", { color: "#9DC4BA", duration: 0.5, ease: "power2.inOut" }, 5.8);
    tl.to("#s2-row2 .s2-addr", { color: "#2E6B63", duration: 0.3 }, 6.3);
    tl.fromTo("#s2-hero", { backgroundColor: "rgba(255,90,31,0)", color: "#0B2A30", scale: 1 },
      { backgroundColor: "rgba(255,90,31,1)", color: "#ffffff", scale: 1.25, duration: 0.3, ease: "back.out(2.5)" }, 6.1);
    // push in on it; the tile of the next scene takes over at this size and place
    gsap.set("#s2-wall", { transformOrigin: "1415px 280px" });
    tl.fromTo("#s2-wall", { scale: 1 }, { scale: 5.6, duration: 0.8, ease: "power3.in" }, 8.3);
""")

# ---- 3: the byte alone ----
p = "s3"
scene("byte", p, 9.6, PAPER + """
    .{p}-tile { position: absolute; left: 192px; top: 240px; width: 640px; height: 600px; background: #FF5A1F; color: #fff;
      border: 12px solid #0B2A30; box-shadow: 18px 18px 0 #0B2A30; font-size: 440px; font-weight: 700; line-height: 576px; text-align: center; }
    .{p}-wrong { position: absolute; left: 960px; top: 300px; font-family: 'Archivo Black', sans-serif; font-size: 110px; line-height: 1; color: #6A9188; }
    .{p}-strike { position: absolute; left: -16px; right: -16px; top: 52%; height: 14px; background: #0B2A30; }
    .{p}-base { position: absolute; left: 960px; top: 470px; font-size: 54px; font-weight: 700; color: #2E6B63; }
    .{p}-right { position: absolute; left: 960px; top: 580px; font-family: 'Archivo Black', sans-serif; font-size: 230px; line-height: 1; }
""", f"""
      <div id="s3-tile" class="{p}-tile">64</div>
      <div id="s3-wrong" class="{p}-wrong">sixty-four<span id="s3-strike" class="{p}-strike"></span></div>
      <div class="{p}-base"><span id="s3-base">hexadecimal</span><span id="s3-base2"> &middot; base 16</span></div>
      <div id="s3-right" class="{p}-right">= 100</div>""", """
    // the byte arrives from where the wall left it
    tl.fromTo("#s3-tile", { x: 999, y: -110, scale: 0.93 }, { x: 0, y: 0, scale: 1, duration: 0.7, ease: "expo.out" }, 0);
    blurIn("#s3-wrong", 2.7);
    gsap.set("#s3-strike", { transformOrigin: "0 50%" });
    tl.fromTo("#s3-strike", { scaleX: 0 }, { scaleX: 1, duration: 0.25, ease: "power3.out" }, 3.5);
    blurIn("#s3-base", 4.3);
    blurIn("#s3-base2", 5.4);
    land("#s3-right", 7.85);
    // words leave, the tile travels up to head the next shot
    blurOut(["#s3-wrong", "#s3-base", "#s3-base2", "#s3-right"], 8.95);
    tl.to("#s3-tile", { x: 448, y: -290, scaleX: 0.47, scaleY: 0.4, duration: 0.5, ease: "power2.inOut" }, 9.08);
""")

# ---- 4: eight bits ----
p = "s4"
scene("bits", p, 8.1, PAPER + TILE + """
    .{p}-tile { position: absolute; left: 810px; top: 130px; width: 300px; height: 240px; background: #FF5A1F; color: #fff;
      border: 10px solid #0B2A30; box-shadow: 12px 12px 0 #0B2A30; font-size: 170px; font-weight: 700; line-height: 220px; text-align: center; }
    .{p}-stem { position: absolute; left: 954px; top: 382px; width: 12px; height: 108px; background: #0B2A30; }
    .{p}-row { position: absolute; left: 270px; top: 490px; display: flex; gap: 26px; }
    .{p}-cap { position: absolute; left: 0; right: 0; top: 760px; text-align: center; font-family: 'Archivo Black', sans-serif; font-size: 120px; line-height: 1; }
""", f"""
      <div id="s4-tile" class="{p}-tile">64</div>
      <div id="s4-stem" class="{p}-stem"></div>
      <div id="s4-row" class="{p}-row">{cells(p, "01100100", prefix="s4-c")}</div>
      <div id="s4-cap" class="{p}-cap">1 byte = 8 bits</div>""", """
    gsap.set("#s4-stem", { transformOrigin: "50% 0" });
    tl.fromTo("#s4-stem", { scaleY: 0 }, { scaleY: 1, duration: 0.3, ease: "power2.out" }, 1.4);
    for (let i = 0; i < 8; i++) land("#s4-c" + i, 2.3 + i * 0.22, 1.35, 0.3);
    blurIn("#s4-cap", 5.2);
    // the label and the tile leave; the eight cells stay for the split
    blurOut(["#s4-cap", "#s4-tile", "#s4-stem"], 7.7, 0.25);
""")

# ---- 5: split into nibbles ----
p = "s5"
scene("split", p, 10.2, PAPER + TILE + """
    .{p}-grp { position: absolute; top: 200px; display: flex; gap: 22px; }
    .{p}-sum { position: absolute; top: 400px; width: 666px; text-align: center; font-size: 60px; font-weight: 700; color: #2E6B63; }
    .{p}-dig { position: absolute; top: 490px; width: 666px; text-align: center; font-size: 330px; font-weight: 700; line-height: 1; color: #E8490F; }
    .{p}-eq { position: absolute; left: 0; right: 0; top: 860px; text-align: center; font-family: 'Archivo Black', sans-serif; font-size: 104px; line-height: 1; }
    .{p}-eq em { font-style: normal; color: #E8490F; }
""", f"""
      <div id="s5-g1" class="{p}-grp" style="left: 192px">{cells(p, "0110", pv=True, prefix="s5-a")}</div>
      <div id="s5-g2" class="{p}-grp" style="left: 1062px">{cells(p, "0100", pv=True, prefix="s5-b")}</div>
      <div id="s5-sum1" class="{p}-sum" style="left: 192px">4 + 2</div>
      <div id="s5-sum2" class="{p}-sum" style="left: 1062px">4</div>
      <div id="s5-d1" class="{p}-dig" style="left: 192px">6</div>
      <div id="s5-d2" class="{p}-dig" style="left: 1062px">4</div>
      <div id="s5-eq" class="{p}-eq"><em>6</em> &times; 16 + <em>4</em> = 100</div>""", """
    // the same eight cells, starting where the last shot held them, part in the middle
    for (let i = 0; i < 4; i++) {
      tl.fromTo("#s5-a" + i, { x: 270 + i * 176 - (192 + i * 172), y: 290 }, { x: 0, y: 0, duration: 0.8, ease: "power2.inOut" }, 0.7);
      tl.fromTo("#s5-b" + i, { x: 270 + (i + 4) * 176 - (1062 + i * 172), y: 290 }, { x: 0, y: 0, duration: 0.8, ease: "power2.inOut" }, 0.7);
    }
    tl.fromTo(".s5-pv", { opacity: 0 }, { opacity: 1, duration: 0.15, stagger: 0.07 }, 2.3);
    blurIn("#s5-sum1", 3.9);
    land("#s5-d1", 5.15);
    blurIn("#s5-sum2", 6.2);
    land("#s5-d2", 7.1);
    blurIn("#s5-eq", 7.8);
    blurOut("#s5-stage", 9.9, 0.25);
""")

# ---- 6: digit table ----
p = "s6"
trs = []
for n in range(16):
    col, row = divmod(n, 8)
    hexd = "0123456789ABCDEF"[n]
    trs.append(f'      <div id="s6-r{n}" class="{p}-r{" az" if n >= 10 else ""}" style="left: {250 + col * 760}px; top: {168 + row * 100}px">'
               f'<span>{n:04b}</span><i></i><b>{hexd}</b><u>{n}</u></div>')
scene("table", p, 9.9, PAPER + """
    .{p}-head { position: absolute; left: 0; right: 0; top: 60px; text-align: center; font-family: 'Archivo Black', sans-serif; font-size: 72px; line-height: 1; }
    .{p}-r { position: absolute; width: 660px; height: 84px; display: flex; align-items: center; font-weight: 700; background: #fff;
      border: 6px solid #0B2A30; box-shadow: 8px 8px 0 #0B2A30; }
    .{p}-r span { width: 270px; text-align: center; font-size: 60px; letter-spacing: 0.08em; }
    .{p}-r i { width: 70px; height: 8px; background: #0B2A30; }
    .{p}-r b { width: 150px; text-align: center; font-size: 70px; }
    .{p}-r u { width: 140px; text-align: center; font-size: 44px; text-decoration: none; color: #2E6B63; }
    .{p}-r.az { background: #E8490F; color: #fff; }
    .{p}-r.az i { background: #fff; }
    .{p}-r.az u { color: #fff; }
""", f"""
      <div id="s6-head" class="{p}-head">4 bits &rarr; 16 patterns &rarr; 16 digits</div>
{chr(10).join(trs)}""", """
    blurIn("#s6-stage", 0, 0.25);
    blurIn("#s6-head", 0.5);
    // one row per count: 0-9 quickly, then A-F with room to read each
    gsap.set(".s6-r", { transformOrigin: "50% 0" });
    for (let n = 0; n < 16; n++) {
      const t = n < 10 ? 3.5 + n * 0.2 : 6.6 + (n - 10) * 0.3;
      tl.fromTo("#s6-r" + n, { opacity: 0, scaleY: 0.2 }, { opacity: 1, scaleY: 1, duration: 0.22, ease: "power3.out" }, t);
    }
    blurOut("#s6-stage", 9.6, 0.25);
""")

# ---- 7: FF ----
p = "s7"
on = '<b class="s7-on">1</b>'
scene("full", p, 9.7, PAPER + TILE + """
    .{p}-grp { position: absolute; top: 150px; display: flex; gap: 22px; }
    .{p}-on { position: absolute; inset: 0; background: #E8490F; color: #fff; }
    .{p}-dig { position: absolute; top: 330px; width: 666px; text-align: center; font-size: 400px; font-weight: 700; line-height: 1; color: #E8490F; }
    .{p}-eq { position: absolute; left: 0; right: 0; top: 740px; text-align: center; font-family: 'Archivo Black', sans-serif; font-size: 150px; line-height: 1; }
    .{p}-cap { position: absolute; left: 0; right: 0; top: 905px; text-align: center; font-size: 54px; font-weight: 700; color: #2E6B63; }
    .{p}-flood { position: absolute; inset: 0; background: #FF5A1F; }
""", f"""
      <div id="s7-g1" class="{p}-grp" style="left: 192px">{cells(p, "0110", prefix="s7-a", extra=on)}</div>
      <div id="s7-g2" class="{p}-grp" style="left: 1062px">{cells(p, "0100", prefix="s7-b", extra=on)}</div>
      <div id="s7-d1" class="{p}-dig" style="left: 192px">F</div>
      <div id="s7-d2" class="{p}-dig" style="left: 1062px">F</div>
      <div id="s7-eq" class="{p}-eq">FF = 255</div>
      <div id="s7-cap" class="{p}-cap">the most one byte can hold</div>
      <div id="s7-flood" class="{p}-flood" data-layout-ignore></div>""", """
    blurIn(["#s7-g1", "#s7-g2"], 0, 0.25);
    // every bit flips to 1, left to right
    const faces = gsap.utils.toArray(".s7-on");
    faces.forEach((el, i) => {
      tl.fromTo(el, { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.18, ease: "power3.out" }, 0.7 + i * 0.2);
    });
    land("#s7-d1", 3.5, 1.4);
    land("#s7-d2", 3.85, 1.4);
    land("#s7-eq", 5.3, 1.2);
    blurIn("#s7-cap", 6.95);
    // the orange of the byte floods the frame; the next shot pulls back out of it
    tl.fromTo("#s7-flood", { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(75% at 50% 50%)", duration: 0.4, ease: "power3.in" }, 9.28);
""")

# ---- 8: back to the HUD ----
p = "s8"
scene("back", p, 7.8, ARENA + """
    .{p}-chip { position: absolute; z-index: 5; left: 1010px; top: 150px; padding: 26px 34px; background: #E4F2EC; color: #0B2A30; border: 8px solid #0B2A30;
      box-shadow: 12px 12px 0 #093840; font-family: 'IBM Plex Mono', monospace; font-weight: 700; font-size: 50px; display: flex; gap: 26px; align-items: center; }
    .{p}-chip span { color: #6A9188; }
    .{p}-chip b { background: #FF5A1F; color: #fff; padding: 4px 18px; font-size: 64px; }
    .{p}-chip .{p}-a { color: #2E6B63; }
""", f"""
      <div id="s8-cam" class="{p}-cam" data-layout-allow-overflow>{ARENA_WORLD.replace("{p}", p)}
        <div id="s8-chip" class="{p}-chip"><span class="{p}-a">00F8A4AC</span><b id="s8-ff">FF</b><span>00 00 00</span></div>
        <div id="s8-hud" class="{p}-hud">
          <div class="{p}-label">HEALTH</div>
          <div id="s8-num" class="{p}-num">255</div>
          <div class="{p}-bar" data-layout-allow-overflow><div id="s8-fill" class="{p}-fill" style="width: 255%"></div></div>
        </div>
      </div>""", """
    // pull back out of the byte into the game
    gsap.set("#s8-cam", { transformOrigin: "1378px 226px" });
    tl.fromTo("#s8-cam", { scale: 40 }, { scale: 3.2, duration: 1.0, ease: "expo.out" }, 0);
    tl.to("#s8-cam", { scale: 1, duration: 1.1, ease: "power3.inOut" }, 2.3);
    tl.fromTo("#s8-world", { x: 30 }, { x: -50, duration: 7.8, ease: "none" }, 0);
    // the game reads the byte: 100 becomes 255 and the bar runs past its frame
    const hp = { v: 100 };
    const num = document.querySelector("#s8-num");
    tl.fromTo(hp, { v: 100 }, { v: 255, duration: 0.9, ease: "power2.out", onUpdate: () => { num.textContent = Math.round(hp.v); } }, 4.75);
    tl.fromTo("#s8-fill", { clipPath: "inset(0 60.8% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.9, ease: "power2.out" }, 4.75);
    gsap.set("#s8-num", { transformOrigin: "0 100%" });
    tl.fromTo("#s8-num", { scale: 1 }, { scale: 1.12, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }, 5.6);
""")

# ---- 9: claim ----
p = "s9"
words1 = "".join(f'<span class="s9-w">{w}</span> ' for w in "Hex is the same bits,".split())
words2 = "".join(f'<span class="s9-w">{w}</span> ' for w in "four at a time.".split())
scene("claim", p, 7.5, PAPER + TILE + """
    .{p}-cell { width: 110px; height: 110px; font-size: 80px; line-height: 94px; }
    .{p}-grp { position: absolute; top: 170px; display: flex; gap: 16px; }
    .{p}-dig { position: absolute; top: 170px; width: 150px; height: 110px; line-height: 110px; text-align: center; font-size: 130px; font-weight: 700; color: #E8490F; }
    .{p}-line { position: absolute; left: 192px; right: 192px; top: 420px; font-family: 'Archivo Black', sans-serif; font-size: 128px; line-height: 1.06; letter-spacing: -0.01em; }
    .{p}-line em { font-style: normal; color: #E8490F; }
    .{p}-w { display: inline-block; }
    .{p}-cover { position: absolute; inset: 0; background: #0E4A55; }
""", f"""
      <div id="s9-g1" class="{p}-grp" style="left: 192px">{cells(p, "0110", prefix="s9-a")}</div>
      <div id="s9-d1" class="{p}-dig" style="left: 710px">6</div>
      <div id="s9-g2" class="{p}-grp" style="left: 960px">{cells(p, "0100", prefix="s9-b")}</div>
      <div id="s9-d2" class="{p}-dig" style="left: 1478px">4</div>
      <div id="s9-line" class="{p}-line" data-hold>{words1}<br><em>{words2}</em></div>
      <div id="s9-cover" class="{p}-cover" data-layout-ignore></div>""", """
    // the game is wiped off the paper, left to right
    tl.fromTo("#s9-cover", { clipPath: "inset(0 0 0 0%)" }, { clipPath: "inset(0 0 0 100%)", duration: 0.45, ease: "power3.inOut" }, 0);
    tl.fromTo(".s9-cell", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: "expo.out", stagger: 0.05 }, 0.45);
    land("#s9-d1", 1.1);
    land("#s9-d2", 1.4);
    tl.fromTo("#s9-line > .s9-w", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.16, ease: "power2.out", stagger: 0.1 }, 2.5);
    tl.fromTo("#s9-line em .s9-w", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.16, ease: "power2.out", stagger: 0.1 }, 3.7);
""")

import json
DUR = {l["id"]: l["duration"] for l in json.loads((P / "assets/voice/index.json").read_text())["lines"]}
SC = [("hud", 0, 8.5, 0.5), ("wall", 8.5, 9.1, 0.4), ("byte", 17.6, 9.6, 0.4), ("bits", 27.2, 8.1, 0.4), ("split", 35.3, 10.2, 0.4),
      ("table", 45.5, 9.9, 0.4), ("full", 55.4, 9.7, 0.4), ("back", 65.1, 7.8, 0.4), ("claim", 72.9, 7.5, 0.4)]
hosts = "\n".join(
    f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{a}" '
    f'data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
    for sid, a, d, v in SC)
audio = "\n".join(
    f'      <audio id="vo{i:02d}" class="clip" src="assets/voice/{i:02d}.wav" data-start="{round(a + v, 2)}" data-duration="{DUR[f"{i:02d}"]}" data-track-index="3" data-volume="1"></audio>'
    for i, (sid, a, d, v) in enumerate(SC, 1))
(P / "index.html").write_text(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #E4F2EC; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="80.4" data-width="1920" data-height="1080">
{hosts}
{audio}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""", encoding="utf-8")
print("ok")
