'''
Created on Aug 25, 2018

@author: fred
'''

import time
import os
from .target import Target
from . import me


class UxTarget(Target):
    """
        unix, linux like targets
        this kind of targets share similar commands
        so it makes sense for them to share a same parent class
    """

    def __init__(self, address, svc='ssh', username='root', password=None, conn=None, timeout=60):
        self.newline = '\n'
        Target.__init__(self, address, svc, username, password, conn, timeout)

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
        # for sh in self.shs:
        #     sh.disconnect()
        self.wait_down()
        if wait:
            self.wait_alive()

    def shutdown(self, wait=True, log=True):
        if log:
            self.log("shutting down %s" % self.address)
        self.shell.conn.write("shutdown -h now")
        self.shell.conn.nl()
        # for sh in self.shs:
        #     sh.disconnect()
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
        if log:
            self.log("copying %s to %s" % (src, tgt))

        if (os.path.exists(self.password)):  # the password is an IdentityFile for ssh authentication
            args = ("scp", "-q", "-r", "-p", "-o", "StrictHostKeyChecking=no", "-o", "IdentityFile=%s" % (self.password), "-o", "ServerAliveInterval=60",
                    "-o", "ServerAliveCountMax=3", "-o", "TCPKeepAlive=yes", "-o", "UserKnownHostsFile=/dev/null", "%s" % (src), "%s" % (tgt))
        else:
            args = ("scp", "-q", "-r", "-p", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=60", "-o",
                    "ServerAliveCountMax=3", "-o", "TCPKeepAlive=yes", "-o", "UserKnownHostsFile=/dev/null", "%s" % (src), "%s" % (tgt))
        cmd = " ".join(args)
        output, status = me.expect(cmd, [("password:", self.password)])
        if (status != 0):
            self.log("error: scp returned %d:\n%s" % (status, output), 1)
            return False
        return True

    def upload(self, local_path, remote_path, log=True):
        flist = me.ls(local_path)
        src_str = ' '.join(flist)
        return self._scp(src_str, "%s@%s:%s" % (self.username, self.address, remote_path))

    def download(self, local_path, remote_path, log=True):
        co = self.exe("ls -d %s" % (remote_path))
        path_str = ' '.join(
            ['%s@%s:%s' % (self.username, self.address, path) for path in co.getlist()])
        return self._scp(path_str, local_path)
