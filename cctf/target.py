'''
Created on Aug 25, 2018

@author: fred
'''

import time

from .common import Common
from .me import is_server_svc_alive
from .shell import Shell
from .connection import Connection


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

    def newshell(self, conn: Connection = None) -> Shell:
        """
            Create and return a new shell object associated with this target.

            newshell() returns a shell object. Users use shell object to operate on this target. A
            target object can have multiple shell objects associated on it. newshell() is actually a
            factory method of shell objects.

            Args:
                conn (Connection, optional): a connection object this shell reuses. Defaults to
                None. if conn is None, a new connection will be created.

            Returns:
                Shell: a shell object.
        """
        shell = Shell(self, conn)
        if shell:
            self.shs.append(shell)
        return shell

    def __str__(self):
        if self.hostname:
            return f"{self.address} - {self.hostname}"
        else:
            return f"{self.address}"

    def gethostname(self) -> str:
        """Return the hostname of this target."""

        raise NotImplementedError()

    def reboot(self, wait=True, log=True):
        """Reboot the target. 

        Reboot the target gracefully, the target gets a chance to shutdown all services and then
        reboot.

        Args:
            wait (bool, optional): wait until the target is back online. Defaults to True. 
            log (bool, optional): log the reboot event. Defaults to True.
        """
        raise NotImplementedError()

    def panic(self, log=True):
        """ Panic the target.

        Panic the target immediately, the target hangs immediately without any chance to shutdown.
        Caution: The server will never come back online unless it is manually rebooted.

        Args:
            log (bool, optional): log the panic event. Defaults to True.
        """
        raise NotImplementedError()

    def panicreboot(self, wait=True, log=True):
        """ Panic the target and reboot it. 

        Panic the target immediately and reboot it. The target hangs immediately without any chance
        to shutdown, but it will reboot automatically. 

        Args:
            wait (bool, optional): wait until the target is back online. Defaults to True.
            log (bool, optional): log the panic event. Defaults to True.
        """
        raise NotImplementedError()

    def upload(self, local_path, remote_path, log=True) -> bool:
        """ Upload a file to the target.

        Upload a file from local_path to remote_path on the target.

        Args:
            local_path (str): local file path, can be a file or a directory or a wildcard.
            remote_path (str): remote file path, can be a file or a directory.

        Returns:
            bool: True if success, False if failed.
        """
        raise NotImplementedError()

    def download(self, local_path, remote_path, log=True) -> bool:
        """ Download a file from the target. 

        Download a file from remote_path on the target to local_path.

        Args:
            local_path (str): local file path, can be a file or a directory.
            remote_path (str): remote file path, can be a file or a directory or a wildcard.

        Returns:
            bool: True if success, False if failed. 
        """
        raise NotImplementedError()

    def wait_alive(self, svc=None, timeout=None) -> bool:
        """ Wait until the target is back online. 

        Wait until the target is back online. If svc is specified, wait until the service is back
        online. If timeout is specified, wait until the target is back online or timeout.

        Args:
            svc (str, optional): service name. Defaults to the service that was used to connect this
            target. 
            timeout (int, optional): timeout in seconds. Defaults to None, means wait forever.

        Returns:
            bool: True if the target is back online, False if timeout.
        """
        self.log(
            f"waiting on {self.address}:{str(svc) if svc else self.svc} to be online...")
        start = time.time()
        while not self.alive(svc, 1):
            dur = time.time() - start
            if timeout and dur >= timeout:
                return False
        self.log(f"{self.address}:{str(svc) if svc else self.svc} is back online.")
        return True

    def wait_down(self, svc=None, timeout=None) -> bool:
        """ Wait until the target is down. 

        Wait until the target is down. If svc is specified, wait until the service is down. If
        timeout is specified, wait until the target is down or timeout.

        Args:
            svc (str, optional): service name. Defaults to the service that was used to connect this
            target.
            timeout (int, optional): timeout in seconds. Defaults to None, means wait forever.

        Returns:
            bool: True if the target is down, False if timeout.
        """
        start = time.time()
        while self.alive(svc, 1):
            dur = time.time() - start
            if timeout and dur >= timeout:
                return False
        self.log(f"{self.address}:{str(svc) if svc else self.svc} is down.")
        return True

    def alive(self, svc=None, timeout=1) -> bool:
        """ Check if the target is alive. 

        Check if the target is alive. If svc is specified, check if the service is alive. If timeout
        is specified, check if the target is alive or timeout.

        Args:
            svc (str, optional): service name. Defaults to the service that was used to connect this
            target.
            timeout (int, optional): timeout in seconds. Defaults to 1.

        Returns:
            bool: True if the target is alive, False if timeout.
        """
        service = svc if svc else self.svc
        return is_server_svc_alive(host=self.address, svc=service, timeout=timeout)


