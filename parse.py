#!/usr/bin/env python

import webapp2

class ParseHandler(webapp2.RequestHandler):
	def get(self, command):
		self.response.write(command)

class RedirectHandler(webapp2.RedirectHandler):
	def get(self):
		self.response.write(command)

def get_redirect_uri(handler, *args, **kwargs):
    return handler.uri_for('view', item=kwargs.get('item'))


app = webapp2.WSGIApplication([(r'/parse/(.*)', 
	webapp2.Route('/parse/<command>', ParseHandler, 'parse'),
	webapp2.Route('/parse/query=<command>', RedirectHandler, defaults={'uri': get_redirect_uri}))],
                              debug=True)
