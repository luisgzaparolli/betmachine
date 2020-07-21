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
    st.header('Alterar parâmetros')
    slider_fc = st.empty()
    fc = float(slider_fc.slider('Fator conservador %', 51, 80, 60, 1)/100)
    slider_fa = st.empty()
    fa = float(slider_fa.slider('Fator arrojado %', 0, 80, 40, 1)/100)
    slider_pc = st.empty()
    pc = float(slider_pc.slider('Percentual conservador %', 50, 100, 60, 1)/100)
    dias=st.number_input(label='Quero ver jogos de hoje e no máximo daqui quantos dias?',min_value=1,step=1)
    valor=st.number_input(label='Valor a apostar',min_value=10,step=10)
    calc=st.button(label='Calcular')
    if calc:
        #df_fil = df[(df['league'].isin(add_multiselect))]
        df_bet=calc_bet(df,fc,fa,pc,valor,dias)
        st.table(df_bet)
        st.markdown(get_table_download_link(df_bet), unsafe_allow_html=True)


if __name__ == '__main__':
    main()
