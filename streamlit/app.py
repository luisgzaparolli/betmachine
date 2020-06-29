import streamlit as st
import pandas as pd
from ger_bet import calc_bet

@st.cache
def load_data():
    return pd.read_csv('preview.csv')

df = load_data()



def main():
    st.title('Betmachine')
    agree = st.checkbox("Visualizar jogos")
    if agree:
        st.table(df[['home_team','away_team']])
    st.header('Alterar parâmetros')
    slider_fc = st.empty()
    fc = float(slider_fc.slider('Fator conservador %', 51, 80, 60, 1)/100)
    slider_fa = st.empty()
    fa = float(slider_fa.slider('Fator arrojado %', 0, 50, 40, 1)/100)
    slider_pc = st.empty()
    pc = float(slider_pc.slider('Percentual conservador %', 50, 100, 60, 1)/100)
    valor=st.number_input(label='Valor a apostar',min_value=10,step=10)
    calc=st.button(label='Calcular')
    if calc:
        st.table(calc_bet(df,fc,fa,pc,valor))


if __name__ == '__main__':
    main()