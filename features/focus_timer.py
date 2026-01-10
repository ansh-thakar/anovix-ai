from PyQt6.QtCore import QTimer

class FocusTimer:
    def __init__(self, minutes: int, on_finish):
        self.minutes = minutes
        self.on_finish = on_finish
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.finish)

    def start(self):
        milliseconds = self.minutes * 60 * 1000
        self.timer.start(milliseconds)

    def finish(self):
        if callable(self.on_finish):
            self.on_finish()
