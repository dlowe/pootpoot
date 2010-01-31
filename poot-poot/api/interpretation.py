#!/usr/bin/env python
"""fetch metadata describing a single random interpretation"""

## app engine
from google.appengine.api.labs import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

## this app
from api import api_request_handler
from pypoot import interpretation

def _get_filter_arguments(request):
    """turn interpretation filter arguments into a dictionary"""
    filters = {}

    for name in interpretation.FILTERS:
        if request.get(name):
            filters[name] = request.get(name)

    return filters

class List(api_request_handler.APIRequestHandler):
    """request handler for /list"""

    def get(self):
        """GET handler"""
        self.api_worker()

    def _data(self):
        """fetch list of matching interpretations"""
        if not self.request.get('items'):
            raise api_request_handler.MalformedRequest()
        return interpretation.list_interpretations(_get_filter_arguments(self.request),
            int(self.request.get('items')))

    def _logic(self, interpretation_list):
        """convert empty set to 404, package the rest"""
        if interpretation_list == []:
            status  = 404
            content = { 'error': 'Not Found' }
        else:
            status  = 200
            content = []
            for i in interpretation_list:
                content.append(i.get_public_info())
        return (status, content)

class ListPages(api_request_handler.APIRequestHandler):
    """request handler for /list_pages"""

    def get(self):
        """GET handler"""
        self.api_worker()

    def _data(self):
        """fetch list of pages of matching interpretations"""
        if not self.request.get('items'):
            raise api_request_handler.MalformedRequest()
        return interpretation.list_pages(_get_filter_arguments(self.request),
            int(self.request.get('items')))

    def _logic(self, page_list):
        """convert empty set to 404, package the rest"""
        if page_list == []:
            status  = 404
            content = { 'error': 'Not Found' }
        else:
            status  = 200
            content = page_list
        return (status, content)

class Count(api_request_handler.APIRequestHandler):
    """request handler for /count"""

    def get(self): 
        """GET handler"""
        self.api_worker()

    def _data(self):
        """fetch count of matching interpretations"""
        return interpretation.count(_get_filter_arguments(self.request))

    def _logic(self, count):
        """..."""
        return (200, { 'count': str(count) })

class Poot(api_request_handler.APIRequestHandler):
    """request handler for /poot"""

    def get(self):
        """GET handler"""
        self.api_worker()

    def _data(self):
        """fetch random interpretation"""
        return interpretation.poot(_get_filter_arguments(self.request))

    def _logic(self, i):
        """convert no interpretation found to 404"""
        if i == None:
            status = 404
            content = { 'error': 'Not Found' }
        else:
            status  = 200
            content = i.get_public_info()
        return (status, content)

class Submit(api_request_handler.APIRequestHandler):
    """request handler for /submit"""

    def post(self):
        """POST handler"""
        self.api_worker()

    def _data(self):
        """submit a new interpretation"""
        i = interpretation.submit(
                 title=self.request.get('title'),
                 author=self.request.get('author'),
                 type=self.request.get('type'),
                 content=self.request.get('content'))
        task = taskqueue.Task(
            method='GET',
            params={'key_string': str(i.key())})
        task.add(queue_name='new-interpretation')
        return i

    def _logic(self, i):
        """..."""
        return (200, { 'key_string': str(i.key()),
                       'owner_baton': i.owner_baton })

class Approve(api_request_handler.APIRequestHandler):
    """request handler for /approve"""

    def post(self):
        """POST handler"""
        self.api_worker()

    def _data(self):
        """fetch and approve by key"""
        i = interpretation.poot(
            { 'key_string': self.request.get('key_string') })
        if i != None:
            interpretation.approve(i, self.request.get('owner_baton'))
        return i

    def _logic(self, i):
        """convert None to 404"""
        if i == None:
            status = 404
            content = { 'error': 'Not Found' }
        else:
            status  = 200
            content = i.get_public_info()
        return (status, content)

class Disapprove(api_request_handler.APIRequestHandler):
    """request handler for /disapprove"""

    def post(self):
        """POST handler"""
        self.api_worker()

    def _data(self):
        """fetch and delete by key"""
        i = interpretation.poot(
            { 'key_string': self.request.get('key_string') })
        if i != None:
            interpretation.delete(i, self.request.get('owner_baton'))
        return i

    def _logic(self, i):
        """convert None to 404"""
        if i == None:
            status  = 404
            content = { 'error': 'Not Found' }
        else:
            status  = 200
            content = i.get_public_info()
        return (status, content)

APPLICATION = webapp.WSGIApplication([
   ('/poot', Poot),
   ('/list', List),
   ('/list_pages', ListPages),
   ('/count', Count),
   ('/submit', Submit),
   ('/approve', Approve),
   ('/disapprove', Disapprove)],
   debug=True)

def main():
    """invoke the wsgi thingy"""
    run_wsgi_app(APPLICATION)

if __name__ == "__main__":
    main()
