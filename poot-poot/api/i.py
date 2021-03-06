#!/usr/bin/env python
"""fetch a single interpretation's content"""

## standard
import time
import re

## app engine
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

## this app
from pypoot import interpretation

EXPIRE = 86400 ## how long to let browsers cache the content, in seconds

class InterpretationContent(webapp.RequestHandler):
    """request handler for /i"""

    def get(self):
        """fetch the content of a single interpretation by key"""

        status       = None
        content      = None
        content_type = None
        i            = None

        match = re.search('/([^/]+)$', self.request.path)
        if match:
            key_string = match.group(1)
            i = interpretation.poot({ 'key_string': key_string })
        if i == None:
            status = 404
            content_type = 'text/plain'
            content      = "{\"error\":\"Not Found\"}"
        else:
            if 'Cache-Control' in self.response.headers:
                del self.response.headers['Cache-Control']
            self.response.headers.add_header('Cache-Control', 'public')
            self.response.headers.add_header('Expires',
                time.strftime('%a, %d %b %Y %H:%M:%S GMT',
                              time.localtime(time.time() + EXPIRE)))
            status       = 200
            content_type = i.content_type
            content      = i.content

        self.response.set_status(status)
        if 'Content-Type' in self.response.headers:
            del self.response.headers['Content-Type']
        self.response.headers.add_header('Content-Type', content_type)
        self.response.out.write(content)

APPLICATION = webapp.WSGIApplication([('/i/.*', InterpretationContent)],
                                     debug=True)

def main():
    """invoke the wsgi thingy"""
    run_wsgi_app(APPLICATION)

if __name__ == "__main__":
    main()
