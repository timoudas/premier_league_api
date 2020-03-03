import pymongo
import os
from pymongo import MongoClient
import json
os.chdir("../json")

with open("test_leauges.json") as leagues:
    json_leagues = json.load(leagues)

with open("test_teams.json") as teams:
    json_teams = json.load(teams)

cluster = MongoClient('mongodb+srv://admin:kommer10@db-k0ycg.mongodb.net/test?retryWrites=true&w=majority')
db = cluster['db']
collectionLeague = db['leagues']
collectionTeam = db['teams']



def pushLeagues():
    print('Pushing leagues to database...')
    for league in json_leagues:
        # Iterating through all objects in leagues JSON object and pushing them to database.
        post = {
            'id': json_leagues[league]["id"],
            'abbreviation': json_leagues[league]["abbreviation"],
            'descripion': json_leagues[league]["description"],
            'level': json_leagues[league][ "level"]
        }
        existingPost = collectionLeague.find_one(post)
        if existingPost == None: # If the league doesnt exist in the database then push it
            collectionLeague.insert_one(post)
        else: # If the league already exists in the databse then update it with new values from the json file.
            updatedPost = {
            '$set': {'id': json_leagues[league]["id"]},
            '$set': {'abbreviation': json_leagues[league]["abbreviation"]},
            '$set': {'descripion': json_leagues[league]["description"]},
            '$set': {'level': json_leagues[league][ "level"]}
            }
            collectionLeague.update_one(post, updatedPost)
        

    print('Finished!')

def pushTeams():
    print('Pushing teams to database...')
    for team in json_teams:
        # Iterating through all objects in leagues JSON object and pushing them to database.
        
        post = {
        'id': json_teams[team]["club"]["id"],
        'name': json_teams[team]["club"]["name"],
        'abbreviation': json_teams[team]["club"]["abbr"],
        'teamType': json_teams[team]["teamType"],
        'stadium': json_teams[team]["grounds"][0]["name"],
        'location': json_teams[team]["grounds"][0]["city"],
        'stadium_id': json_teams[team]["grounds"][0]["id"],
        'league_id': json_teams[team]["competition"]
        }
       
        existingPost = collectionLeague.find_one(post)
        if existingPost == None: # If the league doesnt exist in the database then push it
            collectionTeam.insert_one(post)
        else: # If the league already exists in the databse then update it with new values from the json file.
           
            updatedPost = {
            '$set': {'id': json_teams[team]["club"]["id"]},
            '$set': {'name': json_teams[team]["club"]["name"]},
            '$set': {'abbreviation': json_teams[team]["club"]["abbr"]},
            '$set': {'teamType': json_teams[team]["teamType"]},
            '$set': {'stadium': json_teams[team]["grounds"][0]["name"]},
            '$set': {'location': json_teams[team]["grounds"][0]["city"]},
            '$set': {'stadium_id': json_teams[team]["grounds"][0]["id"]},
            '$set': {'league_id': json_teams[team]["competition"]}
            }
            
            collectionTeam.update_one(post, updatedPost)
            
    print('Finished!')



#pushLeagues()
pushTeams()

