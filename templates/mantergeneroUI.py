import streamlit as st
import pandas as pd
from views import View
import time

class ManterGeneroUI:
  def main():
    st.header("Cadastro de Clientes")
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
    with tab1: ManterGeneroUI.listar()
    with tab2: ManterGeneroUI.inserir()
    with tab3: ManterGeneroUI.atualizar()
    with tab4: ManterGeneroUI.excluir()

  def listar():
    generos = View.genero_listar()
    if len(generos) == 0:
      st.write("Nenhum gÊnero cadastrado")
    else:
      dic = []
      for obj in generos: dic.append(obj.__dict__)
      df = pd.DataFrame(dic)
      st.dataframe(df)

  def inserir():
    nome = st.text_input("Informe o nome do gênero literário")

    if st.button("Inserir"):
      try:
        View.genero_inserir(nome)
        st.success("Gênero inserido com sucesso")
      except ValueError as error:
        st.write(f"Erro: {error}")

  def atualizar():
    generos = View.genero_listar()
    if len(generos) == 0:
      st.write("Nenhum genero cadastrado")
    else:
      op = st.selectbox("Atualização de generos", generos)
      nome = st.text_input("Informe o novo nome do gênero", op.get_nome())
      if st.button("Atualizar"):
        try:
          id = op.get_id()
          View.genero_atualizar(id, nome)
          st.success("Gênero atualizado com sucesso")
          time.sleep(0.5)
          st.rerun()
        except ValueError as error:
          st.write(f"Erro: {error}")

  def excluir():
    generos = View.genero_listar()
    if len(generos) == 0:
      st.write("Nenhum gênero cadastrado")
    else:
      op = st.selectbox("Exclusão de Gêneros", generos)
      if st.button("Excluir"):
        id = op.get_id()
        View.genero_excluir(id)
        st.success("Gênero excluído com sucesso")
        time.sleep(0.5)
        st.rerun()