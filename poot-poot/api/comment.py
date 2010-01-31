#!/usr/bin/env python
"""fetch metadata describing a single random interpretation"""

## app engine
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

## this app
from api import api_request_handler
from pypoot import comment

class CommentList(api_request_handler.APIRequestHandler):
    """request handler for /comment_list"""

    def get(self):
        """GET handler"""
        self.api_worker()

    def _data(self):
        """fetch list of matching comments"""
        if not self.request.get('interpretation_key_string'):
            raise api_request_handler.MalformedRequest()
        return comment.list_comments(self.request.get('interpretation_key_string'))

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

class Submit(api_request_handler.APIRequestHandler):
    """request handler for /comment_submit"""

    def post(self):
        """POST handler"""
        self.api_worker()

    def _data(self):
        """submit a new comment"""
        new_comment = comment.submit(
              author=self.request.get('author'),
              content=self.request.get('content'),
              interpretation_key_string=self.request.get('interpretation_key_string'))
        return new_comment

    def _logic(self, new_comment):
        """..."""
        return (200, { 'key_string': str(new_comment.key()) })

APPLICATION = webapp.WSGIApplication([
   ('/comment_list', CommentList),
   ('/comment_submit', Submit)],
   debug=True)

def main():
    """invoke the wsgi thingy"""
    run_wsgi_app(APPLICATION)

if __name__ == "__main__":
    main()
