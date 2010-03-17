#!/usr/bin/env python
"""pootify a web page"""

## standard
import re
import logging

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

        url = self.request.get('url')
        if not url:
            self.response.set_status(400)
            self.response.out.write('Huh?')
            return

        result    = urlfetch.fetch(url, follow_redirects=True)
        content   = result.content

        ## if we got redirected, switch to the final url
        if result.final_url:
            url = result.final_url

        parts = str(url).split('/')

        ## if the url had exactly 3 parts, assume it's unslashed domain (http://www.pootpoot.net)
        ## add a slash and re-split
        if len(parts) == 3:
            url = url + '/'
            parts = str(url).split('/')

        ## build a base url for the proxied page...
        base_url = '/'.join(parts[:-1]) + '/'

        if result.status_code == 200:
            ## stuff a header into pages which don't already have one
            if not re.compile('<head>', re.IGNORECASE).search(content):
                content = re.compile('<html>', re.IGNORECASE).sub('<html><head></head>', content, 1)

            ## base adjustment
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
