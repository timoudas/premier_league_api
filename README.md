# Premier League CLI and Dashboard

## CLI

The ```cli_stats.py``` is an interactive command line interface to fetch, clean and push data from the API to a MongoDB. To be able to utilize the ICLI season_params.json and the league_season_init is required.

### Example usage

```bash 
>>> python cli_stats.py -i
>>> download -p en_pr 2019 #Downloads playerstats for PremierLeague season 2019/2020
>>> clean -p en_pr 2019 #Cleans the data
>>> db -p en_pr 2019 #Pushes the data to a collection EN_PR2019
>>> exit
```

## Dashboard

The `dashboard.py` is a build upon `plotly.dash`. This is under development.

## Directory

`directory` is a package to help deal with the loading/saving and writing of json-files that are used extensively through out the process.
This package is needed to use the ICLI and the dashboard. 

### Install

clone the repository and stand in the same directory as the `setup.py` and run below.
`pip install .`
