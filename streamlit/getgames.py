import sys
sys.path.append('../')
from src.params import Params
from src.get_inputs import get_my_games
from src.add_odds import add_odds_next
import pandas as pd
from model.ger_model import predict_proba
from model.model_performance import check_performance
import warnings
warnings.filterwarnings('ignore')

def main():
    params=Params()
    leagues=params.leagues
    df = pd.DataFrame()
    for league in leagues:
        try:
            df_league=get_my_games(params.link_leagues[league],params)
            if (df_league.shape[0] == 0) or (check_performance(league,params)==False):
                pass
            else:
                df_league=add_odds_next(df_league,league,params)
                df_league=predict_proba(df_league,league,params)
                df=pd.concat([df,df_league])
        except:
            pass
    df=df.reset_index(drop=True)
    df.to_csv('preview.csv',index=False)

if __name__ == '__main__':
    main()
