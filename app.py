from flask import Flask, request
from ipl import API

api_obj = API()

app = Flask("__main__")

@app.route('/')
def index():
    return "Welcome to API Project"

@app.route('/api/teams')
def teams():
    response = api_obj.teams_api()
    return response


@app.route('/api/teamvsteam')
def team_vs_team():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    response = api_obj.team_vs_team_api(team1, team2)

    return response

app.run(debug=True)