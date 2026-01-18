import os


ROOT = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(ROOT, 'assets')
GIF_DIR = os.path.join(ASSETS_DIR, 'gifs')
SOUND_DIR = os.path.join(ASSETS_DIR, 'sounds')
CONFIG_PATH = os.path.join(ASSETS_DIR, 'config.json')


# default filenames
IDLE_GIF = os.path.join(GIF_DIR, 'miku_idle.gif')
WAVE_GIF = os.path.join(GIF_DIR, 'miku_wave.gif')
TALK_GIF = os.path.join(GIF_DIR, 'miku_talk.gif')
SLEEP_GIF = os.path.join(GIF_DIR, 'miku_sleep.gif')
HELLO_SOUND = os.path.join(SOUND_DIR, 'hello.wav')