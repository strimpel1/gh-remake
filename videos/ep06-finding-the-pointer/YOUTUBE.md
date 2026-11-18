# YouTube package: Game Hacking from Scratch #6

**Title:** How to Find a Pointer in a Game You Have Never Seen (Game Hacking from Scratch #6)

**Thumbnail:** `thumbnail.png`

**Description:**

Game Hacking from Scratch, Episode 6. The address a memory scan finds is dead after one restart. This episode finds the pointer that survives: by hand, by following the game's own code with Cheat Engine's "Find out what writes to this address", and automatically, with a pointer scan. Then it saves the result in a cheat table and puts it on a hotkey. Everything is shown on a real open-source game running offline, over three restarts.

📚 IN THIS EPISODE
✅ Find out what writes to / accesses an address, and what More information tells you
✅ Reading the offset and the register out of one instruction
✅ Scanning for an address in hex to find who points at it
✅ Green addresses: what "static" means in Cheat Engine
✅ Add Address Manually with Pointer: base at the bottom, offsets bottom-up
✅ Pointer scan and Rescan memory: from 4196 paths to 392 after one restart
✅ Manual or automatic: when to use which
✅ Cheat tables: names, headers, the .CT file as plain XML, loading it in a new run
✅ Hotkeys: one key that sets the ammo back to 20

🧪 PRACTICE
Compile vault.cpp, find its coins, find the pointer, save a table, restart, and see it still work. Press t and the program tells you the right answer:
https://github.com/strimpel1/gh-remake/blob/main/videos/ep06-finding-the-pointer/lab/vault.cpp

🛠️ TOOLS IN THIS EPISODE (all free)
• AssaultCube 1.3.0.2, open-source shooter, offline: https://assault.cubers.net
• Cheat Engine, open-source memory scanner: https://github.com/cheat-engine/cheat-engine
• A C++ compiler for the practice program (MSVC in the episode)

⚠️ THE ONE RULE
Everything in this series is practiced on open-source games, offline and single player, and on programs we wrote ourselves. Never on online games, never against other players.

⏱️ CHAPTERS
0:00 The address that dies
0:44 Let the game's code show the way
0:57 Find out what writes to this address
1:24 More information: one line up
2:02 Scan for the address itself
2:32 One level up: what accesses it
3:20 The green, static address
3:48 The whole chain
4:04 Add Address Manually: Pointer
4:41 The test: restart the game
4:59 The automatic way: Pointer scan
5:32 Rescan memory after a restart
6:11 Manual or automatic?
6:26 Cheat tables and the .CT file
7:04 Loading the table in a new run
7:22 Hotkeys
8:00 Recap and practice
8:41 Next: Changing the Code

▶️ Earlier episodes: #2 explains what a pointer is, #3 reads the instruction used here, #5 finds the address with a scan.
🤖 Created with AI assistance.

#gamehacking #reverseengineering #cheatengine #cpp #programming

**Tags:** game hacking, reverse engineering, cheat engine, pointer, pointer scan, pointer chain, cheat table, hotkeys, find what writes to this address, static address, memory scanning, assaultcube, c++, low level programming
