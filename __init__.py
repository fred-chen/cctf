"""
The CCTF - Concurrency Control Test Framework.

CCTF package is designed to be used in a test framework, where the test framework can use the CCTF
to simulate all kinds of user actions on the server nodes then capture the output of the commands,
then use the output to determine if the test is passed or failed.
"""
from .cctf import Target, gettarget
from .cctf import Shell
from .cctf import Command

__all__ = ["Target", "gettarget", "Shell", "Command"]
