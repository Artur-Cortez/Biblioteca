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
    exemplares = View.exemplar_listar()
    if len(exemplares) == 0:
      st.write("Nenhum exemplar cadastrado")
    else:
      dic = []
      for obj in exemplares: dic.append(obj.__dict__)
      df = pd.DataFrame(dic)
      st.dataframe(df)

  def inserir():
    titulo = st.text_input("Informe o título do livro:")

    livros = View.livro_listar()
    idlivro = 0
    for l in livros:
      if l.get_titulo() == titulo:
        idlivro = l.get_id()
   
    if st.button("Inserir"):
      try:
        View.exemplar_inserir(idlivro)
        st.success("Exemplar inserido com sucesso")
      except ValueError as error:
        st.write(f"Erro: {error}")

  def atualizar():
    pass
    # exemplares = View.exemplar_listar()
    # if len(exemplares) == 0:
    #   st.write("Nenhum exemplar cadastrado")
    # else:
    #   op = st.selectbox("Atualização de Exemplares", exemplares)
    #   nome = st.text_input("Informe o novo título", op.get_nome())
      

    #   senha = st.text_input("Informe a nova senha")
    #   if st.button("Atualizar"):
    #     try:
    #       id = op.get_id()
    #       View.exemplar_atualizar(id, nome, email, senha)
    #       st.success("exemplar atualizado com sucesso")
    #       time.sleep(0.5)
    #       st.rerun()
    #     except ValueError as error:
    #       st.write(f"Erro: {error}")

  def excluir():
    exemplares = View.exemplar_listar()
    if len(exemplares) == 0:
      st.write("Nenhum exemplar cadastrado")
    else:
      op = st.selectbox("Exclusão de exemplares", exemplares)
      if st.button("Excluir"):
        id = op.get_id()
        View.exemplar_excluir(id)
        st.success("exemplar excluído com sucesso")
        time.sleep(0.5)
        st.rerun()

    