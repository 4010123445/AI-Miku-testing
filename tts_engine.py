import requests
import soundfile as sf
import sounddevice as sd
import textwrap
import subprocess
import time
import os

# 🗣️ VOICEVOX local server URL and settings
VOICEVOX_URL = "http://127.0.0.1:50021"
SPEAKER_ID = 1  # 無名トラック

# 🔧 Path to your Voicevox Engine executable (update if needed)
VOICEVOX_PATH = r"C:\Users\Enzo\AppData\Local\Programs\VOICEVOX\vv-engine\run.exe"  # or run.bat if using engine-only

def ensure_voicevox_running():
    """
    Checks if VOICEVOX engine is running, otherwise starts it automatically.
    """
    try:
        requests.get(f"{VOICEVOX_URL}/version", timeout=1)
        print("[TTS] VOICEVOX engine is running..")
        return True
    except Exception:
        print("[TTS] 🚀 Starting VOICEVOX engine...")

        if not os.path.exists(VOICEVOX_PATH):
            print(f"❌ VOICEVOX executable not found at {VOICEVOX_PATH}")
            return False

        # This Will Start Voicevox silently
        subprocess.Popen(
            [VOICEVOX_PATH],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # Wait for it to start up
        for _ in range(15):
            try:
                requests.get(f"{VOICEVOX_URL}/version", timeout=1)
                print("[TTS] ✅ VOICEVOX is ready.")
                return True
            except Exception:
                time.sleep(1)

        print("❌ VOICEVOX failed to start in time.")
        return False


def speak(text, max_chunk=40):
    """
    Generate speech with VOICEVOX and play it in chunks for faster response.
    """
    if not ensure_voicevox_running():
        print("⚠️ Skipping TTS because VOICEVOX could not start.")
        return

    print(f"[TTS] Miku is speaking...")

    # Split text into smaller chunks
    chunks = textwrap.wrap(text, width=max_chunk)

    for chunk in chunks:
        try:
            # 1️⃣ Create audio query for the chunk
            q = requests.post(
                f"{VOICEVOX_URL}/audio_query",
                params={"text": chunk, "speaker": SPEAKER_ID}
            ).json()

            # 2️⃣ Synthesize audio from the query
            r = requests.post(
                f"{VOICEVOX_URL}/synthesis",
                params={"speaker": SPEAKER_ID},
                json=q
            )

            # 3️⃣ Save chunk temporarily
            with open("chunk.wav", "wb") as f:
                f.write(r.content)

            # 4️⃣ Play the chunk
            data, samplerate = sf.read("chunk.wav")
            sd.play(data, samplerate)
            sd.wait()

        except requests.exceptions.RequestException as e:
            print(f"❌ VOICEVOX request failed: {e}")
            return

    print(f"[TTS] Miku said: {text}")
