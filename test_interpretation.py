#!/usr/bin/env python

import sys
import unittest
sys.path = [ './poot-poot' ] + sys.path

## import from the app
from pypoot import interpretation

class TestOwnerBaton(unittest.TestCase):
    def test(self):
        owner_baton = interpretation._new_owner_baton()
        self.assertTrue(isinstance(owner_baton, str))

class TestInterpretation(unittest.TestCase):
    def test_bad_key(self):
        ## does not look like a real key
        self.assertEquals(interpretation.poot('asdf'), None)
        self.assertEquals(interpretation.count('asdf'), 0)
        self.assertEquals(interpretation.list('asdf'), [])

        ## looks like a real key, but refers to no element
        self.assertEquals(interpretation.poot('aglwb290LXBvb3RyFAsSDkludGVycHJldGF0aW9uGAIM'), None)
        self.assertEquals(interpretation.count('aglwb290LXBvb3RyFAsSDkludGVycHJldGF0aW9uGAIM'), 0)
        self.assertEquals(interpretation.list('aglwb290LXBvb3RyFAsSDkludGVycHJldGF0aW9uGAIM'), [])

    def test_submit_disapprove(self):
        ## submitting an interpretation should create an inactive one
        i = interpretation.submit(
                            title='Test',
                            author='Anonymous',
                            type='text',
                            content_type='text/plain',
                            content='blart')
        self.assertFalse(i.is_active)

        ## cannot disapprove with no owner_baton
        self.assertRaises(interpretation.BadOwnerBaton, interpretation.delete, i, None)
        ## cannot disapprove with bunk owner_baton
        self.assertRaises(interpretation.BadOwnerBaton, interpretation.delete, i, "blah blah blah")

        ## can delete with correct owner_baton
        interpretation.delete(i, i.owner_baton)

    def test_create_bad_type(self):
        self.assertRaises(interpretation.BunkInterpretation, interpretation.submit, 
                               title='Test',
                               author='Anonymous',
                               type='foo',
                               content_type='text/plain',
                               content='fnord')

    def test_submit_approve(self):
        ## submitting an interpretation should create an inactive one
        i = interpretation.submit(
                           title='Test',
                           author='Anonymous',
                           type='text',
                           content_type='text/plain',
                           content='fnord')
        self.assertFalse(i.is_active)

        ## fetching it is possible if specific key is provided
        self.assertEquals(interpretation.count(str(i.key())), 1)
        for j in [interpretation.poot(str(i.key())), interpretation.list(str(i.key()))[0]]:
            ## and the fetched interpretation should be identical
            self.assertEquals(i.title, j.title)
            self.assertEquals(i.type, j.type)
            self.assertEquals(i.content_type, j.content_type)
            self.assertEquals(i.content, j.content)
            self.assertEquals(i.is_active, j.is_active)

        ## but fetching without a key should return nothing
        self.assertEquals(interpretation.count(), 0)
        self.assertEquals(interpretation.list(), [])
        self.assertEquals(interpretation.poot(), None)

        ## attempting to approve with no owner_baton or bunk owner_baton should fail
        self.assertRaises(interpretation.BadOwnerBaton, interpretation.approve, i, None)
        self.assertRaises(interpretation.BadOwnerBaton, interpretation.approve, i, "blah blah blah")

        ## approving it should activate it
        interpretation.approve(i, i.owner_baton)
        self.assertTrue(i.is_active)
        for j in [interpretation.poot(str(i.key())), interpretation.list(str(i.key()))[0]]:
            self.assertEquals(i.is_active, j.is_active)

        ## now fetching without a key should bring it up
        self.assertEquals(interpretation.count(), 1)
        k = interpretation.poot(None)
        self.assertEquals(str(i.key()), str(k.key()))
        l = interpretation.list(None)
        self.assertEquals(str(i.key()), str(l[0].key()))

if __name__ == '__main__':
    unittest.main()
