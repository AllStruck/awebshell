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

# This is the parse handler for awebshell.
# Here we actually take in a command and decide how to handle it,
#   and in most cases the entire command is handled here.

from google.appengine.ext import db
import urllib
import webapp2
import logging
import httplib
import uuid
import types

from awebshell import WebShell, WebShellError, UnknownCommandError

from command import Command

# Main handler for the parser, handles first response decisions depending on command squence provided by user.
class ParseHandler(webapp2.RequestHandler):
	def __init__(self, *args, **kwargs):
		webapp2.RequestHandler.__init__(self, *args, **kwargs)
		self.__command_database = GqlCommandDatabase()
		self.__web_shell = WebShell(self.__command_database)
	def get(self, enteredCommand):
		if self.request.get('q'):
			enteredCommand = self.request.get('q') # Use q= gttp get var if supplied.

		#enteredCommand = enteredCommand.replace('+', ' ')
		#enteredCommand = enteredCommand.replace('&#43;', ' ')
		#enteredCommand = enteredCommand.replace('%20', ' ')

		enteredCommandString = urllib.quote(enteredCommand.encode('utf-8'), ' /') # Store string of entered command.
		enteredCommand = enteredCommand.split() # Split entered command into separate words.

		if len(enteredCommand) > 0:
			if enteredCommand[0].lower() == 'create': # User wants to create a command, let's try.
				self.response.write(create_new_command(enteredCommand))
			elif enteredCommand[0].lower() == 'ls': # User is performing a command search.
				search = enteredCommandString[3:]
				self.redirect('/ls/' + search)
			else: # User is performing a command, convert it into a URI and redirect to it.
				# Send hit to Google Analytics, since we're not displaying a page...
				thisUUID = uuid.uuid4()
				httplib.HTTPConnection('www.google-analytics.com/collect/?v=1&tid=UA-34105964-1&cid=thisUUID&an=awebshell&t=event&ec=parse&ea=redirected', 80, timeout=10)
				
				try:
					logging.info('enteredCommandString = ' + repr(enteredCommandString))
					final_url, can_inline = self.__web_shell.evaluate(enteredCommandString)
					self.redirect(final_url)
				except WebShellError, web_shell_error:
					exception_name = web_shell_error.__class__.__name__
					error_message = str(web_shell_error)
					logging.info('ERROR: ' + exception_name + ': ' + error_message)
					#TODO: do something about error, like display the error message and offer a new command entry
					
					
					self.redirect('http://google.com/search?q=' + urllib.quote(enteredCommandString)) #ZZZ default to google search on error.
				
				# logging.info("Redirecting to: " + redirectURI)
				# self.redirect(str(redirectURI))
		else:
			self.redirect("/")


# Used to create new commands when a user submits the 'create' command.
def create_new_command(query):
	if len(query) > 2: # Check that both command name and URI were provided.
		enteredCommandString = ' '.join(query)
		commands = db.GqlQuery("SELECT * FROM Command")
		commandAlreadyExists = False
		for command in commands:
			if command.name == query[1]:
				commandAlreadyExists = True
		if not commandAlreadyExists:
			# make sure something usable was entered for command name and search string.
			if len(query[1]) > 0 and len(query[2]) > 5: 
				if (query[2][0:7] == "http://") or (query[2][0:8] == "https://"):
					command = Command(
						name=query[1],
						searchString=query[2],
						description='',
						usage='',
						builtin='no')
					command.put()
					return ('<p>Created command: ' + query[1] +
											' => ' + query[2] + "</p>" +
											'<a href="/">Home</a>')
				else: # Command URI did not begin with 'http://'' or 'https://'.
					return ('<a href="/?try_again=' + 
								enteredCommandString + 
								'">Try again</a>: Command URI must begin with http:// or https://.')
			else: # Command name and/or URI too short.
				return ('<a href="/?try_again=' + 
								enteredCommandString + 
								'">Try again</a>: You must enter a valid command name followed by a URI.')
		else: # Command already exists.
			return ('<a href="/?try_again=' + 
								enteredCommandString + 
								'">Try again</a>: Command "' + 
								query[1] + 
								'" already exists, please use a unique command name.')
	else: # Command name and/or URI missing.
		return ('<a href="/?try_again=' + 
								enteredCommandString + 
								'">Try again</a>: You must enter at least a command name followed by a URI.')


class GqlCommandDatabase:
	def __init__(self):
		pass
	
	# Handles conversion of search command into a URI that can be redirected to.
	def get_command_web_shell_url(self, command_name):
		logging.info('Command Name = ' + command_name)
		command_name = command_name.lower()
		matchedCommand = db.GqlQuery("SELECT * FROM Command WHERE name = :name", name=command_name).get()
		if (matched_command):
			web_shell_url = matchedCommand.searchString
			logging.info('web_shell_url = ' + repr(web_shell_url))
			assert type(web_shell_url) in (types.StringType, types.UnicodeType)
			return (web_shell_url, False)
		else:
			raise UnknownCommandError("Error: command '%s' not found in the database." % command_name)


app = webapp2.WSGIApplication([(r'/parse/(.*)', ParseHandler)],
                              debug=True)
