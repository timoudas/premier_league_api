#!/usr/bin/python
#Class to create/save/load the json folders and files in relative paths
#dir

#Function to create subfolder depending on depth in json directory
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

import json
import os

from pathlib import Path

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
            print(self.working_dir, *path,'coult not be created', e)

    def check_if_file_exist(self, *path):
        if os.path.exists(os.path.join(self.working_dir, *path)):
            return True
        else:
            return False


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
        #print(filename)
        file = os.path.join(self.working_dir, *path, filename)
        with open(file, 'r') as temp_file:
            return json.load(temp_file)

    def write_json(self, filename, *path):
        """writes to json file
        Args:
            filename(str): The file name of the requested file
            *path(str): The path of the file
        """

        file = os.path.join(self.working_dir, *path, filename)
        with open(file, 'w') as temp_file:
            return json.load(temp_file)


class StorageConfig:
    #Need to be changed to a relative path
    STORAGE_BASE_DIR = Path('/Users/andreas/Desktop/Projekt/premier_league/API_scraper/')
    PARAMS_DIR = STORAGE_BASE_DIR / "params"
    STATS_DIR = STORAGE_BASE_DIR / "raw_data"
    DB_DIR = STORAGE_BASE_DIR / "clean_data"
    PICKLE_DIR = STORAGE_BASE_DIR / "cli_stats/pickle"



if __name__ == '__main__':
    print(StorageConfig.PARAMS_DIR)
    #d = Directory()
    #print(d.check_path('..', 'json', 'test_leauges.json'))


