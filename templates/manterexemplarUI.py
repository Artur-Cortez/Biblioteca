import streamlit as st
import pandas as pd
from views import View
import time
from streamlit_searchbox import st_searchbox

class ManterExemplarUI:
  def main():
    st.header("Cadastro de Exemplares")
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
      for obj in exemplares:
        id = obj.get_id()
        idLivro = obj.get_idLivro()
        titulo = View.livro_listar_id(idLivro).get_titulo()
        emprestado = obj.get_emprestado()
        dic.append([id, titulo, idLivro, emprestado])
      df = pd.DataFrame(dic, columns=["Id do exemplar", "Título", "ID do livro correspondente", "Emprestado?"])
      st.dataframe(df, hide_index=True)
      

  def inserir():
    titulo = st_searchbox(
    View.livro_searchbox_titulo,
    key="livro_searchbox",
    clearable=True,
    placeholder = "Busque por um livro...",
    default_options=[livro.get_titulo() for livro in View.livro_listar()]
)

   
    if st.button("Inserir"):
      try:
        idLivro = View.livro_buscar_por_titulo(titulo).get_id()
        View.exemplar_inserir(idLivro, emprestado=False)

       
        st.success("Exemplar inserido com sucesso")
        time.sleep(0.3)
        st.rerun()
      except ValueError as error:
        st.write(f"Erro: {error}")

  def atualizar():
    exemplares = View.exemplar_listar()
    if len(exemplares) == 0:
      st.write("Nenhum exemplar cadastrado")
    else:
      op = st.selectbox("Atualização de Exemplares", exemplares, format_func= lambda x: f"ID: {x.get_id()} | Livro: {View.livro_listar_id(x.get_idLivro()).get_titulo()} | IdLivro: {x.get_idLivro()} | Emprestado: {x.get_emprestado()} ")
      emprestado = st.checkbox("Emprestado?")

      if st.button("Atualizar"):
        try:
          id = op.get_id()
          idLivro = op.get_idLivro()
          View.exemplar_atualizar(id, idLivro, emprestado)
          st.success("exemplar atualizado com sucesso")
          time.sleep(0.5)
          st.rerun()
        except ValueError as error:
          st.write(f"Erro: {error}")

  def excluir():
    exemplares = View.exemplar_listar()
    if len(exemplares) == 0:
      st.write("Nenhum exemplar cadastrado")
    else:
      op = st.selectbox("Exclusão de Exemplares", exemplares, format_func= lambda x: f"ID: {x.get_id()} | Livro: {View.livro_listar_id(x.get_idLivro()).get_titulo()} | IdLivro: {x.get_idLivro()} | Emprestado: {x.get_emprestado()} ")
      if st.button("Excluir"):
        id = op.get_id()
        View.exemplar_excluir(id)
        st.success("exemplar excluído com sucesso")
        time.sleep(0.5)
        st.rerun()

    