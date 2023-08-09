"""
Created on Aug 25, 2018

@author: fred

===============================================================================

DESCRIPTION
-------------------------------------------------------------------------------
This module provides a command object class to be returned by shell object. The
Command object contains the command line, the output, the error, the exit code,
and the duration of the command. It can be used to track the progress of command
being executed on remote target, or check the result of the command.
"""

import threading
import time
import datetime
from .common import Common, lockable


class Command(Common, lockable):
    """
    Command object is created by shell object, and put into shell's queue to be
    executed.

    Command object is created and returned by 'shell.exe()' method. It contains
    information that can be used to track the progress(done or not done) of the
    associated command, or check the result of the command.
    """

    def __init__(self, cmd, log=True, longrun_report=1800, wait_report=30):
        lockable.__init__(self)
        self.printlog = log
        self.longrun_report = longrun_report
        self.wait_report = wait_report
        self.stdout = None
        self.stderr = None
        self.exit = None
        self.cmdline = cmd
        self.reserve = ""
        # command.screentext is the stdout and stderr outputed on terminal screen.
        self.screentext = ""
        # will be captured every 1 second by shell object.
        self.shell = None  # command.shell will be assigned by shell object
        # command.start will be filled when the shell actually starts executing it
        self.start = None
        self.dur = None  # command.dur will be filled by the shell when it finishes executing it
        self._done = False
        self.cv = threading.Condition()

    def done(self):
        """Return True if the command is done, otherwise return False."""
        return self._done

    def setdone(self):
        """Set the command status to done."""
        self.cv.acquire()
        self.lock()
        self._done = True
        self.unlock()
        self.cv.notifyAll()
        if self.printlog:
            self.cmdlog()
        self.cv.release()

    def wait(self, timeout=None) -> int:
        """Wait for the command to be done.

        Args:
            timeout (int, optional): timeout in seconds. Defaults to None.

        Returns:
            int: the exit code of the command or None if timeout.
        """
        start = time.time()
        while not self._done:
            dur_wait = time.time() - start
            # print notification every 30s by default for long wait command
            if (
                self.wait_report
                and dur_wait >= self.wait_report
                and int(dur_wait) % self.wait_report == 0
            ):
                msg = "waited for %d secs ... %s\n\n" % (dur_wait, self)
                self.log(msg)
            if timeout and dur_wait > timeout:
                break
            self.cv.acquire()
            self.cv.wait(1)
            self.cv.release()
        return int(self.exit.strip()) if self._done else None

    def __str__(self):
        if self._done:
            cmd = (
                self.cmdline.strip()
                if len(self.cmdline.strip().splitlines()) <= 1
                else "\n" + self.cmdline.strip()
            )
            if self.exit is None:  # command failed to exec
                return (
                    "command failed execution.\n%s\nTARGET  : %s\nSHELL   : %s\nCOMMAND : %s\nSTDOUT  : %s\nSTDERR  : %s\nEXIT    : %s\nDURATION: %d ms\n%s\n"
                    % (
                        "-" * 60,
                        self.shell.target,
                        self.shell.shell_id,
                        cmd,
                        None,
                        None,
                        None,
                        self.dur,
                        "-" * 60,
                    )
                )
            out = (
                self.stdout.strip()
                if len(self.stdout.strip().splitlines()) <= 1
                else "\n" + self.stdout.strip()
            )
            err = (
                self.stderr.strip()
                if len(self.stderr.strip().splitlines()) <= 1
                else "\n" + self.stderr.strip()
            )
            return (
                "\n%s COMMAND FININSHED %s\n" % ("=" * 40, "=" * 40)
                + "TARGET  : %s\nSHELL   : %s\nCOMMAND : %s\nSTDOUT  : %s\nSTDERR  : %s\nEXIT    : %s\nDURATION: %d ms\n"
                % (
                    self.shell.target,
                    self.shell.shell_id,
                    cmd,
                    out,
                    err,
                    self.exit.strip(),
                    self.dur,
                )
                + "=" * 99
            )
        if not self.start:
            return (
                "command hasn't started yet. target: '%s [shell: %s]'  CMD : %s\n\n"
                % (self.shell.target.address, self.shell.shell_id, self.cmdline)
            )
        else:
            dur = datetime.datetime.now() - self.start
            return (
                "\n%s COMMAND RUNNING %s\n" % ("." * 40, "." * 40)
                + "SCREEN :\n%s\n\nTARGET  : %s [shell: %s]\nRUNTIME : %d secs.\nCMD     : %s\n"
                % (
                    self.screentext.strip(),
                    self.shell.target,
                    self.shell.shell_id,
                    dur.total_seconds(),
                    self.cmdline,
                )
                + "." * 97
            )

    def cmdlog(self):
        """Log the command object with cmdline, host, exit code, stdout, stderr etc."""
        self.log(f"{self}\n")

    def succ(self) -> bool:
        """Return True if the command exit code is 0, otherwise return False."""
        self.wait()
        exitcode = self.exit.strip()
        return exitcode and exitcode.isdigit() and int(exitcode) == 0

    def fail(self) -> bool:
        """Return True if the command exit code is not 0, otherwise return False."""
        return not self.succ()

    def getint(self) -> int:
        """Return the command stdout as an integer."""
        self.wait()
        result = None
        try:
            result = int(self.stdout.strip())
        except Exception as e:
            result = None
        return result

    def getfloat(self) -> float:
        """Return the the command stdout as a Python float number."""
        self.wait()
        result = None
        try:
            result = float(self.stdout.strip())
        except:
            result = None
        return result

    def getlist(self, splitter="\r\n") -> list:
        """Return the the command stdout in a Python list."""
        self.wait()
        result = []
        try:
            result = self.stdout.strip().split(splitter) if self.stdout.strip() else []
        except:
            result = []
        return result

    def get_stdout(self) -> str:
        """Return the the command stdout as a string."""
        self.wait()
        return self.stdout.strip()

    def get_stderr(self) -> str:
        """Return the the command stderr as a string."""
        self.wait()
        return self.stderr.strip()

    def get_exitcode(self) -> int:
        """Return the the command exit code as an integer."""
        self.wait()
        return int(self.exit.strip())

    def get_cmdline(self) -> str:
        """Return the the command line as a string."""
        return self.cmdline.strip()
