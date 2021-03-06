import pandas as pd
import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
from hyperopt import Trials, STATUS_OK, tpe
from keras.datasets import mnist
from keras.layers.core import Dense, Dropout, Activation
from keras.models import Sequential
from keras.utils import np_utils
from hyperas import optim
from hyperas.distributions import choice, uniform
from keras import optimizers
import tensorflow as tf

df = pd.read_csv('Seasons_Stats.csv')

df= df.sort_values(by=['Player', 'Year'])
df=df.dropna(subset=['Player'])
df = df[df.Tm != "TOT"]

playerMoveDS = pd.DataFrame(columns=np.append(df.columns.values+'1', df.columns.values+'2'))
np_df=df.values

#Detect instances of players switching teams

j=0
for i in range(np_df.shape[0]):
    if np_df[i][2]==np_df[i-1][2]:
        if np_df[i][5]!=np_df[i-1][5]:
            a=np.append(np_df[i-1],np_df[i])
            playerMoveDS.loc[j]=a
            j+=1
            
cols_to_standardize_1=['OBPM1', 'DBPM1', 'BPM1','FG1', 'FGA1',
       '3P1', '3PA1', '2P1', '2PA1', 'FT1', 'FTA1',
       'ORB1', 'DRB1', 'TRB1', 'AST1', 'STL1', 'BLK1', 'TOV1', 'PF1',
       'PTS1']
cols_to_standardize_2= ['OBPM2', 'DBPM2', 'BPM2','FG2', 'FGA2',
       '3P2', '3PA2', '2P2', '2PA2', 'FT2', 'FTA2',
       'ORB2', 'DRB2', 'TRB2', 'AST2', 'STL2', 'BLK2', 'TOV2', 'PF2',
       'PTS2', 'DWS', 'OWS']

#Put stats on per minute basis (except for percentage stats)

for i in cols_to_standardize_1:
    playerMoveDS[i]=playerMoveDS[i]/playerMoveDS['MP1']
for i in cols_to_standardize_2:
    playerMoveDS[i]=playerMoveDS[i]/playerMoveDS['MP2']

playerMoveDS['MP1']=playerMoveDS['MP1']/playerMoveDS['G1']
playerMoveDS['MP2']=playerMoveDS['MP2']/playerMoveDS['G2']
playerMoveDS=playerMoveDS.round(4)
playerMoveDS=playerMoveDS.drop(['blanl','blanl1', 'blank2', 'blank21','Unnamed: 01', 'Unnamed: 0'], axis=1)
playerMoveDS["Year1"] = playerMoveDS["Year1"].astype(int)
playerMoveDS["Year2"] = playerMoveDS["Year2"].astype(int)
playerMoveDS = playerMoveDS.rename(columns={'Tm1': 'Team1'})
playerMoveDS = playerMoveDS.rename(columns={'Tm2': 'Team2'})

team_name_replace_dict={'GSW': 'Golden State Warriors', 'LAL': 'Los Angeles Lakers','PHO': 'Phoenix Suns',
                       'DAL': 'Dallas Mavericks','CHI': 'Chicago Bulls','IND': 'Indiana Pacers',
                       'WAS': 'Washington Wizards','MIN': 'Minnesota Timberwolves','CLE': 'Cleveland Cavaliers',
                       'HOU': 'Houston Rockets','SAC': 'Sacramento Kings','DEN': 'Denver Nuggets', 
                       'NOH': 'New Orleans Hornets','TOR': 'Toronto Raptors', 'POR': 'Portland Trail Blazers',
                       'DET': 'Detroit Pistons','PHI': 'Philadelphia 76ers','UTA': 'Utah Jazz', 'MIL': 'Milwaukee Bucks',
                       'VAN': 'Vancouver Grizzlies', 'SEA': 'Seattle SuperSonics', 'NJN': 'New Jersey Nets', 
                       'NOK': 'New Orleans Hornets', 'BOS': 'Boston Celtics', 'ATL': 'Atlanta Hawks', 'CHA': 'Charlotte Hornets',
                       'MEM': 'Memphis Grizzlies', 'ORL': 'Orlando Magic','NYK': 'New York Knicks', 'CHO': 'Charlotte Bobcats',
                       'LAC': 'Los Angeles Clippers', 'SDC': 'San Diego Clippers', 'NOP': 'New Orleans Pelicans', 'BRK': 'Brooklyn Nets',
                       'MIA': 'Miami Heat', 'SAS': 'San Antonio Spurs', 'CHH': 'Charlotte Hornets', 'WSB': 'Washington Bullets', 
                       'OKC': 'Oklahoma City Thunder','KCK': 'Kansas City Kings'
                       }

playerMoveDS=playerMoveDS.replace({'Team1': team_name_replace_dict}, regex=True)
playerMoveDS=playerMoveDS.replace({'Team2': team_name_replace_dict}, regex=True)

#Read in NBA season TEAM stats datasets (seperate from individual stats datasets) 
#Each dataset is composed of 3 seperate datasets per season: Team Statistics, Team Opponent Statistics, Miscellaneous Statistics    
#Separating inputted data team, opponent, misc datasets ; Data file shape depends on year due to different # teams/available stats

