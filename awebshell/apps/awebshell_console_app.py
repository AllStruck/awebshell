#! /usr/bin/python
#
# awebshell console app - Command line program quickly accessing web pages with short command line interface-style commands.
#                         This application provides a good example of how to use the awebshell Python library.
#
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





__all__ = ['main', 'run_interactive_shell']


import sys
USAGE = \
'''awebshell console app - Command line program quickly accessing web pages with short command line interface-style commands.

Usage:
 %s                #start an interactive shell
 %s COMMAND...     #run one web shell command
 %s --help         #show this message

Examples:
 %s gim penguins   #search Google Images for pictures of penguins

''' % ((sys.argv[0], )*4)




#system imports ----
import os
import readline #sets up nicer console input (command history, etc.)
import webbrowser



#ZZZ this is a little bit of a hack. Let's leave this in until we get this directory structure figured out.
try:
	import awebshell
except ImportError:
	sys.path.insert(0, os.path.join('..', '..')) #ensure awebshell library is importable, especially if it hasn't been installed yet.
	import awebshell


#import required awebshell library functionality ----
from awebshell.database.CSVCommandDatabase import CSVCommandDatabase #choose the CSV Command Database backend.
from awebshell import WebShell, WebShellError



def run_one_command(command_database, command_text):
	web_shell = WebShell(command_database)
	final_url, can_inline = web_shell.evaluate(command)
	webbrowser.open(final_url)


def run_interactive_shell(command_database):
	web_shell = WebShell(command_database)
	print '-' * 80
	print 'Welcome to the AWebShell Console.'
	print 
	print "Type 'webbrowser=disabled' if you wish to disable browser control."
	print '-' * 80
	print
	print
	webbrowser_enabled = True
	try:
		while (True): #loop forever (well, until an exception...)
			raw_query = raw_input('> ')
			
			if (raw_query.strip() == 'webbrowser=enabled'):
				webbrowser_enabled = True
			elif (raw_query.strip() == 'webbrowser=disabled'):
				webbrowser_enabled = False
			else:
			
				try:
					evaluated_url, can_inline = web_shell.evaluate(raw_query)
					if (evaluated_url):
						print
						
						if (webbrowser_enabled):
							print 'GOTO', evaluated_url
							webbrowser.open(evaluated_url)
						else:
							print 'RESULT:', evaluated_url
							print 'CAN_INLINE:', can_inline
						
						print
					
					
					
					
				except WebShellError, wse:
					print
					print 'ERROR: ' + wse.__class__.__name__ + ': ' + str(wse)
					print
				
			
	except EOFError:
		pass
	except KeyboardInterrupt:
		pass



def main():
	
	
	csv_filename = os.path.join(os.path.dirname(sys.argv[0]), '..', 'tests', 'test_web_shell_command_database.csv') #TODO: un-hardcode this.
	command_database = CSVCommandDatabase(csv_filename)
	
	arg_count = len(sys.argv)
	if (arg_count <= 1):
		run_interactive_shell(command_database)
	elif (arg_count == 2) and (sys.argv[1] == '--help'):
		print USAGE
	else:
		command_tokens = sys.argv[1:]
		command = ' '.join(command_tokens)
		run_one_command(command_database, command)



if __name__ == '__main__':
	main()
