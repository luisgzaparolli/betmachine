import pandas as pd
from tpot import TPOTClassifier
import pickle


def data_prep(df):
    def encoder_result(x):
        if x == 'Home' or x == 'Win':
            return 1
        elif x == 'Draw':
            return 0
        elif x == 'Away' or x == 'Lose':
            return -1
        else:
            return x

    def encoder_teams(x):
        with open('C:/Users/pedro/Projetos/betmachine/model/list_premiere.sav', 'rb') as fp:
            teams = pickle.load(fp)
        return teams.index(x)

    df.drop(columns=['link'], inplace=True)
    df['result'] = df['result'].apply(lambda x: encoder_result(x))
    df['home_team'] = df['home_team'].apply(lambda x: encoder_teams(x))
    df['away_team'] = df['away_team'].apply(lambda x: encoder_teams(x))
    df['home_form_1'] = df['home_form_1'].apply(lambda x: encoder_result(x))
    df['home_form_2'] = df['home_form_2'].apply(lambda x: encoder_result(x))
    df['home_form_3'] = df['home_form_3'].apply(lambda x: encoder_result(x))
    df['home_form_4'] = df['home_form_4'].apply(lambda x: encoder_result(x))
    df['home_form_5'] = df['home_form_5'].apply(lambda x: encoder_result(x))
    df['away_form_1'] = df['away_form_1'].apply(lambda x: encoder_result(x))
    df['away_form_2'] = df['away_form_2'].apply(lambda x: encoder_result(x))
    df['away_form_3'] = df['away_form_3'].apply(lambda x: encoder_result(x))
    df['away_form_4'] = df['away_form_4'].apply(lambda x: encoder_result(x))
    df['away_form_5'] = df['away_form_5'].apply(lambda x: encoder_result(x))
    return df

def update_model():
    df=pd.read_csv('../data/games.csv')
    new_df=df.copy()
    new_df = data_prep(new_df)
    y = new_df.result
    X = new_df.drop(columns=['result'])
    tpot = TPOTClassifier(generations=2, n_jobs=-1,population_size=X.shape[0], max_time_mins=2, verbosity=2)
    tpot.fit(X,y)
    with open('C:/Users/pedro/Projetos/betmachine/model/model.pkl', 'wb') as f:
        pickle.dump(tpot.fitted_pipeline_, f)



