#!/bin/bash
# Episode 7: launch AssaultCube windowed, offline (same home dir as run_ac.sh).
#   ep07_run_ac.sh            the game's default start: an empty map, no bots
#   ep07_run_ac.sh bots [A|B] try to start a bot team deathmatch (see lab/README.md for what worked)
cd "/c/Program Files (x86)/AssaultCube 1.3.0.2"
HOOK="addnbot 1 RVSF bad; addnbot 2 CLA bad"
if [ "$1" = "bots" ]; then
  case "${2:-A}" in
    A) S="sleep 2500 [ addOnLoadOnce [ $HOOK ]; mode 7; loadmap ac_desert ]" ;;
    B) S="mode 7; sleep 100 [ addOnLoadOnce [ $HOOK ] ]" ;;
    C) S="sleep 2500 [ mode 7; loadmap ac_desert; sleep 3000 [ $HOOK ] ]" ;;
  esac
else
  S="sleep 10 [ ]"
fi
bin_win32/ac_client.exe "--home=D:\AI\gh-remake\lab\ac-home" --init -t0 -w1280 -h720 "-e$S" > /d/AI/gh-remake/lab/ac.log 2>&1 &
