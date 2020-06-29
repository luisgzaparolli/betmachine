from src.data_preparation import get_games
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
import time
import os


def find_result(home_goals, away_goals):
    if home_goals > away_goals:
        return 'Home'
    elif away_goals > home_goals:
        return 'Away'
    else:
        return 'Draw'


def form_home(result):
    home = int(result[0])
    away = int(result[1])
    if home > away:
        return 'Win'
    elif away > home:
        return 'Lose'
    else:
        return 'Draw'


def form_away(result):
    home = int(result[0])
    away = int(result[1])
    if away > home:
        return 'Win'
    elif home > away:
        return 'Lose'
    else:
        return 'Draw'

def get_info(df,url):
    html = requests.get(url, headers={'User-Agent': 'test'}).content
    soup = BeautifulSoup(html, 'lxml')
    tables = pd.read_html(html)
    teams = soup.find_all('h2', {'class': 'mt01e ac bold'})
    final = {}
    final['link']=url
    final['round']=int(soup.find('p',{'class':'mt05e'}).find('span').text)
    final['home_team'] = teams[0].text
    final['away_team'] = teams[1].text
    class_all = tables[6]
    final['home_position_all'] = class_all.loc[class_all['Team'] == final['home_team'], '#'].values[0]
    final['away_position_all'] = class_all.loc[class_all['Team'] == final['away_team'], '#'].values[0]
    final['home_winperc_all'] = float(class_all.loc[class_all['Team'] == final['home_team'], 'Win%'].values[0].strip('%')) / 100
    final['away_winperc_all'] = float(class_all.loc[class_all['Team'] == final['away_team'], 'Win%'].values[0].strip('%')) / 100
    class_home = tables[4]
    final['home_position_home'] = int(class_home.loc[class_home['Team'] == final['home_team'], '#'].values[0])
    final['away_position_home'] = int(class_home.loc[class_home['Team'] == final['away_team'], '#'].values[0])
    final['home_winperc_home'] = float(
        class_home.loc[class_home['Team'] == final['home_team'], 'Win%'].values[0].strip('%')) / 100
    final['away_winperc_home'] = float(
        class_home.loc[class_home['Team'] == final['away_team'], 'Win%'].values[0].strip('%')) / 100
    class_away = tables[5]
    final['home_position_away'] = class_away.loc[class_away['Team'] == final['home_team'], '#'].values[0]
    final['away_position_away'] = class_away.loc[class_away['Team'] == final['away_team'], '#'].values[0]
    final['home_winperc_away'] = float(
        class_away.loc[class_away['Team'] == final['home_team'], 'Win%'].values[0].strip('%')) / 100
    final['away_winperc_away'] = float(
        class_away.loc[class_away['Team'] == final['away_team'], 'Win%'].values[0].strip('%')) / 100
    home_form_results = soup.find_all('div', {'class': 'h2h-history-results-wrapper'})[0].find_all('div', {
        'class': 'w16 fl ac score-box'})
    home_form = [form_home(list(map(str.strip, item.text.split('-')))) for item in home_form_results]
    final['home_form_1'] = home_form[0]
    final['home_form_2'] = home_form[1]
    final['home_form_3'] = home_form[2]
    final['home_form_4'] = home_form[3]
    final['home_form_5'] = home_form[4]
    away_form_results = soup.find_all('div', {'class': 'h2h-history-results-wrapper'})[1].find_all('div', {
        'class': 'w16 fl ac score-box'})
    away_form = [form_away(list(map(str.strip, item.text.split('-')))) for item in away_form_results]
    final['away_form_1'] = away_form[0]
    final['away_form_2'] = away_form[1]
    final['away_form_3'] = away_form[2]
    final['away_form_4'] = away_form[3]
    final['away_form_5'] = away_form[4]
    final['home_previous'] = float(
        soup.find('div', {'class': 'w30 fl ac lh14e teamA pr r-w20'}).find('span', {'class': 'dark-gray'}).text.replace(
            '(', '').replace('%)', '')) / 100
    try:
        final['draw_previous'] = float(
        soup.find('div', {'class': 'lh14e draw-line semi-bold'}).find('span', {'class': 'dark-gray'}).text.replace('(',
                                                                                                                   '').replace(
            '%)', '')) / 100
    except:
        final['draw_previous'] = 0
    final['away_previous'] = float(
        soup.find('div', {'class': 'w30 fl ac lh14e teamB pr r-w20'}).find('span', {'class': 'dark-gray'}).text.replace(
            '(', '').replace('%)', '')) / 100
    new_df=pd.DataFrame(final,index=[0])
    df = pd.concat([df, new_df])
    return df

