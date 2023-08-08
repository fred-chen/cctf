#!/usr/bin/env python3

from typing import List
import os
import sys
import unittest
import re


sys.path.append(os.path.dirname(__file__))
from .test_common import get_nodes
from cctf import gettarget, Target, Shell, Command

class TestTarget(unittest.TestCase):
    def setUp(self):
        cur_dir = os.path.dirname(__file__)
        config_file = os.path.join(cur_dir, 'nodes.json')
        self.nodes: List[List[str]] = get_nodes(config_file)

    def tearDown(self):
        pass

    def test_gettarget(self):
        for i in range(10):
            for host, user, password in self.nodes:
                t: Target = gettarget(host, user, password)
                self.assertTrue(t)
                self.assertTrue(re.match(r'^\S+(\.\S+)*$', t.gethostname()),
                                f"hostname '{t.gethostname()}' is not valid.\nhost: {host}\nuser: {user}\npassword: {password}")
                sh = t.newshell()
                self.assertTrue(sh.exe("hostname").get_stdout()
                                == t.gethostname())

    def test_reboot_target(self):
        for host, user, password in self.nodes:
            t: Target = gettarget(host, user, password)
            self.assertTrue(t)
            sh: Shell = t.newshell()

            t.reboot(wait=True)  # wait for the target to be down and up
            # the command should be executed when the target is back up again
            self.assertTrue(sh.exe("hostname").get_stdout()
                            == t.gethostname())

        # reboot immediately after a command is issued
        # the shell should automatically reconnect after the target is back online again
        cos: List[Command] = []
        for host, user, password in self.nodes:
            cos.append(sh.exe("hostname", wait=False))
            t.reboot(wait=False)
        for host, user, password in self.nodes:
            t.wait_alive()  # wait for the target to be back up again
            # the command issued before rebooting, should be executed when the target is back up again
            for co in cos:
                self.assertTrue(co.get_stdout() == t.gethostname())

        # panic reboot immediately after a command is issued
        cos = []
        for host, user, password in self.nodes:
            cos = []
            cos.append(sh.exe("hostname", wait=False))
            t.panicreboot(wait=False)
        for host, user, password in self.nodes:
            t.wait_alive()
            for co in cos:
                self.assertTrue(co.get_stdout() == t.gethostname())

        # multiple reboot immediately after a command is issued
        cos = []
        for host, user, password in self.nodes:
            cos.append(sh.exe("hostname", wait=False))
            t.panicreboot(wait=False)  # first reboot
        for host, user, password in self.nodes:
            t.wait_alive()
            t.reboot(wait=False)  # first reboot
        for host, user, password in self.nodes:
            t.wait_alive()
        for co in cos:
            self.assertTrue(co.get_stdout() == t.gethostname())


if __name__ == '__main__':
    unittest.main()
