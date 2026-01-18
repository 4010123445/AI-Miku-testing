import sounddevice as sd
import queue
import vosk
import json

# Path to the Vosk speech recognition model
MODEL_PATH = r"C:\desktop_miku\models\vosk-model-small-en-us-0.15"

# Load the model and initialize recognizer
model = vosk.Model(MODEL_PATH)
rec = vosk.KaldiRecognizer(model, 16000)

# Create a queue to hold audio data
q = queue.Queue()

# Callback function to process audio input
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Function to start listening and transcribing speech
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