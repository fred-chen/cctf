'''
Created on Aug 25, 2018

@author: fred

===============================================================================
'''

import time
import sys
import os
from threading import RLock

g_printlck = RLock()

class Common():
    UNIQIDENTIFIER = "CCTF2018_NO_WAY_OF_DUPLICATION:"
    STEP = 0
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
        elif level == 99:
            pri = "STEP"
        else:
            pri = "UNKNOWN"
        t = time.localtime()
        if pri == "STEP":
            print ("\n\nSTEP %d: %s\n\n" % (cls.STEP, msg))
        else:
            tstr = '%4d-%02d-%02d %02d:%02d:%02d' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
            print ("[" + pri + "]" + "[" + tstr + "]" + "[" + os.path.basename(sys.argv[0]) + ":" + cls.__name__ + "] " + msg)
        sys.stdout.flush()
        g_printlck.release()
    
    @classmethod
    def warn(cls, msg):
        cls.log(msg, 2)

    @classmethod
    def info(cls, msg):
        cls.log(msg, 3)

    @classmethod
    def error(cls, msg):
        cls.log(msg, 1)

    @classmethod
    def critical(cls, msg):
        cls.log(msg, 0)

    @classmethod
    def step(cls, msg):
        Common.STEP += 1
        cls.log(msg, 99)

class lockable():
    def __init__(self):
        self.lck = RLock()
    def lock(self, blocking=1):
        self.lck.acquire(blocking)
    def unlock(self):
        self.lck.release()
