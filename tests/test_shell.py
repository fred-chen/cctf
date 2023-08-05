#!/usr/bin/env python3

import time
from typing import List
import os
import unittest
import sys


from .test_common import get_nodes
from cctf import gettarget, target, shell, command

class TestShell(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.targets: List[target] = []
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        cur_dir = os.path.dirname(__file__)
        config_file = os.path.join(cur_dir, 'nodes.json')
        self.nodes: List[List[str]] = get_nodes(config_file)
        for host, user, password in self.nodes:
            t = gettarget(host, user, password)
            self.assertTrue(t)
            self.targets.append(t)

    def tearDown(self):
        pass

    def test_newshell(self):
        shs: List[shell] = []
        for t in self.targets:
            for i in range(20):
                sh = t.newshell()
                self.assertTrue(sh)
                self.assertTrue(sh.exe("hostname").get_stdout()
                                == t.gethostname())
                shs.append(sh)
        start = time.time()
        cos = []
        for sh in shs:
            cos.append(sh.exe("sleep 2", wait=False))
        for co in cos:
            self.assertTrue(co.succ())
        dur = time.time() - start
        self.assertLess(dur, 2.5)
        

if __name__ == '__main__':
    unittest.main()