team_data={}
for i in range(1980,2019):
       team_data[i]={}
       td=pd.read_excel('nba'+str(i)+'.xlsx', header=0)
       na_ind=nba1980.index[nba1980['Team'].isna()].tolist()
       #:a, a+2:b , b+2: 
       team=td[:na_ind[0]]
       opp=td[na_ind[0]+2:na_ind[1]]
       misc=td[na_ind[1]+2:]
        
       team=team.drop(['z'], axis=1)
       opp=opp.drop(['z'], axis=1)
       misc=misc.drop(['Arena'], axis=1)
    
       team['year']=i
       opp['year']=i
       misc['year']=i
       
       team_data[i]['team']=team
       team_data[i]['opp']=opp
       team_data[i]['misc']=misc

#Merge team,opp, misc stats by year
       
teams_dict={}
for i in range(1980,2019):
    merge_1=team_data[i]['team'].merge(team_data[i]['opp'], on="Team")
    merge_final=merge_1.merge(team_data[i]['misc'], on="Team")
    
    #take out * from team and convert team to 3 letter abrev
    #change some col names
    merge_final['Team'] = merge_final['Team'].map(lambda x: x.rstrip('*'))
    merge_final['Team1']=merge_final['Team']
    merge_final.columns.values[66]="eFG%Off"
    merge_final.columns.values[70]="eFG%Def"
    merge_final.columns.values[69]="FT/FGAOff"
    merge_final.columns.values[73]="FT/FGADef"
    merge_final.columns.values[67]="TOV%Off"
    merge_final.columns.values[71]="TOV%Def"
    teams_dict[i]=merge_final
    teams_dict[i].set_index("Team", inplace=True)
    
teams_dict[1980].columns.values[74] = "Attend."
teams_dict[1980].columns.values[75] = "Attend./G"
teams_dict[1980]["Attend."]=0
teams_dict[1980]["Attend./G"]=0
teams_dict[2017].columns.values[9]="3P%_x"
teams_dict[2017].columns.values[12]="2P%_x"
teams_dict[2017].columns.values[34]="3P%_y"
teams_dict[2017].columns.values[37]="2P%_y"

#No attendance data for 1980 season -- Use 1981 season attendance data in this case
for i in range(len(teams_dict[1980]['Team'].values)):
    team1981attend= teams_dict[1981].loc[teams_dict[1981]['Team']==teams_dict[1980]['Team'].values[i]]['Attend.']
    teams_dict[1980].at[i,'Attend.']=team1981attend
        
teams_adj = pd.DataFrame(columns=np.append(teams_dict[2018].columns.values, teams_dict[2018].columns.values+'2'))

#Make datasets consistent in terms of team names

for i in range(playerMoveDS.shape[0]): 
    team1=playerMoveDS.iloc[i]['Team1'] 
    team2=playerMoveDS.iloc[i]['Team2']
    
    year1=playerMoveDS.iloc[i]['Year1']
    year2=playerMoveDS.iloc[i]['Year2']

    if year1==2005 or year1==2006 or year1==2007:
        if team1=="New Orleans Hornets":
            team1="Charlotte Bobcats"
    
    if year2==2005 or year2==2006 or year2==2007:
        if team2=="New Orleans Hornets":
            team2="Charlotte Bobcats"   

    hornetsyears=[2005,2006,2007,2008,2009,2010,2011,2012,2013,2014]
    bobcatsyears=[2015,2016,2017]

    if year1 in hornetsyears:
        if team1=="Charlotte Hornets":
            team1="Charlotte Bobcats"

    if year2 in hornetsyears:
        if team2=="Charlotte Hornets":
            team2="Charlotte Bobcats"

    if year1 in bobcatsyears:
        if team1=="Charlotte Bobcats":
            team1="Charlotte Hornets"
    
    if year2 in bobcatsyears:
        if team2=="Charlotte Bobcats":
            team2="Charlotte Hornets"

    row1=teams_dict[str(year1)].loc[[team1]]
    row2=teams_dict[str(year2)].loc[[team2]]
    row2.columns=teams_dict[2018].columns.values+'2'
    rows=pd.concat([row1.reset_index(drop=True), row2.reset_index(drop=True)], axis=1)
    
    teamsadj=teamsadj.append(rows.iloc[0],ignore_index=True)
    
PlayerTeamDF = pd.concat([playerMoveDS.reset_index(drop=True), teamsadj], axis=1)

#Interesting Variables: G1, GS1, MP1, USG%1,3PA1, 2PA1,FTA1
PlayerTeamDF=PlayerTeamDF.drop(['Team1', 'Year1', 'Year2', 'Player2',
       'Pos2', 'Age2', 'Tm2', 'G2', 'GS2', 'PER2', 'TS%2', '3PAr2',
       'FTr2', 'ORB%2', 'DRB%2', 'TRB%2', 'AST%2', 'STL%2', 'BLK%2',
       'TOV%2', 'OWS2', 'DWS2', 'WS2', 'OBPM2',
       'DBPM2', 'BPM2', 'VORP2', 'FG2', 'FGA2', 'FG%2', '3P2',
       '3P%2', '2P2', '2P%2', 'eFG%2', 'FT2', 'FTA2', 'FT%2',
       'ORB2', 'DRB2', 'TRB2', 'AST2', 'STL2', 'BLK2', 'TOV2', 'PF2',
       'PTS2'], axis=1)
    
