'''
Created on Aug 25, 2018

@author: fred
'''

import time

from .common import Common
from .connfactory import connect
from .me import is_server_svc_alive
from .shell import Shell


def __execmd(conn, cmd, timeout=60):
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


class Target(Common):
    """
        The target class. 
        
        A target object represents a remote host or any device that can be connected or logged in.
    """

    def __init__(self, address, svc='ssh', username='root', password=None, conn=None, timeout=60):
        self.address = address
        self.svc = svc
        self.username = username
        self.password = password
        self.timeout = timeout
        self.hostname = None
        self.conn = conn
        self.shs = []
        self.shell = self.newshell(self.conn)
        self.shs.append(self.shell)
        self.exe = self.shell.exe   # target.exe() is just a delegation of target.shell.exe()
        self.__inittarget()

    def __inittarget(self):
        self.gethostname()

    def newshell(self, conn=None) -> Shell:
        """
            Create and return a new shell object associated with this target.
            
            newshell() returns a shell object. Users use shell object to operate on this target. A
            target object can have multiple shell objects associated on it. newshell() is actually a
            factory method of shell objects.
        """
        shell = Shell(self, conn)
        if shell:
            self.shs.append(shell)
        return shell

    def __str__(self):
        if self.hostname:
            return "%s - %s" % (self.address, self.hostname)
        else:
            return "%s" % (self.address)

    def gethostname(self):
        """Return the hostname of this target."""

        raise NotImplementedError()

    def reboot(self, wait=True, log=True):
        """Reboot the target. 
        
        Reboot the target gracefully. If wait is True, wait until the target is back online, otherwise the function will return
        immediately. If log is True, log the reboot event.
        """
        
        raise NotImplementedError()

    def panic(self, log=True):
        """ Panic the target.
        
        Panic the target immediately. If log is True, log the panic event.
        """
        raise NotImplementedError()

    def panicreboot(self, wait=True, log=True):
        """ Panic the target and reboot it. 
        
        Panic the target immediately and reboot it. If wait is True, wait until the target is back
        online, otherwise the function will return immediately. If log is True, log the panic event.
        """
        raise NotImplementedError()

    def upload(self, local_path, remote_path, log=True) -> bool:
        """ Upload a file to the target.
        
        Upload a file from local_path to remote_path on the target.
        """
        raise NotImplementedError()

    def download(self, local_path, remote_path, log=True) -> bool:
        """ Download a file from the target. 
        
        Download a file from remote_path on the target to local_path.
        """
        raise NotImplementedError()

    def wait_alive(self, svc=None, timeout=None) -> bool:
        """ Wait until the target is back online. 
        
        Wait until the target is back online. If svc is specified, wait until the service is back
        online. If timeout is specified, wait until the target is back online or timeout.
        """
        self.log("waiting on %s:%s to be online..." %
                 (self.address, str(svc) if svc else self.svc))
        start = time.time()
        while not self.alive(svc, 1):
            dur = time.time() - start
            if timeout and dur >= timeout:
                return False
        self.log("%s:%s is back online." %
                 (self.address, str(svc) if svc else self.svc))
        return True

    def wait_down(self, svc=None, timeout=None) -> bool:
        """ Wait until the target is down. 
        
        Wait until the target is down. If svc is specified, wait until the service is down. If
        timeout is specified, wait until the target is down or timeout.
        """
        start = time.time()
        while self.alive(svc, 1):
            dur = time.time() - start
            if timeout and dur >= timeout:
                return False
        self.log("%s:%s is down." %
                 (self.address, str(svc) if svc else self.svc))
        return True

    def alive(self, svc=None, timeout=1) -> bool:
        """ Check if the target is alive. 
        
        Check if the target is alive. If svc is specified, check if the service is alive. If timeout is specified, check if the target is alive or timeout.
        """
        service = svc if svc else self.svc
        return is_server_svc_alive(host=self.address, svc=service, timeout=timeout)


def gettarget(host, username=None, password=None, svc="ssh", timeout=60) -> Target:
    """
    factory function of target. creating connection to the target address 
    and issue simple command to detect target type then create target object respectively.

    Args:
        host (str): hostname or ip address.
        username (str, optional): user name to login. Defaults to None.
        password (str, optional): password of the user. Defaults to None.
        svc (str, optional): service to connect. Defaults to "ssh".
        timeout (int, optional): timeout. Defaults to 60.

    Returns:
        target: a target object.
    """
    conn = connect(host, username, password, svc, timeout)
    if not conn:
        return None
    txt = __execmd(conn, "uname -s", timeout)
    t = None
    if txt and txt.find("Linux") >= 0:
        from .linuxtarget import LinuxTarget
        txt = __execmd(conn, "ceph -s", timeout)
        t = LinuxTarget(host, svc, username, password, conn, timeout)
    else:
        conn.printlog()
        Common.log("unsupported target type.")
    return t
