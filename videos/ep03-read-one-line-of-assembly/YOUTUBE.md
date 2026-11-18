# YouTube package: Game Hacking from Scratch #3

**Title:** The One Line of Assembly That Takes Your Ammo (Game Hacking from Scratch #3)

**Thumbnail:** `thumbnail.png`

**Description:**

Game Hacking from Scratch, Episode 3. Every shot takes one round from your magazine, and one instruction in the game does it: dec [eax]. This episode finds that instruction in a real open-source game running offline, reads it part by part, and then follows a function call on the stack: where the arguments go, where the return address sits, and how 32-bit and 64-bit code differ.

📚 IN THIS EPISODE
✅ Assembly is machine code written as text: instruction, destination, source
✅ Registers, and why [register + offset] is a field of an object
✅ Cheat Engine: find out what writes to an address, and what reads it
✅ Reading real game code in the disassembler: address, bytes, text
✅ cmp and conditional jumps: what an if looks like
✅ The stack: push, pop, esp, call, ret and the return address
✅ Arguments in 32-bit code: cdecl in our own listing; thiscall in our listing and in the game
✅ 64-bit Windows: the first four arguments travel in rcx, rdx, r8, r9

🧪 PRACTICE
Compile calls.cpp with /FA, find the instruction that writes the health in calls.asm, then add a field and predict the new offset. The video reads the 32-bit listing: run cl in the "x86 Native Tools Command Prompt for VS". In the 64-bit prompt the listing looks like the 64-bit part of the video instead.
https://github.com/strimpel1/gh-remake/blob/main/videos/ep03-read-one-line-of-assembly/lab/calls.cpp

🛠️ TOOLS IN THIS EPISODE (all free)
• AssaultCube 1.3.0.2, open-source shooter, offline: https://assault.cubers.net
• Cheat Engine, open-source memory scanner and debugger: https://github.com/cheat-engine/cheat-engine
• Microsoft C++ compiler (cl) from Visual Studio Community: https://visualstudio.microsoft.com/vs/community/

⚠️ THE ONE RULE
Everything in this series is practiced on open-source games, offline, against bots, and on programs we wrote ourselves. Never on online games, never against other players. In this episode we only read code; nothing is changed.

⏱️ CHAPTERS
0:00 One shot, one instruction
0:29 Machine code written as text
0:42 Our own program and its listing
1:09 Registers
1:25 Instruction, destination, source
1:38 Brackets mean memory
2:07 Live: what writes to the ammo
2:38 Reading dec [eax]
3:15 The game's code in the disassembler
3:48 What reads the health
4:05 Compare and jump
4:49 The stack
5:05 A breakpoint in the game
5:36 Call, ret and the return address
6:07 Arguments on the stack: cdecl
6:39 Methods: thiscall
7:30 64-bit Windows
8:04 Recap and practice

▶️ New to C++? Start with the full C++ course on this channel.
🤖 Created with AI assistance.

#gamehacking #reverseengineering #cheatengine #assembly #cpp

**Tags:** game hacking, reverse engineering, cheat engine, assembly, x86 assembly, reading assembly, registers, the stack, calling conventions, cdecl, thiscall, disassembler, assaultcube, c++, low level programming
