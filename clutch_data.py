from nba_api.stats.endpoints.leaguedashteamclutch import LeagueDashTeamClutch

season = '2020-21'
season_type = 'Regular Season'
clutch_time = 'Last 5 Minutes'
point_diff = 5
df = LeagueDashTeamClutch(season_type_all_star=season_type,
                          clutch_time=clutch_time,
                          measure_type_detailed_defense='Base',
                          point_diff=point_diff,
                          per_mode_detailed='PerGame',
                          season=season).league_dash_team_clutch.get_data_frame()
df.to_csv('clutch_data.csv', index=False)
df['KLAW_Score'] = (df['MIN'] * df['W_PCT']) * df['PLUS_MINUS']
df2 = df[['TEAM_NAME','KLAW_Score']]
df2.sort_values(ascending=False,by='KLAW_Score',inplace=True)
df2 = df2.reset_index(drop=True)
df2.to_csv('results.csv', index=False)