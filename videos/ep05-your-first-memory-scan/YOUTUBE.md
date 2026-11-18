# YouTube package: Game Hacking from Scratch #5

**Title:** How to Find a Value in a Game's Memory with Cheat Engine (Game Hacking from Scratch #5)

**Thumbnail:** `thumbnail.png`

**Description:**

Game Hacking from Scratch, Episode 5. Until now every address in this series was handed to you. This is the episode where you find one yourself. A first scan for the ammo counter returns 2,253 addresses; one scan later there are 2, and writing to each tells you which one the game uses. Then the harder case: a health bar with no number at all, found with an unknown initial value scan. Everything is done for real in Cheat Engine, on an open-source game running offline and on a small practice program you can compile yourself.

📚 IN THIS EPISODE
✅ Attaching Cheat Engine to a process, and what the three parts of its window are for
✅ First Scan and Next Scan: 2,253 results, then 2
✅ Telling the address the game uses from one it does not, by writing to each
✅ Changing a value and freezing it, and what a freeze really does
✅ Unknown initial value, then Decreased, Unchanged and Increased: finding a bar with no number
✅ Why a scan finds nothing: 4 Bytes against Float, and Value between
✅ Why the address you found is gone after a restart

🧪 PRACTICE
Compile scanme.cpp and attach Cheat Engine to it. Find the gold (one of the two addresses is a display copy that snaps back), then find the health behind the bar and set it to exactly half:
https://github.com/strimpel1/gh-remake/blob/main/videos/ep05-your-first-memory-scan/lab/scanme.cpp

🛠️ TOOLS IN THIS EPISODE (all free)
• AssaultCube 1.3.0.2, open-source shooter, single player, offline: https://assault.cubers.net
• Cheat Engine 7.7, open-source memory scanner: https://github.com/cheat-engine/cheat-engine
• scanme.cpp, the practice program written for this episode (link above)

⚠️ THE ONE RULE
Everything in this series is practiced on open-source games, offline, and on programs we wrote ourselves. Never on online games, never against other players.

⏱️ CHAPTERS
0:00 2,253 places hold the number 20
0:32 The setup
0:47 Attach to the game
1:01 The three parts of the window
1:31 First Scan
1:50 Change the value, then Next Scan
2:44 New Scan is not Next Scan
2:56 The address list
3:09 Which address is real? Write to it
3:51 Freezing a value
4:29 A bar with no number
5:08 Unknown initial value
6:24 Two rules for unknown values
6:41 When a scan finds nothing
7:34 Which type to try first
7:51 After a restart
8:11 Recap
8:28 Practice

▶️ New to C++? Start with the full C++ course on this channel.
🤖 Created with AI assistance.

#gamehacking #cheatengine #reverseengineering #memoryscanning #cpp

**Tags:** game hacking, cheat engine, cheat engine tutorial, memory scanning, first scan, next scan, unknown initial value, value types, float, reverse engineering, assaultcube, c++, low level programming
