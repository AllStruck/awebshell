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

# This is the ls (list) handler for awebshell.
# This is a special command not handled like other search commands.
# Here we present a template file which shows a list of commands, 
#   usually those matching what the user looks for, 
#	or if the ls command is used alone we list all commands.

import cgi
import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from command import Command

class ListHandler(webapp2.RequestHandler):
    def get(self, search):
    	if search:
    		commands = db.GqlQuery("SELECT * FROM Command")
    		results = []
    		for command in commands:
    			if (command.name.find(search) > -1) or\
    			(command.searchString.find(search) > -1):
    				results.append(command)
    			if command.description:
    				if command.description.find(search) > -1:
    					results.append(command)


    		#commands = db.GqlQuery("SELECT * FROM Command")
    	else:
    		results = db.GqlQuery("SELECT * FROM Command")

    	template_vars = {
    		'commands': results
    	}
    	self.response.headers['Content-Type'] = "text/html"
    	self.response.out.write(template.render('template/ls.html', template_vars))

app = webapp2.WSGIApplication([(r'/ls/(.*)', ListHandler)],
                              debug=True)