regPT=PlayerTeamDF.copy()
regPT.columns=['Player', 'Pos', 'Age', 'G', 'GS', 'MP', 'PER', 'TS%', '3PAr',
       'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%',
       'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP',
       'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%',
       'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK',
       'TOV', 'PF', 'PTS','MP1','USG%1','WS/481','3PA1','2PA1', 'Rk_xTeam1', 'G_xTeam1', 'MP_xTeam1', 'FG_xTeam1',
       'FGA_xTeam1', 'FG%_xTeam1', '3P_xTeam1', '3PA_xTeam1', '3P%_xTeam1', '2P_xTeam1', '2PA_xTeam1',
       '2P%_xTeam1', 'FT_xTeam1', 'FTA_xTeam1', 'FT%_xTeam1', 'ORB_xTeam1', 'DRB_xTeam1', 'TRB_xTeam1',
       'AST_xTeam1', 'STL_xTeam1', 'BLK_xTeam1', 'TOV_xTeam1', 'PF_xTeam1', 'PTS_xTeam1', 'year_xTeam1',
       'Rk_yTeam1', 'G_yTeam1', 'MP_yTeam1', 'FG_yTeam1', 'FGA_yTeam1', 'FG%_yTeam1', '3P_yTeam1', '3PA_yTeam1',
       '3P%_yTeam1', '2P_yTeam1', '2PA_yTeam1', '2P%_yTeam1', 'FT_yTeam1', 'FTA_yTeam1', 'FT%_yTeam1',
       'ORB_yTeam1', 'DRB_yTeam1', 'TRB_yTeam1', 'AST_yTeam1', 'STL_yTeam1', 'BLK_yTeam1', 'TOV_yTeam1',
       'PF_yTeam1', 'PTS_yTeam1', 'year_yTeam1', 'RkTeam1', 'AgeTeam1', 'WTeam1', 'LTeam1', 'PWTeam1', 'PLTeam1',
       'MOVTeam1', 'SOSTeam1', 'SRSTeam1', 'ORtgTeam1', 'DRtgTeam1', 'PaceTeam1', 'FTrTeam1', '3PArTeam1', 'TS%Team1',
       'eFG%OffTeam1', 'TOV%OffTeam1', 'ORB%Team1', 'FT/FGAOffTeam1', 'eFG%DefTeam1', 'TOV%DefTeam1', 'DRB%Team1', 'FT/FGADefTeam1',
       'Attend.Team1', 'Attend./GTeam1', 'yearTeam1', 'Team1', 'Rk_xTeam2', 'G_xTeam2', 'MP_xTeam2',
       'FG_xTeam2', 'FGA_xTeam2', 'FG%_xTeam2', '3P_xTeam2', '3PA_xTeam2', '3P%_xTeam2', '2P_xTeam2',
       '2PA_xTeam2', '2P%_xTeam2', 'FT_xTeam2', 'FTA_xTeam2', 'FT%_xTeam2', 'ORB_xTeam2',
       'DRB_xTeam2', 'TRB_xTeam2', 'AST_xTeam2', 'STL_xTeam2', 'BLK_xTeam2', 'TOV_xTeam2',
       'PF_xTeam2', 'PTS_xTeam2', 'year_xTeam2', 'Rk_yTeam2', 'G_yTeam2', 'MP_yTeam2', 'FG_yTeam2',
       'FGA_yTeam2', 'FG%_yTeam2', '3P_yTeam2', '3PA_yTeam2', '3P%_yTeam2', '2P_yTeam2', '2PA_yTeam2',
       '2P%_yTeam2', 'FT_yTeam2', 'FTA_yTeam2', 'FT%_yTeam2', 'ORB_yTeam2', 'DRB_yTeam2',
       'TRB_yTeam2', 'AST_yTeam2', 'STL_yTeam2', 'BLK_yTeam2', 'TOV_yTeam2', 'PF_yTeam2',
       'PTS_yTeam2', 'year_yTeam2', 'RkTeam2', 'AgeTeam2', 'WTeam2', 'LTeam2', 'PWTeam2', 'PLTeam2',
       'MOVTeam2', 'SOSTeam2', 'SRSTeam2', 'ORtgTeam2', 'DRtgTeam2', 'PaceTeam2', 'FTrTeam2', '3PArTeam2',
       'TS%Team2', 'eFG%OffTeam2', 'TOV%OffTeam2', 'ORB%Team2', 'FT/FGAOffTeam2', 'eFG%DefTeam2', 'TOV%DefTeam2',
       'DRB%Team2', 'FT/FGADefTeam2', 'Attend.Team2', 'Attend./GTeam2', 'yearTeam2', 'Team2']

