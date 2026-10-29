import pyaudio
import numpy as np
from openwakeword.model import Model
def _pipewire_index(direction):
    key = "maxInputChannels" if direction == "input" else "maxOutputChannels"
    for wanted in ("pipewire", "pulse", "default"):
        for i in range(audio.get_device_count()):
            d = audio.get_device_info_by_index(i)
            if d[key] > 0 and d["name"].lower() == wanted:
                return i
    raise RuntimeError(f"No PipeWire {direction} device found")


# Use "onnx" if you installed onnxruntime, "tflite" if tflite-runtime worked
model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")

CHUNK = 1280  # 80 ms at 16 kHz
audio = pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000,
                    input=True, frames_per_buffer=CHUNK,
                    input_device_index=_pipewire_index("input"))

#prototype
#while True:
#    frame = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
#    scores = model.predict(frame)
#    for name, score in scores.items():
#        if score > 0.5:
#            print(f"Detected {name} ({score:.2f})")
def flush_stream():
    #throws the leftover audio that has piled up and flushes it
    available = stream.get_read_available()

    while available >= CHUNK:

        stream.read(CHUNK, exception_on_overflow=False)
        available = stream.get_read_available()

    model.reset()

def wakeword_detection() :
    #scores the audio based on how likely the wakeword was spoken
    frame = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
    scores = model.predict(frame)
    for name, score in scores.items():
        if score > 0.5:
            print(f"Detected {name} ({score:.2f})")
            return True
    return False
