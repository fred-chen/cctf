#!/usr/bin/env python3

import unittest
import socket


from cctf import gettarget, target, shell

# 本机必须有ssh服务
# [host, user, password]
nodes = [['localhost', 'root', 'password'], ]


class TestTarget(unittest.TestCase):
    def test_gettarget(self):
        for host, user, password in nodes:
            t: target = gettarget(host, user, password)
            self.assertTrue(t)
            hostname = socket.gethostname()
            self.assertEqual(hostname, t.gethostname())


if __name__ == '__main__':
    unittest.main()
