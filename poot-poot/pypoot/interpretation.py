#!/usr/bin/env python
"""datastore stuff related to interpretations"""

## standard
import random
from datetime import datetime

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
    created_at   = db.DateTimeProperty(required=True)

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

    key = None
    if (key_string != None):
        try:
            key = db.Key(key_string)
        except datastore_errors.BadKeyError:
            return None
    else:
        query = db.GqlQuery("SELECT __key__ "
                          + "FROM Interpretation WHERE is_active = TRUE")
        keys = query.fetch(1000)
        if len(keys) == 0:
            return None
        key = random.choice(keys)

    i = db.get(key)

    ## this can happen when a specific key is provided, but there's no
    ## such entity
    if (i == None):
        return None

    return i

def count(key_string=None):
    """count interpretations"""

    if (key_string != None):
        key = None
        try:
            key = db.Key(key_string)
        except datastore_errors.BadKeyError:
            return 0

        if (db.get(key) == None):
            return 0
        return 1

    query = db.GqlQuery("SELECT __key__ "
                      + "FROM Interpretation WHERE is_active = TRUE")
    return query.count()

def list(key_string=None):
    """list interpretations"""

    if (key_string != None):
        key = None
        try:
            key = db.Key(key_string)
        except datastore_errors.BadKeyError:
            return []

        i = db.get(key)
        if (i == None):
            return []
        return [i]

    query = db.GqlQuery("SELECT * "
                      + "FROM Interpretation WHERE is_active = TRUE")
    return query.fetch(1000)

def submit(**attributes):
    """save an interpretation"""
    try:
        i = Interpretation(
                is_active=False,
                owner_baton=_new_owner_baton(),
                created_at=datetime.utcnow(),
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
