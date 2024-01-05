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
        titulo_searchbox= st_searchbox(
                                View.exemplar_searchbox_titulo,
                                key="fazer_emprestimo_searchbox",
                                clearable=True,
                                placeholder = "Busque por um livro...",
                                default_options= "None"
                            )
        
        dataEmprestimo = st.date_input("Informe a data de empréstimo")

        if st.button("Fazer empréstimo"):
            try:
                lista = View.exemplares_disponiveis_por_titulo(titulo_searchbox)          
                View.insercao_emprestimo(lista, dataEmprestimo)
                
                if len(lista) != 0:
                    st.success("Empréstimo feito com sucesso, bjs")
                    time.sleep(0.3)
                    st.rerun()
            except ValueError as error:
                st.write(f"Erro: {error}")

