import streamlit as st
import pandas as pd
from views import View
import time

class ManterExemplarUI:
  def main():
    st.header("Cadastro de Clientes")
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
    with tab1: ManterExemplarUI.listar()
    with tab2: ManterExemplarUI.inserir()
    with tab3: ManterExemplarUI.atualizar()
    with tab4: ManterExemplarUI.excluir()

  def listar():
    exemplars = View.exemplar_listar()
    if len(exemplars) == 0:
      st.write("Nenhum exemplar cadastrado")
    else:
      dic = []
      for obj in exemplars: dic.append(obj.__dict__)
      df = pd.DataFrame(dic)
      st.dataframe(df)

  def inserir():
    nome = st.text_input("Informe o nome")
    email = st.text_input("Informe o e-mail")
    senha = st.text_input("Informe a senha", type="password")
    if st.button("Inserir"):
      try:
        View.exemplar_inserir(nome, email, senha)
        st.success("exemplar inserido com sucesso")
      except ValueError as error:
        st.write(f"Erro: {error}")

  def atualizar():
    exemplars = View.exemplar_listar()
    if len(exemplars) == 0:
      st.write("Nenhum exemplar cadastrado")
    else:
      op = st.selectbox("Atualização de Clientes", exemplars)
      nome = st.text_input("Informe o novo nome", op.get_nome())
      email = st.text_input("Informe o novo e-mail", op.get_email())

      senha = st.text_input("Informe a nova senha")
      if st.button("Atualizar"):
        try:
          id = op.get_id()
          View.exemplar_atualizar(id, nome, email, senha)
          st.success("exemplar atualizado com sucesso")
          time.sleep(0.5)
          st.rerun()
        except ValueError as error:
          st.write(f"Erro: {error}")

  def excluir():
    exemplars = View.exemplar_listar()
    if len(exemplars) == 0:
      st.write("Nenhum exemplar cadastrado")
    else:
      op = st.selectbox("Exclusão de Clientes", exemplars)
      if st.button("Excluir"):
        id = op.get_id()
        View.exemplar_excluir(id)
        st.success("exemplar excluído com sucesso")
        time.sleep(0.5)
        st.rerun()