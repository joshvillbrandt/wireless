#!/usr/bin/env python

import unittest
from wireless import Wireless
from wireless.Wireless import cmd


class TestWireless(unittest.TestCase):
    def setUp(self):
        # TODO
        pass

    def test_import(self):
        # if this module loads, then the import worked...
        self.assertTrue(hasattr(Wireless, 'connect'))


class TestCMD(unittest.TestCase):
    """
        Tests against cmd function.
    """
    def setUp(self):
        self.com = cmd('echo "test_ok"')
        self.empty_com = cmd('echo -n')

    def test_cmdcomparission(self):
        """
            Check if we can test against the output of
            the current test command
        """
        self.assertTrue('test_ok' in self.com)

    def test_cmdlen(self):
        """
            Check if the output is > 0 chars.
        """
        self.assertFalse(len(self.empty_com) > 0)
        self.assertTrue(len(self.com) > 0)
