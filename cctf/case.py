"""
Created on Aug 25, 2018

@author: fred

===============================================================================

This module provides a case object class to be used by test cases. The case
object represents a test case. It contains the test case name, the target list,
the parameters, and the load percentage. It also provides a simple way to
capture the output and errors of the commands and log them to files.

A Case can succ() or fail(). When a case fails, it will exit the program with
errno. When a case succeeds, it will exit the program with exit code 0.
"""

import time
import getopt
import sys
import re
from .common import Common


class Case(Common):
    """Case object represents a test case.

    A Case object is created by calling the Case() constructor. It parses the
    sys.argv[1:] to get a target list and a load percentage for the case logic's
    reference. It also parses the sys.argv[1:] to get a list of parameters. The
    parameters are passed into the case object as a dictionary. The case object
    can use the parameters to configure itself.

    when running a script that uses the Case object, the user can pass in a list
    of targets, a load percentage, and a list of parameters. The list of targets
    is passed in by the "-t" option. The load percentage is passed in by the
    "-l" option. The list of parameters is passed in by the rest of the
    arguments. The format of the arguments is:

    1. target list: "-t user:password@address0, user:password@address1, ..."
    2. load percentage: "-l 50"
    3. parameters: "param_name=value param_name=value ..."

    Example:
    ```python
        # if the user runs the script with the following command line:
        python script.py -t root@10.1.0.91,root@10.1.0.92 -l 50 param1=1 param2=2

        # in script.py
        tc = Case(casename = "script.py")

        # then the script can get the target list, load percentage, and parameters from Case object:
        # tc.targets = [('root', None, '10.1.0.91'), ('root', None, '10.1.0.92')]
        # tc.load = 50
        # tc.params = {'param1': '1', 'param2': '2'}

    ```

    """

    def __init__(self, casename):
        self.casename = casename
        self.start = time.time()
        self.end = None
        self.targets = []  # list of target addresses: [(user, pass, addr), ...]
        self.params = {}  # the customized parameters for the case
        self.load = 50
        self._parse_params()
        self.log("Starting case %s..." % (self.casename))

    def succ(self):
        """Exit the program with exit code 0."""
        self.log("Case %s succeeds." % (self.casename))
        exit(0)

    def fail(self, exitcode=1):
        """Exit the program with errno. Default errno is 1."""
        self.log("Case %s failed." % (self.casename), 1)
        exit(exitcode)

    def log(self, msg, level=3):
        """Log a message to stdout."""
        super().log("CASE " + self.casename + ": " + msg, level)

    def _parse_params(self):
        """
        standard parameters:
            -t: a target list, format: user:password@address0, user:password@address1, ...
            -l: a percentage from 0-100, indicating how big load should a case generates
        other case-specific parameters:
            format: param_name=value param_name=value ...
            any parameter can be passed into a case, the case interprets them respectively
        """
        s = "-t:-l:"
        opts = []
        args = []
        try:
            opts, args = getopt.gnu_getopt(sys.argv[1:], s)
        except Exception as msg:
            print(msg)
        for opt in opts:
            if opt[0] == "-t":
                # parse target addresses
                addrs = opt[1].split(",")
                reg = re.compile("(([^:,]+)(:(.+))?@([^,]+))")
                for a in addrs:
                    if not a:
                        continue
                    m = re.match(reg, a)
                    if m:
                        self.targets.append((m.group(2), m.group(4), m.group(5)))
                    else:
                        self.log("invalid address string: '%s'" % (a))
                        self.fail(1)
            if opt[0] == "-l":
                if opt[1].isdigit():
                    self.load = int(opt[1])
                else:
                    self.log("invalid load percent string: '%s'" % (opt[1]))
                    self.fail(1)

        for arg in args:
            reg = re.compile("(\S+)=(\S+)")
            m = re.match(reg, arg)
            if m:
                self.params[m.group(1)] = m.group(2)
            else:
                self.log("invalid parameter string: '%s'" % (arg))
                self.fail(1)

    def __str__(self):
        return "CASE " + self.casename
