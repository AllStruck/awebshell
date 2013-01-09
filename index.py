#!/usr/bin/env python
#
# Copyright 2012 AllStruck
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# This is the index (front page) handler for awebshell.
# Here we simply show the front page with a searc field, 
# 	and instruction and other information about the app.

# This service converts commands to search strings, 
# 	usually to search an external website.

import cgi
import webapp2
from google.appengine.ext.webapp import template
import datetime



class MainHandler(webapp2.RequestHandler):
    def get(self):
		if cgi.escape(self.request.get('try_again')):
			tryAgain = cgi.escape(self.request.get('try_again'))
		else:
			tryAgain = ""
		
		now = datetime.datetime.now()
		template_vars = {
			'tryAgain': tryAgain,
			'currentYear': now.year
		}
		self.response.headers['Content-Type'] = "text/html"
		self.response.out.write(template.render('template/index.html', template_vars))

app = webapp2.WSGIApplication([('/.*', MainHandler)],
                              debug=True)
