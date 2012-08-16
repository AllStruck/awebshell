#!/usr/bin/env python
#
# Copyright 2012 AllStruck
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

# This is the man (manual) handler for awebshell.
# Man is a special command available at /man/<command_name>,
#	not handled in the usual way other commands are handled.
# Here we present a template file which shows details about one command.


import cgi
import webapp2
from google.appengine.ext import db


