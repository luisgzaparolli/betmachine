import streamlit as st
import pandas as pd
from ger_bet import calc_bet,get_table_download_link

@st.cache(allow_output_mutation=True)
def load_data():
    return pd.read_csv('preview.csv')

df = load_data()



def main():
    st.title('Betmachine')
    add_multiselect = st.multiselect('Selecione as ligas:', list(df['league'].unique()))
    agree = st.checkbox("Visualizar jogos")
    if agree:
        st.table(df[(df['league'].isin(add_multiselect))][['home_team','away_team']])
    dias=st.number_input(label='Quero ver jogos de hoje e no máximo daqui quantos dias?',min_value=1,step=1)
    valor=st.number_input(label='Valor a apostar',min_value=10,step=10)
    calc=st.button(label='Calcular')
    if calc:
        #df_fil = df[(df['league'].isin(add_multiselect))]
        df_bet=calc_bet(df,valor,dias)
        st.table(df_bet)
        st.markdown(get_table_download_link(df_bet), unsafe_allow_html=True)


if __name__ == '__main__':
    main()
