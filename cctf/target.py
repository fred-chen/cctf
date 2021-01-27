'''
Created on Aug 25, 2018

@author: fred
'''

from common import common
from connfactory import connect
from me import is_server_svc_alive
from shell import shell
import time

def gettarget(host, username=None, password=None, svc="ssh", timeout=60):
    """
        factory function of target
        creating connection to the target address
        and issue simple command to detect target type
        then create target object respectively
    """
    conn = connect(host, username, password, svc, timeout)
    if not conn:
        return None
    txt = execmd(conn, "uname -s", timeout)
    t = None
    if txt and txt.find("Linux") >= 0:
        from orcabd import bdtarget
        from linuxtarget import linuxtarget
        txt = execmd(conn, "ceph -s", timeout)   
        if txt and txt.find("cluster:") >= 0: # ceph cluster node
            t = bdtarget(host, svc, username, password, conn, timeout)
        else:
            t = linuxtarget(host, svc, username, password, conn, timeout)
    else:
        conn.printlog()
        common.log("unsupported target type.")
    return t

def execmd(conn, cmd, timeout=60):
    conn.write('ECHO="line_of_cctf2018"')
    conn.nl()
    conn.write("echo start_$ECHO;")
    conn.nl()
    conn.waitfor("start_line_of_cctf2018", timeout)
    conn.write(cmd)
    conn.nl()
    conn.write("echo end_$ECHO")
    conn.nl()
    txt = conn.waitfor("end_line_of_cctf2018", timeout)
    return txt

class target(common):
    """
        target class. a target object represents a login-able host or a device.
    """
    def __init__(self, address, svc='ssh', username='root', password=None, conn=None, timeout=60):
        self.address = address
        self.svc = svc
        self.username = username
        self.password = password
        self.timeout = timeout
        self.hostname = None 
        self.conn = conn
        self.shell = self.newshell()
        self.inittarget()
    
    def inittarget(self):
        self.gethostname()
        
    def newshell(self):
        """
            getshell returns a shell object. Users use shell object to operate on this target.
            a target object can have multiple shell objects associated on it.
            getshell is actually a factory method of shell objects.
        """ 
        sh = shell(self, self.conn)
        return sh

    def exe(self, cmdline, wait=True, log=True):
        return self.shell.exe(cmdline, wait, log)
    
    def __str__(self):
        if self.hostname:
            return self.hostname
        else:
            return self.gethostname()
        
    
    def gethostname(self):
        raise "not implemented"
    
    def reboot(self, wait=True, log=True):
        raise "not implemented"
    
    def panic(self, wait=True, log=True):
        raise "not implemented"
    
    def panicreboot(self, wait=True, log=True):
        raise "not implemented"
    
    def wait_alive(self, timeout=None):
        self.log("waiting %s to be online..." % (self.address))
        start = time.time()
        while not self.alive(1):
            dur = time.time() - start
            if timeout and dur >= timeout:
                return False
        for i in range(3):
            if self.shell.reconnect(): break
            self.log("connection attempt %d" % (i))
        self.log("%s is back online." % self.address)
        return True
    
    def wait_down(self, timeout=None):
        start = time.time()
        while self.alive(1):
            dur = time.time() - start
            if timeout and dur >= timeout:
                return False
        self.log("%s is down." % self.address)
        return True

    def alive(self, timeout=1):
        return is_server_svc_alive(host=self.address, svc=self.svc, timeout=timeout)
    