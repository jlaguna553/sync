from _libs import *


class ThreadStation(threading.Thread):
    def __init__(self, app, direction):
        threading.Thread.__init__(self)
        self.app = app
        self.pool = direction

    def run(self):
        self.app.data_process(self.pool)

