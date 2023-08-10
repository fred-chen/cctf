"""
Created on Aug 25, 2018

@author: fred

===============================================================================
"""

import threading
from .common import Common, LockAble


class LogicUnit(Common, LockAble, threading.Thread):
    """logicunit is a thread that can be paused, resumed, stopped, and restarted."""

    def __init__(self, repeat=1):
        threading.Thread.__init__(self)
        LockAble.__init__(self)
        self._repeat = repeat
        self._pause = False
        self._stop = False
        self._cond = threading.Condition()
        self.setDaemon(True)

    def start(self, repeat=1):
        self._repeat = repeat
        threading.Thread.start(self)

    def init(self):
        """init() will be called before body() is called."""

    def body(self):
        """body() will be called repeatedly until stop() is called."""

    def final(self):
        """final() will be called after all iterations of body() are finished."""

    def stop(self):
        """stop() will stop the logicunit."""
        self.lock()
        self._stop = True
        self.unlock()

    def restart(self, repeat=1):
        """restart() will restart the logicunit."""
        self.lock()
        self._pause = False
        self._stop = False
        self._repeat = repeat
        self.unlock()
        self.start()

    def pause(self):
        """pause() will pause the logicunit."""
        self._pause = True

    def check(self):
        """check() will be called after each iteration of body() is finished.
        
        check() is used to determine whether to pause the logicunit between each iteration.
        """
        self._cond.acquire()
        while self._pause:
            self._cond.wait()
        self._cond.release()

    def resume(self):
        """resume() will resume the logicunit."""
        self._cond.acquire()
        self._pause = False
        self._cond.notifyAll()
        self._cond.release()

    def run(self):
        repeat = self._repeat
        self.init()
        while (self._repeat == 0 or repeat > 0) and not self._stop:
            self.body()
            self.check()
            repeat -= 1
        self.final()
