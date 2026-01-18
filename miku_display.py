import tts_engine

def update_emotion(emotion):
    """Tell tts_engine to change GIF based on emotion"""
    try:
        tts_engine.show_gif(emotion)
    except Exception as e:
        print(f"[miku_display] Failed to update emotion: {e}")
