'''
Created on Aug 25, 2018

@author: fred
'''

import connection
from me import is_server_svc_alive, is_command_executable

class sshconnection(connection.connection):
    def __init__(self, host, username=None, password=None, timeout=30, newline='\n'):
        if not is_command_executable('ssh'):
            self.log( "ssh is NOT there." )
            return None
        connection.connection.__init__(self, host, username, password, timeout, newline)
                
    def connect(self):
        args = ("ssh", "-q", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=60", "-o", "ServerAliveCountMax=3", "-o", "TCPKeepAlive=yes", "-l", self.username, self.host)
        try:
            self._spawn(args)
        except Exception, msg:
            self.log(msg)
            return False
        return self.login()
    
    def svcalive(self):
        return is_server_svc_alive(host=self.host, svc=22, timeout=10)
        
