#!/usr/bin/env python

import os
import unittest
import logging

FILES = [
    '/static/code.html',
    '/static/contact.html',
    '/static/interpretation.html',
    '/static/list_interpretations.html',
    '/static/rest.html',
    '/static/submit.html',
    '/static/what.html',
]

TIDY = 'tidy -qe'

class TestTidy(unittest.TestCase):
    def test(self):
        for file in FILES:
            out = os.popen(TIDY + " " + os.environ['POOTPOOT_APP_DIR'] + file)
            for i in out:
                logging.info(i)
            x = out.close()
            self.assertEquals(x, None, "tidy check of: %s" % file)
