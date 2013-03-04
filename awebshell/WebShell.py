# WebShell.py - class for parsing awebshell commands, parsing web shell URLs, and determining a final resulting URL.
#
# Copyright 2013 Lee Bush. All rights reserved.
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

#There are some TODO and ZZZ items below that need to be addressed.
#Also, I do not claim that this is the most efficient way to parse, but it gets the job done...
#Don't forget to add/maintain the test cases in the 'tests' folder as you change this code.
#  -Lee


__all__ = ['WebShell']




#syntax highlight URLs
#validate URLs
import re
import urllib


KEY_NAME_STRING_REGEX_STRING = r'[_A-Za-z][_A-Za-z0-9]*'
VALUE_STRING_REGEX_STRING = r'[^{}]*'
VAR_REFERENCE_REGEX_STRING = r'\$\{(' + KEY_NAME_STRING_REGEX_STRING + r')\}'
PARAMETER_REGEX = re.compile(r'\$\{(' + KEY_NAME_STRING_REGEX_STRING + r')([=]' + VALUE_STRING_REGEX_STRING + r')?\}')

CASE_THEN_VALUE_REGEX_STRING = r'[^={}]+ \=\> [^={},]+'
CASE_THEN_VALUE_REGEX = re.compile(CASE_THEN_VALUE_REGEX_STRING)

SWITCH_REGEX = re.compile(r'\{ switch ' + VAR_REFERENCE_REGEX_STRING + '( \| )(' + CASE_THEN_VALUE_REGEX_STRING + ')(, ' + CASE_THEN_VALUE_REGEX_STRING +  ')*( \})')
#SWITCH_REGEX = re.compile(r'\{(:\s)*switch(:\s)+' + VAR_REFERENCE_REGEX_STRING + r'(:\s*\|)(\s)*(' + CASE_THEN_VALUE_REGEX_STRING + r')(,(:\s)*' + CASE_THEN_VALUE_REGEX_STRING +  r')*(\s*\})') #ZZZ broken! not working like I want...

#assert(re.compile(r'\{\s*').match('{'))
#assert(re.compile(r'\{\s*').match('{ '))
#print re.compile(r'\{(:\s)*').match('{  ').regs
#assert(not re.compile(r'\{(:\s*)').match('{{ '))

#print OPTION_POST_REGEX.match('[post]').groups() #ZZZ test.
#print OPTION_USE_X_FOR_SPACES_REGEX.match('[use - for spaces]').groups()#ZZZ test.
#print SWITCH_REGEX.match('{ switch ${plat} | xbox => 13 }').groups()
#print SWITCH_REGEX.match('{ switch ${plat} | * => 13 }').groups()
#print SWITCH_REGEX.match('{ switch ${plat} | xbox => 13, dreamcast => 1, * => 0 }').groups() #ZZZ not getting dreamcast. need different loop-group extraction technique.


OPTION_POST_REGEX = re.compile(r'[[]post[]]')
OPTION_USE_X_FOR_SPACES_REGEX = re.compile(r'[[]use ([^]{} ]+) for spaces[]]')
OPTION_NO_URL_ENCODING_REGEX = re.compile(r'[[]no url encoding[]]')


from web_shell_exceptions import WebShellError, UnknownCommandError, CommandParseError, MissingParameterException, InvalidParameterValueException


