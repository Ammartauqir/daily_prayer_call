# AGENTS.md

## Cursor Cloud specific instructions

### Product
Single Python daemon (`daily-adan-player`) meant for a Raspberry Pi: it loads Islamic
prayer times for a hardcoded city (Ingolstadt, Germany), loops every second to find the
next prayer, updates an SH1106 OLED (I2C), and plays `adan2.wav` when a prayer is imminent.
No web app, DB, or CI. Source lives under `src/daily_muslim_adan/`.

### Environment
Python deps live in a virtualenv at `/workspace/venv` (gitignored). The startup update
script provisions it from `requirements.txt`. Use `/workspace/venv/bin/python` (or activate
with `source venv/bin/activate`). System package `libasound2-dev` is required to build
`simpleaudio` and is baked into the VM image.

Note: `requirements.txt` was corrected to match actual imports (`Requests`, `icecream`,
`simpleaudio`, `luma.oled`); the previously listed `playsound`/`pygame` were unused.

### Running the app
`main.py` uses `from handlers...` imports (needs `src/daily_muslim_adan` on the path) while
the handlers resolve data files relative to the repo root (`src/daily_muslim_adan/data/...`).
So run from the repo root with PYTHONPATH set to the package dir:

```
cd /workspace
PYTHONPATH=src/daily_muslim_adan venv/bin/python src/daily_muslim_adan/main.py
```

### Hardware caveats on this cloud VM (not a Raspberry Pi)
- OLED: `handlers/oledhandler.py` opens `/dev/i2c-1` at import time, so importing it (and
  therefore running `main.py` unchanged) fails with `luma.core.error.DeviceNotFoundError`
  off a Pi. This is a hardware requirement, not a bug — do not "fix" it.
- Audio: there is no sound device (`/dev/snd` absent), so `simpleaudio` playback cannot
  produce sound here (it segfaults when opening ALSA). WAV decoding/validation works fine.
- To exercise the core end-to-end without hardware, drive the real handler modules
  (`handlers.prayertimehandler`, `handlers.audiofilehandler`) directly: fetch/compute the
  schedule, find the next prayer, and validate the WAV asset.

### Prayer schedule data
Annual JSON is cached in `src/daily_muslim_adan/data/prayertime_files/` for 2022–2025 only.
For any other year (e.g. the current 2026) `PrayerTimeHandler` downloads it from the Aladhan
API (`https://api.aladhan.com`) on first run, which requires network access.

### Lint / test / build
There is no configured linter, test suite, or CI in this repo. Byte-compile as a sanity
check: `venv/bin/python -m py_compile src/daily_muslim_adan/main.py src/daily_muslim_adan/handlers/*.py`.
Package build (optional): `venv/bin/python -m pip install .` (console script `dailyadan`).
