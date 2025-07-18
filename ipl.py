import pandas as pd
import numpy as np
from flask import jsonify
import ast



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
    

    # this function will return the total number of players played IPL match.
    def all_unique_players_api(self):

        if isinstance(matches['Team1Players'].iloc[0], str):
            matches['Team1Players'] = matches['Team1Players'].apply(ast.literal_eval)
            matches['Team2Players'] = matches['Team2Players'].apply(ast.literal_eval)
            
        all_players = matches['Team1Players'].sum() + matches['Team2Players'].sum()
        unique_players = list(set(all_players))

        response = {}
        response['List of All PLayer'] = unique_players
        response['IPL Played by Number of Players'] = len(unique_players)

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
        
        return response


    def team_record_api(self, team):

        response = {}

        temp_df = matches[(matches['Team1'] == team) | (matches['Team2'] == team)]
        
        total_match_played = temp_df.shape[0]
        matches_won = temp_df[temp_df['WinningTeam'] == team].shape[0] 
        matches_draw = temp_df[temp_df['WinningTeam'].isnull()].shape[0]
        matches_loss = total_match_played - (matches_won + matches_draw)
    
        inner_dict = {}
        for t in list(set(list(matches['Team1'].unique()) + list(matches['Team2'].unique()))): 
            if t != team:
                result = API().team_vs_team_api(team, t)
                # print(result)
                inner_dict[t] = result

        response['All Records'] = {
            'Total Match Played' : total_match_played, 
            'Matches Won' : matches_won, 
            'Matches Loss' : matches_loss, 
            'Draw' : matches_draw
        }
        response['Against'] = inner_dict
        print(response)

        return response