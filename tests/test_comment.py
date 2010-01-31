#!/usr/bin/env python
# coding: utf-8

import logging
import unittest

## import from the app
from pypoot import interpretation
from pypoot import comment

## app engine
from google.appengine.ext import db

class CommentTestCase(unittest.TestCase):
    def setUp(self):
        # Magic logging cleanup
        rootLogger = logging.getLogger()
        for handler in rootLogger.handlers:
            if isinstance(handler, logging.StreamHandler):
                rootLogger.removeHandler(handler)

        # clear existing interpretations
        for i in db.Query(interpretation.Interpretation, False).fetch(1000):
            i.delete()

        # clear existing comments
        for i in db.Query(comment.Comment, False).fetch(1000):
            i.delete()

class TestComment(CommentTestCase):
    def test_submit(self):
        i = interpretation.submit(
                           title=u'untitled',
                           author='Anonymous',
                           type=interpretation.T_TEXT,
                           content='fnord')

        self.assertEquals(comment.count(i), 0)

        c = comment.submit(author='Anonymous', content='yadda', interpretation_key_string=str(i.key()))

        self.assertEquals(comment.count(i), 1)

        l = comment.list_comments(str(i.key()))
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0].is_active, True)
        self.assertEquals(l[0].author, 'Anonymous')
        self.assertEquals(l[0].content, 'yadda')
