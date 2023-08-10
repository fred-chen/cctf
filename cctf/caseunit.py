"""
Created on Aug 25, 2018

@author: fred

===============================================================================
"""

from .logicunit import LogicUnit


class Caseunit(LogicUnit):
    """Caseunit is a logicunit with result."""

    SUCC = True
    FAIL = False

    def __init__(self):
        LogicUnit.__init__(self)
        self.result = None

    def setresult(self, result):
        """setresult() is a method to set the result of the case"""
        self.result = result

    def getresult(self, timeout=None):
        """getresult() is a blocking method to get the result of the case"""
        while self.is_alive():
            self.join(timeout)
        return self.result

    def run(self):
        repeat = self._repeat
        self.setresult(self.init())
        while (self._repeat == 0 or repeat > 0) and not self._stop:
            self.setresult(self.body())
            self.check()
            repeat -= 1
        self.setresult(self.final())
