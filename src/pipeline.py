import sys
sys.path.append('../')
from data_preparation import get_links
from data_gathering import get_info, get_info_streamlit
from add_odds import add_odds_feature
from model.ger_model import update_model
from model.best_param import optimize_param
import pandas as pd
from params import Params
import multiprocessing as mp
import warnings
warnings.filterwarnings('ignore')

def update_league(league):
    params = Params()
    try:
        df = pd.read_csv(f'../data/{league}/games.csv')
        links_saved = list(df['link'])
        links_online = get_links(params.link_leagues[league])
        links_to_work = list(set(links_online) - set(links_saved))
    except:
        df = pd.DataFrame()
        links_to_work = get_links(params.link_leagues[league])
    if len(links_to_work) >= 1:
        for link in links_to_work:
            try:
                try:
                    df = get_info(df, link)
                except:
                    df = get_info_streamlit(df, link)
            except Exception as error:
                print('error:', error)
                print(link)
                pass
        df= add_odds_feature(df,league,params)
        df.to_csv(f'../data/{league}/games.csv', index=False)
        #update_model(league,params)
        #optimize_param()

if __name__ == '__main__':
    params=Params()
    leagues = params.leagues
    pool = mp.Pool(mp.cpu_count())
    pool.map(update_league,leagues)
    pool.close()
