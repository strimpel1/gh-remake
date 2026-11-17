"""Screenshot one window by title into lab/shots (cropped to the window): python gshot.py "AssaultCube" name [--nofront]"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "videos", "tools"))
import capture  # noqa: E402

h = capture.find(sys.argv[1])
if "--nofront" not in sys.argv:
    capture.front(h)
out = sys.argv[2] if os.path.isabs(sys.argv[2]) else os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots", sys.argv[2] + ".png")
print(capture.rect(h))
capture.grab(*capture.rect(h), out)
