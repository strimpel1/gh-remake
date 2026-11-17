"""Turn the raw channel listing (data/videos.tsv) into an organized curriculum.

Outputs:
  catalog.json   - every video with track, series, era
  CURRICULUM.md  - tracks in learning order, series collapsed into remake units
"""
import csv
import json
import re
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
FLEEP_ERA_START = 318  # listing is newest-first; rows from here down are the 2011-2015 uploads

# (track id, title, what it covers). Order = suggested learning order.
TRACKS = [
    ("start", "0. Start Here", "Orientation, roadmaps, what to learn in what order"),
    ("foundations", "1. Foundations", "Number bases, C data types, memory, assembly, calling conventions, file formats, Windows internals"),
    ("cheat-engine", "2. Memory Scanning with Cheat Engine", "Scans, value types, pointers, code injection, scripts, tables"),
    ("re-tools", "3. Reverse Engineering Tools", "IDA, Ghidra, x64dbg, OllyDbg, ReClass, radare2, debugging"),
    ("external", "4. External Trainers", "Read/WriteProcessMemory trainers in C++, C#, Python"),
    ("injection", "5. DLL Injection & Shellcode", "LoadLibrary, manual mapping, shellcode execution methods, injectors"),
    ("hooking", "6. Hooking, Pattern Scanning & Calling Functions", "Detours, trampolines, VMT, mid-function hooks, signatures, calling game functions"),
    ("rendering", "7. Rendering: ESP, Overlays & Menus", "View matrix, world-to-screen, D3D/OpenGL hooks, ImGui"),
    ("features", "8. Building Features on Practice Games", "Aimbot math, triggerbot, entity lists, movement - game-by-game walkthroughs"),
    ("engines", "9. Engines & Platforms", "Unity/il2cpp, Unreal, Electron, Java, HTML5, Linux, macOS, Android"),
    ("kernel", "10. Kernel", "Drivers, IOCTL, kernel memory access, WinDbg"),
    ("anticheat", "11. Anti-Cheat & Anti-Debug Internals", "How detection works: integrity checks, thread detection, anti-debug tricks"),
    ("crackme", "12. CrackMes, KeyGens & Unpacking", "Legal RE practice targets, packers, OEP, import fixing"),
    ("malware", "13. Malware Analysis", "Lab setup, triage tools, sample walkthroughs, C2 analysis"),
    ("exploit", "14. Exploit Development", "Buffer overflows, SEH, DEP/ASLR bypass, ROP, fuzzing, CVEs"),
    ("pentest", "15. Pentest & CTF Walkthroughs", "HackTheBox, TryHackMe, picoCTF, privilege escalation"),
    ("misc", "16. Off-Topic & Channel", "Game dev, server admin, podcasts, news - not part of the curriculum"),
]

# First match wins, so specific rules go before general ones.
RULES = [
    ("misc", r"dark ?gdk|darkbasic|fps game|super mario|centmin|xenforo|mailcow|tinyproxy|cloudflare|cfautouam|"
             r"what's new|podcast|interview|unbanned|soundtrack|google doodle|lastpass|solzipper|git repos|"
             r"best of fleep|meet rake|why i quit|teaser|virus as a prank|presentation|gameplay|ddos"),
    ("start", r"how to learn game hacking|series introduction|course intro|squally - the game"),
    ("pentest", r"hackthebox|tryhackme|htb |picoctf|cron jobs|web shell|oscp|defcon"),
    ("exploit", r"exploit|buffer overflow|fuzz|vuln|rop decoder|egg hunter|aslr|patch diffing"),
    ("malware", r"malware|ransomware|stealer|yara|cyberchef|binary refinery|c2 |redline|lockbit|crypter|"
                r"sysinternals|capev2|klbanker|vkeylogger|clipper|blacknet|youhacker|hacker vs\. hacker|"
                r"file types|skid"),
    ("crackme", r"crackme|keygen|key generator|unpack|file patcher|z3 explained|codedefender"),
    ("anticheat", r"anti-?cheat|anti-debug|integrity checks|undetected|hwid|detect threads|return address spoofing|"
                  r"hide process"),
    ("kernel", r"kernel|windbg|interrupt descriptor|mmcopyvirtualmemory"),
    ("foundations", r"c programming"),
    ("engines", r"unity|il2cpp|unreal|electron|java |javascript|html5|linux|macos|rust-lang|frida|android|pince"),
    ("foundations", r"data types in c|low level c|arrays in c|stack pointers|calling conventions|learn assembly|"
                    r"pe file format|elf file|windows api|virtual memory|virtual address|windows internals|"
                    r"base systems|hex edit|edit assembly|memory editing|multi ?level pointers in depth|"
                    r"ntqueryinformationprocess|winsock|c programming|run as administrator|operating syst"),
    ("cheat-engine", r"cheat engine|pointer scan|ghs?\d{3}|struct dissector|witcher"),
    ("re-tools", r"ida pro|ghidra|x64dbg|x32dbg|ollydbg|reclass|radare|r2pipe|classinformer|visual studio debugger|"
                 r"practical reverse engineering|reverse engineer with|bindiff|lost source code"),
    ("injection", r"dll inject|inject a dll|injector|manual map|shellcode|sideload|interpreter injection"),
    ("hooking", r"hook functions|detour|trampoline|mid function|vtable|vmt|pattern scan|signature|call game functions|"
                r"__thiscall|offset dumper|netvar|createinterface|find offsets|entity list finder"),
    ("rendering", r"esp|imgui|directx|direct3d|d3d9|opengl|view ?matrix|chams|wallhack|overlay|crosshair|glow"),
    ("external", r"trainer|external|memory library|memory\.dll|python game hacking|build your own cheat engine"),
    ("features", r"aimbot|triggerbot|trigger bot|bunny ?hop|rcs|recoil|rapid fire|traceray|traceline|tibia|skyrim|"
                 r"entitylist|dormant|fly ?hack|noclip|one hit|outlast|blackwater|call of duty|modern warfare|"
                 r"cod hacks|pixel bot|minesweeper|hack any game|flash|radar|openarena|assault ?cube"),
]
COMPILED = [(t, re.compile(p, re.I)) for t, p in RULES]

