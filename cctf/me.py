'''
Created on Aug 25, 2018

@author: fred
'''

import os, socket
import commands

def is_path_executable(path):
    """
        check whether a path is existed and executable. return boolean.
    """
    if os.access(path, os.F_OK|os.X_OK): return True
    
    return False

def is_command_existed(cmd):
    """
        invoke 'which' command to case_test whether an os command existed.
        suppose 'which' command should always present
        if command doesn't not exist return None
        if command exists return a string object containing the path of command
    """
    status, output = commands.getstatusoutput('which %s' % cmd)
    if status != 0:
        return None
    else:
        return output
    
def is_command_executable(cmd):
    """
        return true if cmd is executable for real uid/gid
        otherwise return false
    """
    cmdpath = is_command_existed(cmd)
    if cmdpath and is_path_executable(cmdpath):
        return True
    else:
        return False

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True
    
def is_server_svc_alive(host='127.0.0.1', svc=22, timeout=None ):
    """
        check whether the TCP service of a given host is being listened or not
        parameters: host - hostname or ip address
                    svc - can be an integer port number or a string service name
        exceptions: None
        return:     True if server tcp port is up
                    False if server tcp port is down
        dependency: Os independent
    """
    port_num = 0
    if isinstance(svc, str):
        if svc.isdigit():
            port_num = int(svc)
        else:
            port_num = socket.getservbyname(svc, 'tcp')  # could raise exception: socket.error: service/proto not found
    else:
        port_num = svc
    return _is_server_port_alive(host, port_num, timeout)

def _is_server_port_alive(host, port, timeout=None ):
    """
        check whether the TCP port of a given host is being listened or not
        parameters: host - hostname or ip address
                    port - must be an integer port number
        exceptions: none
        return:     True if server port is up
                    False if server port is down
        dependency: Os independent
    """
    s = socket.socket()
    try:
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except socket.error, msg:
        s.close()
        return False
