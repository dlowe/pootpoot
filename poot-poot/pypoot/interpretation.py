#!/usr/bin/env python

from google.appengine.ext import db

class Interpretation(db.Model):
    is_active    = db.BooleanProperty(required=True)
    type         = db.StringProperty(required=True, choices=set(['image', 'javascript', 'text']))
    content_type = db.StringProperty(required=True)
    content      = db.BlobProperty(required=True)
