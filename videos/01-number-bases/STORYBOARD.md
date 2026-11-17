---
format: 1920x1080
duration: 80s
message: "Hex is the same bits, four at a time"
arc: Question → Dive → The byte → Bits → Groups of four → Sixteen digits → FF → Payoff → Claim
audience: beginners opening a memory viewer for the first time
mode: collaborative
---

## Frame 1: The health bar (0-8.5s)

- act: Outside, in the game
- status: animated
- src: compositions/hud.html
- duration: 6.5s
- poster: 3s
- transition_in: cut
- scene: A game HUD reads HEALTH 100; the camera starts pushing into the number
- voiceover: "Your health says one hundred. But the game never wrote down a one and two zeros. So what did it store?"
- reads: HEALTH 100 (0.3-3.0s); the push toward the digits (3.0-6.5s)
- sound: bed enters on its strongest bar; no effects

## Frame 2: The wall of bytes (8.5-17.6s)

- act: Inside memory
- status: animated
- src: compositions/wall.html
- duration: 7.5s
- poster: 4.5s
- transition_in: dive through the numeral
- scene: Rows of address plus sixteen byte pairs; everything dims except one orange 64
- voiceover: "Dive into the game's memory and you find rows of this: pairs of digits and letters. One pair is your health."
- reads: rows of pairs arrive (0.5-3.5s); the 64 at 00F8A4AC lights (4.0-7.5s)
- sound: bed drops to near silence; soft key tick per row; pop on the 64

## Frame 3: Six-four, not sixty-four (17.6-27.2s)

- act: Inside memory
- status: animated
- src: compositions/byte.html
- duration: 7.5s
- poster: 4s
- transition_in: the 64 tile scales up out of the wall
- scene: The 64 tile fills the left half; "sixty-four" is struck through; "= 100" prints
- voiceover: "This one. Six-four. Not sixty-four: this is hexadecimal, base sixteen, and it means exactly one hundred."
- reads: 64 (0-1.5s); sixty-four struck (1.5-3.5s); hexadecimal, base 16 (3.5-5.0s); = 100 (5.0-7.5s)
- sound: silence under the voice; pop on "= 100"

## Frame 4: Eight bits (27.2-35.3s)

- act: Inside memory
- status: animated
- src: compositions/bits.html
- duration: 7.5s
- poster: 4.5s
- transition_in: the tile shrinks to the top and unfolds downward
- scene: The 64 tile opens into eight bit cells reading 0 1 1 0 0 1 0 0
- voiceover: "Underneath, it is one byte: eight bits, each a zero or a one. That is all the machine really has."
- reads: eight cells land left to right (1.0-4.0s); "1 byte = 8 bits" (4.0-7.5s)
- sound: one tick per cell, two takes rotated

## Frame 5: Two groups of four (35.3-45.5s)

- act: Inside memory
- status: animated
- src: compositions/split.html
- duration: 9s
- poster: 6s
- transition_in: the same row of cells parts in the middle
- scene: Each group of four gets place values 8 4 2 1 and adds up to one hex digit: 6 and 4
- voiceover: "Now split the eight bits into two groups of four. The first group is worth six. The second is worth four."
- reads: the split and 8 4 2 1 (0.5-2.5s); 4 + 2 gives 6 (2.5-5.0s); 4 gives 4 (5.0-6.5s); 6 x 16 + 4 = 100 (6.5-9.0s)
- sound: pop on each digit landing

## Frame 6: Sixteen digits (45.5-55.4s)

- act: Inside memory
- status: animated
- src: compositions/table.html
- duration: 9s
- poster: 6s
- transition_in: cut on the paper
- scene: A table grows row by row from 0000 to 1111; rows A to F are orange
- voiceover: "Four bits can make sixteen patterns, so you need sixteen digits. Zero to nine, then A through F for ten to fifteen."
- reads: heading (0.3-2.0s); rows 0-9 (2.0-5.5s); rows A-F (5.5-9.0s)
- sound: soft ticks while rows arrive, none after

## Frame 7: FF (55.4-65.1s)

- act: Inside memory
- status: animated
- src: compositions/full.html
- duration: 9s
- poster: 6s
- transition_in: back to the eight cells
- scene: Every cell flips to 1; both digits become F; FF = 255
- voiceover: "Fill every bit with a one and both digits become F. F-F is two hundred fifty-five, the most one byte can hold."
- reads: cells flip to 1 (0.5-3.0s); F F (3.0-5.0s); FF = 255 (5.0-7.0s); the most one byte can hold (7.0-9.0s)
- sound: riser into one impact on FF, the only one in the film

## Frame 8: Back in the game (65.1-72.9s)

- act: Outside, in the game
- status: animated
- src: compositions/back.html
- duration: 8s
- poster: 5s
- transition_in: pull back out through the byte
- scene: The byte at 00F8A4AC now holds FF; the HUD reads 255 and the bar overruns its frame
- voiceover: "So write F-F into that byte, climb back out, and your health reads two hundred fifty-five."
- reads: FF written at 00F8A4AC (0.5-2.5s); HEALTH 255 (2.5-8.0s)
- sound: bed returns in full on the pull-back

## Frame 9: The one idea (72.9-80.4s)

- act: Claim
- status: animated
- src: compositions/claim.html
- duration: 7.5s
- poster: 5s
- transition_in: cut to paper
- scene: 0110 gives 6 and 0100 gives 4 above the line "Hex is the same bits, four at a time."
- voiceover: "Hex is not a different number. It is the same bits, four at a time."
- reads: the two groups and their digits (0.3-2.0s); the line (2.0-7.5s)
- sound: bed ends on a bar line with a short fade
