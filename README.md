# gh-remake

A game-hacking and reverse-engineering curriculum, rebuilt as two things:

- **`site/`**: a Hebrew lesson site. Open `site/index.html`. Lessons are written in `site/_source/<track>/*.md` and built with `python site/_source/build.py`.
- **`videos/`**: short English explainer videos, one folder per lesson. Finished files are in `videos/<name>/renders/*.mp4`.
- **`videos/ep*/`**: *Game Hacking from Scratch*, the long YouTube series (8-10 minutes an episode). Each episode merges two lessons and is built around real captures: an open-source game running offline, Cheat Engine attached to it, and the output of small C++ programs. Renders go to the channel, not the repo.
- **`lab/`**: the capture workflow for those episodes (see `lab/README.md`).

`CURRICULUM.md` maps the 477 source videos into 17 tracks and 306 remake units (`python build_catalog.py` regenerates it from `data/`).

## Watch

The Hebrew site is published at https://strimpel1.github.io/gh-remake/ and each lesson page plays its video.

| Video | File |
|---|---|
| 1. Hex, Decimal & Binary | [mp4](https://strimpel1.github.io/gh-remake/videos/01-number-bases.mp4) |
| 2. Same Bytes, Different Number | [mp4](https://strimpel1.github.io/gh-remake/videos/02-data-types.mp4) |
| 3. Why the Address Changes | [mp4](https://strimpel1.github.io/gh-remake/videos/03-virtual-memory.mp4) |
| 4. Follow the Pointers | [mp4](https://strimpel1.github.io/gh-remake/videos/04-pointer-chains.mp4) |
| 5. Read One Line of Assembly | [mp4](https://strimpel1.github.io/gh-remake/videos/05-reading-assembly.mp4) |
| 6. Edit a Save File, Byte by Byte | [mp4](https://strimpel1.github.io/gh-remake/videos/06-hex-editing.mp4) |
| 7. Where Do the Arguments Go? | [mp4](https://strimpel1.github.io/gh-remake/videos/07-calling-conventions.mp4) |
| 8. What's Inside an EXE | [mp4](https://strimpel1.github.io/gh-remake/videos/08-inside-an-exe.mp4) |

## Game Hacking from Scratch (long episodes)

| Episode | Lessons | Folder |
|---|---|---|
| 1. The Bytes Behind the Health Bar | 1.1 number bases, 1.2 data types | `videos/ep01-bytes-behind-the-health-bar` |
| 2. Why the Address Changes | 1.3 virtual memory, 1.4 pointer chains | `videos/ep02-why-the-address-changes` |

Each episode folder has `build.py` (the scenes), `YOUTUBE.md` (title, description, chapters), `thumbnail.png` and `lab/` (the practice program shown in the episode).

## Making a video

Each video folder has a `build.py` that lists its scenes: narration text, layout and animation. Running it voices the
narration with Azure Speech, sizes every scene to its clip, and writes the HyperFrames project.

```
python videos/02-data-types/build.py
cd videos/02-data-types && npx hyperframes check && npx hyperframes render
```

Narration needs `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION`, in the environment or in a `.env` file at the repo root
(never committed).

Practice targets in the lessons are offline: single-player games, open-source games against bots, and programs you wrote yourself.
