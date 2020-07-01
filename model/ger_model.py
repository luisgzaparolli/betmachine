import pandas as pd
from tpot import TPOTClassifier
import pickle
from sklearn.calibration import CalibratedClassifierCV

def data_prep(df, league, params):
    def encoder_result(x):
        if x == 'Home' or x == 'Win':
            return 1
        elif x == 'Draw':
            return 0
        elif x == 'Away' or x == 'Lose':
            return -1
        else:
            return x

    def encoder_teams(x, league, params):
        teams = params.list_teams[ league ]
        return teams.index(x)

    df = df.dropna()
    df.drop(columns=[ 'link' ], inplace=True)
    try:
        df[ 'result' ] = df[ 'result' ].apply(lambda x: encoder_result(x))
    except:
        pass
    df[ 'home_team' ] = df[ 'home_team' ].apply(lambda x: encoder_teams(x, league, params))
    df[ 'away_team' ] = df[ 'away_team' ].apply(lambda x: encoder_teams(x, league, params))
    df[ 'home_form_1' ] = df[ 'home_form_1' ].apply(lambda x: encoder_result(x))
    df[ 'home_form_2' ] = df[ 'home_form_2' ].apply(lambda x: encoder_result(x))
    df[ 'home_form_3' ] = df[ 'home_form_3' ].apply(lambda x: encoder_result(x))
    df[ 'home_form_4' ] = df[ 'home_form_4' ].apply(lambda x: encoder_result(x))
    df[ 'home_form_5' ] = df[ 'home_form_5' ].apply(lambda x: encoder_result(x))
    df[ 'away_form_1' ] = df[ 'away_form_1' ].apply(lambda x: encoder_result(x))
    df[ 'away_form_2' ] = df[ 'away_form_2' ].apply(lambda x: encoder_result(x))
    df[ 'away_form_3' ] = df[ 'away_form_3' ].apply(lambda x: encoder_result(x))
    df[ 'away_form_4' ] = df[ 'away_form_4' ].apply(lambda x: encoder_result(x))
    df[ 'away_form_5' ] = df[ 'away_form_5' ].apply(lambda x: encoder_result(x))
    return df


def update_model(league, params):
    df = pd.read_csv(f'../data/{league}/games.csv')
    new_df = df.copy()
    new_df = data_prep(new_df, league, params)
    y = new_df.result
    X = new_df.drop(columns=[ 'result' ])
    tpot = TPOTClassifier(memory='Auto',generations=50, population_size=50,verbosity=2,random_state=42,scoring="accuracy")
    tpot.fit(X, y)
    clf = CalibratedClassifierCV(tpot.fitted_pipeline_, cv='prefit', method='sigmoid')
    clf.fit(X, y)
    with open(f'../data/{league}/model.pkl', 'wb') as f:
        pickle.dump(clf, f)


def predict_proba(df, league, params):
    with open(f'../data/{league}/model.pkl', 'rb') as fp:
        model = pickle.load(fp)
    new_df = df.copy()
    new_df = data_prep(df, league, params)
    new_df=new_df.drop(columns=['date','league'])
    df_proba = pd.DataFrame(model.predict_proba(new_df), columns=[ 'Away', 'Draw', 'Home' ])
    df = pd.concat([ df, df_proba ], axis=1)
    df[ 'my_away' ] = df[ 'Away' ] * df[ 'odds_away' ]
    df[ 'my_home' ] = df[ 'Home' ] * df[ 'odds_home' ]
    df[ 'my_draw' ] = df[ 'Draw' ] * df[ 'odds_draw' ]
    return df
