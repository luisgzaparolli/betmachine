import pandas as pd
import numpy as np
import base64


def calc_bet(df,fc,fa,pc,valor):
    df_rodada = df[
        [ 'round', 'home_team', 'away_team', 'Away', 'odds_away', 'my_away', 'Draw', 'odds_draw', 'my_draw', 'Home',
          'odds_home', 'my_home' ] ]
    df_away = df_rodada[ [ 'home_team', 'away_team', 'Away', 'odds_away', 'my_away' ] ]
    df_away[ 'aposta' ] = 'Away'
    df_away.columns = [ 'home_team', 'away_team', 'proba', 'odds', 'probaxodds', 'aposta' ]
    df_home = df_rodada[ [ 'home_team', 'away_team', 'Home', 'odds_home', 'my_home' ] ]
    df_home[ 'aposta' ] = 'Home'
    df_home.columns = [ 'home_team', 'away_team', 'proba', 'odds', 'probaxodds', 'aposta' ]
    df_draw = df_rodada[ [ 'home_team', 'away_team', 'Draw', 'odds_draw', 'my_draw' ] ]
    df_draw[ 'aposta' ] = 'Draw'
    df_draw.columns = [ 'home_team', 'away_team', 'proba', 'odds', 'probaxodds', 'aposta' ]
    df_1 = pd.concat([ df_away, df_draw, df_home ])
    df_1 = df_1.reset_index(drop=True)
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

    df_1[ 'valor' ] = df_1.apply(lambda row: valor_apostado(row), axis=1)
    df_1=df_1[['home_team','away_team','odds','aposta','valor']].reset_index(drop=True)
    return df_1

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="bet.csv">Download csv file</a>'
    return href