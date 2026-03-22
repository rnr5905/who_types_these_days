# Voice Dictation

Real-time speech-to-text with multiple backends. Cross-platform (Linux, macOS, Windows).

**Press a hotkey, speak, and text appears where your cursor is.**

## Quick Start

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# Linux: Install system packages (optional but faster)
sudo dnf install xdotool xclip  # Fedora
# sudo apt install xdotool xclip  # Ubuntu/Debian

# 3. Configure
cp .env.example .env
# Edit .env and set your backend and API keys

# 4. Run
python3 main.py
```

## Usage

**Start the recorder:**
```bash
python3 main.py
```

**Toggle recording:**
```bash
python3 main.py --trigger
# or
./trigger.sh
```

**Set up hotkey:**
- **Linux (GNOME):** Settings → Keyboard → Custom Shortcuts → Add
  - Command: `/path/to/tts-realtime/trigger.sh`
  - Shortcut: Press your key combo (e.g., `Ctrl+Space`)

- **macOS:** System Preferences → Keyboard → Shortcuts → Services
  - Or use Automator to create a Service

- **Windows:** Use AutoHotKey or PowerToys Keyboard Manager

## STT Backends

| Backend | Type | Speed | Accuracy | Setup |
|---------|------|-------|----------|-------|
| **vosk** | Local | Medium | Good | None (downloads model) |
| **groq** | Cloud | Fast | Excellent | API key required |
| **deepgram** | Cloud | Fastest | Excellent | API key required |

### Vosk (Local, Offline)
- No API key needed
- Model downloads automatically (~50MB)
- Works offline
- Good for privacy

### Groq (Cloud)
- Free tier available
- Fast Whisper inference
- Get API key: https://console.groq.com

### Deepgram (Cloud)
- $200 free credit (lasts years for personal use)
- Fastest transcription
- Get API key: https://console.deepgram.com

## Configuration

Edit `.env`:

```bash
# STT Backend: vosk, groq, deepgram
STT_BACKEND=deepgram

# API Keys
GROQ_API_KEY=your-key-here
DEEPGRAM_API_KEY=your-key-here

# Recording Limits
MAX_RECORDING_SECONDS=120     # Auto-stop after 2 minutes
COOLDOWN_SECONDS=3            # Cooldown for long recordings
LONG_RECORDING_THRESHOLD=60   # What counts as "long"
```

## Features

- **Hotkey toggle** - Start/stop recording with keyboard shortcut
- **Auto-stop** - Stops after 2 minutes automatically
- **Cooldown** - 3 second cooldown for recordings > 1 minute
- **Clipboard** - Text copied automatically
- **Overlay** - Visual feedback while recording
- **Cross-platform** - Works on Linux, macOS, Windows

## OS-Specific Behavior

| Feature | Linux | macOS | Windows |
|---------|-------|-------|---------|
| Typing | xdotool (fast) | pyautogui | pyautogui |
| Clipboard | xclip | pyperclip | pyperclip |
| Trigger | SIGUSR1 (instant) | File-based | File-based |

Linux uses native tools for best performance. Other OS use Python libraries.

## Project Structure

```
tts-realtime/
├── main.py              # Entry point
├── config.py            # Settings loader
├── recorder.py          # Audio recording
├── overlay.py           # GUI overlay
├── trigger.sh           # Trigger script
├── requirements.txt     # Dependencies
├── .env                 # Your config
├── .env.example         # Config template
├── stt/                 # Speech-to-text backends
│   ├── __init__.py
│   ├── base.py
│   ├── vosk.py
│   ├── groq.py
│   └── deepgram.py
└── utils/               # Utilities
    ├── __init__.py
    ├── platform.py      # OS detection
    └── typing.py        # Cross-platform typing
```

## Troubleshooting

**No audio detected:**
- Check microphone permissions
- Run `python3 -c "import sounddevice; print(sounddevice.query_devices())"`

**Typing not working (Linux):**
- Install: `sudo dnf install xdotool`
- Test: `xdotool type "hello"`

**Clipboard not working (Linux):**
- Install: `sudo dnf install xclip`
- Test: `echo "test" | xclip -selection clipboard`

**Hotkey not triggering:**
- Make sure `main.py` is running
- Check trigger file: `ls /tmp/voice_dictation_trigger`
- Try: `python3 main.py --trigger`

**Import errors:**
- Activate venv: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

## CLI Commands

```bash
python3 main.py              # Start recorder
python3 main.py --trigger    # Toggle recording
python3 main.py --status     # Check if running
python3 main.py --help       # Show help
```

## License

MIT