def get_info_streamlit(df,url):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tables = pd.read_html(html)
    teams = soup.find_all('h2', {'class': 'mt01e ac bold'})
    final = {}
    final['link'] = url
    final['round'] = int(soup.find('p', {'class': 'mt05e'}).find('span').text)
    final['home_team'] = teams[0].text
    final['away_team'] = teams[1].text
    class_all = tables[6]
    final['home_position_all'] = class_all.loc[class_all['Team'] == final['home_team'], '#'].values[0]
    final['away_position_all'] = class_all.loc[class_all['Team'] == final['away_team'], '#'].values[0]
    final['home_winperc_all'] = float(class_all.loc[class_all['Team'] == final['home_team'], 'Win%'].values[0].strip('%')) / 100
    final['away_winperc_all'] = float(class_all.loc[class_all['Team'] == final['away_team'], 'Win%'].values[0].strip('%')) / 100
    class_home = tables[4]
    final['home_position_home'] = int(class_home.loc[class_home['Team'] == final['home_team'], '#'].values[0])
    final['away_position_home'] = int(class_home.loc[class_home['Team'] == final['away_team'], '#'].values[0])
    final['home_winperc_home'] = float(
        class_home.loc[class_home['Team'] == final['home_team'], 'Win%'].values[0].strip('%')) / 100
    final['away_winperc_home'] = float(
        class_home.loc[class_home['Team'] == final['away_team'], 'Win%'].values[0].strip('%')) / 100
    class_away = tables[5]
    final['home_position_away'] = class_away.loc[class_away['Team'] == final['home_team'], '#'].values[0]
    final['away_position_away'] = class_away.loc[class_away['Team'] == final['away_team'], '#'].values[0]
    final['home_winperc_away'] = float(
        class_away.loc[class_away['Team'] == final['home_team'], 'Win%'].values[0].strip('%')) / 100
    final['away_winperc_away'] = float(
        class_away.loc[class_away['Team'] == final['away_team'], 'Win%'].values[0].strip('%')) / 100
    home_form_results = soup.find_all('div', {'class': 'h2h-history-results-wrapper'})[0].find_all('div', {
        'class': 'w16 fl ac score-box'})
    home_form = [form_home(list(map(str.strip, item.text.split('-')))) for item in home_form_results]
    final['home_form_1'] = home_form[0]
    final['home_form_2'] = home_form[1]
    final['home_form_3'] = home_form[2]
    final['home_form_4'] = home_form[3]
    final['home_form_5'] = home_form[4]
    away_form_results = soup.find_all('div', {'class': 'h2h-history-results-wrapper'})[1].find_all('div', {
        'class': 'w16 fl ac score-box'})
    away_form = [form_away(list(map(str.strip, item.text.split('-')))) for item in away_form_results]
    final['away_form_1'] = away_form[0]
    final['away_form_2'] = away_form[1]
    final['away_form_3'] = away_form[2]
    final['away_form_4'] = away_form[3]
    final['away_form_5'] = away_form[4]
    final['home_previous'] = float(
        soup.find('div', {'class': 'w30 fl ac lh14e teamA pr r-w20'}).find('span', {'class': 'dark-gray'}).text.replace(
            '(', '').replace('%)', '')) / 100
    try:
        final['draw_previous'] = float(
        soup.find('div', {'class': 'lh14e draw-line semi-bold'}).find('span', {'class': 'dark-gray'}).text.replace('(',
                                                                                                                   '').replace(
            '%)', '')) / 100
    except:
        final['draw_previous'] = 0
    final['away_previous'] = float(
        soup.find('div', {'class': 'w30 fl ac lh14e teamB pr r-w20'}).find('span', {'class': 'dark-gray'}).text.replace(
            '(', '').replace('%)', '')) / 100
    new_df=pd.DataFrame(final,index=[0])
    df = pd.concat([df, new_df])
    driver.quit()
    return df

def get_my_games(url,params):
    df = pd.DataFrame()
    links=get_games(url)
    for link in links:
        df = get_info(df, link)
    return df.reset_index(drop=True)
