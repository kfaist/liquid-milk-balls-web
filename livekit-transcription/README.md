# LiveKit Audio Transcription for TouchDesigner

Captures **remote web users' microphones** from LiveKit and sends transcriptions to TouchDesigner via UDP.

## Quick Start

1. Double-click `RUN_TRANSCRIPTION.bat`
2. That's it! Script will connect to LiveKit and listen for web users.

## What Gets Sent to TouchDesigner

- **P6**: Full transcript (immediate, every utterance)
- **P5**: Most concrete noun phrase (sticky - persists until replaced)

Both sent via UDP to `127.0.0.1:8020` by default.

## How It Works

```
Web User's Browser (mic)
    → LiveKit "claymation-live" room
    → This script subscribes to audio tracks
    → Whisper transcribes speech
    → UDP packets to TouchDesigner
        P6:Hello this is a test
        P5:test
```

## Custom Settings

```batch
RUN_TRANSCRIPTION.bat [room] [ip] [port] [model]

# Examples:
RUN_TRANSCRIPTION.bat claymation-live 127.0.0.1 8020 small.en
RUN_TRANSCRIPTION.bat my-room 192.168.1.100 9000 tiny.en
```

### Available Whisper Models
- `tiny.en` - Fastest, least accurate (~72MB)
- `base.en` - Fast, decent accuracy (~142MB)
- `small.en` - Good balance (default) (~466MB)
- `medium.en` - More accurate, slower (~1.5GB)
- `large` - Most accurate, slowest (~2.9GB)

## Dependencies

If you get errors, install these:

```bash
pip install livekit torch openai-whisper nltk spacy soundfile numpy
python -m spacy download en_core_web_sm
```

## TouchDesigner Setup

1. Add a **UDP In DAT** node
2. Set Port to `8020`
3. Messages arrive as:
   - `P6:Full sentence here`
   - `P5:noun phrase`

Parse in a **Text DAT** or script to extract the content after the colon.

## LiveKit Configuration

Currently configured for:
- **URL**: `wss://claymation-transcription-l6e51sws.livekit.cloud`
- **Room**: `claymation-live`

To change, edit the constants at the top of `transcribe_livekit_to_udp.py`.