class WebShell:
	'''
	The WebShell class receives commands (i.e., gim penguins), looks up comand names in the
	provided command database, and then evaluates the final URL.
	
	Example:
	
	  command_database = ... #create your command database somehow
	
	  web_shell = WebShell(command_database) #create web shell object
	
	  url, can_inline = web_shell.evaluate('gim penguins') #run command and determine resulting URL
	
	  #now goto the url...
	
	'''
	
	
	INLINE_COMMANDS_SET = set(['cat', 'date']) #ZZZ this will be refactored and removed
	
	def __init__(self, command_database):
		'''
		Create a WebShell object.
		
		The command_database parameter is an object that must provide a get_command_web_shell_url() method.
		This method receives a command name as a parameter, and must return a Web Shell URL string:
		    command_database.get_command_web_shell_url(command_name) => web_shell_url
		
		'''
		
		assert(hasattr(command_database, 'get_command_web_shell_url'))
		self.__command_database = command_database
	
	
	def validate_web_shell_url(self, web_shell_url):
		'''
		return True if the given Web Shell URL appears to be syntactically correct.
		return False otherwise.
		'''
		raise NotImplemented #ZZZ stub
	
	
	def evaluate(self, query_string):
		'''
		
		return (final_url, can_inline)
		'''
		#print 'query_string: ' + repr(query_string)
		
		query_string = query_string.strip() #remove all spaces from beginning and end of query.
		tokens = query_string.split()
		
		#print 'tokens: ' + repr(tokens)
		if (len(tokens) < 1):
			return ('', False)
		else:
			command = tokens[0]
		
		arguments = tokens[1:]
		arguments_text = ' '.join(arguments)
		
		
		web_shell_url, can_inline = self.__get_command_web_shell_url_and_inline(command)
		
		evaluated_url = self.__execute_web_shell_url(web_shell_url, arguments_text)
		
		return (evaluated_url, can_inline)
	
	
	
	def __get_command_web_shell_url_and_inline(self, name):
		'''
		return tuple of the form (web_shell_url, can_inline) associated with the given command name.
		'''
		
		can_inline = (name in WebShell.INLINE_COMMANDS_SET)
		
		web_shell_url = self.__command_database.get_command_web_shell_url(name)
		
		return (web_shell_url, can_inline) #ZZZ stub

	#return the tuple (respaced_argument_text, parameter_dictionary)
	def __parse_command_arguments(self, raw_argument_text):
		tokens = raw_argument_text.split()
		
		parameter_dictionary = {}
		respaced_argument_text = ''
		current_key = None
		mode = 'initial'
		for token in tokens:
			if (mode == 'initial'):
				if (token.startswith('-')):
					current_key = token[1:]
					parameter_dictionary[current_key] = ''
					mode = 'got_key'
				else:
					if (respaced_argument_text):
						respaced_argument_text += ' '
					respaced_argument_text += token
			elif (mode == 'got_key'):
				if (token.startswith('-')):
					raise ComandParseError("expected an argument value for '%s', but recieved a new argument name of '%s'." % (current_key, token))
				else:
					parameter_dictionary[current_key] = token
				mode = 'more_values'
			elif (mode == 'more_values'):
				if (token.startswith('-')):
					current_key = token[1:]
					parameter_dictionary[current_key] = ''
					mode = 'got_key'

				else:
					if (parameter_dictionary[current_key]):
						parameter_dictionary[current_key] += ' '
					parameter_dictionary[current_key] += token
			else:
				assert(False) #should never happen							
		
		
		#print 'parameter_dictionary=', parameter_dictionary
		return (respaced_argument_text, parameter_dictionary)

	
	def __execute_web_shell_url(self, web_shell_url, raw_argument_text):
		#print web_shell_url
		web_shell_url, options = self.__strip_web_shell_url_options(web_shell_url)
		
		raw_argument_text, arguments = self.__parse_command_arguments(raw_argument_text)			

		#print (web_shell_url, options)
		#print (raw_argument_text, arguments)
	
		
		arguments_and_defaults_dictionary = {} #Note: if value is None, then the parameter is required


		web_shell_url_length = len(web_shell_url)
		

		final_url = ''


		start = 0
		match_result = 'x' #something that is not None
		while (match_result is not None):
			#print 'x'
			
			match_result = SWITCH_REGEX.search(web_shell_url)
			
			if (match_result is not None):
				p0, p1 = match_result.regs[0]
				#print 'switch groups: ', match_result.groups()
				switch_var_name = match_result.group(1)
				p2 = match_result.regs[2][1]
				p3 = match_result.regs[4][1]
				switch_cases_text = web_shell_url[p2:p3]
				#print 'switch_cases_text', switch_cases_text
				final_url = final_url + web_shell_url[0:p0] + self.__execute_switch_case_handler(switch_var_name, switch_cases_text, arguments)
				web_shell_url = web_shell_url[p1:]
				#print (switch_var_name, switch_cases_text)
		web_shell_url = final_url + web_shell_url
		

		#parse and replace ${variable} and ${variable=default_value} forms ----
		web_shell_url_length = len(web_shell_url)
		final_url = ''
		match_result = 'x' #something that is not None
		while (match_result is not None):
			match_result = PARAMETER_REGEX.search(web_shell_url, start)
			if (match_result is None):
				break
			key, value = match_result.groups()
			if (value is not None):
				value = value[1:] #chop off '=' at beginning
			
			
			arguments_and_defaults_dictionary[key] = value
			
			p0, p1 = match_result.regs[0]
				
			first_chunk = web_shell_url[0:p0]
			#print '\n\n\nfirst_chunk=', first_chunk
			final_url += first_chunk
			
			#print 'THING REPLACING: ', repr(web_shell_url[p0:p1])
			
			
			web_shell_url = web_shell_url[p1:]
			#print 'web_shell_url', web_shell_url
			if (arguments.has_key(key)):
				final_url += self.__encode(arguments[key], options)
			else:
				if (value is not None):
					final_url += self.__encode(value, options)
				else:
					raise MissingParameterException("Mandatory value for parameter '%s' not provided." % key)
			
		#print arguments_and_defaults_dictionary
		
		
		
		web_shell_url = final_url + web_shell_url
		
		
		web_shell_url = web_shell_url.replace('%s', self.__encode(raw_argument_text, options))
			
		return web_shell_url
	
	def __encode(self, input_string, options):
		space_replacer = options['space_replacer']
		if (space_replacer is None):
			space_replacer = '+'
		
		tokens = input_string.split() #split on whitespace
		
		if (options['encode_url']):
			
			tokens = map(urllib.quote, tokens, ['']*len(tokens)) #the urllib quote "safe" list is set empty so we can encode the slash.
		
		result_string = space_replacer.join(tokens)
		
		#ZZZ handle options['post'] here????
		
		return result_string
	
	
	def __strip_web_shell_url_options(self, web_shell_url):
		
		options = {}
		
		
		match_result = OPTION_POST_REGEX.search(web_shell_url)
		if (match_result is None):
			options['post'] = False
		else:
			options['post'] = True
			p0, p1 = match_result.regs[0]
			web_shell_url = web_shell_url[0:p0] + web_shell_url[p1:]
		
		
		
		match_result = OPTION_USE_X_FOR_SPACES_REGEX.search(web_shell_url)
		if (match_result is None):
			options['space_replacer'] = None
		else:
			options['space_replacer'] = match_result.group(1)
			p0, p1 = match_result.regs[0]
			web_shell_url = web_shell_url[0:p0] + web_shell_url[p1:]
	
	
		match_result = OPTION_NO_URL_ENCODING_REGEX.search(web_shell_url)
		if (match_result is None):
			options['encode_url'] = True
		else:
			options['encode_url'] = False
			p0, p1 = match_result.regs[0]
			web_shell_url = web_shell_url[0:p0] + web_shell_url[p1:]



		return (web_shell_url, options)
	
	def __execute_switch_case_handler(self, switch_variable_name, switch_case_text, variable_value_dictionary):
		DEFAULT_CASE_KEY = '*'

		#print dir(CASE_THEN_VALUE_REGEX)
		#print switch_variable_name
		#print variable_value_dictionary
		matches = CASE_THEN_VALUE_REGEX.findall(switch_case_text)
		case_dictionary = {}
		for match_text in matches:
			case_value, result_value = match_text.split('=>')	
			case_value = case_value.strip()
			if (case_value.startswith(',')):
				case_value = case_value[1:].lstrip()
			result_value = result_value.strip()
			case_dictionary[case_value] = result_value
		#print 'case_dictionary=', case_dictionary
		
		if (not variable_value_dictionary.has_key(switch_variable_name)):
			if (case_dictionary.has_key(DEFAULT_CASE_KEY)):
				return case_dictionary[DEFAULT_CASE_KEY]
			else:
				raise MissingParameterException("Error: required parameter '%s' not provided." % switch_variable_name)
		else:
			switch_variable_value = variable_value_dictionary[switch_variable_name]
			if (case_dictionary.has_key(switch_variable_value)):
				return case_dictionary[switch_variable_value]
			else:
				acceptable_keys = sorted(case_dictionary.keys())
				error_message = "Error: invalid value for parameter '%s': '%s'. The only acceptable values are: %s." % \
					(switch_variable_name, switch_variable_value, acceptable_keys)
				
				raise InvalidParameterValueException(error_message)
		
		assert(False) #should never get here


	
