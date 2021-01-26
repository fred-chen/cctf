'''
Created on Nov 4, 2018

@author: fred
'''

from cctf import common

class widget(common):
    '''
        a widget object represents a remote widget
    '''
    WIDPATH = "/opt/cctf/widgets/"
    def __init__(self, target, widname, parameters="", start=True):
        '''
            Constructor
        '''
        self._sh = target.newshell()
        self._widname = widname
        self._param = parameters
        self._buildcmd()
        self._co = None
        if start:
            self.start()
    
    def _buildcmd(self):
        self._cmd = self.WIDPATH + self._widname + " " + self._param
    
    def start(self):
        self.log("starting widget %s" % (self._cmd))
        self._co = self._sh.exe(self._cmd, wait=False)
    
    def stop(self):
        if self._co:
            self._sh.getconn().write('\x03')
        
    def exitcode(self):
        self._co.wait()
        return self._co.exit
    
    def stderr(self):
        self._co.wait()
        return self._co.stderr
    
    def stdout(self):
        self._co.wait()
        return self._co.stdout
        