#!/usr/bin/env python3

import time
from typing import List
import os
import unittest
import sys


from tests.test_common import get_nodes
from .scanner import Scanner

class TestScanner(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
    
    def test_scanner(self):
        scanner = Scanner()
        res = scanner.scan('127.0.0.1', '22')
        self.assertEqual(res['scan']['127.0.0.1']['tcp'][22]['state'], 'open')
        