import streamlit as st
from views import View
import datetime

class FazerEmprestimoUI:
    def main():
        FazerEmprestimoUI.Fazer_Emprestimo()

    def Fazer_Emprestimo():
        titulo_input = st.text_input("Informe o nome do livro")
        idUsuario = st.session_state["cliente_id"]
        dataEmprestimo = st.date_input("Informe a data de empréstimo")

        exemplares = View.exemplar_listar()
        idExemplar = 999
        dataDevolucao=datetime.date(2199, 1, 2)
        
        for var1 in exemplares:
            idLivro = var1.get_idLivro()
            titulo = View.livro_listar_id(idLivro).get_titulo()
            if titulo_input == titulo:
                idExemplar = var1.get_id()

        if st.button("Fazer empréstimo"):
            try:
                View.emprestimo_inserir(idExemplar, idUsuario, datetime.datetime.strftime(dataEmprestimo, "%d/%m/%Y"), datetime.datetime.strftime(dataDevolucao, "%d/%m/%Y") )
                st.success("Empréstimo feito com sucesso!")
            except ValueError as error:
                st.write(f"Erro: {error}")