regPT=regPT.drop(['Attend./GTeam1','Attend./GTeam2'], axis=1)

regPT = regPT[['Player','yearTeam1', 'Team1' ,'yearTeam2', 'Team2', 'Pos', 'Age', 'G', 'GS', 'MP', 'PER', 'TS%', '3PAr',
       'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%',
       'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP',
       'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%',
       'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK',
       'TOV', 'PF', 'PTS', 'MP1','USG%1', '3PA1','2PA1', 'Rk_xTeam1', 'G_xTeam1', 'MP_xTeam1', 'FG_xTeam1',
       'FGA_xTeam1', 'FG%_xTeam1', '3P_xTeam1', '3PA_xTeam1', '3P%_xTeam1', '2P_xTeam1', '2PA_xTeam1',
       '2P%_xTeam1', 'FT_xTeam1', 'FTA_xTeam1', 'FT%_xTeam1', 'ORB_xTeam1', 'DRB_xTeam1', 'TRB_xTeam1',
       'AST_xTeam1', 'STL_xTeam1', 'BLK_xTeam1', 'TOV_xTeam1', 'PF_xTeam1', 'PTS_xTeam1', 'year_xTeam1',
       'Rk_yTeam1', 'G_yTeam1', 'MP_yTeam1', 'FG_yTeam1', 'FGA_yTeam1', 'FG%_yTeam1', '3P_yTeam1', '3PA_yTeam1',
       '3P%_yTeam1', '2P_yTeam1', '2PA_yTeam1', '2P%_yTeam1', 'FT_yTeam1', 'FTA_yTeam1', 'FT%_yTeam1',
       'ORB_yTeam1', 'DRB_yTeam1', 'TRB_yTeam1', 'AST_yTeam1', 'STL_yTeam1', 'BLK_yTeam1', 'TOV_yTeam1',
       'PF_yTeam1', 'PTS_yTeam1', 'year_yTeam1', 'RkTeam1', 'AgeTeam1', 'WTeam1', 'LTeam1', 'PWTeam1', 'PLTeam1',
       'MOVTeam1', 'SOSTeam1', 'SRSTeam1', 'ORtgTeam1', 'DRtgTeam1', 'PaceTeam1', 'FTrTeam1', '3PArTeam1', 'TS%Team1',
       'eFG%OffTeam1', 'TOV%OffTeam1', 'ORB%Team1', 'FT/FGAOffTeam1', 'eFG%DefTeam1', 'TOV%DefTeam1', 'DRB%Team1', 'FT/FGADefTeam1',
       'Attend.Team1', 'Rk_xTeam2', 'G_xTeam2', 'MP_xTeam2',
       'FG_xTeam2', 'FGA_xTeam2', 'FG%_xTeam2', '3P_xTeam2', '3PA_xTeam2', '3P%_xTeam2', '2P_xTeam2',
       '2PA_xTeam2', '2P%_xTeam2', 'FT_xTeam2', 'FTA_xTeam2', 'FT%_xTeam2', 'ORB_xTeam2',
       'DRB_xTeam2', 'TRB_xTeam2', 'AST_xTeam2', 'STL_xTeam2', 'BLK_xTeam2', 'TOV_xTeam2',
       'PF_xTeam2', 'PTS_xTeam2', 'year_xTeam2', 'Rk_yTeam2', 'G_yTeam2', 'MP_yTeam2', 'FG_yTeam2',
       'FGA_yTeam2', 'FG%_yTeam2', '3P_yTeam2', '3PA_yTeam2', '3P%_yTeam2', '2P_yTeam2', '2PA_yTeam2',
       '2P%_yTeam2', 'FT_yTeam2', 'FTA_yTeam2', 'FT%_yTeam2', 'ORB_yTeam2', 'DRB_yTeam2',
       'TRB_yTeam2', 'AST_yTeam2', 'STL_yTeam2', 'BLK_yTeam2', 'TOV_yTeam2', 'PF_yTeam2',
       'PTS_yTeam2', 'year_yTeam2', 'RkTeam2', 'AgeTeam2', 'WTeam2', 'LTeam2', 'PWTeam2', 'PLTeam2',
       'MOVTeam2', 'SOSTeam2', 'SRSTeam2', 'ORtgTeam2', 'DRtgTeam2', 'PaceTeam2', 'FTrTeam2', '3PArTeam2',
       'TS%Team2', 'eFG%OffTeam2', 'TOV%OffTeam2', 'ORB%Team2', 'FT/FGAOffTeam2', 'eFG%DefTeam2', 'TOV%DefTeam2',
       'DRB%Team2', 'FT/FGADefTeam2', 'Attend.Team2', 'WS/481']]

#regPT['FT%']=regPT['FT']/regPT['FTA']
#X.isna().sum().sort_values(ascending=False)

#General NA DROP****
#regPT=regPT.dropna(subset=['WS/481', 'ORB%', 'DRB%','TRB%','AST%','STL%','BLK%','TOV%',''])

#Drop 3P% col since it has lot of NA's, can manually reconstruct 3P% col by doing 3PM/3PA 

