#!/usr/bin/env python
"""pootify a web page"""

## standard
import re
import logging
import urlparse
import urllib

## app engine
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch

## this app
from pypoot import integration

class Pootifier(webapp.RequestHandler):
    """request handler for /pootify"""

    def get(self):
        """pootify a web page"""

        ## no url: back to the start!
        url = self.request.get('url')
        if not url:
            self.redirect("/pootify.html")
            return

        ## parse url, or back to the start!
        try:
            parts = urlparse.urlparse(url)
            if not parts.scheme:
                raise Exception("argh!")
        except:
            self.redirect("/pootify.html")
            return

        ## fetch content or explode
        try:
            result = urlfetch.fetch(url, follow_redirects=False)
        except:
            self.response.set_status(500)
            self.response.out.write("argh!")
            return

        ## make redirection the client's job
        if result.status_code in (301, 302):
            self.redirect(integration.INTEGRATIONS['APP_ROOT_URL' ] + 'pootify?url='
                + urllib.quote(result.headers['location']))
            return

        ## if we got served something that's not html, just return it
        if not result.headers['content-type'].startswith('text/html'):
            self.response.set_status(result.status_code)
            self.response.out.write(result.content)
            return

        ## We've got html, let's see what kind of damage we can do....
        content = result.content.decode('utf-8')

        ## stuff a header into pages which don't already have one
        if not re.compile('<head>', re.IGNORECASE).search(content):
            content = re.compile('<html>', re.IGNORECASE).sub('<html><head></head>', content, 1)

        ## base adjustment
        base_url = urlparse.urlunparse((parts[0], parts[1], parts[2], '', '', ''))
        content = re.compile('<head>', re.IGNORECASE).sub('<head><base href="' + base_url + '"/>', content, 1)

        ## insert the script
        content = re.compile('</head>', re.IGNORECASE).sub('''
<script type="text/javascript" src="%spootpoot.js"></script>
<script type="text/javascript">
function pootifier () {
    pootify_document(document.body);
    pootify_links(document.body, '%s', '%s');
}

function add_pootifier () {
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
}
</script>
</head>''' % (integration.INTEGRATIONS['APP_ROOT_URL'], base_url, integration.INTEGRATIONS['APP_ROOT_URL'] + 'pootify?url='), content, 1)

        ## call the script
        if re.compile('</body>', re.IGNORECASE).search(content):
            content = re.compile('</body>', re.IGNORECASE).sub('''
<script type="text/javascript">
add_pootifier();
</script>
</body>''', content, 1)
            pass
        else:
            content = re.compile('</head>', re.IGNORECASE).sub('''
<script type="text/javascript">
add_pootifier();
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
