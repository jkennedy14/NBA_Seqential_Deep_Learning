import pandas as pd
df = pd.read_csv('Seasons_Stats.csv')

df2= df.sort_values(by=['Player', 'Year'])
df2=df2.dropna(subset=['Player'])
df2 = df2[df.Tm != "TOT"]

playerMoveDS = pd.DataFrame(columns=['Unnamed: 0', 'Year', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS',
       'MP', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%',
       'STL%', 'BLK%', 'TOV%', 'USG%', 'blanl', 'OWS', 'DWS', 'WS',
       'WS/48', 'blank2', 'OBPM', 'DBPM', 'BPM', 'VORP', 'FG', 'FGA',
       'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA',
       'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
       'PTS', 'Unnamed: 01', 'Year1', 'Player1', 'Pos1', 'Age1', 'Tm1', 'G1', 'GS1',
       'MP1', 'PER1', 'TS%1', '3PAr1', 'FTr1', 'ORB%1', 'DRB%1', 'TRB%1', 'AST%1',
       'STL%1', 'BLK%1', 'TOV%1', 'USG%1', 'blanl1', 'OWS1', 'DWS1', 'WS1',
       'WS/481', 'blank21', 'OBPM1', 'DBPM1', 'BPM1', 'VORP1', 'FG1', 'FGA1',
       'FG%1', '3P1', '3PA1', '3P%1', '2P1', '2PA1', '2P%1', 'eFG%1', 'FT1', 'FTA1',
       'FT%1', 'ORB1', 'DRB1', 'TRB1', 'AST1', 'STL1', 'BLK1', 'TOV1', 'PF1',
       'PTS1'])

npdf2=df2.values
import numpy as np

#Detect instances of players switching teams

j=0
for i in range(npdf2.shape[0]):
    newline=[]
    if npdf2[i][2]==npdf2[i-1][2]:
        if npdf2[i][5]!=npdf2[i-1][5]:
            a=np.append(npdf2[i-1],npdf2[i])
            playerMoveDS.loc[j]=a
            j+=1
            

colstostd=['OBPM', 'DBPM', 'BPM','FG', 'FGA',
       '3P', '3PA', '2P', '2PA', 'FT', 'FTA',
       'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
       'PTS', 'MP1','OBPM1', 'DBPM1', 'BPM1','FG1', 'FGA1',
       '3P1', '3PA1', '2P1', '2PA1', 'FT1', 'FTA1',
       'ORB1', 'DRB1', 'TRB1', 'AST1', 'STL1', 'BLK1', 'TOV1', 'PF1',
       'PTS1', 'DWS', 'OWS']

#Put stats on per minute basis (except for percentage stats)

for i in colstostd:
    playerMoveDS[i]=playerMoveDS[i]/playerMoveDS['MP']


playerMoveDS['MP']=playerMoveDS['MP']/playerMoveDS['G']

playerMoveDS=playerMoveDS.round(4)


playerMoveDS=playerMoveDS.drop(['blanl','blanl1', 'blank2', 'blank21','Unnamed: 01', 'Unnamed: 0'], axis=1)

playerMoveDS["Year"] = playerMoveDS["Year"].astype(int)
playerMoveDS["Year1"] = playerMoveDS["Year1"].astype(int)

playerMoveDS = playerMoveDS.rename(columns={'Tm': 'Team'})

