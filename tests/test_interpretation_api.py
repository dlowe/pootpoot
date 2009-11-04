#!/usr/bin/env python

import unittest
import urllib2
import os
import logging

class TestAPI(unittest.TestCase):
    def test(self):
        try:
            urllib2.urlopen('http://localhost:' + os.environ['POOTPOOT_APP_PORT'] + '/poot')
        except urllib2.URLError, e:
            self.assertEquals(e.code, 404)
        else:
            self.assert_(0)
