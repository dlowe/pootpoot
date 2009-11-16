#!/usr/bin/env python
"""fetch metadata describing a single random interpretation"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Feed(webapp.RequestHandler):
    """request handler for /list"""

    def get(self):
        """GET handler"""

        if 'Content-Type' in self.response.headers:
            del self.response.headers['Content-Type']
        self.response.headers.add_header('Content-Type', 'application/rss+xml')

        self.response.out.write("""
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <atom:link href="http://www.pootpoot.net/feeds/interpretations/" rel="self" type="application/rss+xml"/>
    <title>poot poot</title>
    <link>http://www.pootpoot.net/</link>
    <description>poot interpretations</description>
    <item>
       <title>Poot Does a Body Good sticker design</title>
       <guid>http://www.pootpoot.net/interpretation/poot-does-a-body-good-sticker-design.html</guid>
       <link>http://www.pootpoot.net/interpretation/poot-does-a-body-good-sticker-design.html</link>
       <description>
        &lt;img src="http://www.pootpoot.net/i/aglwb290LXBvb3RyFQsSDkludGVycHJldGF0aW9uGPlVDA" alt="Poot Does a Body Good sticker design" title="Poot Does a Body Good sticker design"&gt;
       </description>
    </item>
  </channel>
</rss>
""")

APPLICATION = webapp.WSGIApplication([
   ('/feeds/interpretations/.*', Feed)],
   debug=True)

def main():
    """invoke the wsgi thingy"""
    run_wsgi_app(APPLICATION)

if __name__ == "__main__":
    main()
