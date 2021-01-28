'''
Created on Aug 25, 2018

@author: fred
'''

from common import common, lockable
import threading
import re

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
        self.shell = None
        self.dur = None
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
        self.cv.acquire()
        while not self._done:
            self.cv.wait(timeout)
        self.cv.release()
    
    def __str__(self):
        out = self.stdout.strip() if len(self.stdout.strip().splitlines()) <= 1 else "\n" + self.stdout.strip()
        err = self.stderr.strip() if len(self.stderr.strip().splitlines()) <= 1 else "\n" + self.stderr.strip()
        cmd = self.cmdline.strip() if len(self.cmdline.strip().splitlines()) <= 1 else "\n" + self.cmdline.strip()
        return u"\n%s\nTARGET  : %s\nCOMMAND : %s\nSTDOUT  : %s\nSTDERR  : %s\nEXIT    : %s\nDURATION: %d ms\n%s\n" % ('-'*60, self.shell.t, cmd, out.decode('utf-8'), err.decode('utf-8'), self.exit.strip(), self.dur, '-'*60)
    
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

    def getlist(self, splitter='\n'):
        self.wait()
        r = None
        try:
            r = self.stdout.strip().split(splitter)
        except:
            r = None
        return r
        
    