regPT=regPT.drop(['3P%'], axis=1)

regPT=regPT.dropna()
regPT['3P%']=(regPT['3P']/regPT['3PA']).replace(np.inf, 0).replace(np.nan,0)

regPT = regPT[['Player','yearTeam1', 'Team1' ,'yearTeam2', 'Team2', 'Pos', 'Age', 'G', 'GS', 'MP', 'PER', 'TS%', '3PAr',
       'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%',
       'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP',
       'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%',
       'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK',
       'TOV', 'PF', 'PTS', 'MP1','USG%1', '3PA1','2PA1', 'Rk_xTeam1', 'G_xTeam1', 'MP_xTeam1', 'FG_xTeam1',
       'FGA_xTeam1', 'FG%_xTeam1', '3P_xTeam1', '3PA_xTeam1', '3P%_xTeam1', '2P_xTeam1', '2PA_xTeam1',
       '2P%_xTeam1', 'FT_xTeam1', 'FTA_xTeam1', 'FT%_xTeam1', 'ORB_xTeam1', 'DRB_xTeam1', 'TRB_xTeam1',
       'AST_xTeam1', 'STL_xTeam1', 'BLK_xTeam1', 'TOV_xTeam1', 'PF_xTeam1', 'PTS_xTeam1', 'year_xTeam1',
       'Rk_yTeam1', 'G_yTeam1', 'MP_yTeam1', 'FG_yTeam1', 'FGA_yTeam1', 'FG%_yTeam1', '3P_yTeam1', '3PA_yTeam1',
       '3P%_yTeam1', '2P_yTeam1', '2PA_yTeam1', '2P%_yTeam1', 'FT_yTeam1', 'FTA_yTeam1', 'FT%_yTeam1',
       'ORB_yTeam1', 'DRB_yTeam1', 'TRB_yTeam1', 'AST_yTeam1', 'STL_yTeam1', 'BLK_yTeam1', 'TOV_yTeam1',
       'PF_yTeam1', 'PTS_yTeam1', 'year_yTeam1', 'RkTeam1', 'AgeTeam1', 'WTeam1', 'LTeam1', 'PWTeam1', 'PLTeam1',
       'MOVTeam1', 'SOSTeam1', 'SRSTeam1', 'ORtgTeam1', 'DRtgTeam1', 'PaceTeam1', 'FTrTeam1', '3PArTeam1', 'TS%Team1',
       'eFG%OffTeam1', 'TOV%OffTeam1', 'ORB%Team1', 'FT/FGAOffTeam1', 'eFG%DefTeam1', 'TOV%DefTeam1', 'DRB%Team1', 'FT/FGADefTeam1',
       'Attend.Team1', 'Rk_xTeam2', 'G_xTeam2', 'MP_xTeam2',
       'FG_xTeam2', 'FGA_xTeam2', 'FG%_xTeam2', '3P_xTeam2', '3PA_xTeam2', '3P%_xTeam2', '2P_xTeam2',
       '2PA_xTeam2', '2P%_xTeam2', 'FT_xTeam2', 'FTA_xTeam2', 'FT%_xTeam2', 'ORB_xTeam2',
       'DRB_xTeam2', 'TRB_xTeam2', 'AST_xTeam2', 'STL_xTeam2', 'BLK_xTeam2', 'TOV_xTeam2',
       'PF_xTeam2', 'PTS_xTeam2', 'year_xTeam2', 'Rk_yTeam2', 'G_yTeam2', 'MP_yTeam2', 'FG_yTeam2',
       'FGA_yTeam2', 'FG%_yTeam2', '3P_yTeam2', '3PA_yTeam2', '3P%_yTeam2', '2P_yTeam2', '2PA_yTeam2',
       '2P%_yTeam2', 'FT_yTeam2', 'FTA_yTeam2', 'FT%_yTeam2', 'ORB_yTeam2', 'DRB_yTeam2',
       'TRB_yTeam2', 'AST_yTeam2', 'STL_yTeam2', 'BLK_yTeam2', 'TOV_yTeam2', 'PF_yTeam2',
       'PTS_yTeam2', 'year_yTeam2', 'RkTeam2', 'AgeTeam2', 'WTeam2', 'LTeam2', 'PWTeam2', 'PLTeam2',
       'MOVTeam2', 'SOSTeam2', 'SRSTeam2', 'ORtgTeam2', 'DRtgTeam2', 'PaceTeam2', 'FTrTeam2', '3PArTeam2',
       'TS%Team2', 'eFG%OffTeam2', 'TOV%OffTeam2', 'ORB%Team2', 'FT/FGAOffTeam2', 'eFG%DefTeam2', 'TOV%DefTeam2',
       'DRB%Team2', 'FT/FGADefTeam2', 'Attend.Team2', 'WS/481']]

#Calculate Similarity Coefficients between Team variables 
regPT['MOVTeam1']=regPT['MOVTeam1']-regPT['MOVTeam1'].min()+1
regPT['SRSTeam1']=regPT['SRSTeam1']-regPT['SRSTeam1'].min()+1
regPT['SOSTeam1']=regPT['SOSTeam1']-regPT['SOSTeam1'].min()+1

