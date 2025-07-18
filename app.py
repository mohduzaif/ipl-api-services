from flask import Flask, request, jsonify
from ipl import API

api_obj = API()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    return "Welcome to API Project"



@app.route('/api/teams')
def teams():
    response = api_obj.teams_api()
    return response



@app.route('/api/players')
def all_unique_players():
    response = api_obj.all_unique_players_api()
    return response



@app.route('/api/teamvsteam')
def team_vs_team():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    response = api_obj.team_vs_team_api(team1, team2)

    return jsonify(response)

@app.route('/api/team-record')
def team_record():
    team = request.args.get('team')

    response = api_obj.team_record_api(team)

    return jsonify(response)


app.run(debug=True)