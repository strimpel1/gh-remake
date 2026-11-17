# Review: Hex, Decimal & Binary (pilot)

## Creative calls
- Storyline A, "The Health Bar". Not built: B "Three Odometers", C "Ten Fingers" (see STORYLINES.md).
- Opens on a steady 100 with the bar filling, instead of a hit to 99, so the followed byte stays 64.
- Arena floor is a flat drawn grid, not a 3D plane (the 3D plane hid the HUD during camera zooms).
- Narration: Azure Speech, en-US-AvaMultilingualNeural at -4%, one clip per shot. Every shot is timed to its clip's word timings. Film length 80.4 s.
- No music and no sound effects: no music source was signed in.

## Measured vs looked at
- Measured: `check` passes with no errors and no warnings; narration clip lengths and word offsets come from Azure.
- Looked at: still frames of every shot and every cut. Not watched at full speed.
- Not checked by anyone: how the narration sounds, and whether picture and voice feel in sync on playback.

## Weakest shot
- Shot 6 (digit table): rows 0-9 arrive in two seconds while the voice says "zero to nine"; readable on pause, quick at speed.
- Shot 2 to 3 cut: the zoomed byte and the arriving tile differ slightly in size and place.

## With more time
- A music bed that drops out inside memory and returns on the pull-back; ticks on the bit cells; one impact on FF.