regPT['MOVTeam2']=regPT['MOVTeam2']-regPT['MOVTeam2'].min()+1
regPT['SRSTeam2']=regPT['SRSTeam2']-regPT['SRSTeam2'].min()+1
regPT['SOSTeam2']=regPT['SOSTeam2']-regPT['SOSTeam2'].min()+1

regPT2=regPT

regPT2['3PAPlayerDiff']=((regPT2['3PA1']-regPT2['3PA'])/regPT2['3PA']).replace(np.inf, 0).replace(np.nan,0)
regPT2['2PAPlayerDiff']=((regPT2['2PA1']-regPT2['2PA'])/regPT2['2PA']).replace(np.inf, 0).replace(np.nan,0)
regPT2['MPPlayerDiff']=((regPT2['MP1']-regPT2['MP'])/regPT2['MP']).replace(np.inf, 0).replace(np.nan,0)
regPT2['USG%PlayerDiff']=regPT2['USG%1']-regPT2['USG%']


#First attempt: Percentage terms 
teamlist=['Rk_xTeam2','G_xTeam2', 'MP_xTeam2',
       'FG_xTeam2', 'FGA_xTeam2', '3P_xTeam2', '3PA_xTeam2', '2P_xTeam2',
       '2PA_xTeam2', 'FT_xTeam2', 'FTA_xTeam2', 'ORB_xTeam2',
       'DRB_xTeam2', 'TRB_xTeam2', 'AST_xTeam2', 'STL_xTeam2', 'BLK_xTeam2', 'TOV_xTeam2',
       'PF_xTeam2', 'PTS_xTeam2', 'year_xTeam2', 'Rk_yTeam2', 'G_yTeam2', 'MP_yTeam2', 'FG_yTeam2',
       'FGA_yTeam2', '3P_yTeam2', '3PA_yTeam2',  '2P_yTeam2', '2PA_yTeam2',
        'FT_yTeam2', 'FTA_yTeam2', 'ORB_yTeam2', 'DRB_yTeam2',
       'TRB_yTeam2', 'AST_yTeam2', 'STL_yTeam2', 'BLK_yTeam2', 'TOV_yTeam2', 'PF_yTeam2',
       'PTS_yTeam2', 'year_yTeam2', 'RkTeam2', 'AgeTeam2', 'WTeam2', 'LTeam2', 'PWTeam2', 'PLTeam2',
       'MOVTeam2', 'SOSTeam2', 'SRSTeam2', 'ORtgTeam2', 'DRtgTeam2', 'PaceTeam2', 'FTrTeam2', '3PArTeam2',
    'FT/FGAOffTeam2', 'FT/FGADefTeam2', 'Attend.Team2']

for i in teamlist:
    colname=i+'Diff'
    
    team1statname= i[:-1]+'1'
    regPT2[colname]=(regPT2[i]-regPT2[team1statname])/regPT2[team1statname]
    
    
percentteamlist= ['FG%_xTeam2','3P%_xTeam2', '2P%_xTeam2','FT%_xTeam2', 'FG%_yTeam2','3P%_yTeam2', 
                  'FT%_yTeam2', '2P%_yTeam2', 'TS%Team2', 'eFG%OffTeam2', 'TOV%OffTeam2', 'ORB%Team2',
                  'eFG%DefTeam2', 'TOV%DefTeam2','DRB%Team2']

for i in percentteamlist:
    colname=i+'Diff'
    
    team1statname= i[:-1]+'1'
    regPT2[colname]=regPT2[i]-regPT2[team1statname]
                     
regPT2=regPT2.round(4)

