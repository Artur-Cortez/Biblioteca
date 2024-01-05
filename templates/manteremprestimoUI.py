import streamlit as st
import pandas as pd
from views import View
import time
import datetime


from streamlit_searchbox import st_searchbox

class ManterEmprestimoUI:
  def main():
    st.header("Cadastro de Empréstimos")
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
    with tab1: ManterEmprestimoUI.listar()
    with tab2: ManterEmprestimoUI.inserir()
    with tab3: ManterEmprestimoUI.atualizar()
    with tab4: ManterEmprestimoUI.excluir()

  def listar():
    emprestimos = View.emprestimo_listar()
    if len(emprestimos) == 0:
      st.write("Nenhum empréstimo cadastrado")
    else:
      dic = []
      for obj in emprestimos:
        id = obj.get_id()
        idExemplar = obj.get_idExemplar()
        idUsuario = obj.get_idUsuario()
        nome = View.cliente_listar_id(idUsuario).get_nome()
        dataEmprestimo = obj.get_dataEmprestimo()
        dic.append([id, idExemplar, nome, datetime.datetime.strftime(dataEmprestimo, "%d/%m/%Y")])
      df = pd.DataFrame(dic, columns=["Id", "Id do exemplar", "Nome do usuário", "Data de empréstimo"])
      st.dataframe(df, hide_index=True)

  def inserir():
    
    # o valor dessa var vai ser exatamente a opção, que é retornada pela função de busca passada, no caso uma str
    exemplar_searchbox = st_searchbox(
      View.exemplar_searchbox_titulo,
      key="livro_searchbox",
      clearable=True,
      placeholder = "Busque por um livro...",
      default_options=[]
    )

    st.write(f"Selecionado: {exemplar_searchbox}")
 
    dataEmprestimo = st.date_input("Informe a data de empréstimo", key="chave1")   

    if st.button("Inserir"):
      try:
        lista = View.exemplares_disponiveis_por_titulo(exemplar_searchbox)          
        View.insercao_emprestimo(lista, dataEmprestimo)
        
        if len(lista) != 0:
          st.success("Empréstimo feito com sucesso, bjs")
          time.sleep(0.3)
          st.rerun()
        
        
      except ValueError as error:
        st.write(f"Erro: {error}")

  def atualizar():
    st.write("Essa página foi desabilitada por redundância")
    # emprestimos = View.emprestimo_listar()
    # if len(emprestimos) == 0:
    #   st.write("Nenhum emprestimo cadastrado")
    # else:
    #   op = st.selectbox("Atualização de empréstimo", emprestimos)
    
    #   titulo_input = st.text_input("Informe o nome do exemplar de livro a ser escolhido")
    #   idUsuario = st.session_state["cliente_id"]
    #   dataEmprestimo = st.date_input("Informe a data de empréstimo", key="chave2")

    #   exemplares = View.exemplar_listar()
    #   idExemplar = 999
      
    #   for var1 in exemplares:
    #     idLivro = var1.get_idLivro()
    #     titulo = View.livro_listar_id(idLivro).get_titulo()
    #     if titulo_input == titulo:
    #       idExemplar = var1.get_id()

    #   if st.button("Atualizar"):
    #     try:
    #       id = op.get_id()
    #       View.emprestimo_atualizar(id, idExemplar, idUsuario, dataEmprestimo)
    #       st.success("Empréstimo atualizado com sucesso")
    #       time.sleep(0.5)
    #       st.rerun()
    #     except ValueError as error:
    #       st.write(f"Erro: {error}")

  def excluir():
    emprestimos = View.emprestimo_listar()
    if len(emprestimos) == 0:
      st.write("Nenhum empréstimo cadastrado")
    else:
      op = st.selectbox("Exclusão de empréstimos", emprestimos)
      if st.button("Excluir"):
        id = op.get_id()
        View.emprestimo_excluir(id)
        st.success("Empréstimo excluído com sucesso")
        time.sleep(0.5)
        st.rerun()