import pyaudio
import numpy as np
from openwakeword.model import Model


# Use "onnx" if you installed onnxruntime, "tflite" if tflite-runtime worked
model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")

CHUNK = 1280  # 80 ms at 16 kHz
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000,
                    input=True, frames_per_buffer=CHUNK)

#prototype
#while True:
#    frame = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
#    scores = model.predict(frame)
#    for name, score in scores.items():
#        if score > 0.5:
#            print(f"Detected {name} ({score:.2f})")

def wakework_detection() :
    frame = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
    scores = model.predict(frame)
    for name, score in scores.items():
        if score > 0.5:
            print(f"Detected {name} ({score:.2f})")
            return True
    return False
