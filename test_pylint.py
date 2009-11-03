#!/usr/bin/env python

import os
import unittest
import logging

FILES = [
    'poot-poot/api/i.py',
    #'poot-poot/api/interpretation.py',
    #'poot-poot/pypoot/interpretation.py',
    #'poot-poot/pypoot/json.py',
    #'poot-poot/pypoot/permalink.py'
]

PYLINT = '/opt/local/Library/Frameworks/Python.framework/Versions/2.5/bin/pylint --reports=n --persistent=n --max-line-length=100 --output-format=parseable --max-public-methods=30 --deprecated-modules=regsub,TERMIOS,Bastion,rexec'

class TestPylint(unittest.TestCase):
    def test(self):
        for file in FILES:
            out = os.popen(PYLINT + " " + file)
            for i in out:
                logging.info(i)
            x = out.close()
            self.assertEquals(x, None, "pylint check of: %s" % file)
