#!/usr/bin/env python
"""datastore stuff related to interpretations"""

## standard
import random
from datetime import datetime

## app engine
from google.appengine.api import datastore_errors
from google.appengine.api import images
from google.appengine.ext import db

## this module
from pypoot import permalink

class Interpretation(db.Model):
    """interpretation model"""
    is_active    = db.BooleanProperty(required=True)
    type         = db.StringProperty(required=True,
                       choices=set(['image', 'javascript', 'text', 'html']))
    content_type = db.StringProperty(required=True, indexed=False)
    content      = db.BlobProperty(required=True)
    title        = db.StringProperty(required=True)
    title_link   = db.StringProperty(required=True)
    owner_baton  = db.StringProperty(required=True, indexed=False)
    author       = db.StringProperty(required=True)
    created_at   = db.DateTimeProperty(required=True)
    def decorated_location(self):
        """compute & return relative permalink path"""
        return "/interpretation/%s.html" % self.title_link
    def content_location(self):
        """compute & return relative content URI"""
        return "/i/%s" % self.key()

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

def poot(filters):
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

def count(filters):
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

def list(filters):
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

IMAGE_WIDTH_MAX  = 900
IMAGE_HEIGHT_MAX = 900
def _process_image(bytes):
    """process and validate the contents of an image interpretation"""

    height = None
    width  = None
    try:
        image  = images.Image(bytes)
        height = image.height
        width  = image.width
    except images.Error:
        raise BunkInterpretation()

    if (height > IMAGE_HEIGHT_MAX):
        raise BunkInterpretation()

    if (width > IMAGE_WIDTH_MAX):
        raise BunkInterpretation()

    ## note: cut & pasted from the innards of the Image API, because
    ## the API does not provide introspection into the content-type
    content_type = None
    size         = len(bytes)
    if size >= 6 and bytes.startswith("GIF"):
        content_type = 'image/gif'
    elif size >= 8 and bytes.startswith("\x89PNG\x0D\x0A\x1A\x0A"):
        content_type = 'image/png'
    elif size >= 2 and bytes.startswith("\xff\xD8"):
        content_type = 'image/jpeg'
    elif (size >= 8 and (bytes.startswith("II\x2a\x00") or
                         bytes.startswith("MM\x00\x2a"))):
        content_type = 'image/tiff'
    elif size >= 2 and bytes.startswith("BM"):
        content_type = 'image/bmp'
    elif size >= 4 and bytes.startswith("\x00\x00\x01\x00"):
        content_type = 'image/x-icon'
    else:
        raise BunkInterpretation()

    return { 'content_type': content_type }

def _process_text(bytes):
    """process and validate the contents of a text interpretation"""
    return { 'content_type': 'text/plain' }

def _process_html(bytes):
    """process and validate the contents of an html interpretation"""
    return { 'content_type': 'text/html' }

def _process_javascript(bytes):
    """process and validate the contents of a javascript interpretation"""
    return { 'content_type': 'application/x-javascript' }

PROCESSORS = {
    'image':      _process_image,
    'text':       _process_text,
    'html':       _process_html,
    'javascript': _process_javascript
}

def submit(**attributes):
    """save an interpretation"""

    if (attributes['type'] in PROCESSORS):
        attributes.update(PROCESSORS[attributes['type']](attributes['content']))

    try:
        i = Interpretation(
                is_active    = False,
                owner_baton  = _new_owner_baton(),
                title_link   = _make_title_link(attributes['title']),
                created_at   = datetime.utcnow(),
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