playerMoveDS['Team']=playerMoveDS['Team'].replace({'GSW': 'Golden State Warriors'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'LAL': 'Los Angeles Lakers'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'PHO': 'Phoenix Suns'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'DAL': 'Dallas Mavericks'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'CHI': 'Chicago Bulls'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'IND': 'Indiana Pacers'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'WAS': 'Washington Wizards'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'MIN': 'Minnesota Timberwolves'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'CLE': 'Cleveland Cavaliers'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'HOU': 'Houston Rockets'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'SAC': 'Sacramento Kings'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'DEN': 'Denver Nuggets'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'NOH': 'New Orleans Hornets'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'TOR': 'Toronto Raptors'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'POR': 'Portland Trail Blazers'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'DET': 'Detroit Pistons'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'PHI': 'Philadelphia 76ers'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'UTA': 'Utah Jazz'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'MIL': 'Milwaukee Bucks'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'VAN': 'Vancouver Grizzlies'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'SEA': 'Seattle SuperSonics'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'NJN': 'New Jersey Nets'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'NOK': 'New Orleans Hornets'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'BOS': 'Boston Celtics'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'ATL': 'Atlanta Hawks'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'CHA': 'Charlotte Hornets'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'MEM': 'Memphis Grizzlies'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'ORL': 'Orlando Magic'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'NYK': 'New York Knicks'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'CHO': 'Charlotte Bobcats'}, regex=True)#
playerMoveDS['Team']=playerMoveDS['Team'].replace({'LAC': 'Los Angeles Clippers'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'SDC': 'San Diego Clippers'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'NOP': 'New Orleans Pelicans'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'BRK': 'Brooklyn Nets'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'MIA': 'Miami Heat'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'SAS': 'San Antonio Spurs'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'CHH': 'Charlotte Hornets'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'WSB': 'Washington Bullets'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'OKC': 'Oklahoma City Thunder'}, regex=True)
playerMoveDS['Team']=playerMoveDS['Team'].replace({'KCK': 'Kansas City Kings'}, regex=True)

playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'GSW': 'Golden State Warriors'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'LAL': 'Los Angeles Lakers'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'PHO': 'Phoenix Suns'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'DAL': 'Dallas Mavericks'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'CHI': 'Chicago Bulls'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'IND': 'Indiana Pacers'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'WAS': 'Washington Wizards'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'MIN': 'Minnesota Timberwolves'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'CLE': 'Cleveland Cavaliers'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'HOU': 'Houston Rockets'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'SAC': 'Sacramento Kings'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'DEN': 'Denver Nuggets'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'NOH': 'New Orleans Hornets'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'TOR': 'Toronto Raptors'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'POR': 'Portland Trail Blazers'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'DET': 'Detroit Pistons'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'PHI': 'Philadelphia 76ers'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'UTA': 'Utah Jazz'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'MIL': 'Milwaukee Bucks'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'VAN': 'Vancouver Grizzlies'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'SEA': 'Seattle SuperSonics'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'NJN': 'New Jersey Nets'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'NOK': 'New Orleans Hornets'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'BOS': 'Boston Celtics'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'ATL': 'Atlanta Hawks'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'CHA': 'Charlotte Hornets'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'MEM': 'Memphis Grizzlies'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'ORL': 'Orlando Magic'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'NYK': 'New York Knicks'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'CHO': 'Charlotte Bobcats'}, regex=True)#
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'LAC': 'Los Angeles Clippers'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'SDC': 'San Diego Clippers'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'NOP': 'New Orleans Pelicans'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'BRK': 'Brooklyn Nets'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'MIA': 'Miami Heat'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'SAS': 'San Antonio Spurs'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'CHH': 'Charlotte Hornets'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'WSB': 'Washington Bullets'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'OKC': 'Oklahoma City Thunder'}, regex=True)
playerMoveDS['Tm1']=playerMoveDS['Tm1'].replace({'KCK': 'Kansas City Kings'}, regex=True)

#Read in NBA season TEAM stats datasets (seperate from individual stats datasets) 
#Each dataset is composed of 3 seperate datasets per season: Team Statistics, Team Opponent Statistics, Miscellaneous Statistics    

nba1980=pd.read_excel('nba1980.xlsx', header=None)
nba1981=pd.read_excel('nba1981.xlsx', header=None)
nba1982=pd.read_excel('nba1982.xlsx', header=None)
nba1983=pd.read_excel('nba1983.xlsx', header=None)
nba1984=pd.read_excel('nba1984.xlsx', header=None)
nba1985=pd.read_excel('nba1985.xlsx', header=None)
nba1986=pd.read_excel('nba1986.xlsx', header=None)
nba1987=pd.read_excel('nba1987.xlsx', header=None)
nba1988=pd.read_excel('nba1988.xlsx', header=None)
nba1989=pd.read_excel('nba1989.xlsx', header=None)

nba1990=pd.read_excel('nba1990.xlsx', header=None)
nba1991=pd.read_excel('nba1991.xlsx', header=None)
nba1992=pd.read_excel('nba1992.xlsx', header=None)
nba1993=pd.read_excel('nba1993.xlsx', header=None)
nba1994=pd.read_excel('nba1994.xlsx', header=None)
nba1995=pd.read_excel('nba1995.xlsx', header=None)
nba1996=pd.read_excel('nba1996.xlsx', header=None)
nba1997=pd.read_excel('nba1997.xlsx', header=None)
nba1998=pd.read_excel('nba1998.xlsx', header=None)
nba1999=pd.read_excel('nba1999.xlsx', header=None)

