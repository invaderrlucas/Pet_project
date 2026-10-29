import re
from math import gcd
from pathlib import Path
import numpy as np
import pyaudio
from scipy.signal import resample_poly
from piper import PiperVoice

VOICE_PATH = Path(__file__).parent.parent / "voices" / "en_US-lessac-medium.onnx"

voice = PiperVoice.load(str(VOICE_PATH))
audio = pyaudio.PyAudio()

def pick_output():
    """Prefer PipeWire/Pulse (they handle any rate); otherwise the system default."""
    for i in range(audio.get_device_count()):
        d = audio.get_device_info_by_index(i)
        if d["maxOutputChannels"] > 0 and d["name"].lower() in ("pipewire", "pulse"):
            return i, int(d["defaultSampleRate"])
    d = audio.get_default_output_device_info()
    return d["index"], int(d["defaultSampleRate"])

OUT_INDEX, OUT_RATE = pick_output()
print(f"Speech output: device {OUT_INDEX} at {OUT_RATE} Hz")

def clean_for_speech(text):
    text = re.sub(r"[*#_`~>]", "", text)
    return re.sub(r"\s+", " ", text).strip()

def speak(text):
    text = clean_for_speech(text or "")
    if not text:
        return
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=OUT_RATE,
                         output=True, output_device_index=OUT_INDEX)
    try:
        for chunk in voice.synthesize(text):
            samples = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            if chunk.sample_rate != OUT_RATE:
                # convert Piper's 22,050 Hz to the device's rate (e.g. 48,000 Hz) as earier implementation
                # crashes the program.
                g = gcd(OUT_RATE, chunk.sample_rate)
                samples = resample_poly(samples, OUT_RATE // g, chunk.sample_rate // g)
                samples = np.clip(samples, -32768, 32767).astype(np.int16)
            stream.write(samples.tobytes())
    finally:
        stream.stop_stream()
        stream.close()