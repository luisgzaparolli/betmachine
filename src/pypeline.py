from data_preparation import get_links
from data_gathering import get_info, get_info_streamlit
import pandas as pd

try:
    df = pd.read_csv('../data/games.csv')
    links_saved = list(df['link'])
    links_online = get_links()
    links_to_work = list(set(links_online) - set(links_saved))
    for link in links_to_work:
        try:
            try:
                df = get_info(df, link)
            except:
                df = get_info_streamlit(df, link)
        except:
            print(link)
            pass
    df.to_csv('../data/games.csv', index=False)

except:
    df = pd.DataFrame()
    links_online = get_links()
    for link in links_online:
        try:
            try:
                df = get_info(df, link)
            except:
                df = get_info_streamlit(df, link)
        except:
            print(link)
            pass
    df.to_csv('../data/games.csv', index=False)
