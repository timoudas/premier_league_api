#Class to create/save/load the json folders and files in relative paths
#dir

#Function to create subfolder depending on depth in json direktory
#Example
# json  
#   |--premier_league
#   |        |----compseason
#   |                 |-------standings
#   |                 |            |-----team_standing.json xTotal teams
#   |                 |
#   |                 |----fixture_stats.json
#   |                 |----player_stats.json           
#   |                 |----team_stats.json
#   |
#   |--competitions_id.json
#   |--compseason_id.json
#   |--fixtures_id.json
#   |--team_id.json

import os
import json

class Directory:

	def __init__(self):
		self.working_dir = os.path.dirname(__file__) #Get's the current working directory


	def mkdir(self, *path):
		"""Creates folder in the same level as the working directory folder

			Args:
				*args: path to folder that is to be created
		"""
		target_dir = os.path.join(self.working_dir, *path)
		try: 
			if os.path.exists(target_dir) == True:
				print(target_dir, 'exists')
			else:
				os.mkdir(os.path.join(self.working_dir, *path))
				print(os.path.join(self.working_dir, *path), 'succesfully created')
		except OSError as e:
			print(folder,'coult not be created', e)


	def save_json(self, filename, content, *path):
			"""save dictionarirys to .json files        
			Args:
				file (str): The name of the file that is to be saved in .json format
				filename (dict): The dictionary that is to be wrote to the .json file
				folder (str): The folder name in the target directory
			"""
			target_dir = os.path.join(self.working_dir, *path)
			file_dir = os.path.join(self.working_dir, target_dir, filename) 
			with open(file_dir + '.json', "w") as f:
				#pretty prints and writes the same to the json file
				f.write(json.dumps(content, indent=4, sort_keys=False))

	def load_json(self, filename, *path):
		"""loads json file
		Args:
			filename(str): The file name of the requested file
			*path(str): The path of the file
		"""

		file = os.path.join(self.working_dir, *path, filename)
		with open(file, 'r') as temp_file:
			return json.load(temp_file)

if __name__ == '__main__':
	d = Directory()
	d.mkdir('..', 'json')