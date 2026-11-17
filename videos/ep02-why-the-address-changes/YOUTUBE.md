# YouTube package: Game Hacking from Scratch #2

**Title:** Why the Health Address Changes Every Restart (Game Hacking from Scratch #2)

**Thumbnail:** `thumbnail.png`

**Description:**

Game Hacking from Scratch, Episode 2. You find the health address, restart the game, and it holds garbage. Nothing broke: the player moved. This episode shows the real memory map of a running game, why the heap moves on every run, and how a pointer chain leads you back to the same value every time.

📚 IN THIS EPISODE
✅ Virtual memory: every process gets its own address space
✅ Reading a real memory map: regions, permissions, sizes
✅ The module and the heap, and which of them moves
✅ Base + offset, and what ASLR changes
✅ A pointer is just a number that holds an address
✅ Pointer chains with real numbers: player, weapon, ammo
✅ The bracket notation, and why a zero pointer means stop

🧪 PRACTICE
Compile where.cpp, run it three times and write down what moves and what stays:
https://github.com/strimpel1/gh-remake/blob/main/videos/ep02-why-the-address-changes/lab/where.cpp

🛠️ TOOLS IN THIS EPISODE (all free)
• AssaultCube 1.3.0.2, open-source shooter, offline: https://assault.cubers.net
• Cheat Engine, open-source memory scanner: https://github.com/cheat-engine/cheat-engine

⚠️ THE ONE RULE
Everything in this series is practiced on open-source games, offline, against bots, and on programs we wrote ourselves. Never on online games, never against other players.

⏱️ CHAPTERS
0:00 The address that stopped working
0:44 Three runs, and virtual memory
1:21 The real memory map
2:02 The heap, and why the player moves
2:27 Proof with a C++ program
2:47 Base, offset and ASLR
3:17 What a pointer is
3:43 The real pointer in memory
4:22 Read, then add
5:09 Pointer chains
5:51 Zero pointers
6:25 Recap and practice

▶️ New to C++? Start with the full C++ course on this channel.
🤖 Created with AI assistance.

#gamehacking #reverseengineering #cheatengine #cpp #programming

**Tags:** game hacking, reverse engineering, cheat engine, virtual memory, pointers, pointer chain, aslr, heap, memory map, assaultcube, c++, low level programming
