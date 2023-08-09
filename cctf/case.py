'''
Created on Aug 25, 2018

@author: fred

===============================================================================
'''

import time
import getopt
import sys
import re
from .common import Common

class Case(Common):
    def __init__(self, casename):
#         self.args = args
        self.casename = casename
        self.start = time.time()
        self.end = None
        self.targets = []   # list of target addresses: [(user, pass, addr), (user, pass, addr), ...]
        self.params = {}
        self.load = 50
        self._parse_params()
        self.log("Starting case %s..." % (self.casename))
    
    def succ(self):
        self.log("Case %s succeeds." % (self.casename))
        exit(0)
        
    def fail(self, exitcode=1):
        self.log("Case %s failed." % (self.casename), 1)
        exit(exitcode)
    
    def log(self, msg, level=3):
        Common.log("CASE "+ self.casename + ": " + msg, level)
        
    def _parse_params(self):
        """
            standard parameters:
                -t: a target list, format: user:password@address0, user:password@address1, ...
                -l: a percentage from 0-100, represents how big load should a case generates
            other case-specific parameters:
                format: param_name=value param_name=value ...
                any parameter can be passed in to a case, the case interprets them respectively 
        """
        s="-t:-l:"
        opts = []; args = []
        try:
            opts, args = getopt.gnu_getopt(sys.argv[1:], s)
        except Exception as msg:
            print (msg)
        for opt in opts:
            if opt[0] == '-t':
                # parse target addresses
                addrs = opt[1].split(',')
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
            if opt[0] == '-l':
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