#!/usr/bin/env python
"""datastore stuff related to comments"""

## standard
from datetime import datetime

## app engine
from google.appengine.ext import db

class Comment(db.Model):
    """comment model"""
    is_active       = db.BooleanProperty(required=True)
    interpretation  = db.ReferenceProperty(required=True)
    content         = db.TextProperty(required=True)
    author          = db.StringProperty(required=True)
    created_at      = db.DateTimeProperty(required=True)

    def get_public_info(self):
        """compute & return API-visible data"""

        info = { 'author': self.author,
                 'created_at': str(self.created_at),
                 'content': self.content }

        return info

def count(interpretation):
    """count the comments associated with a given interpretation"""

    query = db.Query(Comment, True)
    query.filter('is_active', True)
    query.filter('interpretation', interpretation)

    return query.count(1000)

def list_comments(interpretation_key_string):
    """return all of the comments associated with a given interpretation"""

    query = db.Query(Comment, False)
    query.filter('is_active', True)
    query.filter('interpretation', db.Key(interpretation_key_string))

    return query.fetch(1000)

def submit (**attributes):
    """save a comment"""

    new_comment = Comment(is_active = True,
                          created_at = datetime.utcnow(),
                          **attributes)

    new_comment.put()
    return new_comment
