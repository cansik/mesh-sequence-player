import time


class FPSCounter:
    def __init__(self):
        self.fps = 0.0
        self._last_timestamp = self._millis()

    @staticmethod
    def _millis():
        return time.time() * 1000.0

    def reset(self):
        self._last_timestamp = self._millis()

    def update(self):
        ts = self._millis()
        delta = ts - self._last_timestamp
        self.fps = 1000.0 / delta
        self._last_timestamp = ts
