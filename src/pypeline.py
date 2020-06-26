import sys
sys.path.append('../')
from data_preparation import get_links
from data_gathering import get_info, get_info_streamlit
from model.ger_model import update_model
from model.best_param import optimize_param
import pandas as pd

def main():
    try:
        df = pd.read_csv('../data/games.csv')
        links_saved = list(df['link'])
        links_online = get_links()
        links_to_work = list(set(links_online) - set(links_saved))
    except:
        df = pd.DataFrame()
        links_to_work = get_links()
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
        df.to_csv('../data/games.csv', index=False)
        update_model()
        optimize_param()

if __name__ == '__main__':
    main()
