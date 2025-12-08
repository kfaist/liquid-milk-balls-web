#!/usr/bin/env python
"""
LiveKit Audio Transcription to UDP (v12 - FIFO Noun Queue)
-----------------------------------------------------------
Connects to LiveKit, captures remote user's audio, transcribes with Whisper,
extracts concrete/compound nouns with FIFO queue: new→P6, old P6→P5

Features:
- 1.3 sec recording window, 0.4 sec cooldown
- FIFO noun queue (first in, first out)
- Filters silences, "you" hallucinations, Whisper garbage
- Auto-restarts daily at midnight

Usage:
    python transcribe_livekit_to_udp.py --room claymation-live --port 8020
"""

import argparse
import asyncio
import socket
import time
import sys
import datetime
import gc
from typing import List, Optional

import numpy as np
import soundfile as sf

try:
    import torch
    import whisper
except ImportError:
    raise ImportError("pip install torch openai-whisper")

from livekit import rtc, api

try:
    import nltk
    from nltk.corpus import wordnet as wn
    from nltk.corpus import stopwords
except ImportError:
    raise ImportError("pip install nltk")

try:
    import spacy
except ImportError:
    raise ImportError("pip install spacy && python -m spacy download en_core_web_sm")


# ============================================
# LIVEKIT CONFIG
# ============================================
LIVEKIT_URL = "wss://claymation-transcription-l6e51sws.livekit.cloud"
LIVEKIT_API_KEY = "APITw2Yp2Tv3yfg"
LIVEKIT_API_SECRET = "eVYY0UB69XDGLiGzclYuGUhXuVpc8ry3YcazimFryDW"

# ============================================
# TIMING CONFIG
# ============================================
WINDOW_SEC = 2.5      # Recording window - longer for better speech capture
COOLDOWN_SEC = 0.3    # Minimum gap between transcriptions
DAILY_RESTART_HOUR = 4  # Restart at 4 AM daily

# ============================================
# WHISPER HALLUCINATION FILTER
# ============================================
GARBAGE_PHRASES = {
    "you", "thank you", "thanks", "bye", "goodbye",
    "um", "uh", "hmm", "hm", "ah", "oh",
    "thanks for watching", "subscribe", "like and subscribe",
    "music", "applause", "laughter", "silence",
    "photorealistic", "depth-of-field", "depth of field",
    "", " ", "  "
}

def is_garbage(text: str) -> bool:
    """Check if text is Whisper hallucination or garbage"""
    if not text:
        return True
    cleaned = text.lower().strip().rstrip('.!?,')
    if cleaned in GARBAGE_PHRASES:
        return True
    if len(cleaned) < 2:
        return True
    # Single repeated character
    if len(set(cleaned.replace(" ", ""))) <= 1:
        return True
    return False


# ============================================
# NLP SETUP
# ============================================
def download_resources():
    for pkg in ["wordnet", "omw-1.4", "stopwords"]:
        try:
            nltk.data.find(f"corpora/{pkg}")
        except LookupError:
            nltk.download(pkg)
    try:
        spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")


LEX_WEIGHTS = {
    "noun.artifact": 1.5, "noun.object": 1.5, "noun.natural_object": 1.3,
    "noun.food": 1.3, "noun.animal": 1.3, "noun.plant": 1.2, "noun.body": 1.1,
    "noun.substance": 1.1, "noun.location": 1.0, "noun.person": 0.7,
}


def wn_concreteness(lemma: str) -> float:
    """Score how concrete a noun is using WordNet"""
    best = 0.0
    for syn in wn.synsets(lemma, pos=wn.NOUN):
        w = LEX_WEIGHTS.get(syn.lexname(), 0.0)
        if w > best:
            best = w
    return best


def is_compound_noun(phrase: str) -> bool:
    """Check if phrase is a compound noun (2+ words)"""
    words = phrase.split()
    return len(words) >= 2


def extract_best_noun(text: str, nlp) -> Optional[str]:
    """Extract the best concrete or compound noun from text"""
    doc = nlp(text)
    candidates = []
    
    for chunk in doc.noun_chunks:
        tokens = [t for t in chunk if t.pos_ in {"NOUN", "PROPN", "ADJ"}]
        if not tokens:
            continue
        
        phrase = " ".join(t.text for t in tokens).strip().lower()
        if not phrase or is_garbage(phrase):
            continue
        
        # Score: compound nouns get bonus, then concreteness
        nouns = [t for t in tokens if t.pos_ in {"NOUN", "PROPN"}]
        if not nouns:
            continue
            
        concrete_score = sum(wn_concreteness(t.lemma_.lower()) for t in nouns)
        compound_bonus = 1.5 if is_compound_noun(phrase) else 1.0
        
        # Base score of 1.0 for any valid noun phrase (so WordNet unknowns still work)
        final_score = max(1.0, concrete_score) * compound_bonus
        candidates.append((final_score, phrase))
    
    if not candidates:
        return None
    
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


