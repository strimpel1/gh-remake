# YouTube package: Game Hacking from Scratch #4

**Title:** 9999 Gold With a Hex Editor, and What Is Inside an EXE (Game Hacking from Scratch #4)

**Thumbnail:** `thumbnail.png`

**Description:**

Game Hacking from Scratch, Episode 4. A file on disk is just bytes, the same bytes we have been reading in memory. First we write a tiny game that keeps its state in a 28-byte save file, open that file in a hex editor and type over two bytes: 1000 gold becomes 9999. Then we open an EXE the same way and read what is inside: the MZ and PE headers, the sections, the image base and the import table, and we match them against the memory map from episode 2.

📚 IN THIS EPISODE
✅ Reading a hex editor: offset, bytes, text
✅ A save file is a structure written to disk
✅ Changing a value byte by byte (little endian again)
✅ Why you type over bytes and never insert them
✅ Checksums, compression and encryption in real save files
✅ The PE format: MZ, PE, sections, entry point, image base
✅ Why the memory map is the section table, loaded
✅ From file to process, and the Windows API in the import table

🧪 PRACTICE
Compile savegame.cpp, run it with "new", then set the health to 255 and the name to your own in a hex editor, and load it:
https://github.com/strimpel1/gh-remake/blob/main/videos/ep04-inside-the-files/lab/savegame.cpp

🛠️ TOOLS IN THIS EPISODE (all free)
• ImHex, open-source hex editor: https://github.com/WerWolv/ImHex
• dumpbin, part of the Visual Studio C++ tools (Community edition is free): https://visualstudio.microsoft.com
• AssaultCube 1.3.0.2, open-source shooter, offline (its EXE is only read, never changed): https://assault.cubers.net
• Cheat Engine, open-source memory scanner (here we only read its import table): https://github.com/cheat-engine/cheat-engine

⚠️ THE ONE RULE
Everything in this series is practiced on open-source games, offline, against bots, and on programs we wrote ourselves. Never on online games, never against other players.

⏱️ CHAPTERS
0:00 1000 gold becomes 9999
0:35 A tiny game and its save file
1:01 Reading a hex editor
1:28 The save file, field by field
2:04 Changing the gold byte by byte
2:47 Type over, never insert
3:07 Checksums, compression, encryption
3:23 An EXE is a file too: MZ and PE
4:13 Reading the headers with dumpbin
4:52 Sections and the memory map
5:40 File offset is not memory address
5:53 Where ASLR is decided
6:14 From file to process
7:02 The import table and the Windows API
8:09 Recap and practice

▶️ New to C++? Start with the full C++ course on this channel.
🤖 Created with AI assistance.

#gamehacking #reverseengineering #hexeditor #cpp #programming

**Tags:** game hacking, reverse engineering, hex editor, hex editing, save file, imhex, pe file format, exe file, dumpbin, import table, windows api, assaultcube, c++, low level programming
