#!/bin/bash
# Launch AssaultCube windowed, offline, in a bot match (own home dir so nothing touches the user's settings).
cd "/c/Program Files (x86)/AssaultCube 1.3.0.2"
bin_win32/ac_client.exe "--home=D:\AI\gh-remake\lab\ac-home" --init -t0 -w1280 -h720 "-esleep 2500 [ tmp_mode = 8; tmp_botmap = ac_desert; tmp_numbots = ${1:-3}; tmp_botskill = ${2:-bad}; startbotmap ]" > /d/AI/gh-remake/lab/ac.log 2>&1 &
