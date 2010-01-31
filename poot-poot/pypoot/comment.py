#!/usr/bin/env python
"""datastore stuff related to comments"""

## app engine
from google.appengine.ext import db

class Comment(db.Model):
    """comment model"""
    is_active       = db.BooleanProperty(required=True)
    interpretation  = db.ReferenceProperty(required=True)
    content         = db.TextProperty(required=True)
    author          = db.StringProperty(required=True)
    created_at      = db.DateTimeProperty(required=True)

def count(interpretation_object):
    """count the comments associated with a given interpretation"""

    query = db.Query(Comment, True)
    query.filter('interpretation_key', interpretation_object)

    return query.count()