nba2000=pd.read_excel('nba2000.xlsx', header=None)
nba2001=pd.read_excel('nba2001.xlsx', header=None)
nba2002=pd.read_excel('nba2002.xlsx', header=None)
nba2003=pd.read_excel('nba2003.xlsx', header=None)
nba2004=pd.read_excel('nba2004.xlsx', header=None)
nba2005=pd.read_excel('nba2005.xlsx', header=None)
nba2006=pd.read_excel('nba2006.xlsx', header=None)
nba2007=pd.read_excel('nba2007.xlsx', header=None)
nba2008=pd.read_excel('nba2008.xlsx', header=None)
nba2009=pd.read_excel('nba2009.xlsx', header=None)

nba2010=pd.read_excel('nba2010.xlsx', header=None)
nba2011=pd.read_excel('nba2011.xlsx', header=None)
nba2012=pd.read_excel('nba2012.xlsx', header=None)
nba2013=pd.read_excel('nba2013.xlsx', header=None)
nba2014=pd.read_excel('nba2014.xlsx', header=None)
nba2015=pd.read_excel('nba2015.xlsx', header=None)
nba2016=pd.read_excel('nba2016.xlsx', header=None)
nba2017=pd.read_excel('nba2017.xlsx', header=None)
nba2018=pd.read_excel('nba2018.xlsx', header=None)

nba1982=nba1982.drop([27], axis=1)

#Separating inputted data team, opponent, misc datasets

nba1980team=nba1980[:24]
nba1980opp=nba1980[25:49]
nba1980misc=nba1980[50:]

nba1981team=nba1981[:25]
nba1981opp=nba1981[26:51]
nba1981misc=nba1981[52:]

nba1982team=nba1982[:25]
nba1982opp=nba1982[26:51]
nba1982misc=nba1982[52:]

nba1983team=nba1983[:25]
nba1983opp=nba1983[26:51]
nba1983misc=nba1983[52:]

nba1984team=nba1984[:25]
nba1984opp=nba1984[26:51]
nba1984misc=nba1984[52:]

nba1985team=nba1985[:25]
nba1985opp=nba1985[26:51]
nba1985misc=nba1985[52:]

nba1986team=nba1986[:25]
nba1986opp=nba1986[26:51]
nba1986misc=nba1986[52:]

nba1987team=nba1987[:25]
nba1987opp=nba1987[26:51]
nba1987misc=nba1987[52:]

nba1988team=nba1988[:25]
nba1988opp=nba1988[26:51]
nba1988misc=nba1988[52:]

nba1989team=nba1989[:27]
nba1989opp=nba1989[28:55]
nba1989misc=nba1989[56:]

nba1990team=nba1990[:29]
nba1990opp=nba1990[30:59]
nba1990misc=nba1990[60:]

nba1991team=nba1991[:29]
nba1991opp=nba1991[30:59]
nba1991misc=nba1991[60:]

nba1992team=nba1992[:29]
nba1992opp=nba1992[30:59]
nba1992misc=nba1992[60:]

nba1993team=nba1993[:29]
nba1993opp=nba1993[30:59]
nba1993misc=nba1993[60:]

nba1994team=nba1994[:29]
nba1994opp=nba1994[30:59]
nba1994misc=nba1994[60:]

nba1995team=nba1995[:29]
nba1995opp=nba1995[30:59]
nba1995misc=nba1995[60:]

nba1996team=nba1996[:31]
nba1996opp=nba1996[32:63]
nba1996misc=nba1996[64:]

nba1997team=nba1997[:31]
nba1997opp=nba1997[32:63]
nba1997misc=nba1997[64:]

nba1998team=nba1998[:31]
nba1998opp=nba1998[32:63]
nba1998misc=nba1998[64:]

nba1999team=nba1999[:31]
nba1999opp=nba1999[32:63]
nba1999misc=nba1999[64:]

nba2000team=nba2000[:31]
nba2000opp=nba2000[32:63]
nba2000misc=nba2000[64:]

