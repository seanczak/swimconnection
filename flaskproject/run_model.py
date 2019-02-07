import pandas as pd
import numpy as np
import os
import sys

import pandas as pd, numpy as np, sqlite3, pickle
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from IPython.display import display
from sklearn import metrics
from sklearn.externals import joblib
import os
from bs4 import BeautifulSoup

# model
filename='m_best'
m = joblib.load(filename)

# teams for scoring later
filename='team_arrays'
teams=pd.read_pickle(filename)

# team info pages
filename='team_info'
team_info=pd.read_pickle(filename)


###################################
#################################
swimmer_events=['_50_FR_p',  '_100_FR_p',  '_200_FR_p',  '_500_FR_p',
 '_1000_FR_p', '_1650_FR_p', '_100_BK_p', '_200_BK_p',
 '_100_BR_p', '_200_BR_p', '_100_FL_p', '_200_FL_p',
 '_200_IM_p', '_400_IM_p']
team_events=['_50_FR_0', '_50_FR_1', '_50_FR_2',
 '_50_FR_3', '_50_FR_4', '_50_FR_5',
 '_100_FR_0', '_100_FR_1', '_100_FR_2',
 '_100_FR_3', '_100_FR_4', '_100_FR_5',
 '_200_FR_0', '_200_FR_1', '_500_FR_0',
 '_500_FR_1', '_1000_FR_0', '_1000_FR_1',
 '_1650_FR_0', '_1650_FR_1', '_100_BK_0',
 '_100_BK_1', '_200_BK_0', '_200_BK_1',
 '_100_BR_0', '_100_BR_1', '_200_BR_0',
 '_200_BR_1', '_100_FL_0', '_100_FL_1',
 '_200_FL_0', '_200_FL_1', '_200_IM_0',
 '_200_IM_1', '_400_IM_0', '_400_IM_1']
events=['_50_FR', '_100_FR', '_200_FR', '_500_FR', '_1000_FR', '_1650_FR',
   '_100_BK', '_200_BK', '_100_BR', '_200_BR', '_100_FL', '_200_FL',
   '_200_IM', '_400_IM']
one_per_event=[]
for event in events:
    one_per_event.append(event+'_0')

###########################################
#############################################

def convert_to_seconds(str_time):
    '''example: '4:18.83' to 258.83'''
    split=str_time.split(':')
    if len(split)==1:
        return float(split[0])
    else:
        minute=int(split[0])
        secs=float(split[1])
    return minute*60+secs

def prep_input(dic):
    if dic['gender']=='Female' :dic['gender']='F'
    else:  dic['gender']='M'
        
    
    for event in events:
        if dic[event]=='': continue
        try:
            dic[event]=convert_to_seconds(dic[event])
        except:
            print(f'couldn not convert {event}={dic[event]}')
            return False
    dic['season']=17
    return pd.DataFrame(dic, index=['Times'])


def append_teams(teams,swimmer):
    swimmer=swimmer.reset_index(drop=True)


    teams=teams[one_per_event].reset_index()#[['season','_50_FR_0','gender','team_id']]

    merged=swimmer.merge(teams, on=['season','gender'])
    merged=merged.reset_index().set_index(['gender','season','team_id'])
    merged=merged[events+one_per_event]
    merged.replace('', np.nan, inplace=True) 
    merged.fillna(value=99999,inplace=True)
    return merged

def get_ranks(merged,m):
    merged['result']=m.predict_proba(merged)[:,1]
    merged['rank']=merged['result'].rank(ascending=False)
    ranks=merged[['rank','result']].sort_values(by='rank')
    return ranks

def prep_output(ranks,team_info):
    final=pd.merge(ranks.reset_index(), team_info, left_on = 'team_id', right_on = 'team_id')
    final=final[['rank','team','website','conference','division','img','address']]
    output={}
    i=1
    for idx, row in final.iterrows():
        output[i]=list(row.values)
        i+=1
    return output

def mk_output(entered):
    swimmer=prep_input(entered)
    if type(swimmer)==bool: return False
    merged=append_teams(teams,swimmer)
    ranks=get_ranks(merged,m)
    return prep_output(ranks,team_info)

#####################################################
#####################################################
