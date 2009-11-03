#!/usr/bin/env python
# coding: utf-8

import logging
import unittest

## import from the app
from pypoot import interpretation

## app engine
from google.appengine.ext import db

def _stc(_type, _content):
    return interpretation.submit(title=u'untitled', author='anonymous', type=_type, content=_content)

class InterpretationTestCase(unittest.TestCase):
    def setUp(self):
        # Magic logging cleanup
        rootLogger = logging.getLogger()
        for handler in rootLogger.handlers:
            if isinstance(handler, logging.StreamHandler):
                rootLogger.removeHandler(handler)

        # clear existing interpretations
        for i in db.GqlQuery("SELECT * FROM Interpretation").fetch(1000):
            i.delete()

class TestOwnerBaton(unittest.TestCase):
    def test(self):
        owner_baton = interpretation._new_owner_baton()
        self.assertTrue(isinstance(owner_baton, str))

class TestImageValidation(InterpretationTestCase):
    def test_image_types(self):
        ext_mime = { 'jpg':  'image/jpeg',
                     'png':  'image/png',
                     'gif':  'image/gif',
                     'tiff': 'image/tiff',
                     'ico':  'image/x-icon',
                     'bmp':  'image/bmp' }

        for ext, mime_type in ext_mime.iteritems():
            i = _stc(interpretation.T_IMAGE, open('tests/test_good_image.' + ext).read())
            self.assertEquals(i.content_type, mime_type)
            self.assertTrue(isinstance(i.image_height, int))
            self.assertTrue(isinstance(i.image_width, int))

    def test_not_an_image(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_IMAGE, 'fnord')

    def test_wide_image(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_IMAGE, open('tests/test_wide_image.png').read())

    def test_tall_image(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_IMAGE, open('tests/test_tall_image.png').read())

    def test_giant_image(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_IMAGE, open('tests/test_giant_image.png').read())

class TestTextValidation(InterpretationTestCase):
    def test_text_type(self):
        i = _stc(interpretation.T_TEXT, 'foo')
        self.assertEquals(i.content_type, 'text/plain')

    def test_unicode(self):
        i = _stc(interpretation.T_TEXT, unicode.encode(u'わたし', 'utf-8'))
        self.assertEquals(i.content_type, 'text/plain')
        j = interpretation.poot({'key_string': str(i.key())})
        self.assertEquals(j.content, unicode.encode(u'わたし', 'utf-8'))

    def test_unprintable_text(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_TEXT, '\0')

class TestHtmlValidation(InterpretationTestCase):
    def test_html_type(self):
        i = _stc(interpretation.T_HTML, '<p>foo</p>')
        self.assertEquals(i.content_type, 'text/html')

    def test_unprintable_html(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_HTML, '<p>\0</p>')

    def test_script_tag(self):
        i = _stc(interpretation.T_HTML, '<script>foo</script>other')
        self.assertEquals(i.content, 'other')

    def test_style_attribute(self):
        i = _stc(interpretation.T_HTML, '<p style="foo: bar">foo</p>')
        self.assertEquals(i.content, '<p>foo</p>')

class TestJavascriptValidation(InterpretationTestCase):
    def test_javascript_type(self):
        i = _stc(interpretation.T_JAVASCRIPT, """
function pootpoot () {
    return { 'start': function (target) { },
             'stop':  function () { } };
}
""")
        self.assertEquals(i.content_type, 'application/x-javascript')

    def test_bunk_javascript(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_JAVASCRIPT, """
functon pootpoot () {
}
""")

    def test_pootpoot_arguments(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_JAVASCRIPT, """
function pootpoot (fnord) {
}
""")

    def test_pootpoot_andmore(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_JAVASCRIPT, """
function pootpoot () {
}

function notpootpoot () {
}
""")

    def test_globals_variables(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_JAVASCRIPT, """
var nastyglobal;
function pootpoot () { }
""")

    def test_top_level_statements(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, interpretation.T_JAVASCRIPT, """
foo="bar";
function pootpoot () { }
""")

