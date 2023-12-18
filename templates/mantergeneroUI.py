import streamlit as st
import pandas as pd
from views import View
import time

class ManterGeneroUI:
  def main():
    st.header("Cadastro de gêneros")
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
    with tab1: ManterGeneroUI.listar()
    with tab2: ManterGeneroUI.inserir()
    with tab3: ManterGeneroUI.atualizar()
    with tab4: ManterGeneroUI.excluir()

  def listar():
    generos : View.genero_listar()
    if len(generos) == 0:
      st.write("Nenhum gênero literário cadastrado")
    else:      
      dic = []
      for obj in generos:

        id : obj.get_id()
        nome : obj.get_nome()
        dic.append([id, nome])
      df : pd.DataFrame(dic, columns=["Id", "Nome"])
      st.dataframe(df)

  def inserir():

    traducao = {
      "ANTIQUES & COLLECTIBLES" : "Antiguidades",
      "LITERARY COLLECTIONS" : "Coleções literárias",
      "ARCHITECTURE" : "Arquitetura",
      "LITERARY CRITICISM" : "Crítica literária",
      "ART" : "Arte",
      "MATHEMATICS" : "Matemática",
      "BIBLES" : "Bíblia",
      "MEDICAL" : "Medicina",
      "BIOGRAPHY & AUTOBIOGRAPHY" : "Biografia e autobiografia",
      "MUSIC" : "Música",
      "BODY, MIND & SPIRIT" : "",
      "NATURE"  : "Natureza",
      "BUSINESS & ECONOMICS" : "Economia e negócios",
      "PERFORMING ARTS" : "Artes performáticas",
      "COMICS & GRAPHIC NOVELS" : "Quadrinhos e romance gráfico",
      "PETS" : "Pets",
      "COMPUTERS" : "Informática",
      "PHILOSOPHY" : "Filosofia",
      "COOKING" : "Culinária",
      "PHOTOGRAPHY" : "Fotografia",
      "CRAFTS & HOBBIES" : "Artesanato e passatempos",
      "POETRY" : "Poesia",
      "DESIGN" : "Design",
      "POLITICAL SCIENCE" : "Ciências políticas",
      "DRAMA" : "Drama",
      "PSYCHOLOGY" : "Psicologia",
      "EDUCATION" : "Educação",
      "REFERENCE" : "Geral",
      "FAMILY & RELATIONSHIPS" : "Família e relacionamentos",
      "RELIGION" : "Religião",
      "FICTION" : "Ficção",
      "SCIENCE" : "Ciência",
      "FOREIGN LANGUAGE STUDY" : "Estudo da linguagem estrangeira",
      "SELF-HELP" : "Auto-ajuda",
      "GAMES & ACTIVITIES" : "Jogos e atividades",
      "SOCIAL SCIENCE" : "Sociologia",
      "GARDENING" : "Jardinagem",
      "SPORTS & RECREATION" : "Esportes e lazer",
      "HEALTH & FITNESS" : "Saúde e bem-estar",
      "STUDY AIDS" : "Apostilas de estudo",
      "HISTORY" : "História",
      "TECHNOLOGY & ENGINEERING" :"Tecnologia e engenharia",
      "HOUSE & HOME" : "Casa e lar",
      "TRANSPORTATION" : "Transporte",
      "HUMOR" : "Comédia",
      "TRAVEL" : "Viagem",
      "JUVENILE FICTION" : "Ficção infanto-juvenil",
      "TRUE CRIME" : "Crimes reais",
      "JUVENILE NONFICTION" : "Não-ficção infanto-juvenil",
      "YOUNG ADULT FICTION" : "Ficção juvenil",
      "LANGUAGE ARTS & DISCIPLINES" : "Artes da linguagem e disciplinas",
      "YOUNG ADULT NONFICTION" : "Não-ficção juvenil ",
      "LAW" : "Direito",

    }

    nome : st.text_input("Informe o nome do gênero literário")

    if st.button("Inserir gênero"):
      try:
        View.genero_inserir(nome)
        st.success("Gênero inserido com sucesso")
        time.sleep(0.5)
        st.rerun()
      except ValueError as error:
        st.write(f"Erro: {error}")

  def atualizar():
    generos = View.genero_listar()
    if len(generos) == 0:
      st.write("Nenhum gênero cadastrado")
    else:
      op = st.selectbox("Atualização de gêneros", generos, format_func=lambda x: x.get_nome())
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
      op = st.selectbox("Exclusão de gêneros", [x.get_nome() for x in generos])
      if st.button("Excluir"):
        id = op.get_id()
        View.genero_excluir(id)
        st.success("Gênero excluído com sucesso")
        time.sleep(0.5)
        st.rerun()