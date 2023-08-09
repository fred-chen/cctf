"""
The CCTF package is a framework for running commands on remote servers.

The CCTF package is a framework for running commands on remote servers. It
leverages the multi-threading capability of Python to run multiple commands on
multiple servers simultaneously and asychronously. It also provides a simple way
to capture the output of the commands and log them to files. The CCTF package is
designed to be used in a test framework, where the test framework can use the
CCTF package to run commands on remote servers and capture the output of the
commands, and then use the output to determine if the test is passed or failed.
"""
from .cctf import Target, gettarget
from .cctf import Shell
from .cctf import Command
from .cctf import Case

__all__ = ['Target', 'gettarget', 'Shell', 'Command']