regPT2=regPT2.drop(['2PA','2PA1','3PA', '3PA1', 'MP', 'MP1', 'USG%1','USG%','Rk_xTeam1', 'G_xTeam1', 'MP_xTeam1', 'FG_xTeam1',
       'FGA_xTeam1', 'FG%_xTeam1', '3P_xTeam1', '3PA_xTeam1', '3P%_xTeam1', '2P_xTeam1', '2PA_xTeam1',
       '2P%_xTeam1', 'FT_xTeam1', 'FTA_xTeam1', 'FT%_xTeam1', 'ORB_xTeam1', 'DRB_xTeam1', 'TRB_xTeam1',
       'AST_xTeam1', 'STL_xTeam1', 'BLK_xTeam1', 'TOV_xTeam1', 'PF_xTeam1', 'PTS_xTeam1', 'year_xTeam1',
       'Rk_yTeam1', 'G_yTeam1', 'MP_yTeam1', 'FG_yTeam1', 'FGA_yTeam1', 'FG%_yTeam1', '3P_yTeam1', '3PA_yTeam1',
       '3P%_yTeam1', '2P_yTeam1', '2PA_yTeam1', '2P%_yTeam1', 'FT_yTeam1', 'FTA_yTeam1', 'FT%_yTeam1',
       'ORB_yTeam1', 'DRB_yTeam1', 'TRB_yTeam1', 'AST_yTeam1', 'STL_yTeam1', 'BLK_yTeam1', 'TOV_yTeam1',
       'PF_yTeam1', 'PTS_yTeam1', 'year_yTeam1', 'RkTeam1', 'AgeTeam1', 'WTeam1', 'LTeam1', 'PWTeam1', 'PLTeam1',
       'MOVTeam1', 'SOSTeam1', 'SRSTeam1', 'ORtgTeam1', 'DRtgTeam1', 'PaceTeam1', 'FTrTeam1', '3PArTeam1', 'TS%Team1',
       'eFG%OffTeam1', 'TOV%OffTeam1', 'ORB%Team1', 'FT/FGAOffTeam1', 'eFG%DefTeam1', 'TOV%DefTeam1', 'DRB%Team1', 'FT/FGADefTeam1',
       'Attend.Team1','Rk_xTeam2','G_xTeam2', 'MP_xTeam2',
       'FG_xTeam2', 'FGA_xTeam2', 'FG%_xTeam2', '3P_xTeam2', '3PA_xTeam2', '3P%_xTeam2', '2P_xTeam2',
       '2PA_xTeam2', '2P%_xTeam2', 'FT_xTeam2', 'FTA_xTeam2', 'FT%_xTeam2', 'ORB_xTeam2',
       'DRB_xTeam2', 'TRB_xTeam2', 'AST_xTeam2', 'STL_xTeam2', 'BLK_xTeam2', 'TOV_xTeam2',
       'PF_xTeam2', 'PTS_xTeam2', 'year_xTeam2', 'Rk_yTeam2', 'G_yTeam2', 'MP_yTeam2', 'FG_yTeam2',
       'FGA_yTeam2', 'FG%_yTeam2', '3P_yTeam2', '3PA_yTeam2', '3P%_yTeam2', '2P_yTeam2', '2PA_yTeam2',
       '2P%_yTeam2', 'FT_yTeam2', 'FTA_yTeam2', 'FT%_yTeam2', 'ORB_yTeam2', 'DRB_yTeam2',
       'TRB_yTeam2', 'AST_yTeam2', 'STL_yTeam2', 'BLK_yTeam2', 'TOV_yTeam2', 'PF_yTeam2',
       'PTS_yTeam2', 'year_yTeam2', 'RkTeam2', 'AgeTeam2', 'WTeam2', 'LTeam2', 'PWTeam2', 'PLTeam2',
       'MOVTeam2', 'SOSTeam2', 'SRSTeam2', 'ORtgTeam2', 'DRtgTeam2', 'PaceTeam2', 'FTrTeam2', '3PArTeam2',
       'TS%Team2', 'eFG%OffTeam2', 'TOV%OffTeam2', 'ORB%Team2', 'FT/FGAOffTeam2', 'eFG%DefTeam2', 'TOV%DefTeam2',
       'DRB%Team2', 'FT/FGADefTeam2', 'Attend.Team2'], axis=1)

#Drop extraneous variables

regPT2=regPT2.drop(['WS','3P', '2P', 'FT','TRB','FG_xTeam2Diff','3P_xTeam2Diff','2P_xTeam2Diff', 'FT_xTeam2Diff', 'TRB_xTeam2Diff','year_xTeam2Diff', 'FG_yTeam2Diff','3P_yTeam2Diff', '2P_yTeam2Diff', 'FT_yTeam2Diff', 'TRB_yTeam2Diff', 'year_yTeam2Diff', 'AgeTeam2Diff', 'LTeam2Diff','Rk_xTeam2Diff','Rk_yTeam2Diff','RkTeam2Diff' ], axis=1)

#Put WS481 target as last

regPT2 = regPT2[['Player', 'yearTeam1', 'Team1', 'yearTeam2', 'Team2', 'Pos', 'Age',
       'G', 'GS', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%',
       'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'OWS', 'DWS',
       'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP', 'FG', 'FGA', 'FG%',
       '3P%', '2P%', 'eFG%', 'FTA', 'FT%', 'ORB', 'DRB', 'AST',
       'STL', 'BLK', 'TOV', 'PF', 'PTS', '3PAPlayerDiff', '2PAPlayerDiff' ,'MPPlayerDiff' , 'USG%PlayerDiff',
       'G_xTeam2Diff', 'MP_xTeam2Diff', 'FGA_xTeam2Diff',
       'FG%_xTeam2Diff', '3PA_xTeam2Diff', '3P%_xTeam2Diff',
       '2PA_xTeam2Diff', '2P%_xTeam2Diff', 'FTA_xTeam2Diff',
       'FT%_xTeam2Diff', 'ORB_xTeam2Diff', 'DRB_xTeam2Diff',
       'AST_xTeam2Diff', 'STL_xTeam2Diff', 'BLK_xTeam2Diff',
       'TOV_xTeam2Diff', 'PF_xTeam2Diff', 'PTS_xTeam2Diff',
       'G_yTeam2Diff', 'MP_yTeam2Diff', 'FGA_yTeam2Diff',
       'FG%_yTeam2Diff', '3PA_yTeam2Diff', '3P%_yTeam2Diff',
       '2PA_yTeam2Diff', '2P%_yTeam2Diff', 'FTA_yTeam2Diff',
       'FT%_yTeam2Diff', 'ORB_yTeam2Diff', 'DRB_yTeam2Diff',
       'AST_yTeam2Diff', 'STL_yTeam2Diff', 'BLK_yTeam2Diff',
       'TOV_yTeam2Diff', 'PF_yTeam2Diff', 'PTS_yTeam2Diff', 'WTeam2Diff',
       'PWTeam2Diff', 'PLTeam2Diff', 'MOVTeam2Diff', 'SOSTeam2Diff',
       'SRSTeam2Diff', 'ORtgTeam2Diff', 'DRtgTeam2Diff', 'PaceTeam2Diff',
       'FTrTeam2Diff', '3PArTeam2Diff', 'TS%Team2Diff',
       'eFG%OffTeam2Diff', 'TOV%OffTeam2Diff', 'ORB%Team2Diff',
       'FT/FGAOffTeam2Diff', 'eFG%DefTeam2Diff', 'TOV%DefTeam2Diff',
       'DRB%Team2Diff', 'FT/FGADefTeam2Diff', 'Attend.Team2Diff', 'WS/481']]

