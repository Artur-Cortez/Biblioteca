import streamlit as st
from views import View
from time import sleep
import datetime
import pandas as pd

class DevolucaoUI:
    def main():
        DevolucaoUI.devolver()
    def devolver():        
        c = st.selectbox("Qual o cliente q está devolvendo", View.cliente_listar())
        lista = View.emprestimos_do_usuario(c.get_id())

        st.write("Favor selecionar apenas um empréstimo por vez!!!")

        dic1 = []
        for obj in lista:
            if obj.get_dataDevolucao() == datetime.datetime(1900, 1, 1):
                
                exemplar = View.exemplar_listar_id(obj.get_idExemplar())
                idEmprestimo = obj.get_id()
                titulo = View.livro_listar_id(exemplar.get_idLivro()).get_titulo()
                dataEmprestimo = obj.get_dataEmprestimo()
                prazoDevolucao = obj.get_prazoDevolucao()
                if prazoDevolucao < datetime.datetime.today():
                    status_devolucao = "ATRASADO"
                else: status_devolucao = "EMPRESTADO"
                selecionar = False

                dic1.append([idEmprestimo, titulo, datetime.datetime.strftime(dataEmprestimo, "%d/%m/%Y"), datetime.datetime.strftime(prazoDevolucao, "%d/%m/%Y"),status_devolucao, selecionar])
        df = pd.DataFrame(dic1, columns=["Id", "Título", "Data de empréstimo", "Prazo de devolução", "Status de devolução", "Selecionar"])

        df_filtrado = df.sort_values(by="Prazo de devolução")

        data_editor = st.data_editor(df_filtrado, disabled=("Id", "Título", "Data de empréstimo", "Prazo de devolução", "Status de devolução"), hide_index=True)
        
        if st.button("Realizar devolução"):
            idEmprestimo = data_editor.loc[data_editor["Selecionar"] == True, "Id"].values[0]

            
            
            View.devolucao_livro(int(idEmprestimo), c.get_id())


            st.success("Livro devolvido com sucesso")
            sleep(0.3)
            st.rerun()



        
                