#!/usr/bin/env python
"""fetch metadata describing a single random interpretation"""

## app engine
from google.appengine.ext import webapp

## this app
from pypoot import json
from pypoot import comment
from pypoot import interpretation

class MalformedRequest(Exception):
    """missing a require parameter, etc"""
    pass

class APIRequestHandler(webapp.RequestHandler):
    """class implementing general logic for API methods"""

    def _data(self):
        """implement in sublcass!"""
        pass

    def _logic(self, data):
        """implement in subclass!"""
        pass

    def api_worker(self):
        """generic flow for API methods..."""

        data    = None
        status  = None
        content = None
        try:
            data = self._data()
        except MalformedRequest:
            status  = 403
            content = { 'error': 'malformed request' }
        except interpretation.BunkInterpretation, error:
            status  = 400
            content = { 'error': str(error) }
        except comment.BunkComment, error:
            status  = 400
            content = { 'error': str(error) }
        except interpretation.BadOwnerBaton:
            status  = 403
            content = { 'error': 'Bad owner baton given' }
        else:
            (status, content) = self._logic(data)

        self.response.set_status(status)
        if 'Content-Type' in self.response.headers:
            del self.response.headers['Content-Type']
        self.response.headers.add_header('Content-Type', 'text/plain')

        self.response.out.write(json.ify(content))
