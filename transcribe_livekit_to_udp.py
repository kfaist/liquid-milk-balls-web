#!/usr/bin/env python
"""
LiveKit Audio Transcription to UDP (v11 - Remote User Mic)
-----------------------------------------------------------
Connects to LiveKit, captures remote user's audio, transcribes with Whisper,
sends P5 (noun phrase) and P6 (full transcript) to TouchDesigner via UDP.

Usage:
    python transcribe_livekit_to_udp.py --room claymation-live --port 8020
"""

import argparse
import asyncio
import socket
import time
import sys
from typing import List

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
    "noun.artifact": 1.4, "noun.object": 1.4, "noun.natural_object": 1.2,
    "noun.food": 1.2, "noun.animal": 1.2, "noun.plant": 1.0, "noun.body": 1.0,
    "noun.substance": 1.0, "noun.location": 0.9, "noun.person": 0.6,
}


def wn_concreteness(lemma: str) -> float:
    best = 0.0
    for syn in wn.synsets(lemma, pos=wn.NOUN):
        w = LEX_WEIGHTS.get(syn.lexname(), 0.0)
        if w > best:
            best = w
    return best


def choose_concrete_phrase(text: str, stop_words: set, nlp) -> str:
    doc = nlp(text)
    candidates = []
    for chunk in doc.noun_chunks:
        head = chunk.root
        tokens = [t for t in chunk if t.pos_ in {"NOUN", "PROPN", "ADJ"}]
        if not tokens:
            continue
        phrase = " ".join(t.text for t in tokens).strip()
        if not phrase:
            continue
        nouns = [t for t in tokens if t.pos_ in {"NOUN", "PROPN"}]
        score = sum(wn_concreteness(t.lemma_.lower()) for t in nouns)
        candidates.append((score, phrase))
    if not candidates:
        return ""
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


# ============================================
# MAIN
# ============================================
async def main(args):
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
    stop_words = set(stopwords.words("english"))
    print("Step 5: NLP ready!")
    sys.stdout.flush()

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sticky_phrase = ""
    ignore_phrases = {"thank you", "thanks", "bye", "goodbye"}

    # Audio buffer
    audio_buffer: List[np.ndarray] = []
    buffer_sample_rate = 48000
    last_transcribe = time.time()

    async def process_audio_frames(stream: rtc.AudioStream, participant_id: str):
        nonlocal audio_buffer, buffer_sample_rate, last_transcribe, sticky_phrase
        
        print(f"[AUDIO] Processing audio from: {participant_id}")
        sys.stdout.flush()
        
        async for event in stream:
            frame = event.frame
            # Convert bytes to numpy int16
            samples = np.frombuffer(frame.data, dtype=np.int16)
            buffer_sample_rate = frame.sample_rate
            audio_buffer.append(samples)
            
            # Transcribe every N seconds
            now = time.time()
            if now - last_transcribe >= args.window:
                last_transcribe = now
                
                if not audio_buffer:
                    continue
                
                # Combine buffer
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
                
                # Write temp file
                tmp = "temp_livekit.wav"
                try:
                    with sf.SoundFile(tmp, mode="w", samplerate=16000, channels=1, subtype="PCM_16") as f:
                        f.write(audio_float)
                except Exception as e:
                    print(f"Write error: {e}")
                    continue
                
                # Transcribe
                try:
                    result = model.transcribe(tmp, fp16=False, language="en")
                    text = (result.get("text") or "").strip()
                except Exception as e:
                    print(f"Whisper error: {e}")
                    continue
                
                if not text or text.lower() in ignore_phrases:
                    continue
                
                print(f"[P6] {text}")
                sys.stdout.flush()
                
                # Send P6
                try:
                    udp_sock.sendto(f"P6:{text}".encode(), (args.addr, args.port))
                except Exception as e:
                    print(f"UDP P6 error: {e}")
                
                # Send P5
                phrase = choose_concrete_phrase(text, stop_words, nlp)
                if phrase:
                    sticky_phrase = phrase
                if sticky_phrase:
                    print(f"[P5] {sticky_phrase}")
                    sys.stdout.flush()
                    try:
                        udp_sock.sendto(f"P5:{sticky_phrase}".encode(), (args.addr, args.port))
                    except Exception as e:
                        print(f"UDP P5 error: {e}")

    # Generate token
    print("Step 6: Generating token...")
    sys.stdout.flush()
    token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    token.with_identity(f"transcriber-{int(time.time())}")
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
        # Exit when mirror-user leaves to allow fresh restart
        if participant.identity.startswith("mirror-user"):
            print("[EXIT] Mirror user disconnected - exiting for fresh restart")
            sys.exit(0)

    print(f"\nConnecting to LiveKit room '{args.room}'...")
    await room.connect(LIVEKIT_URL, token.to_jwt())
    print(f"Connected! Waiting for audio from remote users...")
    print(f"UDP -> {args.addr}:{args.port}")
    print("Press Ctrl+C to stop.\n")

    # Check existing participants for audio tracks
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
            await asyncio.sleep(1)
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
    parser.add_argument("--window", type=float, default=2.0)
    args = parser.parse_args()
    
    asyncio.run(main(args))
