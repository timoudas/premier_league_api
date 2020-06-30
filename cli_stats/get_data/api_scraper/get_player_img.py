from api_scraper import Football
import requests
from bs4 import BeautifulSoup


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
  soup = BeautifulSoup(page)
  tags = soup.findAll('img', {'class': 'img statCardImg'})
  print(tags)

get_img_elem(get_team_url(1))
