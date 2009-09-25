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
                       choices=set(['image', 'javascript', 'text', 'html']))
    content_type = db.StringProperty(required=True)
    content      = db.BlobProperty(required=True)
    title        = db.StringProperty(required=True)
    owner_baton  = db.StringProperty(required=True)
    author       = db.StringProperty(required=True)

class NoInterpretation(Exception):
    """no interpretation was available"""
    pass

class BunkInterpretation(Exception):
    """the interpretation cannot be validated"""
    pass

class BadOwnerBaton(Exception):
    """the owner baton doesn't match (permission denied)"""
    pass

def _new_owner_baton():
    """generate a new random owner_baton string"""
    owner_baton = ""
    for i in range(15):
        owner_baton += random.choice('abcdefghijklmnopqrstuvwxyx')
    return owner_baton

def poot(key_string=None):
    """interpretation fetching magic"""

    if (key_string != None):
        try:
            key = db.Key(key_string)
        except datastore_errors.BadKeyError:
            raise NoInterpretation()
    else:
        query = db.GqlQuery("SELECT __key__ "
                          + "FROM Interpretation WHERE is_active = TRUE")
        keys = query.fetch(1000)
        if len(keys) == 0:
            raise NoInterpretation()
        key = random.choice(keys)

    i = db.get(key)

    ## this can happen when a specific key is provided, but there's no
    ## such entity
    if (i == None):
        raise NoInterpretation()

    return i

def submit(**attributes):
    """save an interpretation"""
    try:
        i = Interpretation(
                is_active=False,
                owner_baton=_new_owner_baton(),
                **attributes)
    except datastore_errors.BadValueError:
        raise BunkInterpretation()
    i.put()
    return i

def approve(i, owner_baton):
    """mark an interpretation as approved"""
    if (i.owner_baton != owner_baton):
        raise BadOwnerBaton
    i.is_active = True
    i.put()
    return

def delete(i, owner_baton):
    """delete an interpretation"""
    if (i.owner_baton != owner_baton): 
        raise BadOwnerBaton
    i.delete()
    return
