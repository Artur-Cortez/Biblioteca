import streamlit as st
from views import View
from time import sleep

class DevolucaoUI:
    def main():
        DevolucaoUI.devolver()
    def devolver():
        idEmprestimo = st.text_input("Informe o id do empréstimo")
        dataDevolucao = st.date_input("Informe qual está sendo a data de devolução")

        if st.button("Devolver"):
            View.devolucao_livro(idEmprestimo, dataDevolucao)
