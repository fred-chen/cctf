'''
Created on Aug 25, 2018

@author: fred
'''

import connection
from sshconnection import sshconnection
from telnetconnection import telnetconnection
from rshconnection import rshconnection 
from common import common
from me import is_server_svc_alive

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
    if svc != None:
        conn = createconn(host, svc, username, password, timeout, newline)
    if svc == None and conn ==None:
        for key in svclist.keys():
            if key == svc: continue
            conn = createconn(host, key, username, password, timeout, newline)
            if conn:
                break
    return conn

def createconn(host, svc, username, password, timeout, newline):
    conn = None
    alive = is_server_svc_alive(host, svc, timeout)
    if alive:
        common.log("connecting %s with %s" % (host, svc))
        try:
            if svc == 'shell':
                conn = rshconnection(host, username, password, timeout, newline)
            elif svc == 'ssh':
                conn = sshconnection(host, username, password, timeout, newline)
            elif svc == 'telnet':
                conn = telnetconnection(host, username, password, timeout, newline)
            else:
                return None
        except connection.connError, msg:
            conn = None
            common.log("couldn't connect %s with %s. (%s)" % (host, svc, msg))    
    else:
        common.log("couldn't connect %s with %s. (%s)" % (host, svc, "service is not available."))   
        conn = None
    
    return conn
        
