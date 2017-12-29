import yaml
import os
class Yamlparser():
	"""

	"""
	def __init__(self):
		self.file=file


	def get_data(self,root=None,branch=None):
		"""

		"""
		self.path = os.path.abspath("../resources/config.yaml")
		with open(self.path,'r') as yamlfile:
			data = yaml.load(yamlfile)
			if root:
				return data[root][branch]
			else:
				return data[branch]


    def put_data(self):
    	pass




