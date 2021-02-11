'''
Created on Aug 25, 2018

@author: fred
'''

from common import common, lockable
import threading, time, datetime

class command(common, lockable):
    def __init__(self, cmd, log=True, longrun_report=1800, wait_report=30):
        lockable.__init__(self)
        self.printlog       = log
        self.longrun_report = longrun_report
        self.wait_report    = wait_report
        self.stdout     = None
        self.stderr     = None
        self.exit       = None
        self.cmdline    = cmd
        self.reserve    = ""
        self.screentext = ""       # command.screentext is the stdout and stderr outputed on terminal screen. 
                                   # will be captured every 1 second by shell object.
        self.shell      = None     # command.shell will be assigned by shell object
        self.start      = None     # command.start will be filled when the shell actually starts executing it
        self.dur        = None     # command.dur will be filled by the shell when it finishes executing it
        self._done      = False
        self.cv         = threading.Condition()
    
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
            dur_wait = time.time() - start
            if self.wait_report and dur_wait>=self.wait_report and int(dur_wait) % self.wait_report == 0:  # print notification every 30s by default for long wait command
                msg = "waited for %d secs ... %s" % (dur_wait, self)
                self.log(msg)
            if timeout and dur_wait > timeout:
                break
            self.cv.acquire()
            self.cv.wait(1)
            self.cv.release()
    
    def __str__(self):
        if self._done:
            cmd = self.cmdline.strip() if len(self.cmdline.strip().splitlines()) <= 1 else "\n" + self.cmdline.strip()
            if (self.exit is None):  # command failed to exec
                return u"command failed to execution.\n%s\nTARGET  : %s\nSHELL   : %s\nCOMMAND : %s\nSTDOUT  : %s\nSTDERR  : %s\nEXIT    : %s\nDURATION: %d ms\n%s\n" % ('-'*60, self.shell.t, self.shell.id, cmd, None, None, None, self.dur, '-'*60)
            out = self.stdout.strip() if len(self.stdout.strip().splitlines()) <= 1 else "\n" + self.stdout.strip()
            err = self.stderr.strip() if len(self.stderr.strip().splitlines()) <= 1 else "\n" + self.stderr.strip()
            return u"command finished.\n%s\nTARGET  : %s\nSHELL   : %s\nCOMMAND : %s\nSTDOUT  : %s\nSTDERR  : %s\nEXIT    : %s\nDURATION: %d ms\n%s\n" % ('-'*60, self.shell.t, self.shell.id, cmd, out.decode('utf-8'), err.decode('utf-8'), self.exit.strip(), self.dur, '-'*60)
        elif not self.start:
            return u"command hasn't started yet. target: '%s [shell: %s]'  CMD : %s\n\n" % (self.shell.t.address, self.shell.id, self.cmdline)
        else:
            dur = datetime.datetime.now() - self.start
            return u"\n\n%s COMMAND RUNNING %s\nSCREEN :\n%s\n\nTARGET  : %s [shell: %s]\nRUNTIME : %d secs.\nCMD     : %s\n%s\n\n" % ("."*40, "."*40, self.screentext.strip().decode('utf-8'), self.shell.t.address, self.shell.id, dur.total_seconds(), self.cmdline, "."*97)  
    
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
        
    