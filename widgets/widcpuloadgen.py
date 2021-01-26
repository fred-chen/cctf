'''
Created on Nov 19, 2018

@author: fred
'''

from widget import widget

class widcpuloadgen(widget):
    def __init__(self, target, pct=75, start=True):
        '''
            Constructor
        '''
        self._pct = 75
        widget.__init__(self, target, 'widcpuloadgen', '-c %s' % (pct), start)
