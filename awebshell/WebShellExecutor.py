import parser

class WebShellExecutor(object):
	"""docstring for WebShellExecutor"""
	def __init__(self):
		super(WebShellExecutor, self).__init__()

	def execute_tree(self, tree, parameters):

		if isinstance(child, parser.TreeNode):



		evaluated_list = []
		for child in tree.get_children():
			if isinstance(child, parser.TreeNode):
				result = self.execute_tree(child)
				evaluated_list.append(result)
			else:
				evaluated_list.append(child)

		print evaluated_list

		return 'EXECUTED_STUFF'
# print tree

# run cdb(def, hij)
# run def(returned cdb)