class TestInterpretation(InterpretationTestCase):
    def test_bad_key(self):
        ## none
        self.assertEquals(interpretation.poot({'key_string':None}), None)
        self.assertEquals(interpretation.count({'key_string':None}), 0)
        self.assertEquals(interpretation.list_interpretations({'key_string':None}, 20), [])

        ## does not look like a real key
        self.assertEquals(interpretation.poot({'key_string':'asdf'}), None)
        self.assertEquals(interpretation.count({'key_string':'asdf'}), 0)
        self.assertEquals(interpretation.list_interpretations({'key_string':'asdf'}, 20), [])

        ## looks like a real key, but refers to no element
        self.assertEquals(interpretation.poot({'key_string':'aglwb290LXBvb3RyFAsSDkludGVycHJldGF0aW9uGAIM'}), None)
        self.assertEquals(interpretation.count({'key_string':'aglwb290LXBvb3RyFAsSDkludGVycHJldGF0aW9uGAIM'}), 0)
        self.assertEquals(interpretation.list_interpretations({'key_string':'aglwb290LXBvb3RyFAsSDkludGVycHJldGF0aW9uGAIM'}, 20), [])

    def test_bad_title_link(self):
        ## none
        self.assertEquals(interpretation.poot({'title_link':None}), None)
        self.assertEquals(interpretation.count({'title_link':None}), 0)
        self.assertEquals(interpretation.list_interpretations({'title_link':None}, 20), [])

        ## refers to no element
        self.assertEquals(interpretation.poot({'title_link':'foo-bar-baz'}), None)
        self.assertEquals(interpretation.count({'title_link':'foo-bar-baz'}), 0)
        self.assertEquals(interpretation.list_interpretations({'title_link':'foo-bar-baz'}, 20), [])

    def test_submit_disapprove(self):
        ## submitting an interpretation should create an inactive one
        i = _stc(interpretation.T_TEXT, 'blart')
        self.assertFalse(i.is_active)

        ## cannot disapprove with no owner_baton
        self.assertRaises(interpretation.BadOwnerBaton, interpretation.delete, i, None)
        ## cannot disapprove with bunk owner_baton
        self.assertRaises(interpretation.BadOwnerBaton, interpretation.delete, i, "blah blah blah")

        ## can delete with correct owner_baton
        interpretation.delete(i, i.owner_baton)

    def test_create_bad_type(self):
        self.assertRaises(interpretation.BunkInterpretation, _stc, 'foo', 'fnord')

    def test_title_link_collision(self):
        i = interpretation.submit(
                           title=u'untitled',
                           author='Anonymous',
                           type=interpretation.T_TEXT,
                           content='fnord')
        self.assertEquals(i.title_link, 'untitled')

        j = interpretation.submit(
                           title=u'untitled',
                           author='Anonymous',
                           type=interpretation.T_TEXT,
                           content='fnord')
        self.assertEquals(j.title_link, 'untitled-1')

    def test_submit_approve(self):
        ## submitting an interpretation should create an inactive one
        i = interpretation.submit(
                           title=u'Test',
                           author='Anonymous',
                           type=interpretation.T_TEXT,
                           content='fnord')
        self.assertFalse(i.is_active)

        ## fetching it is possible if specific key is provided
        self.assertEquals(interpretation.count({'key_string': str(i.key())}), 1)
        for j in [interpretation.poot({'key_string': str(i.key())}), interpretation.list_interpretations({'key_string': str(i.key())}, 20)[0]]:
            ## and the fetched interpretation should be identical
            self.assertEquals(i.title_link, j.title_link)
            self.assertEquals(i.title, j.title)
            self.assertEquals(i.type, j.type)
            self.assertEquals(i.content_type, j.content_type)
            self.assertEquals(i.content, j.content)
            self.assertEquals(i.is_active, j.is_active)
            self.assertEquals(i.author, j.author)

        ## even with a title_link (unique) fetch, can't see it yet:
        self.assertEquals(interpretation.count({'title_link': i.title_link}), 0)
        self.assertEquals(interpretation.list_interpretations({'title_link': i.title_link}, 20), [])
        self.assertEquals(interpretation.list_pages({'title_link': i.title_link}, 20), [])
        self.assertEquals(interpretation.poot({'title_link': i.title_link}), None)

        ## with an author fetch, can't see it yet:
        self.assertEquals(interpretation.count({'author': i.author}), 0)
        self.assertEquals(interpretation.list_interpretations({'author': i.author}, 20), [])
        self.assertEquals(interpretation.list_pages({'author': i.author}, 20), [])
        self.assertEquals(interpretation.poot({'author': i.author}), None)

        ## with a type fetch, can't see it yet:
        self.assertEquals(interpretation.count({'type': i.type}), 0)
        self.assertEquals(interpretation.list_interpretations({'type': i.type}, 20), [])
        self.assertEquals(interpretation.list_pages({'type': i.type}, 20), [])
        self.assertEquals(interpretation.poot({'type': i.type}), None)

        ## but fetching without a key should return nothing
        self.assertEquals(interpretation.count({}), 0)
        self.assertEquals(interpretation.list_interpretations({}, 20), [])
        self.assertEquals(interpretation.list_pages({}, 20), [])
        self.assertEquals(interpretation.poot({}), None)

        ## attempting to approve with no owner_baton or bunk owner_baton should fail
        self.assertRaises(interpretation.BadOwnerBaton, interpretation.approve, i, None)
        self.assertRaises(interpretation.BadOwnerBaton, interpretation.approve, i, "blah blah blah")

        ## approving it should activate it; should now be able to see it via title_link fetches
        interpretation.approve(i, i.owner_baton)
        self.assertTrue(i.is_active)
        self.assertEquals(interpretation.count({'title_link': i.title_link}), 1)
        self.assertEquals(interpretation.count({'author': i.author}), 1)
        for j in [interpretation.poot({'key_string': str(i.key())}), interpretation.list_interpretations({'key_string': str(i.key())}, 20)[0], interpretation.poot({'title_link': i.title_link}), interpretation.list_interpretations({'title_link': i.title_link}, 20)[0], interpretation.poot({'author': i.author}), interpretation.list_interpretations({'author': i.author}, 20)[0], interpretation.poot({'type': i.type}), interpretation.list_interpretations({'type': i.type}, 20)[0]]:
            self.assertEquals(i.is_active, j.is_active)

        ## now fetching without a key should bring it up
        self.assertEquals(interpretation.count({}), 1)
        k = interpretation.poot({})
        self.assertEquals(str(i.key()), str(k.key()))
        l = interpretation.list_interpretations({}, 20)
        self.assertEquals(str(i.key()), str(l[0].key()))
        lp = interpretation.list_pages({}, 20)
        self.assertEquals(lp[0]['page_number'], 1)
        self.assertEquals(lp[0]['offset_key_string'], str(i.key()))

class TestPagination(InterpretationTestCase):
    def test_basic_pagination(self):
        actual_count = 21
        for id in range(1, actual_count):
            i = _stc(interpretation.T_TEXT, str(id))
            interpretation.approve(i, i.owner_baton)

        for page_size in [1, 2, 3, 4, 5, 10, 20, 25]:
            looking_for = set(range(1, actual_count))
            pages = interpretation.list_pages({}, page_size)
            logging.info(repr(pages))

            for page in pages:
                logging.info('page %d of %d (size %d)' % (page['page_number'], len(pages), page_size))
                self.assert_(page['page_number'] > 0)
                l = interpretation.list_interpretations({'offset_key_string': page['offset_key_string']}, page_size)
                self.assert_(len(l) <= page_size)

                ## this will blow up if we get a duplicate during page-walking
                for i in l:
                    looking_for.remove(int(i.content))

            ## make sure we found every single interpretation
            self.assertEquals(len(looking_for), 0)
