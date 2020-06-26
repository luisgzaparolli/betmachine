import pandas as pd
from model.ger_model import data_prep
import pickle
import numpy as np

def optimize_param():
    df = pd.read_csv('../data/games.csv')
    new_df = df.copy()
    new_df = data_prep(new_df)
    y = new_df.result
    X = new_df.drop(columns=['result'])
    with open('C:/Users/pedro/Projetos/betmachine/model/model.pkl', 'rb') as fp:
        model = pickle.load(fp)
    df_proba = pd.DataFrame(model.predict_proba(X), columns=['Away', 'Draw', 'Home'])
    df = pd.concat([df, df_proba], axis=1)
    df_final = df[['round', 'home_team', 'away_team', 'result', 'Away', 'Draw', 'Home']]
    df_final = df_final.sort_values(by=['round'])
    with open('C:/Users/pedro/Projetos/betmachine/model/dict_odds.sav', 'rb') as fp:
        team_games = pickle.load(fp)
    odds = pd.read_csv('https://www.football-data.co.uk/mmz4281/1920/E0.csv')
    odds['HomeTeam'] = odds['HomeTeam'].apply(lambda x: team_games[x])
    odds['AwayTeam'] = odds['AwayTeam'].apply(lambda x: team_games[x])
    odds = odds[['HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A', ]]
    def search_odds_ch(row):
        mask = (odds['HomeTeam'] == row['home_team']) & (odds['AwayTeam'] == row['away_team'])
        return odds.loc[mask, ['B365H']].values[0][0]

    def search_odds_dw(row):
        mask = (odds['HomeTeam'] == row['home_team']) & (odds['AwayTeam'] == row['away_team'])
        return odds.loc[mask, ['B365D']].values[0][0]

    def search_odds_aw(row):
        mask = (odds['HomeTeam'] == row['home_team']) & (odds['AwayTeam'] == row['away_team'])
        return odds.loc[mask, ['B365A']].values[0][0]

    df_final['odds_home'] = df_final.apply(lambda row: search_odds_ch(row), axis=1)
    df_final['odds_draw'] = df_final.apply(lambda row: search_odds_dw(row), axis=1)
    df_final['odds_away'] = df_final.apply(lambda row: search_odds_aw(row), axis=1)
    df_final['my_away'] = df_final['Away'] * df_final['odds_away']
    df_final['my_home'] = df_final['Home'] * df_final['odds_home']
    df_final['my_draw'] = df_final['Draw'] * df_final['odds_draw']
    df_final = df_final[
        ['round', 'home_team', 'away_team', 'result', 'Away', 'odds_away', 'my_away', 'Draw', 'odds_draw', 'my_draw',
         'Home', 'odds_home', 'my_home']]

    def busca_ganho(rodada, fator_conservador, fator_arrojado, percentual_conservador, valor_aposta):
        df_rodada = df_final.loc[df['round'] == rodada, :]
        df_rodada.columns
        df_away = df_rodada[['home_team', 'away_team', 'result', 'Away', 'odds_away', 'my_away']]
        df_away['aposta'] = 'Away'
        df_away.columns = ['home_team', 'away_team', 'result', 'proba', 'odds', 'probaxodds', 'aposta']
        df_home = df_rodada[['home_team', 'away_team', 'result', 'Home', 'odds_home', 'my_home']]
        df_home['aposta'] = 'Home'
        df_home.columns = ['home_team', 'away_team', 'result', 'proba', 'odds', 'probaxodds', 'aposta']
        df_draw = df_rodada[['home_team', 'away_team', 'result', 'Draw', 'odds_draw', 'my_draw']]
        df_draw['aposta'] = 'Draw'
        df_draw.columns = ['home_team', 'away_team', 'result', 'proba', 'odds', 'probaxodds', 'aposta']
        df_1 = pd.concat([df_away, df_draw, df_home])
        df_1 = df_1.reset_index(drop=True)

        def set_aposta(x):
            if x >= fator_conservador:
                return 'conservador'
            elif x >= fator_arrojado:
                return 'arrojado'
            else:
                return np.nan

        df_1['tipo'] = df_1['proba'].apply(lambda x: set_aposta(x))
        df_1.dropna(inplace=True)
        sum_conservaodor = df_1.loc[df_1['tipo'] == 'conservador', 'probaxodds'].sum()
        sum_arrojado = df_1.loc[df_1['tipo'] == 'arrojado', 'probaxodds'].sum()

        def valor_apostado(row):
            if row['tipo'] == 'conservador':
                x = valor_aposta * percentual_conservador * (row['probaxodds'] / sum_conservaodor)
            else:
                x = valor_aposta * (1 - percentual_conservador) * (row['probaxodds'] / sum_arrojado)
            return x

        df_1['valor'] = df_1.apply(lambda row: valor_apostado(row), axis=1)

        def valor_ganho(row):
            if row['aposta'] == row['result']:
                return row['valor'] * row['odds']
            else:
                return 0

        df_1['ganho'] = df_1.apply(lambda row: valor_ganho(row), axis=1)
        total_ganho = df_1['ganho'].sum()
        return total_ganho - valor_aposta

    fatores_conservador = [round(item, 2) for item in np.arange(0.4, 0.75, 0.01)]
    fatores_arrojado = [round(item, 2) for item in np.arange(0.2, 0.45, 0.01)]
    percentuais_conservador = [round(item, 2) for item in np.arange(0.5, 0.9, 0.01)]
    valor_aposta = 10
    resultados = {}
    for fator_conservador in fatores_conservador:
        for fator_arrojado in fatores_arrojado:
            for percentual_conservador in percentuais_conservador:
                name = f'FC: {fatores_conservador}, FA: {fator_arrojado}, PC: {percentual_conservador}'
                valor_ganho = [
                    busca_ganho(rodada, fator_conservador, fator_arrojado, percentual_conservador, valor_aposta) for
                    rodada in range(1, 31)]
                resultados[name] = sum(valor_ganho)
    with open('C:/Users/pedro/Projetos/betmachine/model/sugestoes.sav', 'wb') as f:
        pickle.dump(resultados, f)
