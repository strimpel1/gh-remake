# gh-remake

A game-hacking and reverse-engineering curriculum, rebuilt as two things:

- **`site/`**: a Hebrew lesson site. Open `site/index.html`. Lessons are written in `site/_source/<track>/*.md` and built with `python site/_source/build.py`.
- **`videos/`**: short English explainer videos, one folder per lesson. Finished files are in `videos/<name>/renders/*.mp4`.

`CURRICULUM.md` maps the 477 source videos into 17 tracks and 306 remake units (`python build_catalog.py` regenerates it from `data/`).

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
