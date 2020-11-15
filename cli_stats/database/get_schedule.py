import requests

from pprint import pprint


session = requests.Session()

def load_schedule(url):
    """Retreives unplayed matches from the API"""
    page = 0
    data_temp = []
    while True:
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Origin': 'https://www.premierleague.com',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                  }
        params = (('pageSize', '100'),
                 ('page', str(page),),
                 ('statuses', 'U'),
                 ('comps', 1),)

    # request to obtain the team info
        try:
            response = session.get(url, headers=headers, params=params).json()
            data = response["content"]
            for d in data:
                data_temp.append(d)
        except Exception as e:
            print(e, 'Something went wrong with the request')
            return {}

        page += 1
        if page >= response["pageInfo"]["numPages"]:
            break
    return data_temp

def get_schedule():
    url = 'https://footballapi.pulselive.com/football/fixtures'
    data = load_schedule(url)
    return data

if __name__ == '__main__':
    pprint(get_schedule())