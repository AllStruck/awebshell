# __init__.py - main module for the awebshell library.
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
awebshell - a library for quickly accessing web pages with short command line interface-style commands.

This library's functionality was inspired heavily by the 'yubnub' Ruby on Rails project.

----

WebShell is the main class this library provides.
Please see its documentation for more details.

----

DEFINITIONS:

* Command
    A command has a name and an associated web shell URL.
    For example, the command with the name 'gim' has the web shell URL"
        http://images.google.com/images?q=%s
    
    A command can be passed parameters.
    Example: The command 'gim Porche 911' has the parameters 'Porche 911'.
    
    There are also special switch parameters that command be passed in a command.
    Example: the command 'gloc -what shoes -where Washington, DC' communicates that
    ${what} should be set to 'shoes' and that ${where} should be set to 'Washington, DC'.
     
* Web Shell URL
    A URL with special syntax, which can be given arguments to be filled in.
    Some of the special syntax constructs you can use inside of a web shell url:
      1. %s
      2. ${VARIABLE_NAME}
      3. ${VARIABLE_NAME=DEFAULT_VALUE}
      4. { switch ${VARIABLE_NAME} | { CASE_VALUE_1 => RESULT_VALUE_1[, ...][, * => DEFAULT_VALUE] }

    Some of the special syntax which isn't working yet (:P):
      5. {COMMAND_NAME[ COMMAND_ARGUMENTS...]}         #TODO: NOT SUPPORTED YET!!!!
      
      

* Final URL
    A web shell URL that has been evaluated, and all arguments are filled in by .

----

TODO: Add support nested command constructs using braces, and ensure.

TODO: Allow more flexible spacing in the swtich statement.



'''

__author__ = "Lee Bush"
__copyright__ = "Copyright 2013 Lee Bush, all rights reserved. Copyright 2013 AllStruck, all rights reserved."
__credits__ = ["Lee Bush", "David Monaghan"]
__license__ = "Apache 2.0"
__version__ = "0.5"
__maintainer__ = "David Monaghan"
__email__ = "awebshell@allstruck.com"
__status__ = "Development" #TODO: change to "Production" when quality is good enough.




from WebShell import WebShell
from web_shell_exceptions import *
del web_shell_exceptions

