import requests
import json
from pprint import pprint

def load_raw_data(url):
    """Retreives Ids for different pages on the API"""
    page = 0
    game_num = 0
    data_temp = []
    while True:
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Origin': 'https://www.premierleague.com',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                  }
        params = (('pageSize', '100'),
                ('page', str(page)))

    # request to obtain the team info
        try:
            response = requests.get(url, params = params, headers=headers).json()  
            if url.endswith('staff'):
                data = response['players']
                return data
            elif 'fixtures' in url:
                data = response["content"]
                #loop to get info for each game 
                data_temp.extend(data) 
            else:
                data = response['content']
                # note: bit of a hack, for some reason 'id' is a float, but everywhere it's referenced, it's an int
                for d in data:
                    d['id'] = int(d['id'])        
        except Exception as e:
            print(e, "Something wrong")
            return {}

        page += 1
        if page == response["pageInfo"]["numPages"]:
            break

    for d in data_temp:
        d['id'] = int(d['id'])
    return data_temp

values = load_raw_data('https://footballapi.pulselive.com/football/fixtures?compSeasons=274')
ls = [value['id'] for value in values]
print(len(ls))



#print(attrs)


            