#! /usr/bin/python
#
# run_test_cases.py - Test the awebshell library.
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

'''
This program tests the awebshell library.


TODO: add more test cases to appropriate .csv files.

TODO: convert to use 'unittest' library??

TODO: make a command specific Node

TODO: Make top level node concatenate (until further notice)

'''

import sys
import csv
import os

sys.path.insert(0, os.path.join('..', '..')) #ensure awebshell library is importable, especially if it hasn't been installed yet.


from awebshell import WebShell, WebShellError, WebShellUrlParser, WebShellUrlParserException, WebShellExecutor
from awebshell.database.CSVCommandDatabase import CSVCommandDatabase #select the CSV implementatoin of the command database protocol.




def run_test_cases(command_database_filename, test_cases_filename):
	test_command_database = CSVCommandDatabase('test_web_shell_command_database.csv')
	web_shell = WebShell(test_command_database)

	csv_file = open(test_cases_filename, 'r')
	csv_reader = csv.reader(csv_file)
	row_number=1
	successes=0
	failures=0
	first_line_passed = False
	for row in csv_reader:
		if (not first_line_passed):
			first_line_passed = True
			continue
			
		if (row[0].strip()):
				command = row[0].strip()
				if (command.find('\xc2') != -1 or command.find('\xa0') != -1): #detects some garbage that LibreOffice Calc or MS Excel left in the .csv file.
					raise Exception(test_cases_filename + ':' + str(row_number) + ' - ' + 'bad command string in input file (bad characters): ' + repr(command))
				expected_result = row[1].strip()
		
		try:
			actual_result, can_inline = web_shell.evaluate(command)
			
			if (expected_result != actual_result):
				print '--------------MISMATCH! ROW %i--------------------------------' % row_number
				print 'COMMAND:', repr(command)
				print 'EXPECTED:', expected_result
				print '  ACTUAL:', actual_result
				print
				
				failures += 1
			else:
				successes += 1
		
		except WebShellError, wse:
				print '--------------MISMATCH! ROW %i--------------------------------' % row_number
				print 'COMMAND:', repr(command)
				print 'ERROR: ' + wse.__class__.__name__ + ': ' + str(wse)
				print
				
				failures += 1
		
		row_number += 1
	
	csv_file.close()
	
	print
	print "WebShell"
	print failures, 'failures'
	print successes, 'successes'
	
	if (failures > 0):
		sys.exit(1)

def test_parser():
	TEST_CASES = \
	[ \
		# ('asd', "T['asd']"), # string
		# ('def {cdb}', "T['def ', T['cdb']]"), # string followed by command
		# ('def ${cdb}', "T['def ', ${cdb}]"), # string followed by variable
		# ('def {cdb def}', "T['def ', T['cdb', 'def']]"), # string followed by command with argument
		# ('gim {g def hij}', "T['gim', T['g', 'def', 'hij']]"), # string followed by command with two argument
		# ('{cdb def}', "T[T['cdb', 'def']]"), # command with argument
		# ('{${var}abc}', "T[T[T['concatenate', ${var}, 'abc']]]"), # concatenation works within command
		# ('${var}abc', "T[T['concatenate', ${var}, 'abc']]"), # concatenation works properly at root level
		# ('}', WebShellUrlParserException), # close bracket as first character
		# ('{${var}abc {jkaf slkd', WebShellUrlParserException),
		('http://google.com/fasdfasd/{example abc def}', "T['gim', T['g', 'def', 'hij']]"), 
	]

	number_of_test_cases = 0
	number_of_test_case_failures = 0


	for web_shell_url, expected in TEST_CASES:

		csv_filename = 'test_web_shell_command_database.csv' #TODO: un-hardcode this.
		database = CSVCommandDatabase(csv_filename)
		# print web_shell_url
		parser = WebShellUrlParser()
		executor = WebShellExecutor(database)
		
		try:
			tree = parser.build_tree(web_shell_url)
			actual = str(tree)
			executor.execute_tree(tree, (), {'hello': 'world'})

			die

			# print 'AC: ' + actual
			if (actual != expected):
				print 'EX: ' + expected
				print 'AC: ' + actual
				print 'ERROR!-----------------'
				number_of_test_case_failures += 1
		except WebShellUrlParserException, wsupe:
			if expected is WebShellUrlParserException:
				# print 'EX: (WebShellUrlParserException)'
				# print 'AC: (WebShellUrlParserException)'
				pass
			else:
				print 'EX: ' + expected
				print 'AC: ' + 'ERROR: ' + str(wsupe)
				print 'ERROR!-----------------'	
				number_of_test_case_failures += 1
		# print
		# print
		number_of_test_cases += 1
	print
	print "WebShellUrlParser"
	print number_of_test_case_failures, "failures" 
	print number_of_test_cases - number_of_test_case_failures, "successes"
	
if __name__ == '__main__':
	run_test_cases('test_web_shell_command_database.csv', 'test_cases.csv')
	test_parser()
