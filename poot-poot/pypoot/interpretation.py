#!/usr/bin/env python
"""datastore stuff related to interpretations"""

## standard
import random

## app engine
from google.appengine.api import datastore_errors
from google.appengine.ext import db

class Interpretation(db.Model):
    """interpretation model"""
    is_active    = db.BooleanProperty(required=True)
    type         = db.StringProperty(required=True,
                       choices=set(['image', 'javascript', 'text']))
    content_type = db.StringProperty(required=True)
    content      = db.BlobProperty(required=True)
    title        = db.StringProperty(required=True)

class NoInterpretation(Exception):
    """no interpretation was available"""
    pass

class BunkInterpretation(Exception):
    """the interpretation cannot be validated"""
    pass

def poot(key_string=None):
    """interpretation fetching magic"""
    if (key_string != None):
        key = db.Key(key_string)
    else:
        query = db.GqlQuery("SELECT __key__ "
                          + "FROM Interpretation WHERE is_active = TRUE")
        keys = query.fetch(1000)
        if len(keys) == 0:
            raise NoInterpretation()
        key = random.choice(keys)

    i = db.get(key)
    return i

def submit(**attributes):
    """save an interpretation"""
    try:
        i = Interpretation(is_active=False, **attributes)
    except datastore_errors.BadValueError:
        raise BunkInterpretation()
    i.put()
    return i

def approve(i):
    """mark an interpretation as approved"""
    i.is_active = True
    i.put()
    return
