import random
from PyQt6.QtCore import QObject
from resources import IDLE_GIF, WAVE_GIF, SLEEP_GIF


class BehaviorManager(QObject):
def __init__(self, window):
super().__init__()
self.window = window
self.idle_time = 0
self.state = 'idle' # idle, waving, talking, sleeping


def tick(self):
# called every second
self.idle_time += 1
# small probabilistic behaviors
if self.state == 'idle' and self.idle_time > 8:
if random.random() < 0.15:
self.start_wave()
elif random.random() < 0.05:
self.start_sleep()


def on_click(self):
# user clicked — greet and speak
self.idle_time = 0
self.start_wave()
self.window.say('Hi! I\'m Miku. How can I help you today?')


def start_wave(self):
self.state = 'waving'
self.window.set_animation(WAVE_GIF)
# return to idle after a short while
from PyQt6.QtCore import QTimer
QTimer.singleShot(1500, self.end_wave)


def end_wave(self):
self.state = 'idle'
self.window.set_animation(IDLE_GIF)


def start_sleep(self):
self.state = 'sleeping'
self.window.set_animation(SLEEP_GIF)
from PyQt6.QtCore import QTimer
QTimer.singleShot(5000, self.end_sleep)


def end_sleep(self):
self.state = 'idle'
self.window.set_animation(IDLE_GIF)