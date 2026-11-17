"""Type into the AssaultCube window: python ackeys.py cmd "<cubescript>"  |  python ackeys.py keys "{ESC}"."""
import sys, time
sys.path.insert(0, r"D:\AI\gh-remake\videos\tools")
import capture
from pywinauto.keyboard import send_keys
h = capture.find("AssaultCube")
capture.front(h)
if sys.argv[1] == "cmd":
    send_keys("{ESC}", pause=0.1); time.sleep(0.4)
    send_keys("/", pause=0.1); time.sleep(0.4)
    send_keys(sys.argv[2], with_spaces=True, pause=0.02); time.sleep(0.3)
    send_keys("{ENTER}")
else:
    send_keys(sys.argv[2], pause=0.1)
