# asr_engine.py
import sounddevice as sd
import queue
import vosk
import json

# Path to your Vosk model
MODEL_PATH = "C:\desktop_miku\models\vosk-model-small-en-us-0.15"

# Initialize recognizer
model = vosk.Model(MODEL_PATH)
rec = vosk.KaldiRecognizer(model, 16000)

# For streaming audio input
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen():
    print("[ASR] Listening... (say something)")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print(f"[You said]: {text}")
                    return text
            else:
                pass  # Partial results ignored for now
