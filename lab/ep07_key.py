"""Send keys with scan codes to the game, then screenshot: python ep07_key.py "ESC DOWN DOWN ENTER t:hello" name"""
import sys, time
sys.path.insert(0, __file__.rsplit("\\", 1)[0])
import ep07_cmd as k
VK = {"ESC": 0x1B, "DOWN": 0x28, "UP": 0x26, "ENTER": 0x0D, "LEFT": 0x25, "RIGHT": 0x27, "TAB": 9, "F1": 0x70, "BACK": 8}
k.c.e.front("game")
time.sleep(0.3)
for w in sys.argv[1].split():
    if w.startswith("t:"):
        k.text(w[2:].replace("_", " "))
    elif w.startswith("w:"):
        time.sleep(float(w[2:]))
    else:
        k.tap(VK[w], hold=0.06)
    time.sleep(0.35)
if len(sys.argv) > 2:
    time.sleep(0.5)
    k.c.e.shot(sys.argv[2], "game")
