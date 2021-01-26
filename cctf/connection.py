'''
Created on Aug 25, 2018

@author: fred
'''

import common
import me
import os, signal
import pty
import re
import select
import time

class connError(BaseException): pass

class connection(common.common, common.lockable):
    """
        common interface of a connection object.
        all specific connection types should implement this interface.
    """    
    def __init__(self, host='127.0.0.1', username=None, password=None, timeout=30, newline='\n'):
        common.lockable.__init__(self)
        self.pty_fd = None
        self.child_pid = None
        self.host = host
        self.timeout = timeout
        self.username = username
        self.password = password
        self.newline = newline
        self.txt = ""
        if not self.connect():
            raise connError, BaseException("Failed to connect to %s" % (host))
            
    def connect(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def reconnect(self):
        self.disconnect()
        self.connect()
    
    def disconnect(self):
        if self.child_pid:
            os.kill(self.child_pid, signal.SIGKILL);
            os.waitpid(self.child_pid, os.WNOHANG)
            self.child_pid = None
            self.pty_fd = None
        
    def _spawn(self, args):
        (pid, fd) = pty.fork()
        if(pid == 0):
            os.execvp(args[0], args)
        else:
            self.child_pid = pid
            self.pty_fd = fd
            
    def read(self, timeout=None):
        self.lock()
        txt = None
        if timeout:
            r = select.select([self.pty_fd], [], [], timeout)
        else:
            r = select.select([self.pty_fd], [], [])
        if r[0]:
            txt = os.read(self.pty_fd, 4096)
            self.txt += txt
        self.unlock()
        return txt
        
    def write(self, txt):
        if not self.connected():
            self.connect()            
        self.lock()
        os.write(self.pty_fd, txt)
        self.unlock()
        
    def nl(self):
        self.write(self.newline)
    
    def waitfor(self, pattern, timeout=0):
        """
            wait for a specific pattern
            return:
                the text with the pattern if success
                None if timeout
        """
        dur = 0
        reg = re.compile(pattern, re.IGNORECASE|re.DOTALL)
        txt = ""
        start = time.time()
        while True:
            t = self.read(1)
            if t: txt += t
            print txt
            m = reg.search(txt)
            if m:
                break
            dur = time.time() - start
            print "dur: %d timeout: %d" % (dur, timeout)
            print "waiting for %s timeout=%d" % (pattern,timeout)
            if timeout and dur > timeout:
                txt = None
                break
        return txt
    
    def inshell(self, timeout=1):
        self.write("stty -echo")
        self.nl()
        self.write("echo CCTF")
        self.nl()
        if not self.waitfor("CCTF", timeout):
            return False
        return True
        
    def login(self):
        if not self.connected():
            return False
        inshell = 0
        needpasswd = 0
        txt = self.waitfor('.+', self.timeout)
        
        if txt and txt.find("password:") >= 0:
            needpasswd = 1
        if needpasswd:
            self.write(self.password)
            self.nl()
            self.waitfor(".+", self.timeout)
        self.write('bash')
        self.nl()
        self.write('stty -echo')
        self.nl()
        self.write('PS1=CCTF2018:')
        self.nl()
        self.waitfor("CCTF2018:", self.timeout)
        self.nl()
        t1 = self.waitfor("CCTF2018:", self.timeout)
#         print "t1: \n'%s'\n" % t1
        self.write('date "+%D"')
        self.nl()
        t2 = self.waitfor("\d{2}/\d{2}/\d{2}", self.timeout)
#         print "t2: \n'%s'\n" % t2
        self.nl()
        self.waitfor("CCTF2018:", self.timeout)
        self.nl()
        self.waitfor("CCTF2018:", self.timeout)
        return True
    
    def printlog(self):
        print (self.txt)
    
    def svcalive(self):
        raise "need implementation..."
    
    def connected(self):
        if not self.svcalive():
            return False
        r = select.select([self.pty_fd], [self.pty_fd], [self.pty_fd])
        if not r[1] or r[2]:
            return False
        if r[0]:
            return True
        if not me.check_pid(self.child_pid):
            return False
        os.waitpid(self.child_pid, os.WNOHANG)
        return True 
        
    def __del__(self):
        if self.child_pid:
            os.kill(self.child_pid, signal.SIGKILL)
            os.waitpid(self.child_pid, os.WNOHANG)