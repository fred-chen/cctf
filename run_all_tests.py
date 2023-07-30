#!/usr/bin/env python3

import unittest
import os, sys


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

    # discover all tests
    loader = unittest.TestLoader()
    tests = loader.discover('tests')

    # run all tests
    runner = unittest.TextTestRunner()
    result = runner.run(tests)