# parser.py - class for parsing awebshell commands
#
# Copyright 2013 Lee Bush. All rights reserved.
# Copyright 2013 Michael Jeffrey. All rights reserved.
# Copyright 2013 AllStruck. All rights reserved.
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

# WILD IDEA
#  variable names computed by commands at runtime
#  ex. ${{concatenate one blue}}
#   should equal oneblue
#  this could create runtime issues with the commands
#   such as:
#    commands that return spaces

"""
we have the following 5 classes of input characters
	$, {, }, (white_space), (token_character)
"""

import types
from web_shell_exceptions import WebShellUrlParserException


INITIAL_STATE = 0 # none
STRING_STATE = 1 # character
DOLLARSIGN_STATE = 2 # $
COMMAND_STATE = 3 # {
VARIABLE_BEGIN_STATE = 4 # ${
VARIABLE_CHARACTER_STATE = 5 # ${character

WHITESPACE_CHARACTERS = ' \t'


class WebShellUrlParser(object):
	"""docstring for ClassName"""
	def __init__(self):
		super(WebShellUrlParser, self).__init__()
		self.__state = None
		self.__stack = None
		self.__current_context = None

	def build_tree(self, input_string):
		self.__state = INITIAL_STATE
		self.__stack = TreeNode()
		root = self.__stack
		self.__current_context = self.__stack


		for c in input_string: # c = current character
			if(self.__state == INITIAL_STATE):
				if(c == "}"): # DIE
					raise WebShellUrlParserException('Unexpected Charater: }')
				elif(c == "{"):
					new_child = TreeNode(self.__current_context)
					self.__current_context.add_child(new_child)
					self.__current_context = new_child
					self.__state = COMMAND_STATE
				elif(c == "$"):
					self.__state = DOLLARSIGN_STATE
				else: # character or whitespace
					if (len(self.__current_context.get_children()) == 0):
						self.__current_context.add_child(c)
						self.__state = STRING_STATE
					else:
						TOS = self.__current_context.get_children()[-1]
						if (isinstance(TOS, ConcatenateNode)):
							TOS.append_text(c)
						else:
							self.__current_context.get_children().pop()
							new_child = ConcatenateNode(self.__current_context)
							self.__current_context.add_child(new_child)
							new_child.add_child(TOS)
							new_child.add_child(c)

			elif(self.__state == STRING_STATE):
				if(c == "}"): # DIE
					raise WebShellUrlParserException('Unexpected Charater: }')
				elif(c == "{"):
					new_child = TreeNode(self.__current_context)
					self.__current_context.add_child(new_child)
					self.__current_context = new_child
					self.__state = COMMAND_STATE
				elif(c == "$"):
					self.__state = DOLLARSIGN_STATE
				else:
					self.__current_context.get_children()[-1] = "%s%s" % (self.__current_context.get_children()[-1], c) # TOS = TOS + c
					# stay in STRING_STATE

			elif(self.__state == DOLLARSIGN_STATE):
				if(c == "{"):
					new_child = Variable(self.__current_context)
					self.__current_context.add_child(new_child)
					self.__current_context = new_child
					self.__state = VARIABLE_BEGIN_STATE
				elif(c == "}"):
					self.__current_context.get_children()[-1] = "%s%s" % (self.__current_context.get_children()[-1], "$") # TOS = TOS + '$'
					self.__current_context = self.__current_context.get_parent()
					if(self.__current_context is None):
						raise WebShellUrlParserException('Unmatched close brace: }')
				else:
					self.__current_context.get_children()[-1] = "%s%s%s" % (self.__current_context.get_children()[-1], "$" ,c) # TOS = TOS + '$$'
					self.__state = STRING_STATE

			elif(self.__state == COMMAND_STATE):
				if(c == "{"):
					new_child = TreeNode(self.__current_context)
					self.__current_context.add_child(new_child)
					self.__current_context = new_child
					# stay in COMMAND_STATE
				elif(c == "}"):
					if(len(self.__current_context.get_children()) == 0):
						raise WebShellUrlParserException("Cannot have empty command: {}")
					self.__current_context = self.__current_context.get_parent()
					# if the stack is clean
					if(self.__current_context.get_parent() is None):
						self.__state = INITIAL_STATE
					# else stay in the COMMAND_STATE
				elif(c == "$"):
					self.__state = DOLLARSIGN_STATE
				elif(c in WHITESPACE_CHARACTERS):
					if(len(self.__current_context.get_children()) > 0 and self.__current_context.get_children()[-1] != '') or len(self.__current_context.get_children()) == 0:
						new_child = ''
						self.__current_context.add_child(new_child)
					# else eat additional whitespace
				else:
					if(len(self.__current_context.get_children()) == 0):
						self.__current_context.add_child(c)
					else:
						TOS = self.__current_context.get_children()[-1]
						if(type(TOS) is types.StringType):
							self.__current_context.get_children()[-1] = "%s%s" % (self.__current_context.get_children()[-1], c) # TOS = TOS + c
						elif (isinstance(TOS, ConcatenateNode)):
							TOS.append_text(c)
						else: #TOS is either a Variable or a TreeNode
							# take the hot dog off the counter, put bun on the counter, put hot dog in the bun
							self.__current_context.get_children().pop()
							new_child = ConcatenateNode(self.__current_context)

							self.__current_context.add_child(new_child)
							new_child.add_child(TOS)
							new_child.add_child(c)

			elif(self.__state == VARIABLE_BEGIN_STATE):
				if(c in ("$}{"+WHITESPACE_CHARACTERS)):
					raise WebShellUrlParserException("Expected Variable Name, but found: %s." % c)
				else:
					self.__current_context.append_text(c)
					self.__state = VARIABLE_CHARACTER_STATE

			elif(self.__state == VARIABLE_CHARACTER_STATE):
				if(c in ("${"+WHITESPACE_CHARACTERS)):
					raise WebShellUrlParserException("'%s' INVALID inside of Variable Name" % c) # ex. '{' INVALID inside of Variable Name
				elif(c == "}"):
					self.__current_context = self.__current_context.get_parent()
					if(self.__current_context.get_parent() is None):
						self.__state = INITIAL_STATE
					else:
						self.__state = COMMAND_STATE
				else:
					self.__current_context.append_text(c)
					#stay in same state
			else:
				assert(False) #should never get here
		# endfor
		# check for unclosed stack
		if(self.__current_context.get_parent() is not None):
			raise WebShellUrlParserException("Unexpected end of command. Expected: '}'. PARSE TREE: " + str(root))

		return root


