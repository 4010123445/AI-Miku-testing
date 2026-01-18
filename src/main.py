from asr_engine import listen
from tts_engine import speak

while True:
    user_input = listen()
    print("You said:", user_input)
    response = "Hello! I heard you say " + user_input
    speak(response)
