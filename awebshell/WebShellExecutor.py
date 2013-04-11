import urllib, sys
# import httplib
import parser

class WebShellExecutor(object):
	"""docstring for WebShellExecutor"""
	def __init__(self, database):
		super(WebShellExecutor, self).__init__()
		self.__database = database
		self.__parser = parser.WebShellUrlParser()
		self.__max_scrape_bytes = 10*1024

	def scrape_url(self, url):
		print 'scraping ' + url
		f = urllib.urlopen(url)
		scraped_contents = f.read(self.__max_scrape_bytes)
		return scraped_contents

	def execute_tree(self, tree, args, kwargs, recurse_level=0):
		print 'execute_tree' + repr((tree, args, kwargs))

		#evaluate children ----

		



		evaluated_list = []
		for child in tree.get_children():
			if isinstance(child, parser.TreeNode):
				result = self.execute_tree(child, args, kwargs, recurse_level+1)
				evaluated_list.append(result)
			else:
				evaluated_list.append(child)


		#evaluate parent ----

		print 'evaluated_list=', evaluated_list


		if isinstance(tree, parser.Variable):
			# look up variable
			name = tree.get_name()
			if name in kwargs:
				return kwargs[name]
			else:
				default_value = tree.get_default_value()
				if (default_value is None):
					raise Exception("Required variable '%s' not provided." % name)
				else:
					return default_value

		elif isinstance(tree, parser.ConcatenateNode):
			# return concatenated string
			concatednated_text = ''
			for child in evaluated_list[1:]:
				concatednated_text += child
			return concatednated_text
		
		elif isinstance(tree, parser.TreeNode):
			if (recurse_level == 0):
				return ''.join(evaluated_list)
			else:
				#query the database for the command
				command_name = tree.get_children()[0]
				command_parameters = tree.get_children()[1:]
				web_shell_url = self.__database.get_command_web_shell_url(command_name)
				sub_command_tree = self.__parser.build_tree(web_shell_url)

				final_url = self.execute_tree(sub_command_tree, command_parameters, kwargs, )
				scrape_results = self.scrape_url(final_url)

				print 'scrape_results=', scrape_results 
				return scrape_results

		
		else:
			assert(False)


		
# print tree

# run cdb(def, hij)
# run def(returned cdb)