regPT=regPT2

#****************************************************************************************************************************************
#SGD Regressor comparison; We compare proposed algo to SGD Regressor

X=regPT.loc[:, 'Age':'Attend.Team2Diff']
y=regPT['WS/481']

    #Normalize values

mean=X.mean(axis=0)
X-=mean
std=X.std(axis=0)
X/= std

#Given training case example;

train_data = X[4000:5000]
train_ws=y[4000:5000]
test_data=X[5000:5400]
test_ws=y[5000:5400]

robust = SGDRegressor(loss='huber',
                      penalty='l2', 
                      alpha=0.01, 
                      fit_intercept=False, 
                      n_iter=10, 
                      shuffle=False, 
                      verbose=1, 
                      epsilon=0.01, 
                      random_state=42, 
                      learning_rate='invscaling', 
                      eta0=0.1, 
                      power_t=0.5)

robust.fit(train_data, train_ws)

mean_absolute_error(test_ws, robust.predict(test_data))

def data():
    
    regPT = pd.read_csv('regPT.csv')
    X=regPT.loc[:, 'Age':'Attend.Team2Diff']
    y=regPT['WS/481']

    #Normalize values

    mean=X.mean(axis=0)
    X-=mean
    std=X.std(axis=0)
    X/= std

    train_data = X[0:4800]
    train_ws=y[0:4800]
    test_data=X[4800:5300]
    test_ws=y[4800:5300]
    
    return train_data, train_ws, test_data, test_ws

#****Adaptive version runs new create_model function on each training set input

def create_model(train_data, train_ws, test_data, test_ws):
   
    model = Sequential()
    model.add(Dense({{choice([16,32, 64])}}, activation='relu', input_shape=(train_data.shape[1],)))
    model.add(Dropout({{uniform(0, 1)}}))
    model.add(Dense({{choice([16,32,64,256])}}))
    model.add(Dropout({{uniform(0, 1)}}))
    
    if {{choice(['two', 'three'])}} == 'three':
        model.add(Dense({{choice([16,32,64,256, 512])}}))
    
    
    if {{choice(['two', 'three', 'four'])}} == 'four':
        model.add(Dense({{choice([16,32,64,256])}}))
        model.add(Dropout({{uniform(0, 1)}}))
        model.add(Dense({{choice([16,32,64,256])}}))
    
    if {{choice(['two', 'three', 'four', 'five'])}} == 'five':
        model.add(Dense({{choice([16,32,64,256])}}))
        model.add(Dropout({{uniform(0, 1)}}))
        model.add(Dense({{choice([16,32,64,256])}}))
        model.add(Dropout({{uniform(0, 1)}}))
        model.add(Dense({{choice([16,32,64,256])}}))
    
    model.add(Dropout({{uniform(0, 1)}}))
    model.add(Dense(1))
    

    model.compile(loss='mae',optimizer=optimizers.SGD(lr={{choice([0.001,0.0001])}}, momentum={{choice([0.6,0.7])}}))
    
    result = model.fit(train_data, train_ws, 
                       validation_data=(test_data,test_ws),
                      batch_size=1,
                      epochs=15,
                      verbose=2)
                  
    validation_loss = np.amin(result.history['val_loss']) 
                  
    print('Best validation acc of epoch:', validation_loss)
                  
    return {'loss': validation_loss, 'status': STATUS_OK, 'model': model}


with tf.device("/gpu:0"):
    best_run, best_model = optim.minimize(model=create_model,
                                          data=data,
                                          algo=tpe.suggest,
                                          max_evals=5,
                                          trials=Trials(),
                                          notebook_name='simple_notebook2')
train_data, train_ws, test_data, test_ws = data()
print("Evalutation of best performing model:")
print(best_model.evaluate(test_data, test_ws))
print("Best performing model chosen hyper-parameters:")
print(best_run)
