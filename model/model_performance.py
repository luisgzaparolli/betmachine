import pickle
import pandas as pd
import sys
sys.path.append('../')
from model.ger_model import data_prep

def check_performance(league,params):
    df=pd.read_csv(f'../data/{league}/games.csv')
    with open(f'../data/{league}/model.pkl', 'rb') as fp:
        model = pickle.load(fp)
    new_df = df.copy()
    new_df = data_prep(df, league, params)
    new_df.drop(columns=['result'])
    score=model.score(new_df.drop(columns=['result']),new_df['result'])
    if score >= params.threshold:
        return True
    else:
        return False
