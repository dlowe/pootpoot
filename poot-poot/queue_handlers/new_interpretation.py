#!/usr/bin/env python
"""fetch a single interpretation's content"""

## standard
import re
import logging
import urllib

## app engine
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

## this app
from pypoot import interpretation
from pypoot import integration

class NewInterpretation(webapp.RequestHandler):
    """request handler for /_ah/queue/new-interpretation"""

    def get(self):
        """offline processing of a new interpretation"""

        i = interpretation.poot({ 'key_string': self.request.get('key_string') })

        if (('BITLY_KEY' in integration.INTEGRATIONS)
          and ('BITLY_LOGIN' in integration.INTEGRATIONS)):
            url = 'http://api.bit.ly/shorten?version=2.0.1&login=%s&apiKey=%s&longUrl=%s' % (
                integration.INTEGRATIONS['BITLY_LOGIN'],
                integration.INTEGRATIONS['BITLY_KEY'],
                urllib.quote_plus('http://www.pootpoot.net/interpretation/%s.html' % i.title_link))
            result = urlfetch.fetch(url, method='GET')
            if result.status_code == 200:
                ## "shortUrl": "http://bit.ly/1R2vI8",
                match = re.search('shortUrl.*"(http://[^"]*)"', result.content)
                if match:
                    i.short_url = match.group(1)
                    logging.warn(i.short_url)
                    i.put()

        self.response.set_status(200)
        self.response.out.write('ok')

APPLICATION = webapp.WSGIApplication([('/_ah/queue/new-interpretation', NewInterpretation)],
                                     debug=True)

def main():
    """invoke the wsgi thingy"""
    run_wsgi_app(APPLICATION)

if __name__ == "__main__":
    main()
