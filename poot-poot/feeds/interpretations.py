#!/usr/bin/env python
"""fetch metadata describing a single random interpretation"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pypoot import interpretation
from pypoot import integration

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
    <atom:link href="%sfeeds/interpretations/" rel="self" type="application/rss+xml"/>
    <title>poot poot</title>
    <link>%s</link>
    <description>poot interpretations</description>
""" % (integration.INTEGRATIONS['APP_ROOT_URL'], integration.INTEGRATIONS['APP_ROOT_URL']))

        interpretations = interpretation.list_interpretations({}, 1000)
        interpretations.reverse()
        for i in interpretations:
            description = i.title
            if i.type == interpretation.T_IMAGE:
                description = "&lt;img src=\"%si/%s\" " % (integration.INTEGRATIONS['APP_ROOT_URL'],
                    i.key())
                description += "alt=\"%s\" title=\"%s\"&gt;" % (i.title, i.title)

            self.response.out.write("""
    <item>
     <title>%s</title>
     <guid>%sinterpretation/%s.html</guid>
     <link>%sinterpretation/%s.html</link>
     <description>%s</description>
    </item>
""" % (i.title, integration.INTEGRATIONS['APP_ROOT_URL'], i.title_link,
       integration.INTEGRATIONS['APP_ROOT_URL'], i.title_link, description))

        self.response.out.write("""
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
