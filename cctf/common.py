'''
Created on Aug 25, 2018

@author: fred
'''

import time
import sys
import os
from threading import RLock

g_printlck = RLock()

class common():
    @classmethod
    def log(cls, msg, level=3):
        g_printlck.acquire()
        if level == 0:
            pri = "CRITICAL"
        elif level == 1:
            pri = "ERROR"
        elif level == 2:
            pri = "WARN"
        elif level == 3:
            pri = "INFO"
        t = time.localtime()
        tstr = '%4d-%02d-%02d %02d:%02d:%02d' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
        print "[" + pri + "]" + "[" + tstr + "]" + "[" + os.path.basename(sys.argv[0]) + ":" + cls.__name__ + "] " + msg
        sys.stdout.flush()
        g_printlck.release()

class lockable():
    def __init__(self):
        self.lck = RLock()
    def lock(self, blocking=1):
        self.lck.acquire(blocking)
    def unlock(self):
        self.lck.release()

