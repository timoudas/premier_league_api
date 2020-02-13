import requests
import json


response = requests.get('https://footballapi.pulselive.com/football/competitions/1/compseasons?page=0&pageSize=100').json() # request to obtain the id values and corresponding season 

id = int(response["content"][0]["id"]) # converts current season id which is a decimal point value to interger

players = {} # dictionary to store players data

playersAndStats = {} # dictionary to store player name and associated stats

numEntries = 100

page = 0

# loop to get player name and id
while True: 

    params = (
      ('pageSize', '100'),
      ('compSeasons', str(id)), 
      ('altIds', 'true'),
      ('page', str(page)),
      ('type', 'player'),
      ('id', '-1'),
      ('compSeasonId', str(id)),
  )

    response = requests.get('https://footballapi.pulselive.com/football/players',params=params).json()

    playersData = response["content"]

    for playerData in playersData:
        players[playerData["id"]] = playerData["name"]["display"]

    # creating a stat dict for the player
        playersAndStats[players[playerData["id"]]] = {"stats":{}}

    # code to get the current or previous team of the player
        if "currentTeam" in playerData:
            playersAndStats[players[playerData["id"]]]["stats"]["currentTeam"] = playerData["currentTeam"]["club"]["name"]
        elif "previousTeam" in playerData:
            playersAndStats[players[playerData["id"]]]["stats"]["previousTeam"] = playerData["previousTeam"]["club"]["name"]      
    page += 1

    if page == response["pageInfo"]["numPages"]:
        break

print("Total no. of players :",len(players))

count = 0 
total = len(players)

# loop to get player stats 
for player in players:

    count += 1
    #print(count,"/",total)

    params = (
      ('comps', '1'),
      ('compSeasons', str(id)), # setting season id to current season id
  )

    playerId = str(int(player))

  # gets the stat of the player using playerId 
    response = requests.get('https://footballapi.pulselive.com/football/stats/player/'+playerId,params=params).json()

    playerInfo = response["entity"]

    stats = response["stats"]

    

  # storing player info
    playersAndStats[players[player]]["stats"]["name"] = playerInfo["name"]["display"]
    if "age" in playerInfo:
        playersAndStats[players[player]]["stats"]["age"] = playerInfo["age"]
    if "country" in playerInfo["nationalTeam"]:
        playersAndStats[players[player]]["stats"]["country"] = playerInfo["nationalTeam"]["country"]
    if "date" in playerInfo["birth"]:
        playersAndStats[players[player]]["stats"]["birthdate"] = playerInfo["birth"]["date"]["label"]
        playersAndStats[players[player]]["stats"]["name"] = playerInfo["name"]["display"]
        playersAndStats[players[player]]["stats"]["position"] = playerInfo["info"]["position"]
        playersAndStats[players[player]]["stats"]["positionInfo"] = playerInfo["info"]["positionInfo"]
    if "shirtNum" in playerInfo["info"]:
        playersAndStats[players[player]]["stats"]["shirtNum"] = str(int(playerInfo["info"]["shirtNum"]))
    if count == 200:
        print('200')
    elif count == 400:
        print('400')
    elif count == 600:
        print('600')
    elif count == 800:
        print('800')

  # loop to store each stat associated with the player
    for stat in stats:
        playersAndStats[players[player]]["stats"][stat["name"].replace("_"," ").capitalize()] = int(stat["value"])

# to store data to a json file 
f = open("../json/data.json","w")

# pretty prints and writes the same to the json file 
f.write(json.dumps(playersAndStats,indent=4, sort_keys=True))
f.close()

print("Saved to data.json")