nba2001team=nba2001[:31]
nba2001opp=nba2001[32:63]
nba2001misc=nba2001[64:]

nba2002team=nba2002[:31]
nba2002opp=nba2002[32:63]
nba2002misc=nba2002[64:]

nba2003team=nba2003[:31]
nba2003opp=nba2003[32:63]
nba2003misc=nba2003[64:]

nba2004team=nba2004[:31]
nba2004opp=nba2004[32:63]
nba2004misc=nba2004[64:]

nba2005team=nba2005[:32]
nba2005opp=nba2005[33:65]
nba2005misc=nba2005[66:]

nba2006team=nba2006[:32]
nba2006opp=nba2006[33:65]
nba2006misc=nba2006[66:]

nba2007team=nba2007[:32]
nba2007opp=nba2007[33:65]
nba2007misc=nba2007[66:]

nba2008team=nba2008[:32]
nba2008opp=nba2008[33:65]
nba2008misc=nba2008[66:]

nba2009team=nba2009[:32]
nba2009opp=nba2009[33:65]
nba2009misc=nba2009[66:]

nba2010team=nba2010[:32]
nba2010opp=nba2010[33:65]
nba2010misc=nba2010[66:]

nba2011team=nba2011[:32]
nba2011opp=nba2011[33:65]
nba2011misc=nba2011[66:]

nba2012team=nba2012[:32]
nba2012opp=nba2012[33:65]
nba2012misc=nba2012[66:]

nba2013team=nba2013[:32]
nba2013opp=nba2013[33:65]
nba2013misc=nba2013[66:]

nba2014team=nba2014[:32]
nba2014opp=nba2014[33:65]
nba2014misc=nba2014[66:]

nba2015team=nba2015[:32]
nba2015opp=nba2015[33:65]
nba2015misc=nba2015[66:]

nba2016team=nba2016[:32]
nba2016opp=nba2016[33:65]
nba2016misc=nba2016[66:]

nba2017team=nba2017[:32]
nba2017opp=nba2017[33:65]
nba2017misc=nba2017[66:]

nba2018team=nba2018[:32]
nba2018opp=nba2018[33:65]
nba2018misc=nba2018[66:]

nba2018misc=nba2018misc[1:]

#Cleaning headers of data

for i in range(39):
    string=str(1980+i)
    team=eval("nba"+string+"team")
    opp=eval("nba"+string+"opp")
    misc=eval("nba"+string+"misc")
    
    team.columns = team.iloc[0]
    opp.columns = opp.iloc[0]
    misc.columns = misc.iloc[0]
       
    team=team[1:]
    opp=opp[1:]
    misc=misc[1:]   

#Add year column to all datasets, eliminate unecessary columns

teams=[]
opps=[]
miscs=[]
for i in range(39):
    string=str(1980+i)
    team=eval('nba'+string+'team')
    opp=eval('nba'+string+'opp')
    misc=eval('nba'+string+'misc')
    
    team=team.drop(['z'], axis=1)
    opp=opp.drop(['z'], axis=1)
    misc=misc.drop(['Arena'], axis=1)
    
    team['year']=1980+i
    opp['year']=1980+i
    misc['year']=1980+i
    
    teams.append(team)
    opps.append(opp)
    miscs.append(misc)

#Merge team,opp, misc stats by year
       
teamstatsbyyear=[]
for i in range(39):
    a=teams[i].merge(opps[i], on="Team")
    b=a.merge(miscs[i], on="Team")
    
    teamstatsbyyear.append(b)
    
#take out * from team and convert team to 3 letter abrev
#change some col names

for i in teamstatsbyyear:
    i['Team'] = i['Team'].map(lambda x: x.rstrip('*'))
    i['Team1']=i['Team']
    i.columns.values[66]="eFG%Off"
    i.columns.values[70]="eFG%Def"
    
    i.columns.values[69]="FT/FGAOff"
    i.columns.values[73]="FT/FGADef"
    
    i.columns.values[67]="TOV%Off"
    i.columns.values[71]="TOV%Def"
    
    

teamstatsbyyear[0].columns.values[74] = "Attend."
teamstatsbyyear[0].columns.values[75] = "Attend./G"

teamstatsbyyear[0]["Attend."]=0
teamstatsbyyear[0]["Attend./G"]=0

