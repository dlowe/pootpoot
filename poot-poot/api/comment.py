#!/usr/bin/env python
"""fetch metadata describing a single random interpretation"""

## app engine
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

## this app
from api import api_request_handler
from pypoot import comment

class Comments(api_request_handler.APIRequestHandler):
    """request handler for /comment_list"""

    def get(self):
        """GET handler"""
        self.api_worker()

    def _data(self):
        """fetch list of matching comments"""
        if not self.request.get('interpretation_key'):
            raise api_request_handler.MalformedRequest()
        return comment.list_comments(self.request.get('interpretation_key'))

    def _logic(self, comment_list):
        """convert empty set to 404, package the rest"""
        if comment_list == []:
            status  = 404
            content = { 'error': 'Not Found' }
        else:
            status  = 200
            content = []
            for i in comment_list:
                content.append(i.get_public_info())
        return (status, content)

APPLICATION = webapp.WSGIApplication([
   ('/comment_list', Comments)],
   debug=True)

def main():
    """invoke the wsgi thingy"""
    run_wsgi_app(APPLICATION)

if __name__ == "__main__":
    main()
