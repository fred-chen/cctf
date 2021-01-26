'''
Created on Nov 8, 2018

@author: fred
'''

from cctf.linuxtarget import linuxtarget
from bdoperator import bdoperator

class bdtarget(linuxtarget):
    '''
    target class for OrcaBD
    '''

    def __init__(self, address, svc='ssh', username='root', password=None, timeout=60):
        linuxtarget.__init__(self, address, svc, username, password, timeout)
        
    
    def newop(self):
        return bdoperator(self)
    def newshell(self):
        return self.newop()
    
    def getpools(self):
        return self.shell.getpools()