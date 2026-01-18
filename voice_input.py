import os
import queue
import sounddevice as sd
import vosk
import json

# Load Vosk model (make sure you have it downloaded, e.g., "vosk-model-small-en-us-0.15")
MODEL_PATH = r"C:\desktop_miku\models\vosk-model-small-en-us-0.15"

if not os.path.exists(MODEL_PATH):
    print(f"[Error] Vosk model not found at {MODEL_PATH}. Please download one from:")
    print("https://alphacephei.com/vosk/models and extract it into your project folder.")
    exit(1)

model = vosk.Model(MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    """Collects audio chunks"""
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

def listen():
    """Listens to your microphone until you stop talking."""
    samplerate = 16000  # works best for Vosk
    recognizer = vosk.KaldiRecognizer(model, samplerate)

    print("[Voice] Speak now... (pause to stop)")
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        silence_count = 0
        text = ""

        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text += " " + result.get("text", "")
                silence_count = 0
            else:
                silence_count += 1
                if silence_count > 10:  # stop after ~2 seconds of silence
                    break

    final_result = json.loads(recognizer.FinalResult())
    text += " " + final_result.get("text", "")
    text = text.strip()

    if text:
        return text
    else:
        return "(couldn't understand)"
