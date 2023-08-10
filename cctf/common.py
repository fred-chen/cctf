"""
Created on Aug 25, 2018

@author: fred

===============================================================================
"""

import datetime
import sys
import os
from threading import RLock

g_printlck = RLock()


class Common:
    """Common class provides some common functions to be used by other classes."""

    UNIQIDENTIFIER = "CCTF2018_NO_WAY_OF_DUPLICATION:"
    step_number = 0

    def log(self, msg, level=3):
        """Log a message to stdout.

        Args:
            msg: the message to be logged.
            level: the level of the message.
                0: critical, 1: error, 2: warning, 3: info, 99: step. Default is 3.
        """

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
        curr_time = datetime.datetime.now()
        if pri == "STEP":
            print(f"\n\nSTEP {self.step_number}: {msg}\n\n")
        else:
            tstr = f"{curr_time:%Y-%m-%d %H:%M:%S}"
            print(
                f"[{pri}]"
                + f"[{tstr}]"
                + f"[{os.path.basename(sys.argv[0])} : {self.__class__.__name__}] "
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


class LockAble:
    """A LockAble object."""

    def __init__(self):
        self.lck = RLock()

    def lock(self, blocking=1):
        """Acquire the lock."""
        self.lck.acquire(blocking)

    def unlock(self):
        """Release the lock."""
        self.lck.release()
