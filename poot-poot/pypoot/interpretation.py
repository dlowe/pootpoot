#!/usr/bin/env python
"""datastore stuff related to interpretations"""

## standard
import random
from datetime import datetime

## app engine
from google.appengine.api import datastore_errors
from google.appengine.ext import db

## this module
from pypoot import permalink

class Interpretation(db.Model):
    """interpretation model"""
    is_active    = db.BooleanProperty(required=True)
    type         = db.StringProperty(required=True,
                       choices=set(['image', 'javascript', 'text', 'html']))
    content_type = db.StringProperty(required=True)
    content      = db.BlobProperty(required=True)
    title        = db.StringProperty(required=True)
    title_link   = db.StringProperty(required=True)
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

def _make_title_link(title):
    """generate a new permalink from the title"""
    generator = permalink.phrase_link_generator(title)
    for link in generator:
        query = db.GqlQuery("SELECT __key__ "
                          + "FROM Interpretation WHERE title_link = :1", link)
        if query.count() == 0:
            return link

def poot(filters={}):
    """interpretation fetching magic"""

    if ('key_string' in filters):
        try:
            key = db.Key(filters["key_string"])
        except datastore_errors.BadKeyError:
            return None
    else:
        query = db.Query(Interpretation, True).filter('is_active', True)
        if ('title_link' in filters):
            query = query.filter('title_link', filters['title_link'])
        keys = query.fetch(1000)
        if len(keys) == 0:
            return None
        key = random.choice(keys)

    try:
        i = Interpretation.get(key)
    except datastore_errors.BadKeyError:
        return None

    ## this can happen when a specific key is provided, but there's no
    ## such entity
    if (i == None):
        return None

    return i

def count(filters={}):
    """count interpretations"""

    if ('key_string' in filters):
        key = None
        try:
            key = db.Key(filters['key_string'])
            if (Interpretation.get(key) == None):
                return 0
            return 1
        except datastore_errors.BadKeyError:
            return 0

    query = db.Query(Interpretation, True).filter('is_active', True)
    if ('title_link' in filters):
        query = query.filter('title_link', filters['title_link'])
    return query.count()

def list(filters={}):
    """list interpretations"""

    if ('key_string' in filters):
        key = None
        try:
            key = db.Key(filters['key_string'])
            i = Interpretation.get(key)
            if (i == None):
                return []
            return [i]
        except datastore_errors.BadKeyError:
            return []

    query = db.Query(Interpretation, False).filter('is_active', True)
    if ('title_link' in filters):
        query = query.filter('title_link', filters['title_link'])

    return query.fetch(1000)

def submit(**attributes):
    """save an interpretation"""
    try:
        i = Interpretation(
                is_active=False,
                owner_baton=_new_owner_baton(),
                title_link=_make_title_link(attributes['title']),
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
