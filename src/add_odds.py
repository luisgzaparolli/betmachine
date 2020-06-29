import pandas as pd
import numpy as np
import sys
sys.path.append('../')
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def add_odds_feature(df_final,league,params):
    team_games = params.dict_odds[league]
    odds = pd.read_csv(params.link_odds[league])
    odds[ 'HomeTeam' ] = odds[ 'HomeTeam' ].apply(lambda x: team_games[x])
    odds[ 'AwayTeam' ] = odds[ 'AwayTeam' ].apply(lambda x: team_games[x])
    odds = odds[[ 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', ]]

    def search_odds_ch(row):
        try:
            mask = (odds[ 'HomeTeam' ] == row[ 'home_team' ]) & (odds[ 'AwayTeam' ] == row[ 'away_team' ])
            return odds.loc[ mask, [ 'B365H' ] ].values[ 0 ][ 0 ]
        except:
            return np.nan

    def search_odds_dw(row):
        try:
            mask = (odds[ 'HomeTeam' ] == row[ 'home_team' ]) & (odds[ 'AwayTeam' ] == row[ 'away_team' ])
            return odds.loc[ mask, [ 'B365D' ] ].values[ 0 ][ 0 ]
        except:
            return np.nan

    def search_odds_aw(row):
        try:
            mask = (odds[ 'HomeTeam' ] == row[ 'home_team' ]) & (odds[ 'AwayTeam' ] == row[ 'away_team' ])
            return odds.loc[ mask, [ 'B365A' ] ].values[ 0 ][ 0 ]
        except:
            return np.nan

    df_final[ 'odds_home' ] = df_final.apply(lambda row: search_odds_ch(row), axis=1)
    df_final[ 'odds_draw' ] = df_final.apply(lambda row: search_odds_dw(row), axis=1)
    df_final[ 'odds_away' ] = df_final.apply(lambda row: search_odds_aw(row), axis=1)
    return df_final


def get_odds(odds_home,odds_draw,odds_away,driver):
    try:
        time.sleep(5)
        pSource= driver.page_source
        soup=BeautifulSoup(pSource,'lxml')
        odds=soup.find('table',{'class':'table-main h-mb15 sortable'}).find_all('tr')
        for item in odds:
            if item.find('a').text == 'bet365':
                b365=item
                break
        odds_home.append(float(b365.find_all('td')[4].text.strip()))
        odds_draw.append(float(b365.find_all('td')[5].text.strip()))
        odds_away.append(float(b365.find_all('td')[6].text.strip()))
    except:
        driver.refresh()
        time.sleep(10)
        pSource= driver.page_source
        soup=BeautifulSoup(pSource,'lxml')
        odds=soup.find('table',{'class':'table-main h-mb15 sortable'}).find_all('tr')
        for item in odds:
            if item.find('a').text == 'bet365':
                b365=item
                break
        odds_home.append(float(b365.find_all('td')[4].text.strip()))
        odds_draw.append(float(b365.find_all('td')[5].text.strip()))
        odds_away.append(float(b365.find_all('td')[6].text.strip()))

def add_odds_next(df,league,params):
    odds_home,odds_draw,odds_away= [],[],[]
    link=params.link_odds_next[league]
    my_games=list(zip(list(df['home_team']),list(df['away_team'])))
    driver = webdriver.Firefox(executable_path='../src/geckodriver.exe')
    driver.maximize_window()
    my_dict=params.dict_odds_next[league]
    for game in my_games:
        my_text=my_dict[game[0]]+' - '+my_dict[game[1]]
        driver.get(link)
        time.sleep(5)
        elem = driver.find_element_by_link_text(my_text)
        elem.click()
        get_odds(odds_home,odds_draw,odds_away,driver)
    driver.quit()
    odds={'odds_home':odds_home,'odds_draw':odds_draw,'odds_away':odds_away}
    return pd.concat([df,pd.DataFrame(odds)],axis=1)
