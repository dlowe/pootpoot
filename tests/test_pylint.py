#!/usr/bin/env python

import os
import unittest
import logging

FILES = [
    '/api/i.py',
    '/api/api_request_handler.py',
    '/api/interpretation.py',
    '/api/comment.py',
    '/pypoot/interpretation.py',
    '/pypoot/json.py',
    '/pypoot/permalink.py',
    '/pypoot/integration.py',
    '/pypoot/comment.py',
    '/queue_handlers/new_interpretation.py',
    '/feeds/interpretations.py',
]

PYLINT = 'pylint --reports=n --persistent=n --max-line-length=100 --output-format=parseable --max-public-methods=30 --max-branchs=13 --deprecated-modules=regsub,TERMIOS,Bastion,rexec'

class TestPylint(unittest.TestCase):
    def test(self):
        for file in FILES:
            out = os.popen(PYLINT + " " + os.environ['POOTPOOT_APP_DIR'] + file)
            for i in out:
                logging.info(i)
            x = out.close()
            self.assertEquals(x, None, "pylint check of: %s" % file)
