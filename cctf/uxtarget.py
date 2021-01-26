'''
Created on Aug 25, 2018

@author: fred
'''

from target import target
import time

class uxtarget(target):
    """
        unix, linux like targets
        this kind of targets share similar commands
        so it makes sense for them to share a same parent class
    """
    def __init__(self, address, svc='ssh', username='root', password=None, timeout=60):
        self.newline = '\n'
        target.__init__(self, address, svc, username, password, timeout)

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
