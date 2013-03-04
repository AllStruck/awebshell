#!/usr/bin/env python

import webapp2
from google.appengine.ext import db


# Database model for commands.
class Command(db.Model):
	name = db.StringProperty( # Name of the command.
		required=True)
	createdDate = db.DateTimeProperty( # Date and time the command was created.
		auto_now_add=True)
	searchString = db.StringProperty( # Search string for the command.
		required=True)
	description = db.StringProperty(multiline=True) # Description for the command.
	usage = db.StringProperty(multiline=True)
	builtin = db.StringProperty()