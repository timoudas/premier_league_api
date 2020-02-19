from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

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
    
