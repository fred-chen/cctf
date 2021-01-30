'''
Created on Aug 25, 2018

@author: fred
'''

import os, socket, re, time, pty, select, subprocess
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
    except socket.error as msg:
        s.close()
        return False

def expect(cmd, patterns=(), ignorecase=False, timeout=0):
    """
        create a pseudo pty and execute a command
        wait for a specific pattern then send a response if specified
        arguments:
            cmd: command line to execute
            patters: ((pattern, resp), ...)
        return:
            (output, returncode) of command
    """
    dur = 0
    regs = []   # [(reg, resp), ...]
    for pattern in patterns:
        pat, resp = pattern
        regs.append((re.compile(pat, re.IGNORECASE|re.DOTALL if ignorecase else re.DOTALL), resp))

    child_pid = 0; pty_fd = 0
    args = cmd.split()
    (pid, fd) = pty.fork()
    if(pid == 0):
        os.execvp(args[0], args)
    else:
        child_pid = pid
        pty_fd = fd
    txt = ""; dur=0; start = time.time()
    while True:
        try:
            r = select.select([pty_fd], [], [], 1)
            if r[0]:
                line = os.read(pty_fd, 4096)
                txt += line
                for reg in regs:
                    r, resp = reg
                    m = r.search(line)
                    if m:
                        if resp:
                            os.write(pty_fd, resp+'\n')
        except OSError as err:         # child process ended
            break
        dur = time.time() - start
        if (timeout and dur >= timeout):
            os.kill(child_pid, 9)      # timeout, no reason to keep running the command
            break
    pid, rt = os.waitpid(child_pid,0)
    return (txt, rt)

def ls(path):
    '''
        expand a wildcard filenames
        return a list of absolute paths of filenames
    '''
    status, output = commands.getstatusoutput('ls -d %s' % path)
    if status != 0:
        return None
    return output.split()

def call(cmd, *args, **kwargs):
    return subprocess.call(cmd, *args, **kwargs)
