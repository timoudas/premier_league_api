from api_scraper import Football
import requests
from bs4 import BeautifulSoup
import shutil

IMG_SAVE_PATH = '../../../dashboard/assets/'

fb = Football()

def get_team_url(teamID):
  url = f"https://www.premierleague.com/clubs/{teamID}/club/squad"
  return requests.get(url)

def get_team_ids():
  fb.load_leagues()
  fb.leagues['EN_PR'].load_seasons()
  team_keys = fb.leagues['EN_PR'].seasons['2016/2017'].load_teams().keys()
  team_id = [i for i in team_keys]
  return team_id

def get_img_elem(team_request):
  page = team_request.text
  soup = BeautifulSoup(page, 'html.parser')
  tags_raw = soup.find_all('img', {'class': 'img statCardImg'})
  tags = [tag.get('src') for tag in tags_raw]
  return tags

def get_player_name(team_request):
  page = team_request.text
  soup = BeautifulSoup(page, 'html.parser')
  tags_raw = soup.find_all('h4', {'class': 'name'})
  tags = [tag.text for tag in tags_raw]
  return tags

def create_dict(team_request):
  images = get_img_elem(team_request)
  player_names = get_player_name(team_request)
  player_url_tuple = zip(player_names, images)
  player_img_dict = {name: url for name, url in player_url_tuple}
  return player_img_dict



def all_player_imgs():
  team_ids = get_team_ids()
  results = []
  for team_id in team_ids:
    team_players = get_team_url(team_id)
    player_dict = create_dict(team_players)
    results.append(player_dict)
  return results

def download_images():
  all_players = all_player_imgs()
  for d in all_player_imgs:
    for key, value in d.items():
      response = requests.get(value, stream=True)
      last_name = key.split(' ')[-1]
      with open(IMG_SAVE_PATH + last_name + '.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
      del response

print(all_player_imgs())