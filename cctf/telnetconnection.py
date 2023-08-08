'''
Created on Aug 25, 2018

@author: fred
'''

from . import connection, me

class TelnetConnection(connection.connection):
    def __init__(self, host, username, password, timeout, newline):
        if not me.is_command_executable('telnet'):
            self.log( "telnet is NOT there." )
            return None
        connection.connection.__init__(self, host, username, password, timeout, newline)
                
    def connect(self, host, svc, timeout):
        raise "not implemented"