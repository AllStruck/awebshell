#!/usr/bin/env python

import cgi
import webapp2
from google.appengine.ext import db



class Command(db.Model): # Database model for commands
	name = db.StringProperty( # Name of the command
		required=True)
	createdDate = db.DateTimeProperty( # Date and time the command was created
		auto_now_add=True)
	searchString = db.StringProperty( # Search string for the command
		required=True)
	description = db.StringProperty(multiline=True) # Description for the command
	usage = db.StringProperty(multiline=True)

def commands_key(command_name=None):
  """Constructs a Datastore key for a Command entity with command_name."""
  return db.Key.from_path('Command', command_name or 'g')

class ParseHandler(webapp2.RequestHandler):
	def get(self, enteredCommand):
		if self.request.get('q'):
			enteredCommand = self.request.get('q')

		enteredCommandString = enteredCommand
		enteredCommand = enteredCommand.split()

		if enteredCommand[0].find('create') > -1: # user wants to create a command
			if len(enteredCommand) > 2: # Check that both command name and URI were provided
				commands = db.GqlQuery("SELECT * FROM Command")
				commandAlreadyExists = False
				for command in commands:
					if command.name == enteredCommand[1]:
						commandAlreadyExists = True
				if not commandAlreadyExists:
					if len(enteredCommand[1]) > 0 and len(enteredCommand[2]) > 5: # make sure something usable was entered for command name and search string
						if (enteredCommand[2][0:7] == "http://") or (enteredCommand[2][0:8] == "https://"):
							command = Command(
								name=enteredCommand[1],
								searchString=enteredCommand[2])
							command.put()
							self.response.write('<p>Created command: ' + enteredCommand[1] +
													' => ' + enteredCommand[2] + "</p>" +
													'<a href="/">Home</a>')
						else: # Command URI did not begin with http:// or https://
							self.response.write('<a href="/?try_again=' + enteredCommandString + '">Try again</a>: Command URI must begin with http:// or https://.')
					else: # Command name and/or URI too short
						self.response.write('<a href="/?try_again=' + enteredCommandString + '">Try again</a>: You must enter a valid command name followed by a URI.')
				else: # Command already exists
					self.response.write('<a href="/?try_again=' + enteredCommandString + '">Try again</a>: Command "' + enteredCommand[1] + '" already exists, please use a unique command name.')
			else: # Command name and/or URI missing
				self.response.write('<a href="/?try_again=' + enteredCommandString + '">Try again</a>: You must entere at least a command name followed by a URI.')
		else: # user is performing a command
			redirectURI = str(convert_command_to_uri(enteredCommandString))
			self.redirect(redirectURI)

def convert_command_to_uri(query):
	queryList = query.split()
	matchCommand = db.GqlQuery("SELECT * FROM Command WHERE name = :name", name=queryList[0])
	command = matchCommand.get()
	if command:
		searchString = command.searchString
		if searchString.find("%s"):
			commandRoot = queryList.pop(0)
			commandArguments = ''.join(queryList)
			searchString = searchString.replace('%s', commandArguments)
		return searchString

	return 'http://google.com/search?q=' + query

app = webapp2.WSGIApplication([(r'/parse/(.*)', ParseHandler)],
                              debug=True)
