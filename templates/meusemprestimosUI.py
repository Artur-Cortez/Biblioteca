import streamlit as st
from views import View
import datetime
import pandas as pd
class MeusEmprestimosUI:
    def main():
        MeusEmprestimosUI.Listar()

    def Listar():

        meus_emprestimos = View.emprestimos_do_usuario(st.session_state["cliente_id"])
        if len(meus_emprestimos) == 0:
            st.write("Tu não fizesse empréstimo")
        
        # As vezes, não compensa tornar menos redundante um código, devido a complexidade que pode acrescentar
        # e principalmente, se a leitura não fica mais clara em comparação a versão anterior
            
        st.header("A devolver")
        dic1 = []
        for obj in meus_emprestimos:
            if obj.get_dataDevolucao() == datetime.datetime(1900, 1, 1):
                
                exemplar = View.exemplar_listar_id(obj.get_idExemplar())
                titulo = View.livro_listar_id(exemplar.get_idLivro()).get_titulo()
                dataEmprestimo = obj.get_dataEmprestimo()
                prazoDevolucao = obj.get_prazoDevolucao()
                if prazoDevolucao < datetime.datetime.today():
                    status_devolucao = "ATRASADO"
                else: status_devolucao = "EMPRESTADO"

                dic1.append([titulo, datetime.datetime.strftime(dataEmprestimo, "%d/%m/%Y"), datetime.datetime.strftime(prazoDevolucao, "%d/%m/%Y"),status_devolucao])
        if len(dic1) == 0:
            st.write("Nenhum exemplar a devolver")
        else:
            df = pd.DataFrame(dic1, columns=["Título", "Data de empréstimo", "Prazo de devolução", "Status de devolução"])
            new_df = df.sort_values(by="Prazo de devolução")


        st.dataframe(new_df, hide_index=True)

        st.header("Devolvidos")
        dic2 = []
        for obj in meus_emprestimos:
            if obj.get_dataDevolucao() != datetime.datetime(1900, 1, 1):
                
                exemplar = View.exemplar_listar_id(obj.get_idExemplar())
                titulo = View.livro_listar_id(exemplar.get_idLivro()).get_titulo()
                dataEmprestimo = obj.get_dataEmprestimo().date()
                prazoDevolucao = obj.get_prazoDevolucao()
                dataDevolucao = obj.get_dataDevolucao()

                dic2.append([titulo, datetime.datetime.strftime(dataEmprestimo, "%d/%m/%Y"), datetime.datetime.strftime(prazoDevolucao, "%d/%m/%Y"),datetime.datetime.strftime(dataDevolucao, "%d/%m/%Y")])
                
        if len(dic2) == 0:
            st.write("Nenhum exemplar já devolvido")
        else:
            df = pd.DataFrame(dic2, columns=["Título", "Data de empréstimo", "Prazo de devolução", "Data de devolução"])
            st.dataframe(df, hide_index=True)

        