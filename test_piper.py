from piper import PiperVoice

model_path = "C:/desktop_miku/models/PiperModels/n_US-amy-medium.onnx"

voice = PiperVoice.load(model_path)

with open("hello.wav", "wb") as f:
    voice.synthesize("Hello, I am Miku!", f)

print("✅ Piper TTS test done! Check hello.wav in your folder.")