for i in range(len(teamstatsbyyear[0]['Team'].values)):
    team1981attend= teamstatsbyyear[1].loc[teamstatsbyyear[1]['Team']==teamstatsbyyear[0]['Team'].values[i]]['Attend.']
    teamstatsbyyear[0].at[i,'Attend.']=team1981attend


teamstatsbyyear[37].columns.values[9]="3P%_x"
teamstatsbyyear[37].columns.values[12]="2P%_x"
teamstatsbyyear[37].columns.values[34]="3P%_y"
teamstatsbyyear[37].columns.values[37]="2P%_y"

#Merge Individ Stats DF and Team DF
#turn teamsbyyear into dict
teamsdict={}

for i in range(0,39): 
    stri=str(i+1980) 
    teamsdict[stri]=teamstatsbyyear[i]

c=teamsdict 
    
for i in range(1980,2019): 
    j=str(i) 
    c[j].set_index("Team", inplace=True)
        
a=playerMoveDS.values 

teamsadj = pd.DataFrame(columns=
    ['Rk_x', 'G_x', 'MP_x', 'FG_x', 'FGA_x', 'FG%_x', '3P_x', '3PA_x', '3P%_x', '2P_x', 
     '2PA_x', '2P%_x', 'FT_x', 'FTA_x', 'FT%_x', 'ORB_x', 'DRB_x', 'TRB_x', 'AST_x', 
     'STL_x', 'BLK_x', 'TOV_x', 'PF_x', 'PTS_x', 'year_x', 'Rk_y', 'G_y', 'MP_y', 'FG_y', 
     'FGA_y', 'FG%_y', '3P_y', '3PA_y', '3P%_y', '2P_y', '2PA_y', '2P%_y', 'FT_y', 'FTA_y', 
     'FT%_y', 'ORB_y', 'DRB_y', 'TRB_y', 'AST_y', 'STL_y', 'BLK_y', 'TOV_y', 'PF_y', 'PTS_y', 
     'year_y', 'Rk', 'Age', 'W', 'L', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'Pace', 
     'FTr', '3PAr', 'TS%', 'eFG%Off', 'TOV%Off', 'ORB%', 'FT/FGAOff', 'eFG%Def', 'TOV%Def', 'DRB%', 'FT/FGADef', 
     'Attend.', 'Attend./G', 'year', 'Team1', 'Rk_x2', 'G_x2', 'MP_x2', 'FG_x2', 'FGA_x2', 
     'FG%_x2', '3P_x2', '3PA_x2', '3P%_x2', '2P_x2', '2PA_x2', '2P%_x2', 'FT_x2', 'FTA_x2', 
     'FT%_x2', 'ORB_x2', 'DRB_x2', 'TRB_x2', 'AST_x2', 'STL_x2', 'BLK_x2', 'TOV_x2', 'PF_x2', 
     'PTS_x2', 'year_x2', 'Rk_y2', 'G_y2', 'MP_y2', 'FG_y2', 'FGA_y2', 'FG%_y2', '3P_y2', '3PA_y2', 
     '3P%_y2', '2P_y2', '2PA_y2', '2P%_y2', 'FT_y2', 'FTA_y2', 'FT%_y2', 'ORB_y2', 'DRB_y2', 'TRB_y2', 
     'AST_y2', 'STL_y2', 'BLK_y2', 'TOV_y2', 'PF_y2', 'PTS_y2', 'year_y2', 'Rk2', 'Age2', 'W2', 'L2', 
     'PW2', 'PL2', 'MOV2', 'SOS2', 'SRS2', 'ORtg2', 'DRtg2', 'Pace2', 'FTr2', '3PAr2', 'TS%2', 'eFG%Off2', 
     'TOV%Off2', 'ORB%2', 'FT/FGAOff2', 'eFG%Def2', 'TOV%Def2', 'DRB%2', 'FT/FGADef2', 'Attend.2', 'Attend./G2', 'year2', 'Team12' ])

#Make datasets consistent in terms of team names

