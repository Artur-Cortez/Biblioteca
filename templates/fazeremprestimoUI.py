import streamlit as st
from views import View
import datetime
from streamlit_searchbox import st_searchbox
import time

class FazerEmprestimoUI:
    def main():
        FazerEmprestimoUI.Fazer_Emprestimo()

    def Fazer_Emprestimo():

        idUsuario = st.session_state["cliente_id"]
        
        
        # c = View.cliente_listar_id(idUsuario)
        # dias = c.get_dias_timeout() 
        # if dias > 0:
        #     st.write(f"Você está {dias} bloqueado de fazer um empréstimo")

        # else:
        st.subheader("Busque por um título e faça empréstimo.")
        exemplar = st.selectbox("(Dica: vc pode digitar para buscar)", View.exemplar_listar(), format_func=lambda x: View.livro_listar_id(x.get_idLivro()).get_titulo())
        dataEmprestimo = st.date_input("Informe a data de retirada do livro:", format="DD/MM/YYYY")

        if st.button("Fazer empréstimo"):
            try:        
                View.emprestimo_inserir(exemplar.get_id(), st.session_state["cliente_id"], dataEmprestimo)
                View.exemplar_atualizar(exemplar.get_id(), exemplar.get_idLivro(), emprestado=True)
                st.success("Empréstimo feito com sucesso, bjs")
                time.sleep(0.3)
                st.rerun()
            except ValueError as error:
                st.write(f"Erro: {error}")

