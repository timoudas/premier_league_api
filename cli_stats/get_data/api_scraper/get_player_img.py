from api_scraper import Football
import requests

def get_player_img(teamID):
  url = f"https://www.premierleague.com/clubs/{teamID}/club/squad"
  return requests.get(url)

get_player_img(1)