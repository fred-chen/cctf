"""
Created on Aug 25, 2018

@author: fred

===============================================================================

DESCRIPTION
----------------
The CCTF package is a framework for running commands on remote servers.

The CCTF package leverages the multi-threading capability of Python to run
multiple commands on multiple servers simultaneously and asychronously. 

It also provides a simple way to capture the output and errors of the
commands and log them to files. 

The CCTF package is designed to be used in a test framework, where the test
framework can use the CCTF to simulate all kinds of user actions on the
server nodes then capture the output of the commands, then use the output to
determine if the test is passed or failed.

CCTF exposes a set of simple API to the users:
```python
    class Target:
        # which represents a server node, or any other devices.

    class Shell: 
        # which represents a shell session on a server node.
    
    class Command: 
        # which represents a command to be run on a server node.

    def gettarget(): 
        # This function is used to create a Target object. Which is kind
        # of the entry point of the CCTF framework.
```

CCTF intends to be a simple and easy to use framework. The main idea behind CCTF
is to simulate a common use case: a user logs into a bunch of server nodes,
opens many many terminals for multiple notes, runs commands, maybe reboot some
of them, then logs out. CCTF provides an automatic way to do this. The user can
create a Target object, then use the Target object to create as many Shell
objects, each of the Shell objects represents a terminal to that target. Then
use the Shell objects to run Commands. The commands will be sent to the server
nodes and executed by the server nodes, then return the exit status, output and
errors of the command. The user can then use the output and errors to determine
if the command is successful or not.

EXAMPLE
```python
    # create a target object 
    target = gettarget("10.1.0.96", "root", "password") 

    # create a shell object associated on the target 
    shell  = target.newshell()
    
    # run a command on the target 
    command = shell.exe("banner Hello CCTF!")

    # check the result of a command
    if command.succ():
        print("Command succeeded")
    if command.fail():
        print("Command failed")
    if command.get_exitcode() != 0:
        print("Command failed with exit code: %d" % command.get_exitcode())
    
    # you can run a command asynchronously
    command = shell.exe("banner Hello CCTF!", wait=False) # return immediately
    
    # do something else here ...

    # then check the result of the command
    command.wait()  # wait for the command to finish, this is not really necessary 
                    # because the .succ() .fail() .get_exitcode() will wait 
                    # for the command to finish.
    if command.succ():
        print("Command succeeded")

    # reboot the target then wait for it to be back online 
    target.reboot()

    # reboot the target asynchronously
    target.reboot(wait=False) # it will return immediately
    
    # do something else here ...
    
    # then wait for the target to be back online
    target.wait_online() # wait for the target to be back online

    # upload a file to the target 
    target.upload("local_file", "remote_file")
    
    # download a file from the target 
    target.download("local_file", "remote_file")

    # connecto to multiple targets
    target1 = gettarget("10.1.0.91", "root", "password")
    target2 = gettarget("10.1.0.92", "root", "password")
    target3 = gettarget("10.1.0.93", "root", "password")
    
    # get 10 shells from each of the targets, 30 shells in total
    shells = []
    for target in [target1, target2, target3]:
        for i in range(10):
            shell = target.newshell()
            shells.append(shell)
    
    # run a command on all 30 shells (to 3 targets) simultaneously
    commands = []
    for shell in shells:
        command = shell.exe("banner Hello CCTF!", wait=False) # return immediately
        commands.append(command)
    
    # do something else here ...
    
    # wait for all 30 commands to finish
    for command in commands:
        if command.fail():
            print("Command failed with code %d: %s" % 
                command.get_exitcode(), command.get_cmdline())
```

All command execution will be logged to files and stdout. So a tester can
observe the execution of the commands and determine if the commands are executed
correctly.

CCTF is designed to be extensible. It provides a set of base classes, and
"""

__pdoc__ = {
    "aixtarget": False,
    "case": False,
    "caseunit": False,
    "command": False,
    "common": False,
    "connection": False,
    "connfactory": False,
    "hpuxtarget": False,
    "linuxtarget": False,
    "logicunit": False,
    "me": False,
    "rshconnection": False,
    "scanner": False,
    "shell": False,
    "sshconnection": False,
    "sunostarget": False,
    "target": False,
    "targetfactory": False,
    "telnetconnection": False,
    "uxtarget": False,
}

from .target import Target
from .targetfactory import gettarget
from .shell import Shell
from .command import Command
from .case import Case

__all__ = ["Target", "gettarget", "Shell", "Command", "Case"]
