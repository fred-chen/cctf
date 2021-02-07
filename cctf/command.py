'''
Created on Aug 25, 2018

@author: fred
'''

from common import common, lockable
import threading, time, datetime

class command(common, lockable):
    def __init__(self, cmd, log=True):
        lockable.__init__(self)
        self.stdout = None
        self.stderr = None
        self.exit = None
        self.cmdline = cmd
        self.reserve = ""
        self._done = False
        self.cv = threading.Condition()
        self.shell = None   # command.shell will be assigned by shell object
        self.start = None   # command.start will be filled when the shell actually starts executing it
        self.dur = None     # command.dur will be filled by the shell when it finishes executing it
        self.printlog = log
    
    def done(self):
        return self._done
    
    def setdone(self):
        self.cv.acquire()
        self.lock()
        self._done = True 
        self.unlock()
        self.cv.notifyAll()
        if self.printlog:
            self.cmdlog()
        self.cv.release()
    
    def wait(self, timeout=None):
        start = time.time()
        while not self._done:
            self.cv.acquire()
            self.cv.wait(10)
            self.cv.release()
            dur_wait = time.time() - start
            if dur_wait>=30 and int(dur_wait) % 30 == 0:  # print notification every 30s for long wait command
                msg = "waited for %d secs. CMD : %s\n\n" % (dur_wait, self.cmdline)
                if not self.start:
                    msg = "on target '%s' cmd hasn't started yet. " % (self.shell.t.address) + msg
                else:
                    dur = datetime.datetime.now() - self.start
                    msg = "on target '%s' cmd has run for %d secs. " % (self.shell.t.address, dur.total_seconds()) + msg
                self.log(msg)
            if timeout and dur_wait > timeout:
                break
    
    def __str__(self):
        cmd = self.cmdline.strip() if len(self.cmdline.strip().splitlines()) <= 1 else "\n" + self.cmdline.strip()
        if (self.exit is None):  # command failed to exec
            return u"\n%s\nTARGET  : %s\nSHELL   : %s\nCOMMAND : %s\nSTDOUT  : %s\nSTDERR  : %s\nEXIT    : %s\nDURATION: %d ms\n%s\n" % ('-'*60, self.shell.t, self.shell.id, cmd, None, None, None, self.dur, '-'*60)
        out = self.stdout.strip() if len(self.stdout.strip().splitlines()) <= 1 else "\n" + self.stdout.strip()
        err = self.stderr.strip() if len(self.stderr.strip().splitlines()) <= 1 else "\n" + self.stderr.strip()
        return u"\n%s\nTARGET  : %s\nSHELL   : %s\nCOMMAND : %s\nSTDOUT  : %s\nSTDERR  : %s\nEXIT    : %s\nDURATION: %d ms\n%s\n" % ('-'*60, self.shell.t, self.shell.id, cmd, out.decode('utf-8').replace("\r", ""), err.decode('utf-8').replace("\r", ""), self.exit.strip().replace("\r", ""), self.dur, '-'*60)
    
    def cmdlog(self):
        self.log("%s" % (self))
    
    def succ(self):
        self.wait()
        exitcode = self.exit.strip()
        return exitcode and exitcode.isdigit() and int(exitcode) == 0
    
    def fail(self):
        return not self.succeed()

    def getint(self):
        self.wait()
        r = None
        try:
            r = int(self.stdout.strip())
        except:
            r = None
        return r
            
    def getfloat(self):
        self.wait()
        r = None
        try:
            r = float(self.stdout.strip())
        except:
            r = None
        return r

    def getlist(self, splitter='\r\n'):
        self.wait()
        r = []
        try:
            r = self.stdout.strip().split(splitter) if self.stdout.strip() else []
        except:
            r = []
        return r
        
    