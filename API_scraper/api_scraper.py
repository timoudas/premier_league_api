import requests
import json
from pprint import pprint
from tqdm import tqdm

class Premier_league:
    
    def __init__(self):
        self.base_url = 'https://footballapi.pulselive.com/football'
    
    def get_competion_id(self):
        competitions = {} #Store all competitions
        league = {} #Store info for each competion
        url = self.base_url + '/competitions' 
        params = (
            ('pageSize', '100'),#adds ?pageSize=100 to url
        )
        response = requests.get(url, params = params).json() # request to obtain the id values and corresponding competition

        all_comps = response["content"]
        
        #loop to get all info for all competitions
        for comp in all_comps: 
            
            league[comp["id"]] = comp["description"]

          # creating a stat dict for the player
            competitions[league[comp["id"]]] = {"info":{}}
            competitions[league[comp["id"]]]["info"]["abbreviation"] = comp["abbreviation"]
            competitions[league[comp["id"]]]['info']['id'] = comp['id'] 
            
        f = open("competitions.json","w")

        # pretty prints and writes the same to the json file 
        f.write(json.dumps(competitions,indent=4, sort_keys=False))
        f.close()
              
    def get_clubs(self):
        clubs = {} #Store all clubs
        team = {} #Store info for each team
        url = self.base_url + '/clubs' 
        
        page = 0 #starting value of page
        while True:
            params = (
                ('pageSize', '100'),
                ('page', str(page))#adds ?pageSize=100 to url
                    )
            response = requests.get(url, params = params).json() # request to obtain the team info

            all_clubs = response["content"]
            
            
                    #loop to get all info for all competitions
            for club in all_clubs: 
                clubs[club['name']]= club['teams'][0]['id']
                
                #Unessesary code below, might be of use, produces complex dict-structure
                #team[club["id"]] = club["name"]
                #clubs[team[club["id"]]] = {"info":{}}
                #clubs[team[club["id"]]]['info']['name'] = club["name"]
                #clubs[team[club["id"]]]['info']["id"]= club['teams'][0]['id']

            page += 1
            if page == response["pageInfo"]["numPages"]:
                break
            
        f = open("clubs.json","w")

        # pretty prints and writes the same to the json file 
        f.write(json.dumps(clubs,indent=4, sort_keys=False))
        f.close()

    
    def get_fixtures(self,compSeasons):

        fixtures_unplayed = {} #Store info for not played fixtures
        games_unplayed = {} #Store info for not played games
        
        fixtures_played = {} #Store all clubs
        games_played = {} #Store info for each team
        url = self.base_url + '/fixtures' 

        g = 0
        h = 0
        page = 0 #starting value of page
        while True:
            params = (
                ('pageSize', '100'), #adds ?pageSize=100 to url
                ('page', str(page)),
                ('compSeasons', str(compSeasons)),
                    )
            response = requests.get(url, params = params).json() # request to obtain the team info

            all_games = response["content"]
            
            #loop to get info for each game 
            
            for game in tqdm(all_games): 
                if game['status'] == 'U':
                    games_unplayed[game["id"]] = game['id']
                    fixtures_unplayed[games_unplayed[game["id"]]] = {"match":{}}
                    fixtures_unplayed[games_unplayed[game["id"]]]['match'] = game['id']
                    fixtures_unplayed[games_unplayed[game["id"]]]['kickoff'] = game['fixtureType']
                    fixtures_unplayed[games_unplayed[game["id"]]]['preli_date'] = game['provisionalKickoff']['label']
                    fixtures_unplayed[games_unplayed[game["id"]]]['scientific_date'] = game['provisionalKickoff']['millis']
                    fixtures_unplayed[games_unplayed[game["id"]]]['home_team'] = game['teams'][0]['team']['name']
                    fixtures_unplayed[games_unplayed[game["id"]]]['home_team_id'] = game['teams'][0]['team']['club']['id']
                    fixtures_unplayed[games_unplayed[game["id"]]]['home_team_abbr'] = game['teams'][0]['team']['club']['abbr']
                    fixtures_unplayed[games_unplayed[game["id"]]]['away_team'] = game['teams'][1]['team']['name']
                    fixtures_unplayed[games_unplayed[game["id"]]]['away_team_id'] = game['teams'][1]['team']['club']['id']
                    fixtures_unplayed[games_unplayed[game["id"]]]['away_team_abbr'] = game['teams'][1]['team']['club']['abbr']
                    fixtures_unplayed[games_unplayed[game["id"]]]['grounds'] = game['ground']['name']
                    fixtures_unplayed[games_unplayed[game["id"]]]['grounds_id'] = game['ground']['id']
                    fixtures_unplayed[games_unplayed[game["id"]]]['gameweek'] = game['gameweek']['gameweek']
                    fixtures_unplayed[games_unplayed[game["id"]]]['status'] = game['status']

            for game in tqdm(all_games): 

                if game['status'] == 'C':

                    games_played[game["id"]] = game['id']
                    fixtures_played[games_played[game["id"]]] = {"match":{}}
                    fixtures_played[games_played[game["id"]]]['match'] = game['id']
                    fixtures_played[games_played[game["id"]]]['kickoff'] = game['fixtureType']
                    fixtures_played[games_played[game["id"]]]['preli_date'] = game['provisionalKickoff']['label']
                    fixtures_played[games_played[game["id"]]]['scientific_date'] = game['provisionalKickoff']['millis']
                    fixtures_played[games_played[game["id"]]]['home_team'] = game['teams'][0]['team']['name']
                    fixtures_played[games_played[game["id"]]]['home_team_id'] = game['teams'][0]['team']['club']['id']
                    fixtures_played[games_played[game["id"]]]['home_team_abbr'] = game['teams'][0]['team']['club']['abbr']
                    fixtures_played[games_played[game["id"]]]['home_team_score'] = game['teams'][0]['score']
                    fixtures_played[games_played[game["id"]]]['away_team'] = game['teams'][1]['team']['name']
                    fixtures_played[games_played[game["id"]]]['away_team_id'] = game['teams'][1]['team']['club']['id']
                    fixtures_played[games_played[game["id"]]]['away_team_abbr'] = game['teams'][1]['team']['club']['abbr']
                    fixtures_played[games_played[game["id"]]]['away_team_score'] = game['teams'][1]['score']
                    fixtures_played[games_played[game["id"]]]['grounds'] = game['ground']['name']
                    fixtures_played[games_played[game["id"]]]['grounds_id'] = game['ground']['id']
                    fixtures_played[games_played[game["id"]]]['gameweek'] = game['gameweek']['gameweek']
                    fixtures_played[games_played[game["id"]]]['outcome'] = game['outcome']
                    fixtures_played[games_played[game["id"]]]['extraTime'] = game['extraTime']
                    fixtures_played[games_played[game["id"]]]['shootout'] = game['shootout']
                    fixtures_played[games_played[game["id"]]]['played_time'] = game['clock']['secs']
                    fixtures_played[games_played[game["id"]]]['played_time_label'] = game['clock']['label']
                    fixtures_played[games_played[game["id"]]]['status'] = game['status'] 
   
                     

                
            page +=1
            if page == response["pageInfo"]["numPages"]:
                break
        
        fixtures = dict(fixtures_unplayed)
        fixtures.update(fixtures_played)

        with open("unplayed_fixtures.json","w") as f:
            f.write(json.dumps(fixtures_unplayed,indent=4, sort_keys=True))

        with open("played_fixtures.json","w") as f:
            f.write(json.dumps(fixtures_played,indent=4, sort_keys=True))

        with open("fixtures.json","w") as f:
            f.write(json.dumps(fixtures,indent=4, sort_keys=True))

        

         


if __name__ == "__main__":
    prem = Premier_league()
    prem.get_fixtures(274)



    
    
            
    





