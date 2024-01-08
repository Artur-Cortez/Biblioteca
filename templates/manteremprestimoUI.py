import streamlit as st
import pandas as pd
from views import View
import time
import datetime


from streamlit_searchbox import st_searchbox
from streamlit_extras.add_vertical_space import add_vertical_space

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
        titulo = View.livro_listar_id(View.exemplar_listar_id(idExemplar).get_idLivro()).get_titulo()
        idUsuario = obj.get_idUsuario()        
        usuario = View.cliente_listar_id(idUsuario)
        if usuario != None:
          nome = usuario.get_nome()
        else: nome = "Nome/usuário não encontrado"
        dataEmprestimo = obj.get_dataEmprestimo()
        prazoDevolucao = obj.get_prazoDevolucao()
        dic.append([id, idExemplar, titulo, nome, datetime.datetime.strftime(dataEmprestimo, "%d/%m/%Y"), datetime.datetime.strftime(prazoDevolucao, "%d/%m/%Y")])
      df = pd.DataFrame(dic, columns=["Id", "Id do exemplar", "Título", "Nome do usuário", "Data de empréstimo", "Prazo de Devolução"])
      st.dataframe(df, hide_index=True)

  def inserir():
    exemplares = View.exemplar_listar()
    if len(exemplares) == 0:
      st.write("É necessário cadastrar exemplares para fazer um empréstimo")
    else:
      exemplar = st.selectbox("Selecione um exemplar para fazer emprestimo", exemplares, format_func=lambda x: View.livro_listar_id(x.get_idLivro()).get_titulo(), key="exemplar_select")
      st.write(f"Selecionado: {exemplar}")
      add_vertical_space(1)

      opcoes = st.radio("Filtros de busca de clientes", ["Buscar por matrícula", "Buscar por nome", "Buscar por email"], horizontal=True, key="radio_emprestimo_inserir")
        
      if opcoes == "Buscar por matrícula":
        func = lambda x: f"Matrícula: {x.get_matricula()}"

      elif opcoes == "Buscar por nome":
        func = lambda x: f"Nome: {x.get_nome()}"

      else: func = lambda x: f"Email: {x.get_email()}"
      cliente = st.selectbox("Selecione um cliente (Dica: vc pode digitar para buscar)", View.cliente_listar(), format_func=func, key="cliente_selectbox")
      st.write(f"--> Cliente selecionado: {cliente}")
      dataEmprestimo = st.date_input("Informe a data de empréstimo", key="chave1")
        

      if st.button("Inserir"):
        try:
          View.emprestimo_inserir(exemplar.get_id(), cliente.get_id(), dataEmprestimo)
          View.exemplar_atualizar(exemplar.get_id(), exemplar.get_idLivro(), emprestado=True)
      
          st.success("Empréstimo feito com sucesso, bjs")
          time.sleep(0.3)
          st.rerun()
        
          
        except ValueError as error:
          st.write(f"Erro: {error}")

  def atualizar():
   
    emprestimos = View.emprestimo_listar()
    if len(emprestimos) == 0:
      st.write("Nenhum empréstimo cadastrado")
    else:
      op = st.selectbox("Selecione o empréstimo a ser atualizado", emprestimos)
      add_vertical_space(1)

      exemplar = st.selectbox("Selecione um novo exemplar (Dica: vc pode digitar para buscar)", View.exemplar_listar(), format_func=lambda x: View.livro_listar_id(x.get_idLivro()).get_titulo())
      st.divider()
      opcoes = st.radio("Filtros de busca de clientes", ["Buscar por matrícula", "Buscar por nome", "Buscar por email"], horizontal=True)
      
      if opcoes == "Buscar por matrícula":
        func = lambda x: f"Matrícula: {x.get_matricula()}"

      elif opcoes == "Buscar por nome":
        func = lambda x: f"Nome: {x.get_nome()}"

      else: func = lambda x: f"Email: {x.get_email()}"
      cliente = st.selectbox("Selecione um novo cliente (Dica: vc pode digitar para buscar)", View.cliente_listar(), format_func=func)
      st.write(f"--> Cliente selecionado: {cliente}")
      
      st.divider()

      dataEmprestimo = st.date_input("Informe uma nova data para o empréstimo ter sido feito", op.get_dataEmprestimo(), key="widget_dataemprestimo", format='DD/MM/YYYY')
      prazo_devolucao = dataEmprestimo + datetime.timedelta(days=14)
      add_vertical_space(1)
      dataDevolucao = st.date_input("Informe uma data em que esse empréstimo foi devolvido (diferente de 01/01/1900 indica que já foi devolvido)", op.get_dataDevolucao(), key="widget_dataDevolucao", format='DD/MM/YYYY') 

      if st.button("Atualizar"):
        try:
          id = op.get_id()
          idExemplar = exemplar.get_id()
          idUsuario = cliente.get_id()
          View.emprestimo_atualizar(id, idExemplar, idUsuario, dataEmprestimo, prazo_devolucao, dataDevolucao)
          st.success("Empréstimo atualizado com sucesso")
          time.sleep(0.5)
          st.rerun()
        except ValueError as error:
          st.write(f"Erro: {error}")

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