"""Build the Hebrew lesson site: _source/<track>/*.md -> <track>/*.html + index.html.

Lessons are original explanations of the topics mapped in ../CURRICULUM.md.
Standard library only.  Run:  python site/_source/build.py
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent

MODULES = [
    ("start", "00-start-here", "מתחילים כאן"),
    ("foundations", "01-foundations", "יסודות: מספרים, זיכרון ו-Assembly"),
    ("cheat-engine", "02-cheat-engine", "סריקת זיכרון עם Cheat Engine"),
    ("re-tools", "03-re-tools", "כלי Reverse Engineering"),
    ("external", "04-external-trainers", "External Trainers"),
    ("injection", "05-dll-injection", "DLL Injection ו-Shellcode"),
    ("hooking", "06-hooking", "Hooking, Pattern Scanning וקריאה לפונקציות"),
    ("rendering", "07-rendering", "Rendering: ESP, Overlays ותפריטים"),
    ("features", "08-features", "בניית יכולות על משחקי תרגול"),
    ("engines", "09-engines", "מנועים ופלטפורמות"),
    ("kernel", "10-kernel", "Kernel"),
    ("anticheat", "11-anticheat-internals", "איך Anti-Cheat ו-Anti-Debug עובדים"),
    ("crackme", "12-crackmes", "CrackMes, KeyGens ו-Unpacking"),
    ("malware", "13-malware-analysis", "Malware Analysis"),
    ("exploit", "14-exploit-dev", "Exploit Development"),
    ("pentest", "15-pentest-ctf", "Pentest ו-CTF"),
]
SITE = "Game Hacking בעברית"

# lesson (track folder/file stem) -> video project under ../videos
VIDEOS = {
    "01-foundations/01-number-bases": "01-number-bases",
    "01-foundations/02-data-types-in-memory": "02-data-types",
    "01-foundations/03-virtual-memory": "03-virtual-memory",
    "01-foundations/04-pointers-and-pointer-chains": "04-pointer-chains",
    "01-foundations/05-reading-assembly": "05-reading-assembly",
}


def lesson_video(md_path):
    """Copy the lesson's newest render to site/videos/ and return its player card, or ''."""
    name = VIDEOS.get(f"{md_path.parent.name}/{md_path.stem}")
    renders = sorted((OUT.parent / "videos" / name / "renders").glob("*.mp4")) if name else []
    if not renders:
        return ""
    (OUT / "videos").mkdir(exist_ok=True)
    shutil.copyfile(renders[-1], OUT / "videos" / f"{name}.mp4")
    return (f'<section class="card"><h2>סרטון השיעור (באנגלית)</h2>'
            f'<video controls preload="metadata" src="../videos/{name}.mp4" '
            f'style="display:block;width:100%;border-radius:10px;background:#000"></video></section>')


def planned_units():
    """Remake units per track, from the catalog built by ../build_catalog.py."""
    cat = SRC.parent.parent / "catalog.json"
    if not cat.exists():
        return {}
    units = {}
    for v in json.loads(cat.read_text(encoding="utf-8")):
        units.setdefault(v["track"], set()).add(v["series"])
    return {t: len(u) for t, u in units.items()}

NOTICE = "לתרגול על משחקי offline בלבד"
SECTION_CLASS = {"הרעיון בקצרה": "tldr", "מילון מונחים": "glossary", "בדיקה עצמית": "quiz"}

THEME_JS = """<script>
(function(){var r=document.documentElement,k='gh-he-theme';
try{var s=localStorage.getItem(k);if(s)r.setAttribute('data-theme',s);}catch(e){}
window.toggleTheme=function(){var d=r.getAttribute('data-theme');
if(!d){d=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}
var n=d==='dark'?'light':'dark';r.setAttribute('data-theme',n);
try{localStorage.setItem(k,n);}catch(e){}};
addEventListener('scroll',function(){var p=document.querySelector('.progress');if(!p)return;
var h=document.documentElement;var m=h.scrollHeight-h.clientHeight;
p.style.width=(m>0?(h.scrollTop/m*100):0)+'%';},{passive:true});})();
</script>"""


