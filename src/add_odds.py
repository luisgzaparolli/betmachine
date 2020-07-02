import pandas as pd
import numpy as np
import sys
sys.path.append('../')
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def add_odds_feature(df_final,league,params):
    driver = webdriver.Firefox(executable_path='geckodriver.exe')
    url=params.link_odds_next[league]+'results/'
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    df=pd.read_html(html)[0]
    df=df.iloc[:,[0,2,3,4]]
    df.columns=['game','odds_home','odds_draw','odds_away']
    def team(x,num):
        try:
            return params.dict_odds_next[league][x.split('-')[num].strip()]
        except:
            return np.nan
    df['home_team']=df['game'].apply(lambda x: team(x,0))
    df['away_team']=df['game'].apply(lambda x: team(x,1))
    df.dropna(inplace=True)
    df.drop(columns=['game'],inplace=True)
    try:
        df_final.drop(columns=['odds_away','odds_home','odds_draw'],inplace=True)
    except:
        pass
    return pd.merge(df_final,df,how='left',on=['home_team','away_team'])


def add_odds_next(df_final,league,params):
    driver = webdriver.Firefox(executable_path='../src/geckodriver.exe')
    url=params.link_odds_next[league]
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    df=pd.read_html(html)[0]
    df=df.iloc[:,[1,5,6,7]]
    df.columns=['game','odds_home','odds_draw','odds_away']
    def team(x,num):
        try:
            return params.dict_odds_next[league][x.split('-')[num].strip()]
        except:
            return np.nan
    df['home_team']=df['game'].apply(lambda x: team(x,0))
    df['away_team']=df['game'].apply(lambda x: team(x,1))
    df.dropna(inplace=True)
    df.drop(columns=['game'],inplace=True)
    try:
        df_final.drop(columns=['odds_away','odds_home','odds_draw'],inplace=True)
    except:
        pass
    df_final =pd.merge(df_final,df,how='left',on=['home_team','away_team'])
    df_final=df_final.reset_index(drop=True)
    return df_final
