import pandas as pd
import numpy as np
import base64
import datetime

def check_result(row,df):
    game=(df['home_team']==row['home_team']) & (df['away_team']==row['away_team'])
    proba=list(df[game][['Home','Draw','Away']].values[0])
    max_proba=proba.index(max(proba))
    if max_proba == 0:
        result=list(df[game][['Home','odds_home']].values[0])
        result.append('Home')
    elif max_proba == 1:
        result = list(df[game][['Draw','odds_draw']].values[0])
        result.append('Draw')
    else:
        result = list(df[game][['Away','odds_away']].values[0])
        result.append('Away')
    return result

def work_kelly(df,valor):
    kellys=[]
    for proba in df[['odds','proba']].values:
        kellys.append(((proba[0]-1)*proba[1]-(1-proba[1]))/(proba[0]-1))
    df['kellys']=kellys
    df=df.loc[df['kellys']>0,:]
    df['kellys'] = df['kellys']/np.sum(df['kellys'])
    df['aposta']=(df['kellys']*valor).round(2)
    df.drop(columns='kellys',inplace=True)
    return df

def calc_bet(df,valor,dias):
    df['date']=pd.to_datetime(df['date'])
    off_set_date=datetime.date.today() + datetime.timedelta(days=dias)
    df=df[df['date']<=off_set_date]
    new_df = df[['league','home_team', 'away_team']]
    new_df[['proba','odds','aposta']]=new_df.apply(lambda row: check_result(row,df), axis=1,result_type="expand")
    new_df.reset_index(drop=True,inplace=True)
    new_df=new_df.loc[new_df['proba']>=0.55,:].reset_index(drop=True)
    new_df=work_kelly(new_df,valor)
    if new_df['aposta'].min() < 1:
        new_df=new_df.loc[new_df['aposta']>1,:]
        new_df=work_kelly(new_df,valor)
    return new_df


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="bet.csv">Download csv file</a>'
    return href