class TreeNode(object):
	def __init__(self, parent=None):
		self.__parent = parent
		self.__children = []

	def get_parent(self):
		return self.__parent

	def get_children(self):
		return self.__children

	def add_child(self, child):
		self.__children.append(child)
		# raise WebShellUrlParserException('Hal, open the pod bay doors')
	def __str__(self):
		return 'T' + str(self.__children)
	def __repr__(self):
		return 'T' + str(self.__children)

class ConcatenateNode(TreeNode):
	def __init__(self, parent=None):
		TreeNode.__init__(self, parent)
		self.add_child('concatenate')

	def append_text(self, text):
			assert(len(self.get_children()) > 0)

			last_child = self.get_children()[-1]

			if(type(last_child) is types.StringType):
				self.get_children()[-1] = self.get_children()[-1] + text # last_child = last_child + text
			# elif (isinstance(last_child, ConcatenateNode)):

			else: # take the hot dog off the counter, put bun on the counter, put hot dog in the bun
				self.add_child(text)


class Variable(object):
	def __init__(self, parent=None, text=''):
			self.__parent = parent
			self.__text = text
	def get_parent(self):
		return self.__parent

	def append_text(self, text):
		self.__text += text
	
	def __str__(self):
		return '${' + self.__text + '}'
	def __repr__(self):
		return '${' + self.__text + '}'