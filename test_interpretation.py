#!/usr/bin/env python

import sys
import unittest
sys.path = [ './poot-poot' ] + sys.path

## import from the app
from pypoot import interpretation

class TestInterpretation(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_create_bad_type(self):
        self.assertRaises(interpretation.BunkInterpretation, interpretation.submit, 
                               title='Test',
                               type='foo',
                               content_type='text/plain',
                               content='fnord')

    def test_submit(self):
        ## submitting an interpretation should create an inactive one
        i = interpretation.submit(
                           title='Test',
                           type='text',
                           content_type='text/plain',
                           content='fnord')
        self.assertFalse(i.is_active)

        ## fetching it is possible if specific key is provided
        j = interpretation.poot(str(i.key()))

        ## and the fetched interpretation should be identical
        self.assertEquals(i.title, j.title)
        self.assertEquals(i.type, j.type)
        self.assertEquals(i.content_type, j.content_type)
        self.assertEquals(i.content, j.content)
        self.assertEquals(i.is_active, j.is_active)

        ## but fetching without a key should raise NoInterpretation
        self.assertRaises(interpretation.NoInterpretation, interpretation.poot, None)

        ## approving it should activate it
        interpretation.approve(i)
        self.assertTrue(i.is_active)
        j = interpretation.poot(str(i.key()))
        self.assertEquals(i.is_active, j.is_active)

        ## now fetching without a key should bring it up
        k = interpretation.poot(None)
        self.assertEquals(str(i.key()), str(k.key()))

if __name__ == '__main__':
    unittest.main()
