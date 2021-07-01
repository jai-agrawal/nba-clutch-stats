from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints.scoreboard import Scoreboard
import pandas as pd
from difflib import SequenceMatcher
import time

class Team():
    def __init__(self, **kwargs):
        self.name = kwargs.get('team_name')
        self.teams_dict = teams.get_teams()
        time.sleep(.600)

    def _get_team_id(self):
        try:
            team = [team for team in self.teams_dict if similar(team['full_name'],self.name) > 0.5]
            self.name = team[0]['full_name']
            self.teamID = int(team[0]['id'])
            time.sleep(.600)
            return self.teamID
        except:
            pass

    def get_data(self, season, season_type):
        try:
            team_id = self._get_team_id()
            team_log = teamgamelog.TeamGameLog(season=season, season_type_all_star=season_type, team_id=team_id)
            time.sleep(.600)
            return team_log.get_data_frames()[0]
        except:
            print('Incorrect team name, season or season type entered')

    def get_team_list(self):
        teams = [team for team in self.teams_dict]
        team_names = []
        for team in teams:
            team_names.append(team['full_name'])
        return team_names

    def get_4q_scores(self,df):
        scores_4q = list()
        for i in range(len(df)):
            scores_df = Scoreboard(day_offset=0, game_date=df['GAME_DATE'][i]).line_score.get_data_frame()
            time.sleep(.600)
            game = scores_df[(scores_df['GAME_ID'] == (df['Game_ID'][i])) & (scores_df['TEAM_ID'] == self.teamID)]
            score_4q = int(game['PTS_QTR4'])
            scores_4q.append(score_4q)
        return scores_4q

    def get_quarter_scores(self, df):
        scores_Q1 = list()
        scores_Q2 = list()
        scores_Q3 = list()
        scores_Q4 = list()
        for i in range(len(df)):
            scores_df = Scoreboard(day_offset=0, game_date=df['GAME_DATE'][i]).line_score.get_data_frame()
            time.sleep(.600)
            game = scores_df[(scores_df['GAME_ID'] == (df['Game_ID'][i])) & (scores_df['TEAM_ID'] == self.teamID)]
            scores_Q1.append(int(game['PTS_QTR1']))
            scores_Q2.append(int(game['PTS_QTR2']))
            scores_Q3.append(int(game['PTS_QTR3']))
            scores_Q4.append(int(game['PTS_QTR4']))
        df = df.assign(Q1=scores_Q1, Q2=scores_Q2, Q3=scores_Q3, Q4=scores_Q4)
        return df

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def main():
    season = '2020'
    season_type = 'Regular Season'
    all_teams = Team()
    all_team_names = all_teams.get_team_list()
    data = []
    for team_name in all_team_names:
        curr_team = Team(team_name=team_name)
        df_wq = curr_team.get_quarter_scores(curr_team.get_data(season, season_type))
        df_wq.to_csv(f'data/{team_name.split()[-1]}.csv')
        data.append(
            {'Team': team_name, 'Q1_mean': df_wq['Q1'].mean(), 'Q2_mean': df_wq['Q2'].mean(),
             'Q3_mean': df_wq['Q3'].mean(), 'Q4_mean': df_wq['Q4'].mean()}
        )
    df = pd.DataFrame(data)
    highest_scoring_team_idx = df['Q4_mean'].idxmax()
    lowest_scoring_team_idx = df['Q4_mean'].idxmin()
    print(
        f"Highest Scoring Team: {df['Team'][highest_scoring_team_idx]}; {df['Q4_mean'][highest_scoring_team_idx]} Points")
    print(
        f"Lowest Scoring Team: {df['Team'][lowest_scoring_team_idx]}; {df['Q4_mean'][lowest_scoring_team_idx]} Points")
    df.to_csv('data.csv', index=False)
main()