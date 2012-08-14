#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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

# This is the main handler for awebshell
# This service converts commands to search strings, 
# 	usually to search an external website.

import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Command(db.Model): # Database model for commands
	name = db.StringProperty( # Name of the command
		required=True)
	createdDate = db.DateTimeProperty( # Date and time the command was created
		auto_now_add=True)
	searchString = db.StringProperty( # Search string for the command
		required=True)
	description = db.StringProperty() # Description for the command
	usage = db.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	self.response.headers['Content-Type'] = "text/html"
        self.response.out.write(
        	template.render('main.html', {}))

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
