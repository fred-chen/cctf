'''
Created on Aug 25, 2018

@author: fred
'''

from sys import stderr, stdin
from target import target
import time, subprocess, os, pty

class uxtarget(target):
    """
        unix, linux like targets
        this kind of targets share similar commands
        so it makes sense for them to share a same parent class
    """
    def __init__(self, address, svc='ssh', username='root', password=None, conn=None, timeout=60):
        self.newline = '\n'
        target.__init__(self, address, svc, username, password, conn, timeout)

    def gethostname(self):
        if self.hostname:
            return self.hostname
        co = self.shell.exe("hostname", wait=True, log=False)
        if co.succ():
            self.hostname = co.stdout.strip()
        else:
            self.hostname = self.address
        return self.hostname
    
    def reboot(self, wait=True, log=True):
        if log:
            self.log("rebooting %s" % self.address)
        self.shell.conn.write("reboot")
        self.shell.conn.nl()
        if wait:
            while self.alive():
                time.sleep(0.1)
            self.wait_alive()
    
    def shutdown(self, wait=True, log=True):
        if log:
            self.log("shutting down %s" % self.address)
        self.shell.conn.write("shutdown -h now")
        self.shell.conn.nl()
        if wait:
            while self.alive():
                time.sleep(1)
            self.log("%s has been shut down." % self.address)

    def _scp(self, src, tgt, log=True, timeout=0):
        '''
            for uxtarget, use scp for upload and download
        '''
        child_pid = 0
        pty_fd = 0
        if log: self.log("copying %s to %s@%s:%s" % (src, self.username, self.address, tgt))

        if (os.path.exists(self.password)):  # the password is an IdentityFile for ssh authentication
            args = ("scp", "-q", "-r", "-p", "-o", "StrictHostKeyChecking=no", "-o", "IdentityFile=%s" % (self.password), "-o", "ServerAliveInterval=60", "-o", "ServerAliveCountMax=3", "-o", "TCPKeepAlive=yes", "-o", "UserKnownHostsFile=/dev/null", "%s"%(src),"%s@%s:%s" % (self.username, self.address, tgt))
        else:
            args = ("scp", "-q", "-r", "-p", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=60", "-o", "ServerAliveCountMax=3", "-o", "TCPKeepAlive=yes", "-o", "UserKnownHostsFile=/dev/null", "%s" % (src), "%s@%s:%s" % (self.username, self.address, tgt))
        (pid, fd) = pty.fork()
        if(pid == 0):
            os.execvp("scp", args)
        else:
            child_pid = pid
            pty_fd = fd
        try:
            txt = os.read(pty_fd, 4096)
        except OSError as err:
            txt = ""
        if (txt.find("password:") >= 0):
            os.write(pty_fd, "%s\n" % (self.password))
        pid, rt = os.waitpid(child_pid,0)
        if (rt != 0):
            self.log("error: scp returned %d:\n%s" % (rt, txt) ,1)
            return False
        if log: self.log("copying %s to %s@%s:%s. Done!" % (src, self.username, self.address, tgt))
        return True

    def upload(self, local_path, remote_path, log=True):
        return self._scp(local_path, remote_path)

    def download(self, local_path, remote_path, log=True):
        return self._scp(remote_path, local_path)

