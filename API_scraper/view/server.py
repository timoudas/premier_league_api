from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from model.directory import StorageConfig
from model.directory import Directory


"""
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
TO START SERVER REMEMBER:
    * Be in the view folder
    * To have done 'pip install flask'
    * To have done 'pip install datetime'
    * Run 'python server.py'
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
"""

app = Flask(__name__, template_folder="templates")

""" HOME PAGE """
@app.route('/')
def index():
    return render_template('home/index.html')

""" LEAGUES """
@app.route('/leagues/viewLeagues')
def viewLeague():
    print("Here we load all leagues from db")
    return render_template('leagues/viewLeagues.html')

""" GAMES """
@app.route('/games/viewGames')
def viewGames():
    print("Here we load all games from db")

    response = json.dumps(league_params, sort_keys = True, indent = 4, separators = (',', ': '))
    return render_template('games/viewGames.html')

""" BETS """
@app.route('/bets/viewBets')
def viewBets():
    print("Here we load all bets from db")
    return render_template('bets/viewBets.html')

""" STATS """
@app.route('/stats/players')
def viewPlayerStats():
    print("Here we load all player stats")
    return render_template('stats/players.html')


if __name__ == "__main__":
    app.run(debug=True)
    
