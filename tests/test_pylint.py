#!/usr/bin/env python

import os
import unittest
import logging

FILES = [
    '/api/i.py',
    '/api/interpretation.py',
    '/pypoot/interpretation.py',
    '/pypoot/json.py',
    '/pypoot/permalink.py',
    '/pypoot/integration.py',
    '/queue_handlers/new_interpretation.py',
]

PYLINT = '/opt/local/Library/Frameworks/Python.framework/Versions/2.5/bin/pylint --reports=n --persistent=n --max-line-length=100 --output-format=parseable --max-public-methods=30 --max-branchs=13 --deprecated-modules=regsub,TERMIOS,Bastion,rexec'

class TestPylint(unittest.TestCase):
    def test(self):
        for file in FILES:
            out = os.popen(PYLINT + " " + os.environ['POOTPOOT_APP_DIR'] + file)
            for i in out:
                logging.info(i)
            x = out.close()
            self.assertEquals(x, None, "pylint check of: %s" % file)
