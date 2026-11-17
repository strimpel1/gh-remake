# Storylines — Pilot: Hex, Decimal & Binary

Source: `../../site/_source/01-foundations/01-number-bases.md` (own lesson). Every number below comes from it.

**The one idea:** one hex digit is exactly four bits, so two hex digits are exactly one byte. That is why every memory tool shows hex.

**What the viewer remembers:** "Hex isn't a different number. It's the same bits, four at a time."

**Viewer and task:** a beginner opens a memory viewer for the first time, sees a wall of `E8 03 00 00`, and wants to read it.

**Assumptions:** 75–90 s, 16:9 at 1920×1080, English narration plus a quiet music bed. Voice and music sources are not chosen yet: a free local voice if one is available, otherwise a paid HeyGen voice; music from the catalog needs a HeyGen sign-in, otherwise the film ships with voice only.

---

## A. The Health Bar (recommended)

*Device: a moment in someone's play session. Form: an endless zoom.*

A game HUD shows HEALTH 100. The camera dives into the number and lands in the memory behind it, where the same value is the single byte `64`. The film stays on that one byte and reads it three ways, then comes back out to the HUD and changes it.

- **First two seconds:** a full-frame HUD, health bar full, the number `100` large; a hit lands and it ticks to `99`, then the camera starts pushing into the digits.
- **Beats:** HUD takes a hit → dive into the number, wall of hex bytes → "the game doesn't store 100, it stores this" (`64` isolated) → the byte opens into eight bits `0110 0100` → the bits split into two groups of four, each group becomes one hex digit (`6`, `4`) → the 16-row digit table grows one row at a time only as far as needed → same trick on `FF` = `1111 1111` = 255, the most a byte can hold → pull back out: the byte is overwritten with `FF`, the HUD reads 255 → one line: "Hex is the same bits, four at a time."
- **Look:** saturated arcade HUD world on the outside (deep teal ground, chunky condensed display type), a bright graph-paper memory grid on the inside with mono digits; one accent, hot orange, only on the byte being followed.
- **Sound:** light chiptune-leaning bed at ~100 bpm that drops to near silence inside memory and returns on the pull-back; a soft tick on each bit landing, one impact on `FF`.

## B. Three Odometers

*Device: the object is the explanation. Form: one continuous take.*

Three mechanical counters sit on one workbench, geared together: eight binary wheels, three decimal wheels, two hex wheels. They count the same number in step. The camera drifts along the bench and the viewer watches where each one rolls over.

- **First two seconds:** macro shot of counter wheels mid-roll, clicking from 9 to 10 on the decimal counter while the hex one beside it shows `9` → `A`.
- **Beats:** three counters count from 0 together → decimal rolls over at 10, hex keeps going through A–F → push in: the hex wheel turns once for every full cycle of the four binary wheels under it (a visible gear links them) → count runs fast to 100: `0110 0100` / `100` / `64` → runs to 255: binary and hex both hit their last position (`1111 1111`, `FF`) at the same moment, decimal sits at an awkward `255` → the next click overflows binary and hex together → one line on the bench: "Two hex digits. One byte. Exactly."
- **Look:** warm workshop bench under a single lamp, brass and enamel number wheels, engraved labels; type is a stamped grotesque. No screens anywhere.
- **Sound:** no music until 100; mechanical wheel clicks carry the rhythm, a low pulse enters for the run to 255, one heavy clunk on the overflow.

## C. Ten Fingers (the bold one)

*Device: type carries the argument. Form: cut on the beat.*

No objects at all. Giant kinetic type argues the point: you count in tens because of your hands; the machine has two states; hex is the handshake between you. Colour fields flip on every beat and the digits themselves do the acting.

- **First two seconds:** full-frame `10` in black on yellow; the frame flips and the same `10` is captioned "this is sixteen".
- **Beats:** `10` means ten, then two, then sixteen, depending on the base → a screen-filling wall of `0`s and `1`s, unreadable → the wall is cut by vertical rules every four digits → each four-bit block collapses into a single glyph, the wall shrinks to a quarter of its width → `0x3E8` expands in place to `3×256 + 14×16 + 8 = 1000` → three traps flash as struck-through lines (`0x10 ≠ 10`) → final field: "Same bits. Four at a time."
- **Look:** flat poster colour fields (yellow, black, signal red), one heavy condensed sans at huge sizes, mono only for the bit wall.
- **Sound:** driving minimal percussion at ~128 bpm, every cut on a hit; narration is sparse, about half the words of A or B.
