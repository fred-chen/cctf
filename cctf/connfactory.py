'''
Created on Aug 25, 2018

@author: fred

===============================================================================
'''

from .sshconnection import SshConnection
from .telnetconnection import TelnetConnection
from .rshconnection import RshConnection
from .common import Common
from .me import is_server_svc_alive

svclist = {
           'ssh':22,    # ssh
           'shell':514, # rsh
           'telnet':23  # telnet
#           'exec':512,  # rexec
#           'login':513, # rlogin
          }

def connect(host='127.0.0.1', username=None, password=None, svc="ssh", timeout=30, newline='\n'):
    """
        connect is a factory method of connection objects.
        connect detect available connection method ( ssh/rsh/telnet ) and create connection object respectively
        connect will return a connection object ( a child-class object which implements connection interface )
        svc can be any one of: shell(rsh-remote shell), ssh or telnet
    """
    conn = None
    if svc is not None:
        conn = createconn(host, svc, username, password, timeout, newline)
    if svc is None and conn is None:
        for key in svclist:
            if key == svc:
                continue
            conn = createconn(host, key, username, password, timeout, newline)
            if conn:
                break
    return conn

def createconn(host, svc, username, password, timeout, newline):
    Common().log("connecting %s with %s" % (host, svc))
    conn = None
    alive = is_server_svc_alive(host, svc, timeout)
    if alive:
        try:
            if svc == 'shell':
                conn = RshConnection(host, username, password, timeout, newline)
            elif svc == 'ssh':
                conn = SshConnection(host, username, password, timeout, newline)
            elif svc == 'telnet':
                conn = TelnetConnection(host, username, password, timeout, newline)
            else:
                return None
        except connection.connError as err:
            conn = None
            Common.log("couldn't connect %s with %s. (%s)" % (host, svc, err))    
    else:
        Common.log("couldn't connect %s with %s. (%s)" % (host, svc, "service is not available."))   
        conn = None
    
    return conn
        
