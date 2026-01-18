from PyQt6.QtWidgets import QLabel, QMenu, QAction
from PyQt6.QtGui import QMovie, QCursor
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtWidgets import QWidget
from behavior import BehaviorManager
from resources import IDLE_GIF, WAVE_GIF, TALK_GIF, SLEEP_GIF
from tts_engine import TtsEngine



self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
Qt.WindowType.WindowStaysOnTopHint |
Qt.WindowType.Tool)
self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
self.label = QLabel(self)
self.movie = QMovie(IDLE_GIF)
self.label.setMovie(self.movie)
self.movie.start()
self.resize(self.movie.frameRect().size())


self.behavior = BehaviorManager(self)
self.tts = TtsEngine()


# click handling
self.label.mousePressEvent = self.on_click


# right-click context menu
self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
self.customContextMenuRequested.connect(self.open_menu)


# position bottom-right by default
screen = self.screen().availableGeometry()
x = screen.right() - self.width() - 20
y = screen.bottom() - self.height() - 60
self.move(x, y)


# periodic tick for behaviors
self.timer = QTimer()
self.timer.setInterval(1000) # 1s tick
self.timer.timeout.connect(self.behavior.tick)
self.timer.start()


def set_animation(self, gif_path, loop=True):
try:
self.movie.stop()
self.movie = QMovie(gif_path)
if not loop:
self.movie.setLoopCount(1)
self.label.setMovie(self.movie)
self.resize(self.movie.frameRect().size())
self.movie.start()
except Exception as e:
print('Error loading animation:', e)


def on_click(self, event):
# left click wake
if event.button() == Qt.MouseButton.LeftButton:
self.behavior.on_click()
# you can implement drag with middle/left+move if desired


def open_menu(self, pos):
menu = QMenu()
exit_action = QAction('Exit', self)
exit_action.triggered.connect(self.close)
menu.addAction(exit_action)
menu.exec(QCursor.pos())


def say(self, text):
# play tts and switch to talking animation
self.set_animation(TALK_GIF)
self.tts.speak(text)
# return to idle when done (approx)
QTimer.singleShot(2000, lambda: self.set_animation(IDLE_GIF))