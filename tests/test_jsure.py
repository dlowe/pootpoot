#!/usr/bin/env python

import os
import unittest
import logging

FILES = [
    '/static/pootpoot.js'
]

JSURE = 'jsure -quiet'

class TestJsure(unittest.TestCase):
    def test(self):
        for file in FILES:
            out = os.popen(JSURE + " " + os.environ['POOTPOOT_APP_DIR'] + file)
            for i in out:
                logging.info(i)
            x = out.close()
            self.assertEquals(x, None, "jsure check of: %s" % file)
