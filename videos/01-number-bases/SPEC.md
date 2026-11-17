# SPEC — Hex, Decimal & Binary (pilot, storyline A "The Health Bar")

GOAL:    The viewer can look at one hex byte and say "that's two groups of four bits", and knows why memory tools show hex.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps
TIME:    71.5 s x 30 = 2145 frames. Narrated: the voice is the clock (SCRIPT.md). Bed ~100 bpm = 18 frames per beat.
LOOK:    Two worlds, one palette.
         Outside (game): flat-shaded arena, sky #1C7C8A to #0E4A55 radial, floor tiles #14606B / #0F5560, crates #E8B04A with #B9832E shade.
         Inside (memory): graph paper ground #E4F2EC, grid lines #9CCFC0 at 60 px (major, 3 px) and 20 px (minor, 1 px), ink #0B2A30.
         Accent #FF5A1F: only on the byte being followed and the digits made from it. Never decoration.
         Display: League Gothic 400, HUD numerals 300 px, tracking 0. Titles: Archivo Black, 96-120 px, tracking -1%.
         Data: IBM Plex Mono 700, bytes 46 px in the wall, bit cells 150 px, hero digits 420-520 px.
         Medium: printed graph paper and cut tiles. Tiles have a hard 10 px offset shadow #0B2A30 at 100%, no blur. No grain, no vignette.
OBJECTS: HUD (health bar with segmented fill, big numeral, ammo counter, crosshair); memory wall (address column + 16 byte columns per row);
         byte tile (orange square tile, two hex digits); bit cell (square tile holding 0 or 1, place value 8/4/2/1 printed above);
         digit table (bit pattern -> hex digit, 16 rows in two columns of 8).
MOTION:  enter: power3.out 10 frames, tiles are placed (scale 1.15 -> 1, no fade longer than 4 frames); move: power2.inOut 18 frames;
         camera dive/pull-back: expo.inOut 30 frames; stagger between bit cells 3 frames; text never moves after it lands.
SHOTS:   1  f0-195     HUD world. Hero: push toward the numeral 100. Reads "HEALTH 100" (0.3-3s). Bed in; hands off by diving into the digits.
         2  f195-420   Memory wall. Hero: wall scrolls in row by row, then all bytes dim except 64. Reads address 00F8A4A0 row, byte 64 (3-7s). Bed drops out; key ticks on rows.
         3  f420-645   Byte alone. Hero: 64 tile scales to 45% of frame height. Reads "64" then struck "sixty-four", then "= 100" (2-7s). Pop on "= 100".
         4  f645-870   Eight bits. Hero: tile unfolds into 8 bit cells. Reads 0 1 1 0 0 1 0 0 and "1 byte = 8 bits" (1-7s). Tick per cell.
         5  f870-1140  Split. Hero: the row parts in the middle. Reads place values 8 4 2 1, "4+2 = 6", "4 = 4", then "6x16 + 4 = 100" (2-8.5s). Pop on each digit.
         6  f1140-1410 Digit table. Hero: table grows one row per 6 frames. Reads 0000->0 ... 1111->F, A-F rows in accent (1-8.5s). Soft ticks.
         7  f1410-1680 FF. Hero: every cell flips to 1 left to right. Reads F F, "= 255", "the most one byte can hold" (2-8.5s). Impact on FF.
         8  f1680-1920 Pull back to HUD. Hero: camera pulls out of the byte; numeral reads 255, bar overruns its frame. Reads "255" (2.5-7.5s). Bed returns.
         9  f1920-2145 Claim on graph paper. Reads "Hex is the same bits, four at a time." (1-7.5s). Bed ends on a bar line.
BANNED:  spec.md defaults (dark void, glow/neon, glass cards, everything centred, fade-and-slide-up, corner brackets, three cards in a row),
         plus: Matrix-style falling green code, hacker hoodie imagery, terminal-green-on-black, any real game's HUD or logo, decorative binary rain.
QA:      1.5s HUD numeral readable; 10s the 64 is the only accent in the wall; 18s struck "sixty-four" and "= 100" both legible;
         26s eight cells read 01100100; 35s sums agree (6, 4, 100); 44s 16 rows, A-F correct; 53s FF = 255; 61s HUD says 255; 69s claim holds 2 s+.
