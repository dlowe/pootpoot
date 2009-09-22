#!/usr/bin/env python

import sys
import unittest
sys.path = [ './poot-poot' ] + sys.path

from google.appengine.api import datastore_errors

from pypoot import interpretation

class TestInterpretation(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_create_bad_type(self):
        try:
            i = interpretation.Interpretation(is_active=True,
                               title='Test',
                               type='foo',
                               content_type='text/plain',
                               content='fnord')
        except datastore_errors.BadValueError:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_create(self):
        i = interpretation.Interpretation(is_active=True,
                           title='Test',
                           type='text',
                           content_type='text/plain',
                           content='fnord')
        self.assertTrue(True)

    def test_put(self):
        i = interpretation.Interpretation(is_active=True,
                           title='Test',
                           type='text',
                           content_type='text/plain',
                           content='fnord')
        i.put()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
