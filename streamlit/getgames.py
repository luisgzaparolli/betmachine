import sys
sys.path.append('../')
from src.params import Params
from src.get_inputs import get_my_games
from src.add_odds import add_odds_next
import pandas as pd
from model.ger_model import predict_proba

def main():
    params=Params()
    leagues=params.leagues
    df = pd.DataFrame()
    for league in leagues:
        df_league=get_my_games(params.link_leagues[league],params)
        if df_league.shape[0] == 0:
            pass
        else:
            df_league=add_odds_next(df_league,league,params)
            df_league=predict_proba(df_league,league,params)
            df=pd.concat([df,df_league])
    df=df.reset_index(drop=True)
    df.to_csv('preview.csv',index=False)

if __name__ == '__main__':
    main()