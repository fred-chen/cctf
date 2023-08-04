#!/usr/bin/env python3

import unittest
import os, sys


if __name__ == '__main__':
    cur_path = os.path.dirname(__file__)
    sys.path.append(cur_path)
    sys.path.append(os.path.join(cur_path, ".."))

    # discover all tests
    loader = unittest.TestLoader()
    tests = loader.discover('tests')

    # run all tests
    runner = unittest.TextTestRunner()
    result = runner.run(tests)