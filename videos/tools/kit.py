"""Scene kit for the lesson videos: one look, one voice, timings taken from the narration.

A video's build.py lists scenes (narration text + layout + animation) and calls build().
build() voices each scene with Azure Speech (cached), sizes every scene to its clip, resolves
T("word") anchors to the moment that word is spoken, and writes compositions/*.html + index.html.

    from kit import *
    build(__file__, [Scene("hook", "Narration text.", body=..., js='blurIn("#@p-a", <<text>>);')])

In body and js, "@p" is the scene prefix (s1, s2, ...). In js, <<word>> is the scene-local second that
word is spoken; <<word#2>> its second occurrence; <<word+0.3>> an offset; <<end>> the end of the voice;
<<dur-0.5>> relative to the scene's end.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import azure_tts  # noqa: E402

LEAD = 0.4          # silence before the voice in each scene
TAIL = 0.7          # room after the voice for the exit
LAST_TAIL = 2.6     # the final line holds

CSS_COMMON = """
    .{p}-stage { position: absolute; inset: 0; }
    .{p}-h { position: absolute; font-family: 'Archivo Black', sans-serif; font-size: 96px; line-height: 1.05; letter-spacing: -0.01em; color: #0B2A30; }
    .{p}-m { position: absolute; font-family: 'IBM Plex Mono', monospace; font-weight: 700; font-size: 54px; line-height: 1.15; color: #2E6B63; }
    .{p}-acc { color: #E8490F; }
    .{p}-dim { color: #6A9188; }
    .{p}-cell { position: absolute; background: #fff; border: 8px solid #0B2A30; box-shadow: 10px 10px 0 #0B2A30;
      font-family: 'IBM Plex Mono', monospace; font-weight: 700; text-align: center; color: #0B2A30; }
    .{p}-cell.on { background: #FF5A1F; color: #fff; }
    .{p}-tile { position: absolute; background: #FF5A1F; color: #fff; border: 12px solid #0B2A30; box-shadow: 16px 16px 0 #0B2A30;
      font-family: 'IBM Plex Mono', monospace; font-weight: 700; text-align: center; }
    .{p}-card { position: absolute; background: #fff; color: #0B2A30; border: 8px solid #0B2A30; box-shadow: 10px 10px 0 #0B2A30;
      font-family: 'IBM Plex Mono', monospace; font-weight: 700; text-align: center; }
    .{p}-card.on { background: #FF5A1F; color: #fff; }
    .{p}-card.soft { background: #CFE9DF; }
    .{p}-bar { position: absolute; background: #0B2A30; }
    .{p}-shot { position: absolute; overflow: hidden; background: #fff; border: 8px solid #0B2A30; box-shadow: 12px 12px 0 #0B2A30; }
    .{p}-shot img, .{p}-shot video { position: absolute; display: block; max-width: none; }
    .{p}-mark { position: absolute; border: 8px solid #FF5A1F; border-radius: 12px; box-shadow: 0 0 0 6px rgba(255, 90, 31, 0.28); }
    .{p}-tag { position: absolute; background: #FF5A1F; color: #fff; border: 6px solid #0B2A30; box-shadow: 8px 8px 0 #0B2A30;
      font-family: 'IBM Plex Mono', monospace; font-weight: 700; padding: 6px 22px; white-space: nowrap; }
    .{p}-term { position: absolute; background: #0B2A30; border: 8px solid #0B2A30; box-shadow: 12px 12px 0 #2E6B63; padding: 26px 34px;
      font-family: 'IBM Plex Mono', monospace; font-weight: 500; color: #E4F2EC; white-space: pre; }
    .{p}-term .hi { color: #FF9A6B; font-weight: 700; }
    .{p}-term .dimc { color: #7FB5A8; }
    .{p}-media { position: absolute; inset: 0; }
"""

CSS_PAPER = """
    #root { position: absolute; inset: 0; overflow: hidden; background-color: #E4F2EC;
      background-image:
        linear-gradient(#9CCFC0 3px, transparent 3px), linear-gradient(90deg, #9CCFC0 3px, transparent 3px),
        linear-gradient(#C4E3D9 1px, transparent 1px), linear-gradient(90deg, #C4E3D9 1px, transparent 1px);
      background-size: 60px 60px, 60px 60px, 20px 20px, 20px 20px; }
"""

CSS_ARENA = """
    #root { position: absolute; inset: 0; overflow: hidden; background: radial-gradient(ellipse at 50% 38%, #2A97A6 0%, #1C7C8A 35%, #0E4A55 100%); }
    .{p}-wall { position: absolute; left: 0; right: 0; top: 330px; height: 150px; background: #0C4650; border-top: 10px solid #093840; }
    .{p}-floor { position: absolute; left: 0; top: 480px; width: 1920px; height: 600px; }
    .{p}-crate { position: absolute; background: #E8B04A; border: 10px solid #B9832E; box-shadow: 14px 14px 0 #093840; }
    .{p}-crate::after { content: ""; position: absolute; inset: 0; background: linear-gradient(45deg, transparent 47%, #B9832E 47%, #B9832E 53%, transparent 53%); }
    .{p}-hudl { position: absolute; font-family: 'League Gothic', sans-serif; font-size: 64px; letter-spacing: 0.08em; line-height: 1; color: #fff; }
    .{p}-hudn { position: absolute; font-family: 'League Gothic', sans-serif; font-size: 330px; line-height: 0.86; color: #fff; }
    .{p}-hudbar { position: absolute; width: 560px; height: 46px; border: 8px solid #fff; background: #FF5A1F;
      background-image: linear-gradient(90deg, transparent 50px, #093840 50px); background-size: 56px 100%; }
    .{p}-h { color: #fff; }
    .{p}-m { color: #BFE6DD; }
"""

JS_HEAD = """
    const tl = gsap.timeline({ paused: true });
    const blurIn = (sel, t, d = 0.2) =>
      tl.fromTo(sel, { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: d, ease: "power2.out" }, t);
    const blurOut = (sel, t, d = 0.2) => tl.to(sel, { opacity: 0, filter: "blur(8px)", duration: d, ease: "power2.in" }, t);
    const land = (sel, t, from = 1.3, d = 0.35) =>
      tl.fromTo(sel, { opacity: 0, scale: from }, { opacity: 1, scale: 1, duration: d, ease: "expo.out" }, t);
    const each = (sel, t, gap = 0.12, from = 1.3) =>
      tl.fromTo(sel, { opacity: 0, scale: from }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out", stagger: gap }, t);
    const wipe = (sel, t, d = 0.3) =>
      tl.fromTo(sel, { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: d, ease: "power2.out" }, t);
    const dim = (sel, t, to = 0.3) => tl.to(sel, { opacity: to, duration: 0.3, ease: "power2.inOut" }, t);
"""


# ---------- layout helpers (ids are yours; "{p}" becomes the scene prefix) ----------
def _style(**kw):
    return "; ".join(f"{k.replace('_', '-')}: {v}" for k, v in kw.items() if v is not None)


def txt(id, x, y, text, cls="h", fs=None, color=None, w=None, align=None):
    st = _style(left=f"{x}px", top=f"{y}px", font_size=f"{fs}px" if fs else None, color=color,
                width=f"{w}px" if w else None, text_align=align)
    return f'      <div id="{id}" class="{{p}}-{cls}" style="{st}">{text}</div>\n'


def tile(id, x, y, w, h, text, fs):
    st = _style(left=f"{x}px", top=f"{y}px", width=f"{w}px", height=f"{h}px", line_height=f"{h - 24}px", font_size=f"{fs}px")
    return f'      <div id="{id}" class="{{p}}-tile" style="{st}">{text}</div>\n'


def card(id, x, y, w, h, text, fs=54, kind=""):
    st = _style(left=f"{x}px", top=f"{y}px", width=f"{w}px", height=f"{h}px", line_height=f"{h - 16}px", font_size=f"{fs}px")
    return f'      <div id="{id}" class="{{p}}-card {kind}" style="{st}">{text}</div>\n'


def cells(prefix, x, y, vals, size=180, gap=24, on=(), fs=None):
    """A row of byte/bit tiles; ids are prefix0, prefix1, ... and all share class {p}-c-<prefix>."""
    fs = fs or int(size * (0.5 if max(len(v) for v in vals) > 1 else 0.72))
    out = ""
    for i, v in enumerate(vals):
        st = _style(left=f"{x + i * (size + gap)}px", top=f"{y}px", width=f"{size}px", height=f"{size}px",
                    line_height=f"{size - 16}px", font_size=f"{fs}px")
        out += f'      <div id="{prefix}{i}" class="{{p}}-cell c-{prefix}{" on" if i in on else ""}" style="{st}">{v}</div>\n'
    return out


def bar(id, x, y, w, h=12):
    return f'      <div id="{id}" class="{{p}}-bar" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px"></div>\n'


def tag(id, x, y, text, fs=40):
    return f'      <div id="{id}" class="{{p}}-tag" style="left: {x}px; top: {y}px; font-size: {fs}px">{text}</div>\n'


def term(id, x, y, w, lines, fs=40, lh=1.5):
    """A terminal / code card. Every line is its own element (id-l0, id-l1, ...) so lines can be revealed one by one."""
    rows = "".join(f'<div id="{id}-l{i}" style="height: {round(fs * lh)}px; line-height: {round(fs * lh)}px">{ln or "&nbsp;"}</div>' for i, ln in enumerate(lines))
    return f'      <div id="{id}" class="{{p}}-term" style="left: {x}px; top: {y}px; width: {w}px; font-size: {fs}px">{rows}</div>\n'


class Shot:
    """A real screenshot (or a recording) in a frame. mark()/tag_at() take pixel coordinates of the SOURCE image,
    so a highlight is placed by reading positions off the screenshot itself.

        s = Shot("@p-ce", ASSETS / "shots/ce_table.png", x=120, y=160, w=1100, crop=(0, 590, 902, 350))
        body = s.html() + s.mark("@p-m1", 676, 44, 90, 26)
    """
    B = 8

    def __init__(self, id, path, x, y, w, crop=None, size=None):
        if size is None:
            from PIL import Image
            size = Image.open(path).size
        self.id, self.path, self.x, self.y, self.w = id, Path(path), x, y, w
        self.W, self.H = size
        self.cx, self.cy, self.cw, self.ch = crop or (0, 0, self.W, self.H)
        self.s = (w - 2 * self.B) / self.cw
        self.h = round(self.ch * self.s + 2 * self.B)
        self.src = "assets/" + self.path.as_posix().split("/assets/", 1)[1]

    def _inner(self):
        return (f'left: {-self.cx * self.s:.1f}px; top: {-self.cy * self.s:.1f}px; width: {self.W * self.s:.1f}px; '
                f'height: {self.H * self.s:.1f}px')

    def html(self):
        return (f'      <div id="{self.id}" class="{{p}}-shot" style="left: {self.x}px; top: {self.y}px; width: {self.w}px; height: {self.h}px">'
                f'<img src="{self.src}" style="{self._inner()}"></div>\n')

    def video(self, start=0, dur=None, media_start=0):
        """The same frame around a muted recording. Goes in Scene(media=...), never in body."""
        return (f'      <div id="{self.id}" class="{{p}}-shot" style="left: {self.x}px; top: {self.y}px; width: {self.w}px; height: {self.h}px">'
                f'<video id="{self.id}-v" class="clip" src="{self.src}" muted playsinline data-start="{start}" data-duration="{dur}" '
                f'data-media-start="{media_start}" data-track-index="2" style="{self._inner()}"></video></div>\n')

    def pos(self, px, py):
        return (round(self.x + self.B + (px - self.cx) * self.s), round(self.y + self.B + (py - self.cy) * self.s))

    def mark(self, id, px, py, pw, ph, pad=8):
        x, y = self.pos(px, py)
        return (f'      <div id="{id}" class="{{p}}-mark" style="left: {x - pad}px; top: {y - pad}px; width: {round(pw * self.s) + 2 * pad}px; '
                f'height: {round(ph * self.s) + 2 * pad}px"></div>\n')


def fit_clip(src, dur, start=0.0):
    """Cut a recording to exactly `dur` seconds from `start`, holding its last frame if it is shorter. Cached next to the source."""
    import subprocess
    src = Path(src)
    out = src.with_name(f"{src.stem}_fit{int(start * 10)}_{int(round(dur * 10))}.mp4")
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-i", str(src), "-vf", f"tpad=stop_mode=clone:stop_duration={dur}",
                        "-t", str(dur), "-r", "30", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-an", str(out)], check=True)
    return out


def arena(hud_value="100"):
    lines = "".join(f'<line x1="960" y1="-150" x2="{960 + k * 340}" y2="600"/>' for k in range(-12, 13))
    lines += "".join(f'<line x1="0" y1="{y}" x2="1920" y2="{y}"/>' for y in (18, 48, 96, 172, 300, 520))
    return (
        '      <div class="{p}-wall"></div>\n'
        '      <svg class="{p}-floor" viewBox="0 0 1920 600" preserveAspectRatio="none"><rect width="1920" height="600" fill="#14606B"/>'
        f'<g stroke="#0C4650" stroke-width="6">{lines}</g></svg>\n'
        '      <div class="{p}-crate" style="left: 1210px; top: 380px; width: 230px; height: 230px"></div>\n'
        '      <div class="{p}-crate" style="left: 1470px; top: 450px; width: 170px; height: 170px"></div>\n'
        '      <div class="{p}-hudl" style="left: 192px; top: 560px">HEALTH</div>\n'
        f'      <div id="{{p}}-hudn" class="{{p}}-hudn" style="left: 192px; top: 630px">{hud_value}</div>\n'
        '      <div class="{p}-hudbar" style="left: 192px; top: 926px"></div>\n')


class Scene:
    def __init__(self, sid, say, body, js, bg="paper", css="", enter=True, exit=True, media=None, early=True):
        """media: optional function(dur) -> html for recordings (Shot.video). Videos must sit outside the timed stage.
        early: move the first reveals forward so the screen is never empty under narration (see _early)."""
        self.sid, self.say, self.body, self.js, self.bg, self.css, self.enter, self.exit = sid, say, body, js, bg, css, enter, exit
        self.media, self.early = media, early


ENTER = re.compile(r'\b(blurIn|land|each|wipe)\((\[[^\]]*\]|"[^"]*"),\s*(-?\d+(?:\.\d+)?)')
FIRST_AT, VISUAL_BY, VISUAL_AT = 0.3, 2.0, 1.0


def _early(js, body, p):
    """Never leave the screen empty under narration: the scene's first element is on screen at 0.3 s, and its first
    real visual (not just a heading, a highlight or a tag) by 2 s. Only the calls that come too late are moved; every
    other reveal stays on its spoken word. Scene(early=False) switches this off."""
    kinds = {m.group(1): m.group(2) for m in re.finditer(r'id="([^"]+)" class="' + p + r'-(\w+)', body)}

    def kind(sel):
        first = re.search(r'[#.][\w-]+', sel).group()
        if first.startswith(".c-"):
            return "cell"
        k = kinds.get(first[1:], "x")
        if k in ("h", "m") and re.search(r"-(t|s)$", first):
            return "heading"
        return k

    calls = [(float(m.group(3)), m, kind(m.group(2))) for m in ENTER.finditer(js)]
    animated = {s for _, m, _ in calls for s in re.findall(r'#([\w-]+)', m.group(2))}
    animated_cls = {s for _, m, _ in calls for s in re.findall(r'\.c-([\w-]+)', m.group(2))}
    static = [(i, k) for i, k in kinds.items() if i not in animated and not any(i.startswith(c) for c in animated_cls)
              and ("#" + i) not in js]
    skip = ("mark", "tag", "bar", "x")
    moves = {}
    shown = [c for c in calls if c[2] not in skip]
    if not static and shown:
        t, m, _ = min(shown, key=lambda c: c[0])
        if t > FIRST_AT:
            moves[m.start(3)] = (m.end(3), FIRST_AT)
    static_visual = any(k not in skip and not re.search(r"-(t|s)$", i) for i, k in static)
    visuals = [c for c in shown if c[2] != "heading"]
    if not static_visual and visuals:
        t, m, _ = min(visuals, key=lambda c: c[0])
        if t > VISUAL_BY and m.start(3) not in moves:
            moves[m.start(3)] = (m.end(3), VISUAL_AT)
    for a in sorted(moves, reverse=True):
        b, t = moves[a]
        js = js[:a] + str(t) + js[b:]
    return js


def _norm(w):
    return re.sub(r"[^a-z0-9'-]", "", w.lower())


def build(build_file, scenes, title=""):
    project = Path(build_file).resolve().parent
    comp = project / "compositions"
    comp.mkdir(exist_ok=True)
    voice = azure_tts.voice_lines(project, [s.say for s in scenes])

    start, hosts, audio, script = 0.0, [], [], [f"# Narration: {title}", "",
                                                f"Voiced with Azure Speech ({azure_tts.VOICE}, rate {azure_tts.RATE}). Generated by build.py.", ""]
    for n, (s, v) in enumerate(zip(scenes, voice), 1):
        p = f"s{n}"
        last = n == len(scenes)
        dur = round(LEAD + v["duration"] + (LAST_TAIL if last else TAIL), 1)
        words = [(_norm(w), t) for w, t in v["words"]]

        def T(word, k=0, off=0.0, _words=words, _sid=s.sid):
            hits = [t for w, t in _words if w == _norm(word)] or [t for w, t in _words if w.startswith(_norm(word))]
            if len(hits) <= k:
                sys.exit(f'scene "{_sid}": word "{word}" (occurrence {k}) not in narration: {" ".join(w for w, _ in _words)}')
            return round(LEAD + hits[k] + off, 2)

        T.end = round(LEAD + v["duration"], 2)
        T.dur = dur
        def tok(m, _T=T):
            mm = re.match(r"^(.+?)(?:#(\d+))?([+-]\d+(?:\.\d+)?)?$", m.group(1))
            word, k, off = mm.group(1), int(mm.group(2) or 1) - 1, float(mm.group(3) or 0)
            if word == "end":
                return str(round(_T.end + off, 2))
            if word == "dur":
                return str(round(_T.dur + off, 2))
            return str(_T(word, k, off))

        js = re.sub(r"<<(.+?)>>", tok, s.js)
        if s.early:
            js = _early(js.replace("@p", p), s.body.replace("{p}", p).replace("@p", p), p)
        media = f'    <div id="{p}-media" class="{p}-media">\n{s.media(dur).rstrip()}\n    </div>\n' if s.media else ""
        both = f"#{p}-stage, #{p}-media" if s.media else f"#{p}-stage"
        if s.enter and n > 1:
            js = f'    blurIn("{both}", 0, 0.25);\n' + js
        if s.exit and not last:
            js += f'\n    blurOut("{both}", {round(dur - 0.3, 2)}, 0.25);'
        css = (CSS_PAPER if s.bg == "paper" else CSS_ARENA) + CSS_COMMON + s.css
        if s.bg == "arena":
            css = CSS_COMMON + CSS_ARENA + s.css
        doc = f"""<template>
  <style>{css}  </style>
  <div id="root" data-composition-id="{s.sid}" data-width="1920" data-height="1080">
{media}    <div id="{p}-stage" class="clip {p}-stage" data-start="0" data-duration="{dur}">
{s.body.rstrip()}
    </div>
  </div>
  <script>{JS_HEAD}{js}
    window.__timelines["{s.sid}"] = tl;
  </script>
</template>
""".replace("{p}", p).replace("@p", p)
        ids = re.findall(r'id="([^"]+)"', doc)
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:   # one animation call would hide or move two elements
            sys.exit(f'scene "{s.sid}": duplicate ids {dup}')
        (comp / f"{s.sid}.html").write_text(doc, encoding="utf-8")
        hosts.append(f'      <div id="{s.sid}" data-composition-id="{s.sid}" data-composition-src="compositions/{s.sid}.html" data-start="{round(start, 2)}" '
                     f'data-duration="{dur}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
        audio.append(f'      <audio id="vo{n:02d}" class="clip" src="assets/voice/{n:02d}.wav" data-start="{round(start + LEAD, 2)}" '
                     f'data-duration="{v["duration"]}" data-track-index="3" data-volume="1"></audio>')
        script.append(f"{n}. ({round(start, 1)}–{round(start + dur, 1)}) {s.say}")
        print(f"{n:2d} {s.sid:10s} {start:6.1f}s  +{dur:4.1f}s  voice {v['duration']:.2f}s")
        start = round(start + dur, 2)

    (project / "SCRIPT.md").write_text("\n".join(script) + "\n", encoding="utf-8")
    nl = "\n"
    (project / "index.html").write_text(f"""<!doctype html>
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
    <div id="root" data-composition-id="main" data-start="0" data-duration="{start}" data-width="1920" data-height="1080">
{nl.join(hosts)}
{nl.join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""", encoding="utf-8")
    print(f"total {start:.1f}s -> {project}")
