'''
Created on Nov 8, 2018

@author: fred
'''

from cctf.shell import shell
import re

class bdoperator(shell):
    '''
    OrcaBD operator
    '''

    def __init__(self, target):
        shell.__init__(self, target)
    
    def createpool(self, poolname, pgnum=100, wait=True):
        return self.exe("ceph osd pool create %s %d" % (poolname, pgnum), wait).succ()
    
    def getpools(self):
        pools = []
        out = self.exe("ceph osd lspools").stdout.strip()
        if not out:
            return None
        reg = re.compile("\d+ (.+)", re.DOTALL)
        ll = out.split(',')
        for l in ll:
            if l:
                m = reg.search(l)
                if m:
                    pools.append(m.group(1))
        return pools
    
    
    