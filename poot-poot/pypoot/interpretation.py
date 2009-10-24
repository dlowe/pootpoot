#!/usr/bin/env python
"""datastore stuff related to interpretations"""

## standard
import urllib
import logging
import unicodedata
import random
from datetime import datetime

## app engine
from google.appengine.api import datastore_errors
from google.appengine.api import images
from google.appengine.ext import db

## this module
from pypoot import permalink
from pypoot import feedparser
from pypoot import jsparser

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
    image_height = db.IntegerProperty(required=False, indexed=False)
    image_width  = db.IntegerProperty(required=False, indexed=False)
    def decorated_location(self):
        """compute & return relative permalink path"""
        return "/interpretation/%s.html" % self.title_link
    def content_location(self):
        """compute & return relative content URI"""
        return "/i/%s" % self.key()
    def author_location(self):
        """compute & return relative author list URI"""
        return "/list_interpretations/a/%s/" % urllib.quote(self.author)

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

def _apply_filters(query, filters):
    """modify a Query object by the general-case interpretation filters"""
    if 'key_string' in filters:
        if filters['key_string'] == None:
            raise datastore_errors.BadKeyError()
        query = query.filter('__key__', db.Key(filters['key_string']))
    else:
        query = query.filter('is_active', True)

    if 'title_link' in filters:
        query = query.filter('title_link', filters['title_link'])
    if 'author' in filters:
        query = query.filter('author', filters['author'])
    if 'offset_key_string' in filters:
        query = query.filter('__key__ >=', db.Key(filters['offset_key_string']))

    query.order('__key__')

    return query

def poot(filters):
    """interpretation fetching magic"""

    try:
        query = _apply_filters(db.Query(Interpretation, True), filters)
    except datastore_errors.BadKeyError:
        return None

    keys = query.fetch(1000)
    if (len(keys)) == 0:
        return None

    return Interpretation.get(random.choice(keys))

def count(filters):
    """count interpretations"""

    try:
        query = _apply_filters(db.Query(Interpretation, True), filters)
    except datastore_errors.BadKeyError:
        return 0

    return query.count()

INTERPRETATIONS_PER_PAGE = 20
def list(filters, interpretations_per_page=INTERPRETATIONS_PER_PAGE):
    """list interpretations"""

    try:
        query = _apply_filters(db.Query(Interpretation, False), filters)
    except datastore_errors.BadKeyError:
        return []

    return query.fetch(interpretations_per_page)

def list_pages(filters, interpretations_per_page=INTERPRETATIONS_PER_PAGE):
    """get list of pages"""

    try:
        query = _apply_filters(db.Query(Interpretation, True), filters)
    except datastore_errors.BadKeyError:
        return []

    index = 0
    pages = []
    for key in query.fetch(1000):
        if (index % interpretations_per_page) == 0:
            pages.append({
                'page_number': (index // interpretations_per_page) + 1,
                'offset_key_string': str(key) })
        index += 1

    return pages

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
        raise BunkInterpretation("Content doesn't look like an image to me")

    if (height > IMAGE_HEIGHT_MAX):
        raise BunkInterpretation("Image too tall (limit is %d pixels)"
            % IMAGE_HEIGHT_MAX)

    if (width > IMAGE_WIDTH_MAX):
        raise BunkInterpretation("Image too wide (limit is %d pixels)"
            % IMAGE_WIDTH_MAX)

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
        raise BunkInterpretation("Content doesn't look like an image to me")

    return { 'content_type': content_type,
             'image_height': height,
             'image_width':  width }

def _assert_printable(bytes):
    """raise BunkInterpretation if non-printable characters are in the input"""

    for char in bytes.decode('utf-8'):
        if (unicodedata.category(char) == 'Cc') and not (ord(char)
          in (9, 10, 11, 13)):
            raise BunkInterpretation("Non-printable characters in the content")

def _process_text(bytes):
    """process and validate the contents of a text interpretation"""

    _assert_printable(bytes)

    return { 'content_type': 'text/plain' }

def _process_html(bytes):
    """process and validate the contents of an html interpretation"""

    _assert_printable(bytes)

    bytes = feedparser._sanitizeHTML(bytes, 'utf-8')

    logging.warn(bytes)

    return { 'content_type': 'text/html',
             'content':      bytes }

def _process_javascript(bytes):
    """process and validate the contents of a javascript interpretation"""

    ## attempt to parse
    parsed = None
    try:
        parsed = jsparser.parse(bytes)
    except jsparser.SyntaxError_, error:
        raise BunkInterpretation("Can't parse your javascript: " + str(error))

    ## ensure that we have a function 'pootpoot' taking zero arguments
    found_pootpoot = 0
    for function in parsed.funDecls:
        if function.name == 'pootpoot' and function.params == []:
            found_pootpoot = 1

    if not found_pootpoot:
        raise BunkInterpretation("Can't find function pootpoot ()")

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
    except datastore_errors.BadValueError, error:
        raise BunkInterpretation(str(error))

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
