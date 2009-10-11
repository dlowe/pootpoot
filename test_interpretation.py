#!/usr/bin/env python

import logging
import sys
import unittest
sys.path = [ './poot-poot' ] + sys.path

## import from the app
from pypoot import interpretation

## app engine
from google.appengine.ext import db

class TestOwnerBaton(unittest.TestCase):
    def test(self):
        owner_baton = interpretation._new_owner_baton()
        self.assertTrue(isinstance(owner_baton, str))

class TestImageValidation(unittest.TestCase):
    def setUp(self):
        # Magic logging cleanup
        rootLogger = logging.getLogger()
        for handler in rootLogger.handlers:
            if isinstance(handler, logging.StreamHandler):
                rootLogger.removeHandler(handler)

    def test_image_types(self):
        ext_mime = { 'jpg':  'image/jpeg',
                     'png':  'image/png',
                     'gif':  'image/gif',
                     'tiff': 'image/tiff',
                     'ico':  'image/x-icon',
                     'bmp':  'image/bmp' }

        for ext, mime_type in ext_mime.iteritems():
            i = interpretation.submit(title=u'Test' + ext, 
                                  author=ext,
                                  type='image',
                                  content=open('test_good_image.' + ext).read())
            self.assertEquals(i.content_type, mime_type)

    def test_not_an_image(self):
        self.assertRaises(interpretation.BunkInterpretation, interpretation.submit,
                               title=u'Test',
                               author='Anonymous',
                               type='image',
                               content='fnord')

class TestInterpretation(unittest.TestCase):
    def setUp(self):
        # Magic logging cleanup
        rootLogger = logging.getLogger()
        for handler in rootLogger.handlers:
            if isinstance(handler, logging.StreamHandler):
                rootLogger.removeHandler(handler)

        for i in db.GqlQuery("SELECT * FROM Interpretation").fetch(1000):
            i.delete()

    def test_bad_key(self):
        ## none
        self.assertEquals(interpretation.poot({'key_string':None}), None)
        self.assertEquals(interpretation.count({'key_string':None}), 0)
        self.assertEquals(interpretation.list({'key_string':None}), [])

        ## does not look like a real key
        self.assertEquals(interpretation.poot({'key_string':'asdf'}), None)
        self.assertEquals(interpretation.count({'key_string':'asdf'}), 0)
        self.assertEquals(interpretation.list({'key_string':'asdf'}), [])

        ## looks like a real key, but refers to no element
        self.assertEquals(interpretation.poot({'key_string':'aglwb290LXBvb3RyFAsSDkludGVycHJldGF0aW9uGAIM'}), None)
        self.assertEquals(interpretation.count({'key_string':'aglwb290LXBvb3RyFAsSDkludGVycHJldGF0aW9uGAIM'}), 0)
        self.assertEquals(interpretation.list({'key_string':'aglwb290LXBvb3RyFAsSDkludGVycHJldGF0aW9uGAIM'}), [])

    def test_bad_title_link(self):
        ## none
        self.assertEquals(interpretation.poot({'title_link':None}), None)
        self.assertEquals(interpretation.count({'title_link':None}), 0)
        self.assertEquals(interpretation.list({'title_link':None}), [])

        ## refers to no element
        self.assertEquals(interpretation.poot({'title_link':'foo-bar-baz'}), None)
        self.assertEquals(interpretation.count({'title_link':'foo-bar-baz'}), 0)
        self.assertEquals(interpretation.list({'title_link':'foo-bar-baz'}), [])

    def test_submit_disapprove(self):
        ## submitting an interpretation should create an inactive one
        i = interpretation.submit(
                            title=u'Test',
                            author='Anonymous',
                            type='text',
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
                               title=u'Test',
                               author='Anonymous',
                               type='foo',
                               content='fnord')

    def test_title_link_collision(self):
        i = interpretation.submit(
                           title=u'untitled',
                           author='Anonymous',
                           type='text',
                           content='fnord')
        self.assertEquals(i.title_link, 'untitled')

        j = interpretation.submit(
                           title=u'untitled',
                           author='Anonymous',
                           type='text',
                           content='fnord')
        self.assertEquals(j.title_link, 'untitled-1')

    def test_submit_approve(self):
        ## submitting an interpretation should create an inactive one
        i = interpretation.submit(
                           title=u'Test',
                           author='Anonymous',
                           type='text',
                           content='fnord')
        self.assertFalse(i.is_active)

        ## fetching it is possible if specific key is provided
        self.assertEquals(interpretation.count({'key_string': str(i.key())}), 1)
        for j in [interpretation.poot({'key_string': str(i.key())}), interpretation.list({'key_string': str(i.key())})[0]]:
            ## and the fetched interpretation should be identical
            self.assertEquals(i.title_link, j.title_link)
            self.assertEquals(i.title, j.title)
            self.assertEquals(i.type, j.type)
            self.assertEquals(i.content_type, j.content_type)
            self.assertEquals(i.content, j.content)
            self.assertEquals(i.is_active, j.is_active)

        ## even with a title_link (unique) fetch, can't see it yet:
        self.assertEquals(interpretation.count({'title_link': i.title_link}), 0)
        self.assertEquals(interpretation.list({'title_link': i.title_link}), [])
        self.assertEquals(interpretation.poot({'title_link': i.title_link}), None)

        ## but fetching without a key should return nothing
        self.assertEquals(interpretation.count({}), 0)
        self.assertEquals(interpretation.list({}), [])
        self.assertEquals(interpretation.poot({}), None)

        ## attempting to approve with no owner_baton or bunk owner_baton should fail
        self.assertRaises(interpretation.BadOwnerBaton, interpretation.approve, i, None)
        self.assertRaises(interpretation.BadOwnerBaton, interpretation.approve, i, "blah blah blah")

        ## approving it should activate it; should now be able to see it via title_link fetches
        interpretation.approve(i, i.owner_baton)
        self.assertTrue(i.is_active)
        self.assertEquals(interpretation.count({'title_link': i.title_link}), 1)
        for j in [interpretation.poot({'key_string': str(i.key())}), interpretation.list({'key_string': str(i.key())})[0], interpretation.poot({'title_link': i.title_link}), interpretation.list({'title_link': i.title_link})[0]]:
            self.assertEquals(i.is_active, j.is_active)

        ## now fetching without a key should bring it up
        self.assertEquals(interpretation.count({}), 1)
        k = interpretation.poot({})
        self.assertEquals(str(i.key()), str(k.key()))
        l = interpretation.list({})
        self.assertEquals(str(i.key()), str(l[0].key()))

if __name__ == '__main__':
    unittest.main()
