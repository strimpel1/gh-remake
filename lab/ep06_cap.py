"""Episode 6 capture helpers: drive Cheat Engine's real windows (any form, not only the main one) with the mouse and
keyboard, through the Lua command channel of lab/ce/ep06.CT, and screenshot or record them.

    python ep06_cap.py lua "<lua code>"        # run Lua in the lab Cheat Engine, print the answer
    python ep06_cap.py forms                   # visible forms: class, caption, rectangle
    python ep06_cap.py comps "<caption part or class>"   # the components of one form (name, class, caption, rectangle)
    python ep06_cap.py shot "<window title part>" name   # screenshot of one window into lab/shots/ep06/name.png
    python ep06_cap.py menu "<caption part or class>"    # menu items of a form (name = caption)

As a module: lua(), crect(form, control), click(), keys(), shot(), fire(), Rec (a screen-rectangle recorder).
Cheat Engine must have been started with lab/ce/start_ce.py lab/ce/ep06.CT. Hold the screen lock while this runs.
"""
import os
import subprocess
import sys
import time

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, "..", "videos", "tools"))
import capture  # noqa: E402
import win32api  # noqa: E402
import win32gui  # noqa: E402
from pywinauto import mouse  # noqa: E402
from pywinauto.keyboard import send_keys  # noqa: E402

RAW = os.path.join(D, "shots", "ep06")
os.makedirs(RAW, exist_ok=True)
CMD, OUT = os.path.join(D, "ce", "cmd.lua"), os.path.join(D, "ce", "cmd.lua.out")

PRELUDE = r"""
function E6F(pat)
  for i = 0, getFormCount() - 1 do
    local f = getForm(i)
    if f.Visible and (((f.Caption or ''):find(pat, 1, true)) or f.ClassName == pat) then return f end
  end
end
function E6R(c)
  local x, y = c.clientToScreen(0, 0)
  return string.format('%d %d %d %d', x, y, c.Width, c.Height)
end
return 'ok'
"""


def lua(code, wait=20):
    if os.path.exists(OUT):
        os.remove(OUT)
    with open(CMD + ".tmp", "w", encoding="utf-8") as f:
        f.write(code)
    os.replace(CMD + ".tmp", CMD)
    t0 = time.time()
    while time.time() - t0 < wait:
        time.sleep(0.1)
        if os.path.exists(OUT):
            time.sleep(0.1)
            return open(OUT, encoding="utf-8", errors="replace").read()
    return "no answer"


def val(code, wait=20):
    """lua() without the leading 'true '; exits on an error."""
    r = lua(code, wait)
    if not r.startswith("true"):
        raise RuntimeError(f"lua failed: {r}\n{code}")
    return r[5:]


def prelude():
    return lua(PRELUDE)


def forms():
    return val("""local s='' for i=0,getFormCount()-1 do local f=getForm(i) if f.Visible then
      s=s..f.ClassName..' | '..tostring(f.Caption)..' | '..E6R(f)..'\\n' end end return s""")


def comps(pat):
    return val(f"""local f=E6F([[{pat}]]) if not f then return 'no form' end local s=f.ClassName..' '..tostring(f.Caption)..'\\n'
      for j=0,f.ComponentCount-1 do local c=f.Component[j]
        local ok,r=pcall(function() return E6R(c) end)
        local ok2,cap=pcall(function() return c.Caption end)
        local ok3,vis=pcall(function() return c.Visible end)
        s=s..c.Name..' : '..c.ClassName..' : '..tostring(ok2 and cap or '')..' : '..tostring(ok and r or '-')..' : '..tostring(ok3 and vis)..'\\n' end return s""")


def crect(form, name):
    """Screen rectangle (x, y, w, h) of a control of the form whose caption contains / class equals `form` ('main' = main form)."""
    f = "getMainForm()" if form == "main" else f"E6F([[{form}]])"
    return [int(v) for v in val(f"return E6R({f}.{name})").split()[:4]]


def glide(x, y, t=0.3, steps=16):
    cx, cy = win32api.GetCursorPos()
    for i in range(1, steps + 1):
        k = i / steps
        k = k * k * (3 - 2 * k)
        win32api.SetCursorPos((int(cx + (x - cx) * k), int(cy + (y - cy) * k)))
        time.sleep(t / steps)


def click(x, y, double=False, button="left"):
    glide(x, y)
    time.sleep(0.15)
    if double:
        mouse.double_click(coords=(x, y))
    else:
        mouse.click(button=button, coords=(x, y))
    time.sleep(0.3)


def cclick(form, name, dx=None, dy=None, **kw):
    x, y, w, h = crect(form, name)
    click(x + (w // 2 if dx is None else dx), y + (h // 2 if dy is None else dy), **kw)


def keys(k, pause=0.08):
    send_keys(k, pause=pause, with_spaces=True)
    time.sleep(0.3)


def hwnd(title):
    if title == "ce":
        return [h for h, t in capture.windows() if t.startswith("Cheat Engine") and capture.rect(h)[2] > 300][0]
    return capture.find({"game": "AssaultCube"}.get(title, title))


def front(title):
    capture.front(hwnd(title))


def shot(name, title, front_first=False):
    h = hwnd(title)
    if front_first:
        capture.front(h)
    out = os.path.join(RAW, name + ".png")
    capture.grab(*capture.rect(h), out)
    return out


def area(name, x, y, w, h):
    capture.grab(x, y, w, h, os.path.join(RAW, name + ".png"))


def move(title, x, y):
    h = hwnd(title)
    l, t, r, b = win32gui.GetWindowRect(h)
    win32gui.MoveWindow(h, x, y, r - l, b - t, True)


def fire(n, gap=0.9):
    g = capture.find("AssaultCube")
    capture.front(g)
    x, y, w, h = capture.rect(g)
    p = (x + w // 2, y + h // 2 - 100)
    for _ in range(n):
        mouse.press(coords=p)
        time.sleep(0.05)
        mouse.release(coords=p)
        time.sleep(gap)


class Rec:
    """with Rec('name', x, y, w, h): ...   records that screen rectangle to lab/shots/ep06/name.mp4"""

    def __init__(self, name, x, y, w, h):
        self.out = os.path.join(RAW, name + ".mp4")
        self.a = (x, y, w // 2 * 2, h // 2 * 2)

    def __enter__(self):
        x, y, w, h = self.a
        self.p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "gdigrab", "-framerate", "30", "-offset_x", str(x), "-offset_y", str(y),
                                   "-video_size", f"{w}x{h}", "-i", "desktop", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
                                   "-pix_fmt", "yuv420p", self.out], stdin=subprocess.PIPE)
        time.sleep(1.5)
        self.t0 = time.time()
        return self

    def __exit__(self, *a):
        print(f"{self.out}: {time.time() - self.t0:.1f}s of actions")
        try:
            self.p.communicate(b"q", timeout=20)
        except Exception:
            self.p.kill()


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "lua":
        print(lua(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 20))
    elif c == "forms":
        prelude()
        print(forms())
    elif c == "comps":
        prelude()
        print(comps(sys.argv[2]))
    elif c == "menu":
        prelude()
        print(val(f"""local f=E6F([[{sys.argv[2]}]]) local s='' for j=0,f.ComponentCount-1 do local c=f.Component[j]
          if c.ClassName=='TMenuItem' then s=s..c.Name..' = '..tostring(c.Caption)..'\\n' end end return s"""))
    elif c == "shot":
        print(shot(sys.argv[3], sys.argv[2], "--front" in sys.argv))