for i in range(len(a)): 
    team=a[i][4] 
    team1=a[i][54]
    
    year=a[i][0]
    year2=a[i][50]
    stryear=str(year)
    stryear2=str(year2)
    
    #print(year, team, team1)
    if year==2005 or year==2006 or year==2007:
        if team=="New Orleans Hornets":
            team="Charlotte Bobcats"
    
    if year2==2005 or year2==2006 or year2==2007:
        if team1=="New Orleans Hornets":
            team1="Charlotte Bobcats"   

    hornetsyears=[2005,2006,2007,2008,2009,2010,2011,2012,2013,2014]
    bobcatsyears=[2015,2016,2017]

    if year in hornetsyears:
        if team=="Charlotte Hornets":
            team="Charlotte Bobcats"

    if year2 in hornetsyears:
        if team1=="Charlotte Hornets":
            team1="Charlotte Bobcats"

    if year in bobcatsyears:
        if team=="Charlotte Bobcats":
            team="Charlotte Hornets"
    
    if year2 in bobcatsyears:
        if team1=="Charlotte Bobcats":
            team1="Charlotte Hornets"

    row1=c[stryear].loc[[team]]
    row2=c[stryear2].loc[[team1]]
    
    row2.columns=['Rk_x2', 'G_x2', 'MP_x2', 'FG_x2', 'FGA_x2', 
     'FG%_x2', '3P_x2', '3PA_x2', '3P%_x2', '2P_x2', '2PA_x2', '2P%_x2', 'FT_x2', 'FTA_x2', 
     'FT%_x2', 'ORB_x2', 'DRB_x2', 'TRB_x2', 'AST_x2', 'STL_x2', 'BLK_x2', 'TOV_x2', 'PF_x2', 
     'PTS_x2', 'year_x2', 'Rk_y2', 'G_y2', 'MP_y2', 'FG_y2', 'FGA_y2', 'FG%_y2', '3P_y2', '3PA_y2', 
     '3P%_y2', '2P_y2', '2PA_y2', '2P%_y2', 'FT_y2', 'FTA_y2', 'FT%_y2', 'ORB_y2', 'DRB_y2', 'TRB_y2', 
     'AST_y2', 'STL_y2', 'BLK_y2', 'TOV_y2', 'PF_y2', 'PTS_y2', 'year_y2', 'Rk2', 'Age2', 'W2', 'L2', 
     'PW2', 'PL2', 'MOV2', 'SOS2', 'SRS2', 'ORtg2', 'DRtg2', 'Pace2', 'FTr2', '3PAr2', 'TS%2', 'eFG%Off2', 
     'TOV%Off2', 'ORB%2', 'FT/FGAOff2', 'eFG%Def2', 'TOV%Def2', 'DRB%2', 'FT/FGADef2', 'Attend.2', 'Attend./G2', 'year2', 'Team12']

    rows=pd.concat([row1.reset_index(drop=True), row2.reset_index(drop=True)], axis=1)

        #print(row)
    teamsadj=teamsadj.append(rows.iloc[0],ignore_index=True)
    
PlayerTeamDF = pd.concat([playerMoveDS.reset_index(drop=True), teamsadj], axis=1)

#Interesting Variables: G1, GS1, MP1, USG%1,3PA1, 2PA1,FTA1
regPT = PlayerTeamDF
len(regPT.columns.values)


regPT=regPT.drop(['Team', 'Year', 'Year1', 'Player1',
       'Pos1', 'Age1', 'Tm1', 'G1', 'GS1', 'PER1', 'TS%1', '3PAr1',
       'FTr1', 'ORB%1', 'DRB%1', 'TRB%1', 'AST%1', 'STL%1', 'BLK%1',
       'TOV%1', 'OWS1', 'DWS1', 'WS1', 'OBPM1',
       'DBPM1', 'BPM1', 'VORP1', 'FG1', 'FGA1', 'FG%1', '3P1',
       '3P%1', '2P1', '2P%1', 'eFG%1', 'FT1', 'FTA1', 'FT%1',
       'ORB1', 'DRB1', 'TRB1', 'AST1', 'STL1', 'BLK1', 'TOV1', 'PF1',
       'PTS1'], axis=1)
    
    
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

#SGD Regressor comparison; We compare proposed algo to SGD Regressor

from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler

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

import numpy as np
import keras

from hyperopt import Trials, STATUS_OK, tpe
from keras.datasets import mnist
from keras.layers.core import Dense, Dropout, Activation
from keras.models import Sequential
from keras.utils import np_utils
#import keras

from hyperas import optim
from hyperas.distributions import choice, uniform
from keras import optimizers
import pandas as pd
import tensorflow as tf


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
