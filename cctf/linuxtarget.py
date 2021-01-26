'''
Created on Aug 25, 2018

@author: fred
'''

from uxtarget import uxtarget
import time

class linuxtarget(uxtarget):
    def __init__(self, address, svc='ssh', username='root', password=None, timeout=60):
        uxtarget.__init__(self, address, svc, username, password, timeout)
        self.newline = '\n'

    def panic(self, log=True):
        if log:
            self.log("panicing %s" % self.address)
        self.shell.conn.write("echo 0 >/proc/sys/kernel/panic")
        self.shell.conn.nl()
        self.shell.conn.write("echo 1 > /proc/sys/kernel/sysrq")
        self.shell.conn.nl()
        self.shell.conn.write("echo c > /proc/sysrq-trigger")
        self.shell.conn.nl()
        if log:
            self.log("%s paniced." % self.address)
    
    def panicreboot(self, wait=True, log=True):
        if log:
            self.log("panic rebooting %s" % self.address)
        self.shell.conn.write("echo 1 >/proc/sys/kernel/panic")
        self.shell.conn.nl()
        self.shell.conn.write("echo 1 > /proc/sys/kernel/sysrq")
        self.shell.conn.nl()
        self.shell.conn.write("echo c > /proc/sysrq-trigger")
        self.shell.conn.nl()
        if wait:
            self.wait_alive()
            if log:
                self.log("%s is back online." % self.address)