def inline(text):
    """Inline markdown -> HTML (code, links, bold, italic)."""
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00",
                  lambda m: f"<code>{html.escape(codes[int(m.group(1))])}</code>", text)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse(md):
    """Return (title, meta_chips, sections) where sections = [(heading|None, html)]."""
    lines = [l.rstrip() for l in md.splitlines()]
    lines = [l for l in lines if l.strip() not in ('<div dir="rtl">', "</div>")]
    title, chips = "", []
    sections, cur_head, buf = [], None, []

    def flush():
        nonlocal buf
        if cur_head is not None or any(b.strip() for b in buf):
            sections.append((cur_head, "\n".join(buf)))
        buf = []

    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("# "):
            title = s[2:].strip()
            i += 1
        elif s.startswith("## "):
            flush()
            cur_head = s[3:].strip()
            i += 1
        elif s.startswith("### "):
            buf.append(f"<h3>{inline(s[4:].strip())}</h3>")
            i += 1
        elif s.startswith("**מודול:**"):
            for part in s.split("·"):
                m = re.match(r"\s*\*\*(.+?)\*\*\s*(.*)", part)
                if m:
                    chips.append((m.group(1), m.group(2).strip()))
            i += 1
        elif s.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            buf.append('<pre dir="ltr"><code>' + html.escape("\n".join(code)) + "</code></pre>")
        elif s.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            paras = "".join(f"<p>{inline(b)}</p>" for b in block if b)
            buf.append(f"<blockquote>{paras}</blockquote>")
        elif s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            head = cells(rows[0])
            body = [cells(r) for r in rows[2:]]
            t = ['<div class="table-wrap"><table><thead><tr>']
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            buf.append("".join(t))
        elif re.match(r"^(-|\d+\.)\s+", s):
            ordered = bool(re.match(r"^\d+\.", s))
            pat = r"^\d+\.\s+" if ordered else r"^-\s+"
            items = []
            while i < len(lines) and re.match(pat, lines[i].strip()):
                items.append(re.sub(pat, "", lines[i].strip()))
                i += 1
            tag = "ol" if ordered else "ul"
            buf.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
        else:
            para = [s]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^(#|>|\||-\s|\d+\.\s)", lines[i].strip()):
                para.append(lines[i].strip())
                i += 1
            buf.append(f"<p>{inline(' '.join(para))}</p>")
    flush()
    return title, chips, sections


def page(title, body, crumb, root, toc=""):
    layout = "layout" if toc else "layout single"
    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{root}assets/style.css">
{THEME_JS}
</head>
<body>
<div class="progress"></div>
<header class="topbar">
  <a class="home" href="{root}index.html">🎮 {SITE}</a>
  <span class="crumb">{crumb}</span>
  <span class="spacer"></span>
  <span class="badge">{NOTICE}</span>
  <button class="theme-btn" onclick="toggleTheme()" title="מצב בהיר / כהה" aria-label="מצב בהיר או כהה">◐</button>
</header>
<div class="{layout}">
<main>
{body}
<footer class="foot">{SITE} · שיעורים מקוריים · {NOTICE}</footer>
</main>
{toc}
</div>
</body>
</html>
"""


def build_lesson(md_path, mod_title, prev, nxt):
    title, chips, sections = parse(md_path.read_text(encoding="utf-8"))
    m = re.match(r"(שיעור\s+[\d.]+)\s*[—-]\s*(.+)", title)
    kicker, h1 = (m.group(1), m.group(2)) if m else ("", title)
    chip_html = "".join(f'<span class="chip">{html.escape(k)} <b dir="auto">{html.escape(v)}</b></span>'
                        for k, v in chips)
    parts = [f'<section class="hero"><div class="kicker">{html.escape(kicker)}</div>'
             f'<h1>{inline(h1)}</h1><div class="chips">{chip_html}</div></section>']
    video = lesson_video(md_path)
    if video:
        parts.append(video)
    toc_links = []
    for n, (head, content) in enumerate(sections):
        if head is None:
            parts.append(f'<section class="card">{content}</section>')
            continue
        cls = SECTION_CLASS.get(head, "")
        parts.append(f'<section class="card {cls}" id="s{n}"><h2>{inline(head)}</h2>\n{content}</section>')
        toc_links.append(f'<a href="#s{n}">{inline(head)}</a>')

    def link(item, cls, label):
        if not item:
            return "<span></span>"
        return f'<a class="{cls}" href="{item[0]}"><small>{label}</small>{html.escape(item[1])}</a>'

    parts.append(f'<nav class="pager">{link(prev, "prev", "→ השיעור הקודם")}'
                 f'{link(nxt, "next", "השיעור הבא ←")}</nav>')
    toc = '<aside class="toc"><div class="toc-title">בעמוד זה</div>' + "".join(toc_links) + "</aside>"
    crumb = f'<span dir="auto">{html.escape(mod_title)}</span>'
    return title, page(title, "\n".join(parts), crumb, "../", toc)


def main():
    index_modules = []
    total = 0
    for num, (track, folder, mod_title) in enumerate(MODULES):
        src_dir = SRC / folder
        files = sorted(src_dir.glob("*.md")) if src_dir.is_dir() else []
        titles = []
        for f in files:
            t, _, _ = parse(f.read_text(encoding="utf-8"))
            titles.append(t)
        lessons = []
        for i, f in enumerate(files):
            prev = (files[i - 1].stem + ".html", titles[i - 1]) if i > 0 else None
            nxt = (files[i + 1].stem + ".html", titles[i + 1]) if i + 1 < len(files) else None
            title, doc = build_lesson(f, mod_title, prev, nxt)
            out_dir = OUT / folder
            out_dir.mkdir(exist_ok=True)
            (out_dir / (f.stem + ".html")).write_text(doc, encoding="utf-8")
            lessons.append((f"{folder}/{f.stem}.html", title))
            total += 1
        index_modules.append((num, track, mod_title, lessons))

    cards = []
    planned = planned_units()
    for num, track, mod_title, lessons in index_modules:
        state = (f"{len(lessons)} שיעורים · " if lessons else "בקרוב · ") + f"{planned.get(track, 0)} יחידות מקור"
        items = "".join(f'<li><a href="{href}">{html.escape(t)}</a></li>' for href, t in lessons)
        ul = f'<ul class="lessons">{items}</ul>' if lessons else ""
        cards.append(f'<div class="module{"" if lessons else " empty"}"><div class="module-head">'
                     f'<span class="module-num">{num:02d}</span>'
                     f'<span class="module-title">{inline(mod_title)}</span>'
                     f'<span class="module-state">{state}</span></div>{ul}</div>')
    body = f"""<section class="hero"><div class="kicker">קורס בעברית</div>
<h1>{SITE}</h1>
<div class="chips"><span class="chip"><b>{len(MODULES)}</b> מסלולים</span><span class="chip"><b>{total}</b> שיעורים עד כה</span></div></section>
<div class="notice"><p><strong>מה יש כאן.</strong> שיעורים מקוריים בעברית על Reverse Engineering ו-Game Hacking, מסודרים לפי סדר לימוד: מיסודות הזיכרון ועד Kernel וניתוח Malware. מונחים מקצועיים נשארים באנגלית, עם הסבר בפעם הראשונה שהם מופיעים.</p>
<p><strong>{NOTICE}.</strong> מתרגלים על משחקי single-player, על משחקי קוד פתוח כמו AssaultCube מול בוטים, ועל תוכנות שכתבתם בעצמכם. לא על משחקים מקוונים ולא נגד שחקנים אחרים.</p></div>
<div class="modules">{''.join(cards)}</div>"""
    (OUT / "index.html").write_text(page(SITE, body, "", ""), encoding="utf-8")
    print(f"built {total} lessons + index.html")


if __name__ == "__main__":
    sys.exit(main())
