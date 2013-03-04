# CSVCommandDatabase.py - The CSV of the command database protocol that WebShell class interacts with.
#                         Note that there are other implementations of this command database protocol available.
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


import csv

from ..web_shell_exceptions import UnknownCommandError


class CSVCommandDatabase:
	def __init__(self, csv_filename):
		#read in CSV file and store for lookup in self.__command_dictionary
	
		self.__command_dictionary = {} #map name -> web_shell_url
	
		csv_file = open(csv_filename, 'r')
		csv_reader = csv.reader(csv_file)
		
		
		for row in csv_reader:
			if (row[0].strip()):
				name = row[0].strip()
				web_shell_url = row[1].strip()
				assert(web_shell_url)
			
				assert(name not in self.__command_dictionary)
				self.__command_dictionary[name] = web_shell_url
				
		csv_file.close()
		
	def get_command_web_shell_url(self, name):
		if (name not in self.__command_dictionary):
			raise UnknownCommandError("Unknown command: '%s'." % name)
		
		return self.__command_dictionary[name]
