'''
Created on Aug 25, 2018

@author: fred
'''

from . import connection
from .me import is_server_svc_alive, is_command_executable
import os

class sshconnection(connection.connection):
    def __init__(self, host, username=None, password=None, timeout=30, newline='\n'):
        if not is_command_executable('ssh'):
            self.log( "ssh is NOT there." )
            return None
        connection.connection.__init__(self, host, username, password, timeout, newline)
        self.log(f"host={host}")
        self.log(f"self.host={self.host}")
                
    def connect(self):
        if (self.password and os.path.exists(self.password)):  # the password is an IdentityFile for ssh authentication
            args = ("ssh", "-q", "-o", "StrictHostKeyChecking=no", "-o", "IdentityFile=%s" % (self.password), "-o", "ServerAliveInterval=60", "-o", "ServerAliveCountMax=3", "-o", "TCPKeepAlive=yes", "-o", "UserKnownHostsFile=/dev/null", "-l", self.username, self.host)
        else:
            args = ("ssh", "-q", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=60", "-o", "ServerAliveCountMax=3", "-o", "TCPKeepAlive=yes", "-o", "UserKnownHostsFile=/dev/null", "-l", self.username, self.host)
        try:
            self._spawn(args)
        except Exception as msg:
            self.log(str(msg))
            return False
        return self.login()
    
    def svcalive(self):
        return is_server_svc_alive(host=self.host, svc=22, timeout=10)
        