# Multi-part series whose part titles are too inconsistent for series_key() to line up.
# (title regex, unit name, track). Checked before RULES, and keeps every part in one track.
# Numbered *courses* with a distinct topic per video (CS420, GH1xx/2xx, Exploit Dev N) are
# deliberately not listed: each video there is its own remake unit.
SERIES = [
    (r"c# aimbot tutorial|aimbot tutorial in c#", "C# Aimbot Tutorial", "features"),
    (r"skyrim (mods|hacks|cheats) part", "C++ Skyrim Hacks", "features"),
    (r"shellcode (injection )?tutorial part", "C++ Shellcode Injection Tutorial", "injection"),
    (r"cheat engine tutorial.*\b[123]/3", "Cheat Engine Tutorial Guide (built-in tutorial walkthrough)", "cheat-engine"),
    (r"mmcopyvirtualmemory", "Kernel Read/Write Memory with MmCopyVirtualMemory", "kernel"),
    (r"picoctf 2019", "picoCTF 2019 Buffer Overflows", "pentest"),
    (r"tibia.*\b[123]/3", "Tibia Packet Reverse Engineering & Bot", "features"),
    (r"iamismael", "Buffer Overflow Tutorial (Vuln Server)", "exploit"),
    (r"c programming tutorial for linux", "C Programming Tutorial for Linux", "foundations"),
    (r"triggerbot tutorial external", "CSGO External Triggerbot Tutorial", "external"),
    (r"cody's c\+\+ csgo bunnyhop", "CSGO Bunnyhop Tutorial (External + Internal)", "features"),
    (r"esp (cheat )?tutorial c\+\+ pt", "Counter Strike ESP Tutorial C++", "rendering"),
    (r"triggerbot.*\b\d/6", "Memory TriggerBot Tutorial C++", "features"),
    (r"triggerbot.*\b\d/7", "TriggerBot Tutorial C++ (Any Game)", "features"),
    (r"bunny hop.*\b\d/4", "Bunny Hop Tutorial C++", "features"),
    (r"color aimbot tutorial", "Color Aimbot Tutorial C++", "features"),
    (r"rapid fire.*\bp\d", "Call of Duty 4 Rapid Fire Tutorial", "features"),
    (r"super mario.*dark ?gdk \d", "Super Mario Dark GDK Tutorial", "misc"),
    (r"fps game design tutorial", "C++ FPS Game Design Tutorial", "misc"),
    (r"centmin ?mod tutorial", "CentMinMod Tutorial", "misc"),
    (r"manual mapping dll injection tutorial", "Manual Mapping DLL Injection Tutorial", "injection"),
    (r"pattern scanning tutorial pt", "Signature / Pattern Scanning Tutorial C++", "hooking"),
    (r"csgo glow ?hack tutorial", "External CSGO Glow Hack Tutorial", "rendering"),
    (r"call game functions tutorial|__thiscall functions", "How To Call Game Functions (x64dbg & C++)", "hooking"),
    (r"ollydbg", "Hacking Games with OllyDbg", "re-tools"),
    (r"practical reverse engineering", "Practical Reverse Engineering Exercises", "re-tools"),
    (r"practical malware analysis", "Practical Malware Analysis Labs", "malware"),
    (r"ziggy'?s? keygenme", "Ziggy KeyGenMe", "crackme"),
    (r"youhacker", "YouHacker Python Malware Analysis", "malware"),
    (r"hack(ing)? electron games", "Hacking Electron Games", "engines"),
    (r"hack any game tutorial (pt )?[1-7]\b", "How to Hack Any Game 1-7: Pointers & External Trainer", "external"),
    (r"hack any game tutorial (8|9|1\d)\b", "How to Hack Any Game 8-17: DLL Injection", "injection"),
]
SERIES_COMPILED = [(re.compile(p, re.I), n, t) for p, n, t in SERIES]

