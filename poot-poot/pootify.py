#!/usr/bin/env python
"""pootify a web page"""

## standard
import re

## app engine
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch

## this app

class Pootifier(webapp.RequestHandler):
    """request handler for /pootify"""

    def get(self):
        """pootify a web page"""

        url = self.request.get('url')
        if not url:
            self.response.set_status(400)
            self.response.out.write('Huh?')
            return

        result  = urlfetch.fetch(url, follow_redirects=True)
        content = result.content
        if result.status_code == 200:
            content = re.compile('<head>', re.IGNORECASE).sub('<head><base href="' + str(url) + '"/>', content, 1)
            content = re.compile('</head>', re.IGNORECASE).sub('''
<script type="text/javascript" src="http://www.pootpoot.net/pootpoot.js"></script>
<script type="text/javascript">
var pootifier    = function () { pootify_document(document.body); };
var prior_onload = window.onload; 
if (typeof prior_onload != 'function') { 
    window.onload = pootifier;
} else { 
    window.onload = function() { 
        if (prior_onload) { 
            prior_onload(); 
        }
        pootifier(); 
    };
} 
</script>
</head>''', content, 1)

        self.response.set_status(result.status_code)
        self.response.out.write(content)

APPLICATION = webapp.WSGIApplication([('/pootify', Pootifier)], debug=True)

def main():
    """invoke the wsgi thingy"""
    run_wsgi_app(APPLICATION)

if __name__ == "__main__":
    main()
