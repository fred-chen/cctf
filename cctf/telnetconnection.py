'''
Created on Aug 25, 2018

@author: fred
'''

from . import connection, me

class TelnetConnection(connection.Connection):
    def __init__(self, host, username, password, timeout, newline):
        if not me.is_command_executable('telnet'):
            self.log( "telnet is NOT there." )
            return None
        connection.Connection.__init__(self, host, username, password, timeout, newline)
                
    def connect(self, host, svc, timeout):
        raise NotImplementedError()