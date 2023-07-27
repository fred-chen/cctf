'''
Created on Aug 25, 2018

@author: fred
'''

from . import connection
from . import me

class rshconnection(connection.connection):
    def __init__(self, host, username, password, timeout, newline):
        if not me.is_command_executable('rsh'):
            self.log( "rsh is NOT there." )
            return None
        connection.connection.__init__(self, host, username, password, timeout, newline)
                
    def connect(self, host, svc, timeout):
        raise "not implemented"