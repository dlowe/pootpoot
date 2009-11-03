#!/usr/bin/env python

import os
import unittest
import logging

FILES = [
    'poot-poot/static/pootpoot.js',
    'archive/pootpoot.js',
    'archive/findpoot.js',
    'archive/pootris.js',
    'archive/wpoot.js'
]

JSURE = 'jsure -quiet'

class TestJsure(unittest.TestCase):
    def test(self):
        for file in FILES:
            out = os.popen(JSURE + " " + file)
            for i in out:
                logging.info(i)
            x = out.close()
            self.assertEquals(x, None, "jsure check of: %s" % file)
