import streamlit as st

class FazerEmprestimoUI:
    def main():
        FazerEmprestimoUI.Fazer_Emprestimo()

    def Fazer_Emprestimo():
        st.text_input("Insira o nome do livro desejado")
        # [...]
        st.date_input("Informe a data de retirada na biblioteca")
        #
        st.button("Confirmar empréstimo")
