import pandas as pd
import numpy as np
from flask import jsonify

# import the dataset from local machine.
matches = pd.read_csv('./datasets/ipl-matches.csv')
deliveries = pd.read_csv('./Datasets/ipl_deliveries - ipl_deliveries.csv')

# define a class for all API function.
class API:

    # this function is return the number of teams played in IPL history
    def teams_api(self):
        response = {}
        response['Teams'] = list(set(list(matches['Team1']) + list(matches['Team2'])))
        return jsonify(response)
    

    # this function return the track record of the given teams
    def team_vs_team_api(self, team1, team2):
        
        temp_df = matches[(matches['Team1'] == team1) & (matches['Team2'] == team2) | (matches['Team1'] == team2) & (matches['Team2'] == team1)]

        total_matches = temp_df.shape[0]
        won_by_team1 = temp_df[temp_df['WinningTeam'] == team1].shape[0]
        won_by_team2 = temp_df[temp_df['WinningTeam'] == team2].shape[0]
        draw_matches = total_matches - (won_by_team1 + won_by_team2)

        response = {}
        response['Total Matches'] = total_matches
        response[team1] = won_by_team1
        response[team2] = won_by_team2
        response['Draw'] = draw_matches
        
        return jsonify(response) 