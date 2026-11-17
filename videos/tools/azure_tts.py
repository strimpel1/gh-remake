"""Narration for a video project with Azure Speech, same settings as the PixelCode channel pipeline.

Reads the numbered lines of <project>/SCRIPT.md and writes, per line:
  <project>/assets/voice/NN.wav         48 kHz mono 16-bit
  <project>/assets/voice/NN.words.json  [[word, seconds_from_clip_start], ...]
plus <project>/assets/voice/index.json with each clip's duration.

Key and region come from the environment (AZURE_SPEECH_KEY, AZURE_SPEECH_REGION) or from
gh-remake/.env with those two names. Clips are cached by voice + rate + text.

Run:  python videos/tools/azure_tts.py videos/01-number-bases
"""
import hashlib
import html
import json
import os
import re
import sys
import time
import wave
from pathlib import Path

VOICE = "en-US-AvaMultilingualNeural"
RATE = "-4%"
ROOT = Path(__file__).resolve().parents[2]  # gh-remake/


def load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    missing = [k for k in ("AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION") if not os.environ.get(k)]
    if missing:
        sys.exit(f"Missing {', '.join(missing)}. Set them in the environment or in {env}.")


def ssml(text):
    return (f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
            f'<voice name="{VOICE}"><prosody rate="{RATE}">{html.escape(text)}</prosody></voice></speak>')


def tts(text, wav_path):
    """Synthesize one line. Returns [[word, seconds], ...]."""
    import azure.cognitiveservices.speech as sdk

    cfg = sdk.SpeechConfig(subscription=os.environ["AZURE_SPEECH_KEY"], region=os.environ["AZURE_SPEECH_REGION"])
    cfg.set_speech_synthesis_output_format(sdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)
    for attempt in range(8):
        words = []
        synth = sdk.SpeechSynthesizer(speech_config=cfg, audio_config=sdk.audio.AudioOutputConfig(filename=str(wav_path)))
        synth.synthesis_word_boundary.connect(
            lambda e: words.append([e.text, round(e.audio_offset / 1e7, 3)])
            if e.boundary_type == sdk.SpeechSynthesisBoundaryType.Word else None)
        res = synth.speak_ssml_async(ssml(text)).get()
        del synth  # releases the file handle
        if res.reason == sdk.ResultReason.SynthesizingAudioCompleted:
            return words
        detail = res.cancellation_details.error_details if res.reason == sdk.ResultReason.Canceled else str(res.reason)
        if "429" in str(detail) or "Timeout" in str(detail):
            time.sleep(2 + attempt * 2)
            continue
        sys.exit(f"Azure Speech failed: {detail}")
    sys.exit("Azure Speech kept throttling; try again later.")


def voice_lines(project, texts):
    """Synthesize (or reuse cached) one clip per text. Returns [{id, duration, words, text}]."""
    load_env()
    out = Path(project) / "assets" / "voice"
    out.mkdir(parents=True, exist_ok=True)
    index = []
    for n, text in enumerate(texts, 1):
        text = text.strip()
        wav = out / f"{n:02d}.wav"
        wj = out / f"{n:02d}.words.json"
        key = hashlib.sha1(f"{VOICE}|{RATE}|{text}".encode()).hexdigest()
        cached = wj.exists() and wav.exists() and json.loads(wj.read_text(encoding="utf-8")).get("key") == key
        if not cached:
            words = tts(text, wav)
            wj.write_text(json.dumps({"key": key, "text": text, "words": words}, ensure_ascii=False, indent=1), encoding="utf-8")
        words = json.loads(wj.read_text(encoding="utf-8"))["words"]
        with wave.open(str(wav)) as w:
            dur = round(w.getnframes() / w.getframerate(), 3)
        index.append({"id": f"{n:02d}", "duration": dur, "words": words, "text": text})
    (out / "index.json").write_text(json.dumps({"voice": VOICE, "rate": RATE,
        "lines": [{k: v for k, v in i.items() if k != "words"} for i in index]}, indent=1), encoding="utf-8")
    return index


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    project = Path(sys.argv[1]).resolve()
    lines = re.findall(r"^(\d+)\.\s+\(([\d.]+)[–-]([\d.]+)\)\s+(.+)$", (project / "SCRIPT.md").read_text(encoding="utf-8"), flags=re.M)
    if not lines:
        sys.exit("No numbered lines found in SCRIPT.md")
    for i in voice_lines(project, [t for _, _, _, t in lines]):
        print(f"{i['id']}  {i['duration']:6.2f}s")


if __name__ == "__main__":
    main()
