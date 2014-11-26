#!/usr/bin/env python

import unittest
from wireless import Wireless


class TestWireless(unittest.TestCase):
    def setUp(self):
        # TODO
        pass

    def test_import(self):
        # if this module loads, then the import worked...
        self.assertTrue(hasattr(Wireless, 'connect'))
