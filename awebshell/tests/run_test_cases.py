#! /usr/bin/python
#
# run_test_cases.py - Test the awebshell library.
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

'''
This program tests the awebshell library.


TODO: add more test cases to appropriate .csv files.

TODO: convert to use 'unittest' library??



'''

import sys
import csv
import os

sys.path.insert(0, os.path.join('..', '..')) #ensure awebshell library is importable, especially if it hasn't been installed yet.


from awebshell import WebShell, WebShellError
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
					raise Exception('bad command string in input file (bad characters): ' + repr(command))
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
	
	print failures, 'failures'
	print successes, 'successes'
	
	if (failures > 0):
		sys.exit(1)
	
if __name__ == '__main__':
	run_test_cases('test_web_shell_command_database.csv', 'test_cases.csv')
