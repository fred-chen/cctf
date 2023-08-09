'''
Created on Aug 25, 2018

@author: fred

===============================================================================
'''

from .common import Common, lockable
import threading

class logicunit(Common, lockable, threading.Thread):
    def __init__(self, repeat=1):
        threading.Thread.__init__(self)
        lockable.__init__(self)
        self._repeat = repeat
        self._pause = False
        self._stop = False
        self._cond = threading.Condition()
        self.setDaemon(True)
                
    def start(self, repeat=1):
        self._repeat = repeat
        threading.Thread.start(self)
        
    def init(self):
        pass

    def body(self):
        pass
    
    def final(self):
        pass
    
    def stop(self):
        self.lock()
        self._stop = True
        self.unlock()
        
    def restart(self, repeat=1):
        self.lock()
        self._pause = False
        self._stop = False
        self._repeat = repeat
        self.unlock()
        self.start()
    
    def pause(self):
        self._pause = True
        
    def check(self):
        self._cond.acquire()
        while self._pause:
            self._cond.wait()
        self._cond.release()
    
    def resume(self):
        self._cond.acquire()
        self._pause = False
        self._cond.notifyAll()
        self._cond.release()
        
    def run(self):
        r = self._repeat
        self.init()
        while ( self._repeat == 0 or r > 0 ) and not self._stop:
            self.body()
            self.check()
            r -= 1
        self.final()