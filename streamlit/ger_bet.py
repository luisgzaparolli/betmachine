import pandas as pd
import numpy as np
import base64
import datetime

def calc_bet(df,fc,fa,pc,valor,dias):
    df['date']=pd.to_datetime(df['date'])
    off_set_date=datetime.date.today() + datetime.timedelta(days=dias)
    df=df[df['date']<=off_set_date]
    def check_result(row):
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
    df_1 = df[[ 'league','home_team', 'away_team']]
    df_1[['proba','odds','aposta']]=df_1.apply(lambda row: check_result(row), axis=1,result_type="expand")
    df_1.reset_index(drop=True,inplace=True)
    def set_aposta(x):
        if x >= fc:
            return 'conservador'
        elif x >= fa:
            return 'arrojado'
        else:
            return np.nan

    df_1[ 'tipo' ] = df_1[ 'proba' ].apply(lambda x: set_aposta(x))
    df_1.dropna(inplace=True)
    sum_conservaodor = df_1.loc[ df_1[ 'tipo' ] == 'conservador', 'probaxodds' ].sum()
    sum_arrojado = df_1.loc[ df_1[ 'tipo' ] == 'arrojado', 'probaxodds' ].sum()

    def valor_apostado(row):
        if row[ 'tipo' ] == 'conservador':
            x = valor * pc * (row[ 'probaxodds' ] / sum_conservaodor)
        else:
            x = valor * (1 - pc) * (row[ 'probaxodds' ] / sum_arrojado)
        return x

    df_1[ 'valor' ] = df_1.apply(lambda row: valor_apostado(row), axis=1).round(2)

    df_1=df_1[['league','home_team','away_team','odds','proba','aposta','tipo','valor']].reset_index(drop=True)
    return df_1.sort_values(by='league')

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="bet.csv">Download csv file</a>'
    return href
