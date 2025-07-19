import pandas as pd
import numpy as np
from flask import jsonify
import ast
import json



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


    # this function return the team record of the given team.
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

        response['Overall Records'] = {
            'Total Match Played' : total_match_played, 
            'Matches Won' : matches_won, 
            'Matches Loss' : matches_loss, 
            'Draw' : matches_draw
        }
        response['Against'] = inner_dict
        print(response)

        return response
    

    # this function return the record of the given batsman.
    def batter_record_api(self, batsman):

        response = {}
        
        temp_df = deliveries[deliveries['batter'] == batsman]
        
        total_runs_scored = int(temp_df.groupby('batter')['batsman_run'].sum().values[0])
        total_ball_faced = int(temp_df.groupby('batter')['batsman_run'].count().values[0])
        overall_strike_rate = int(np.round((total_runs_scored / total_ball_faced) * 100, 2))
        hit_fours = temp_df[temp_df['batsman_run'] == 4].shape[0]
        hit_sixes = temp_df[temp_df['batsman_run'] == 6].shape[0]


        run_scored_against_each_team = temp_df.groupby('BowlingTeam')['batsman_run'].sum() 
        ball_faced_against_each_team = temp_df.groupby('BowlingTeam')['batter'].count() 
        strike_rate_against_each_team = np.round((run_scored_against_each_team / ball_faced_against_each_team) * 100, 2) 
        hit_fours_against_each_team = temp_df[temp_df['batsman_run'] == 4].groupby('BowlingTeam')['batter'].count() 
        hit_sixes_against_each_team = temp_df[temp_df['batsman_run'] == 6].groupby('BowlingTeam')['batter'].count()
        
        inner_dict = {}
        for row in pd.DataFrame([run_scored_against_each_team, ball_faced_against_each_team, strike_rate_against_each_team, hit_fours_against_each_team, hit_sixes_against_each_team]).transpose().reset_index().itertuples(index=False):
       
            inner_dict[row.BowlingTeam] = {
                'Total Runs Scored': int(row.batsman_run) if not pd.isna(row.batsman_run) else 0,
                'Total Balls Faced': int(row.batter) if not pd.isna(row.batter) else 0,
                'Strike Rate': float(row._3) if not pd.isna(row._3) else 0.0,
                'Hit Fours': int(row._4) if not pd.isna(row._4) else 0,
                'Hit Sixes': int(row._5) if not pd.isna(row._5) else 0
            }
        
        
        response['Overall Records'] = {
            'Total Runs Scored' : total_runs_scored, 
            'Total ball faced' : total_ball_faced, 
            'Overall Strike Rate' : overall_strike_rate, 
            'Hit Boundary as Four' : hit_fours,
            'Hit Boundary as Six' : hit_sixes
        }

        response['Against'] = inner_dict
        
        return jsonify(response)

    # this function return the record of the given Bowler.
    def bowler_record_api(self, bowler_name): 

        response = {}

        Overall_record = {}
        new_df1 = deliveries[~(deliveries['extra_type'] == 'wides')]
        balls_deliver = new_df1.groupby('bowler')['ballnumber'].count()[bowler_name]
        Overall_record['Total Balls Deliver'] = int(balls_deliver)


        new_df1 = deliveries[~(deliveries['extra_type'] == 'legbyes')]
        runs_conceed = new_df1.groupby('bowler')['total_run'].sum()[bowler_name]
        Overall_record['Total Runs Conceed'] = int(runs_conceed)

        economy = float(round((runs_conceed / (balls_deliver / 6)), 2))
        Overall_record['Economy'] = economy

        new_df2 = deliveries[(deliveries['isWicketDelivery'] == 1) & ~(deliveries['kind'] == 'run out') & ~(deliveries['kind'] == 'retired hurt')]
        wickets_taken = int(new_df2.groupby('bowler')['isWicketDelivery'].count()[bowler_name])
        Overall_record['Wickets'] = wickets_taken

        average = round(runs_conceed / wickets_taken, 2)
        Overall_record['Average'] = float(average)

        strike_rate = round(balls_deliver / wickets_taken, 2)
        Overall_record['Strike Rate'] = float(strike_rate)

        new_df3 = deliveries[['ID', 'bowler']].drop_duplicates(keep = 'first')
        matches_played = int(new_df3.groupby('bowler')['ID'].count()[bowler_name])
        Overall_record['Total Matches'] = matches_played
        
        response['Overall Record'] = Overall_record
        return jsonify(response)
