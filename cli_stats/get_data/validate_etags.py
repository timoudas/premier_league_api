import json
import requests

from directory import Directory
from storage_config import StorageConfig


class ValidateEtag():
    E_TAG = {}
    UPDATED_E_TAGS = {}
    dirs = Directory()

    def __init__(self):
        try: 
            ValidateEtag.E_TAG = self.load_etags()
        except FileNotFoundError as e:
            print('No previous etags exist')
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'https://www.premierleague.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                  }
        self.params = (('pageSize', '100'),)


    def get_data(self, url):
        try:
            with requests.Session() as s:
                if self.check_etag(url):
                    response = s.get(url, headers=headers, params=params).json()
                    data = response
                    return data
        except Exception as e:
            print(e, 'Something went wrong with the request')
            return {}


    def check_etag(self, url):
        response = self.load_headers(url)
        if not self.url in ValidateEtag.E_TAG:
            ValidateEtag.E_TAG[url] = response['etag']
            return True
        elif url in ValidateEtag.E_TAG:
            if not self.assert_etag(ValidateEtag.E_TAG[url], response['etag']):
                ValidateEtag.E_TAG[url] = response['etag']
                UPDATED_E_TAGS[url] = response['etag']
                return True
            else:
                return False
        else:
            raise(KeyError, 'etag not found')


    def load_headers(self, url):
        """Retreives Ids for different pages on the API"""
        # request to obtain the team info
        try:
            with requests.Session() as s:
                response = s.get(url, headers=self.headers, params=self.params)
            return response.headers
        except Exception as e:
            print(e, 'Something went wrong with the request')
            return {}

    def assert_etag(self, old_etag, new_etag):
        if old_etag == new_etag:
            print('Same as old etag')
            return True
        else:
            print('New etag!')
            return False

    def load_etags(self, ):
        return dirs.load_json('latest_etags.json', StorageConfig.PARAMS_DIR)

    def save_etags(self, visited_dict):
        dirs.save_json('latest_etags.json', visited_dict, StorageConfig.PARAMS_DIR)


