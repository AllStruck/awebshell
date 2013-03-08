# web_shell_exceptions.py - Exceptions in the awebshell library.
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

class WebShellError(Exception):
	'''This is the base exception for all exceptions in the awebshell library.
	   By catching this exception, you will also be catching the exception of all of those below.
	'''
	pass


class UnknownCommandError(WebShellError):
	pass


class CommandParseError(WebShellError):
	pass


class MissingParameterException(WebShellError):
	pass


class InvalidParameterValueException(WebShellError):
	pass


class WebShellUrlParserException(WebShellError):
	pass