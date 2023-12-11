import streamlit as st

class PesquisarLivrosUI:
    def main():
        PesquisarLivrosUI.Pesquisar()

    def Pesquisar():
        entrada = st.text_input("Insira o título/autor")
        opcoes = st.radio("", ["Buscar por título", "Buscar por autor"])
        pesquisar = st.button("Pesquisar")
        
  

