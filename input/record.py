import numpy as np
from faster_whisper import WhisperModel

CHUNK = 1280
RATE = 16000

whisper = WhisperModel("base.en", device="cpu", compute_type="int8")


def record_until_silence(stream, silence_threshold=500, silence_time=5.5,
                         wait_time=5, max_time=15):
    frames = []
    silent_chunks = 0
    heard_speech = False
    chunks_per_second = RATE / CHUNK

    for i in range(int(max_time * chunks_per_second)):
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        frames.append(data)
        volume = np.sqrt(np.mean(data.astype(np.float32) ** 2))

        if volume > silence_threshold:
            heard_speech = True
            silent_chunks = 0
        else:
            silent_chunks += 1

        if heard_speech and silent_chunks >= silence_time * chunks_per_second:
            break
        if not heard_speech and i >= wait_time * chunks_per_second:
            break

    return np.concatenate(frames)


def transcribe(audio):
    audio_float = audio.astype(np.float32) / 32768.0
    segments, _ = whisper.transcribe(audio_float, language="en")
    return " ".join(segment.text for segment in segments).strip()