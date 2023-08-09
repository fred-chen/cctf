"""
Created on Aug 25, 2018

@author: fred

===============================================================================
"""

import time
import sys
import os
from threading import RLock

g_printlck = RLock()


class Common:
    """Common class provides some common functions to be used by other classes."""

    UNIQIDENTIFIER = "CCTF2018_NO_WAY_OF_DUPLICATION:"
    step_number = 0

    def __init__(self) -> None:
        self.step_number = 0

    def log(self, msg, level=3):
        """Log a message to stdout."""

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
            print("\n\nSTEP %d: %s\n\n" % (self.step_number, msg))
        else:
            tstr = "%4d-%02d-%02d %02d:%02d:%02d" % (
                t.tm_year,
                t.tm_mon,
                t.tm_mday,
                t.tm_hour,
                t.tm_min,
                t.tm_sec,
            )
            print(
                "["
                + pri
                + "]"
                + "["
                + tstr
                + "]"
                + "["
                + os.path.basename(sys.argv[0])
                + ":"
                + self.__class__.__name__
                + "] "
                + msg
            )
        sys.stdout.flush()
        g_printlck.release()

    def warn(self, msg):
        """Log a warning message."""
        self.log(msg, 2)

    def info(self, msg):
        """Log an information message."""
        self.log(msg, 3)

    def error(self, msg):
        """Log an error message."""
        self.log(msg, 1)

    def critical(self, msg):
        """Log a critical message."""
        self.log(msg, 0)

    def step(self, msg):
        """Log a step message with the auto-increamental step number."""
        Common.step_number += 1
        self.log(msg, 99)


class lockable:
    """A lockable object."""

    def __init__(self):
        self.lck = RLock()

    def lock(self, blocking=1):
        """Acquire the lock."""
        self.lck.acquire(blocking)

    def unlock(self):
        """Release the lock."""
        self.lck.release()