# ============================================
# FIFO NOUN QUEUE
# ============================================
class NounQueue:
    """FIFO queue: new noun → P6, old P6 → P5"""
    def __init__(self):
        self.p5: Optional[str] = None  # Older noun
        self.p6: Optional[str] = None  # Newer noun
    
    def push(self, noun: str) -> tuple:
        """Push new noun, return (p5, p6) to send"""
        if noun == self.p6:
            # Same as current, no change
            return (self.p5, self.p6)
        
        # Shift: P6 → P5, new → P6
        self.p5 = self.p6
        self.p6 = noun
        return (self.p5, self.p6)
    
    def clear(self):
        self.p5 = None
        self.p6 = None


# ============================================
# MAIN
# ============================================
async def main(args):
    start_time = datetime.datetime.now()
    print(f"[START] {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Step 1: Loading Whisper model...")
    sys.stdout.flush()
    
    model = whisper.load_model(args.model)
    if not torch.cuda.is_available():
        model = model.to("cpu")
    print(f"Step 2: Whisper {args.model} loaded!")
    sys.stdout.flush()

    print("Step 3: Downloading NLP resources...")
    sys.stdout.flush()
    download_resources()
    print("Step 4: Loading spaCy...")
    sys.stdout.flush()
    nlp = spacy.load("en_core_web_sm")
    print("Step 5: NLP ready!")
    sys.stdout.flush()

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    noun_queue = NounQueue()

    # Audio buffer
    audio_buffer: List[np.ndarray] = []
    buffer_sample_rate = 48000
    last_transcribe = time.time()
    last_send = 0.0  # For cooldown

    async def process_audio_frames(stream: rtc.AudioStream, participant_id: str):
        nonlocal audio_buffer, buffer_sample_rate, last_transcribe, last_send
        
        print(f"[AUDIO] Processing audio from: {participant_id}")
        sys.stdout.flush()
        
        async for event in stream:
            frame = event.frame
            samples = np.frombuffer(frame.data, dtype=np.int16)
            buffer_sample_rate = frame.sample_rate
            
            # Accumulate audio up to window size, then throw away oldest
            audio_buffer.append(samples)
            # Keep only last ~2.5 seconds of audio (roughly 120 frames at 48kHz)
            if len(audio_buffer) > 120:
                audio_buffer = audio_buffer[-120:]
            
            now = time.time()
            
            # Check recording window
            if now - last_transcribe < WINDOW_SEC:
                continue
            
            # Check cooldown
            if now - last_send < COOLDOWN_SEC:
                continue
                
            last_transcribe = now
            
            if not audio_buffer:
                continue
            
            # Combine and clear buffer
            audio_data = np.concatenate(audio_buffer)
            audio_buffer = []
            
            # Resample to 16kHz for Whisper
            if buffer_sample_rate != 16000:
                ratio = 16000 / buffer_sample_rate
                new_len = int(len(audio_data) * ratio)
                indices = np.linspace(0, len(audio_data) - 1, new_len).astype(int)
                audio_data = audio_data[indices]
            
            # Normalize
            audio_float = audio_data.astype(np.float32) / 32768.0
            
            # Skip if audio too short
            if len(audio_float) < 16000:  # Less than 1 second
                continue
            
            # Show RMS but don't filter
            rms = np.sqrt(np.mean(audio_float ** 2))
            
            # Write temp file
            tmp = "temp_livekit.wav"
            try:
                with sf.SoundFile(tmp, mode="w", samplerate=16000, channels=1, subtype="PCM_16") as f:
                    f.write(audio_float)
            except Exception as e:
                print(f"[ERROR] Write: {e}")
                continue
            
            # Transcribe
            try:
                result = model.transcribe(tmp, fp16=False, language="en")
                text = (result.get("text") or "").strip()
                print(f"[WHISPER] rms={rms:.4f} -> '{text}'")
                sys.stdout.flush()
            except Exception as e:
                print(f"[ERROR] Whisper: {e}")
                continue
            
            # Skip empty
            if not text:
                continue
            
            # Extract concrete/compound noun ONLY
            noun = extract_best_noun(text, nlp)
            print(f"[NOUN] '{text}' -> '{noun}'")
            sys.stdout.flush()
            
            if not noun:
                continue
            
            # Accept compound nouns (2+ words) OR any noun spaCy found
            # (removed strict WordNet check - too many valid nouns missing from WordNet)
            
            print(f"[ACCEPT] {noun}")
            sys.stdout.flush()
            
            # Push to FIFO queue
            p5, p6 = noun_queue.push(noun)
            last_send = time.time()
            
            # Send P6 (current/newer noun) - raw noun only
            if p6:
                print(f"[P6] {p6}")
                sys.stdout.flush()
                try:
                    udp_sock.sendto(f"P6:{p6}".encode(), (args.addr, args.port))
                except Exception as e:
                    print(f"[ERROR] UDP P6: {e}")
            
            # Send P5 (previous/older noun) - raw noun only
            if p5:
                print(f"[P5] {p5}")
                sys.stdout.flush()
                try:
                    udp_sock.sendto(f"P5:{p5}".encode(), (args.addr, args.port))
                except Exception as e:
                    print(f"[ERROR] UDP P5: {e}")
            
            # Periodic garbage collection to prevent memory leak
            gc.collect()

    # Generate token with 24h TTL
    print("Step 6: Generating token...")
    sys.stdout.flush()
    token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    token.with_identity(f"transcriber-{int(time.time())}")
    token.with_ttl(datetime.timedelta(hours=24))
    token.with_grants(api.VideoGrants(
        room_join=True,
        room=args.room,
        can_subscribe=True,
        can_publish=False,
    ))
    print("Step 7: Token generated!")
    sys.stdout.flush()

    room = rtc.Room()
    audio_tasks = []

    @room.on("track_subscribed")
    def on_track_subscribed(track: rtc.Track, publication: rtc.RemoteTrackPublication, participant: rtc.RemoteParticipant):
        print(f"[TRACK] Subscribed: {track.kind} from {participant.identity}")
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            stream = rtc.AudioStream(track)
            task = asyncio.create_task(process_audio_frames(stream, participant.identity))
            audio_tasks.append(task)

    @room.on("track_unsubscribed")
    def on_track_unsubscribed(track: rtc.Track, publication: rtc.RemoteTrackPublication, participant: rtc.RemoteParticipant):
        print(f"[TRACK] Unsubscribed: {track.kind} from {participant.identity}")

    @room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        print(f"[JOIN] {participant.identity}")

    @room.on("participant_disconnected")
    def on_participant_disconnected(participant: rtc.RemoteParticipant):
        print(f"[LEAVE] {participant.identity}")
        if participant.identity.startswith("mirror-user"):
            print("[EXIT] Mirror user disconnected - exiting for fresh restart")
            sys.exit(0)

    @room.on("disconnected")
    def on_room_disconnected():
        print("[ROOM DISCONNECTED] Lost connection to LiveKit room!")
        print("[ROOM DISCONNECTED] Token expired or network issue - restarting...")
        sys.stdout.flush()
        sys.exit(1)

    print(f"\nConnecting to LiveKit room '{args.room}'...")
    print(f"Window: {WINDOW_SEC}s | Cooldown: {COOLDOWN_SEC}s")
    await room.connect(LIVEKIT_URL, token.to_jwt())
    print(f"Connected! Waiting for audio from remote users...")
    print(f"UDP -> {args.addr}:{args.port}")
    print("Press Ctrl+C to stop.\n")

    # Check existing participants
    for participant in room.remote_participants.values():
        print(f"[EXISTING] {participant.identity}")
        for pub in participant.track_publications.values():
            if pub.track and pub.kind == rtc.TrackKind.KIND_AUDIO:
                print(f"  -> Found audio track, subscribing...")
                stream = rtc.AudioStream(pub.track)
                task = asyncio.create_task(process_audio_frames(stream, participant.identity))
                audio_tasks.append(task)

    try:
        while True:
            await asyncio.sleep(60)
            
            # Check for daily restart
            now = datetime.datetime.now()
            if now.hour == DAILY_RESTART_HOUR and now.minute == 0:
                print(f"[DAILY RESTART] {now.strftime('%Y-%m-%d %H:%M:%S')}")
                sys.exit(0)
            
            # Periodic memory cleanup
            gc.collect()
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        for task in audio_tasks:
            task.cancel()
        await room.disconnect()
        udp_sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--room", default="claymation-live")
    parser.add_argument("--addr", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8020)
    parser.add_argument("--model", default="small.en")
    args = parser.parse_args()
    
    asyncio.run(main(args))
