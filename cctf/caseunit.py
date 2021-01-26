'''
Created on Nov 2, 2018

@author: fred
'''

from logicunit import logicunit

class caseunit(logicunit):
    SUCC = True
    FAIL = False
    def __init__(self):
        logicunit.__init__(self)
        self.result = None
    
    def setresult(self, result):
        self.result = result
        
    def getresult(self, timeout=None):
        while self.isAlive():
            self.join(timeout)
        return self.result

    def run(self):
        r = self._repeat
        self.setresult(self.init())
        while ( self._repeat == 0 or r > 0 ) and not self._stop:
            self.setresult(self.body())
            self.check()
            r -= 1
        self.setresult(self.final())
        