PART_PATTERNS = [
    r"\bp(?:ar)?t\.?\s*#?\s*\d+(\s*(/|of)\s*\d+)?",   # Pt 3/6, Part 2, Part#14, Pt.3
    r"\b\d+\s*(/|of)\s*\d+\b",                          # 3/6, 4of4
    r"\btutorial\s+\d+\s*-.*$",                         # "Tutorial 9 - DLL Injection 2"
    r"\b(lesson|exercise|chapter|lab)\s+\S+.*$",
    r"\bp\d\b",
    r"\[[^\]]*\]|\bhd\b",
    r"[^\w\s+#]",                                       # emoji / punctuation
]


def classify(title: str) -> str:
    for track, rx in COMPILED:
        if rx.search(title):
            return track
    return "misc"


def named_series(title: str):
    for rx, name, track in SERIES_COMPILED:
        if rx.search(title):
            return name, track
    return None


def series_key(title: str) -> str:
    s = title.lower()
    for p in PART_PATTERNS:
        s = re.sub(p, " ", s, flags=re.I)
    s = re.sub(r"\b\d+\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def to_int(v: str) -> int:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return 0


def load():
    rows = []
    with open(ROOT / "data" / "videos.tsv", encoding="utf-8-sig", newline="") as f:
        for i, r in enumerate(csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE), start=1):
            if len(r) < 4:
                continue
            vid, title, dur, views = r[0], r[1], to_int(r[2]), to_int(r[3])
            named = named_series(title)
            rows.append({
                "id": vid,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={vid}",
                "duration_s": dur,
                "views": views,
                "recency_rank": i,
                "era": "legacy-2011-2015" if i >= FLEEP_ERA_START else "modern",
                "track": named[1] if named else classify(title),
                "series": named[0] if named else series_key(title),
                "series_named": bool(named),
            })
    return rows


def fmt_dur(s: int) -> str:
    h, m = divmod(round(s / 60), 60)
    return f"{h}h{m:02d}m" if h else f"{m}m"


def fmt_views(n: int) -> str:
    return f"{n / 1000:.0f}k" if n >= 1000 else str(n)


def main():
    videos = load()
    (ROOT / "catalog.json").write_text(json.dumps(videos, indent=1, ensure_ascii=False), encoding="utf-8")

    by_track = defaultdict(list)
    for v in videos:
        by_track[v["track"]].append(v)

    out = ["# Curriculum map", "",
           f"{len(videos)} source videos, {fmt_dur(sum(v['duration_s'] for v in videos))} total runtime. "
           "Generated by `build_catalog.py` - edit the rules there, not this file.", "",
           "Each row is one **remake unit**: a multi-part series is collapsed into a single lesson. "
           "Views are summed across parts and are the best available signal of demand. "
           "`legacy` = uploaded 2011-2015 (old toolchains, 15-minute chunks) - the strongest remake candidates.", ""]

    for tid, name, blurb in TRACKS:
        vids = by_track.get(tid, [])
        units = OrderedDict()
        for v in vids:
            units.setdefault(v["series"], []).append(v)
        rows = []
        for parts in units.values():
            parts.sort(key=lambda v: -v["recency_rank"])  # oldest (part 1) first
            rows.append({
                "title": parts[0]["series"] if parts[0]["series_named"] else parts[0]["title"],
                "parts": len(parts),
                "dur": sum(p["duration_s"] for p in parts),
                "views": sum(p["views"] for p in parts),
                "legacy": all(p["era"].startswith("legacy") for p in parts),
                "url": parts[0]["url"],
            })
        rows.sort(key=lambda r: -r["views"])
        out += [f"## {name}", "", f"_{blurb}_ - {len(vids)} videos, {len(rows)} units, "
                f"{fmt_dur(sum(r['dur'] for r in rows))}", "",
                "| Unit (links to first part) | Parts | Runtime | Views | Era |", "|---|---:|---:|---:|---|"]
        for r in rows:
            title = r["title"].replace("|", "/")
            out.append(f"| [{title}]({r['url']}) | {r['parts']} | {fmt_dur(r['dur'])} | "
                       f"{fmt_views(r['views'])} | {'legacy' if r['legacy'] else ''} |")
        out.append("")

    (ROOT / "CURRICULUM.md").write_text("\n".join(out), encoding="utf-8")
    for tid, name, _ in TRACKS:
        print(f"{len(by_track.get(tid, [])):4d}  {name}")


if __name__ == "__main__":
    main()
