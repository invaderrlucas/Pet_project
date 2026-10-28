import sys, time, wave
import numpy as np
import pyaudio
from openwakeword.model import Model

RATE, CHUNK = 16000, 1280
audio = pyaudio.PyAudio()

print("Input devices:")
for i in range(audio.get_device_count()):
    d = audio.get_device_info_by_index(i)
    if d["maxInputChannels"] > 0:
        print(f"  {i}: {d['name']}  ({int(d['defaultSampleRate'])} Hz)")

dev = int(sys.argv[1]) if len(sys.argv) > 1 else None
print(f"\nUsing device: {dev if dev is not None else 'default'}")
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK, input_device_index=dev)

# 1) record 3 seconds so you can hear what the program hears
print("Recording 3 s test clip, say something...")
frames = [stream.read(CHUNK, exception_on_overflow=False) for _ in range(int(3 * RATE / CHUNK))]
with wave.open("mic_test.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(b"".join(frames))
print("Saved mic_test.wav (play it with: aplay mic_test.wav)\n")

# 2) live wake word scores
model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")
print("Now say 'hey Jarvis' a few times. Ctrl+C to stop.")
peak, t0 = 0.0, time.time()
try:
    while True:
        frame = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        score = max(model.predict(frame).values())
        vol = np.sqrt(np.mean(frame.astype(np.float32) ** 2))
        peak = max(peak, score)
        if time.time() - t0 > 0.5:
            print(f"vol {vol:6.0f}   score {score:.2f}   peak so far {peak:.2f}")
            t0 = time.time()
        if score > 0.5:
            print(f">>> DETECTED ({score:.2f})")
except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream(); stream.close(); audio.terminate()