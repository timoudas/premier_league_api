# Premier League Betting Calculator

This will become a webb-app for getting odds on primarly PL but also other leagues in the future. Data is feeded through an API to .json files that are loaded into a database. 

To save time a pickled file containg all nesserary id's to fetch playerstats, fixturestats and team standings are stored in a dict where the league and season is the key.

```python
dict['EN_PR_2019/2020']
```

## CLI

The ````cli_stats.py``` is an interactive command line interface to fetch data from the API. To be able to utilize the ICLI season_params.json and the league_season_init is required. 


## Setup

The 

```setup.py```

 loads the pickled file league_seasons_init which contains all the id's.This will developed into a CLI where the user can see which leagues exist and how to query them to get stats.

### Example
```python

import pickle
with open('league_season_init, 'rb') as f:
    leagues = pickle.load(f)
    leagues['EN_PR_2019/2020'].team_standings()
    leagues['EN_PR_2019/2020'].fixture_stats()
    leagues['EN_PR_2019/2020'].player_stats()
```

Files will be saved in ../json/params/stats folder that is created if it doesn't exist.

## Data cleaning

To clean the different .json files in json/params/stats to the  
