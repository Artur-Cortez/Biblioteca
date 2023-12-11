import streamlit as st
import pandas as pd
from views import View
import time
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from urllib.parse import quote

from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.grid import grid


class ManterLivroUI:
  def main():
    st.header("Cadastro de Livros")
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
    with tab1: ManterLivroUI.listar()
    with tab2: ManterLivroUI.inserir()
    with tab3: ManterLivroUI.atualizar()
    with tab4: ManterLivroUI.excluir()

  def listar():
    random_df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    my_grid = grid(2, [2, 4, 1], 1, 4, vertical_align="bottom")

    # Row 1:
    my_grid.dataframe(random_df, use_container_width=True)
    my_grid.line_chart(random_df, use_container_width=True)
    # Row 2:
    my_grid.selectbox("Select Country", ["Germany", "Italy", "Japan", "USA"])
    my_grid.text_input("Your name")
    my_grid.button("Send", use_container_width=True)
    # Row 3:
    my_grid.text_area("Your message", height=40)
    # Row 4:
    my_grid.button("Example 1", use_container_width=True)
    my_grid.button("Example 2", use_container_width=True)
    my_grid.button("Example 3", use_container_width=True)
    my_grid.button("Example 4", use_container_width=True)
    
    # Row 5 (uses the spec from row 1):
    with my_grid.expander("Show Filters", expanded=True):
        st.slider("Filter by Age", 0, 100, 50)
        st.slider("Filter by Height", 0.0, 2.0, 1.0)
        st.slider("Filter by Weight", 0.0, 100.0, 50.0)
    my_grid.dataframe(random_df, use_container_width=True)
    # livros = View.livro_listar()
    # if len(livros) == 0:
    #   st.write("Nenhum livro cadastrado")
    # else:
    #   grade = grid(4)
    #   n_linhas = 1 + len(livros) // 4

    #   for linha in range(n_linhas):
    #     for coluna in range(4):
          
    #       if linha * 4 + coluna < len(livros):
    #         with stylable_container(
    #           key=f"container_with_border_{linha}_{coluna}",
    #           css_styles="""
    #               {
    #                   border: 1px solid rgba(255, 51, 63, 0.2);
    #                   border-radius: 0.5rem;
    #                   padding: calc(1em - 1px)
    #               }
    #               """,
    #           ): grade.text_area(livros[linha *4 + coluna].get_titulo(), use_container_width=True)

              


      

  def inserir():

    def pegar_url(book_name):
            book_name = book_name.upper()
            base_url = 'https://www.livrariacultura.com.br/busca/?ft='
            encoded_book_name = quote(book_name)
            search_link = f'{base_url}{encoded_book_name}&originalText={encoded_book_name}'
            return search_link
    
    titulo_livro = st.text_input("Insira o título EXATO do livro com acentuação correta")
    botao_buscar = st.button('Buscar')

    if st.session_state.get('button') != True:

        st.session_state['button'] = botao_buscar

    if st.session_state['button'] == True:

      opcoes = ChromeOptions()
      opcoes.add_argument("--headless=new")
      driver = webdriver.Chrome(options=opcoes)


      driver.get(pegar_url(titulo_livro.upper()))
      

      elemento = WebDriverWait(driver, 10).until(
          EC.presence_of_all_elements_located((By.LINK_TEXT, titulo_livro.upper()))
      )
      ActionChains(driver).click(elemento[0]).perform()

      img = WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.ID, "image-main"))
      )

      li_autor = WebDriverWait(driver, 20).until(
          EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#Autor span")) 
      )
      li_ano = WebDriverWait(driver, 20).until(
          EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#Ano span"))
      )

      img_url = img.get_attribute('src')
      autor = li_autor[1].get_attribute('innerText')
      ano = li_ano[1].get_attribute('innerText')

      st.session_state["titulo"] = titulo_livro
      st.session_state["img_url"] = img_url
      st.session_state["autor"] = autor
      st.session_state["ano"] = ano

      st.markdown(f'### Título: {titulo_livro}')
      View.exibir_img_crop_via_url(img_url)
      st.markdown(f'##### Autor: {autor}')
      st.markdown(f'##### Ano: {ano}')


      if st.button('Inserir'):
        st.session_state['button'] = False

        try:
          View.livro_inserir(st.session_state["titulo"], st.session_state["autor"], st.session_state["ano"], st.session_state["img_url"], 999)
          st.write("Livro inserido com sucesso")
          time.sleep(1)
          st.rerun() 
        except ValueError as error:
            st.write(f"Erro: {error}")

    

  def atualizar():
    livros = View.livro_listar()
    if len(livros) == 0:
      st.write("Nenhum livro cadastrado")
    else:
      op = st.selectbox("Atualização de livros", livros)
      titulo = st.text_input("Informe o título correto", op.get_titulo())
      autor = st.text_input("Informe o nome correto do autor", op.get_autor())
      ano = st.text_input("Informe o ano correto de publicação", op.get_ano())
      url_img = st.text_input("Cole aqui o url correto da capa*", op.get_url_img())
      genero = st.text_input("Informe o gênero correto do livro", View.genero_listar_id(op.get_idGenero()))
      if st.button("Atualizar"):
        try:
          id = op.get_id()
          View.livro_atualizar(id, titulo, autor, ano, url_img, genero.get_id())
          st.success("Livro atualizado com sucesso")
          time.sleep(0.5)
          st.rerun()
        except ValueError as error:
          st.write(f"Erro: {error}")

  def excluir():
    livros = View.livro_listar()
    if len(livros) == 0:
      st.write("Nenhum livro cadastrado")
    else:
      op = st.selectbox("Exclusão de livros", livros)
      if st.button("Excluir"):
        id = op.get_id()
        View.livro_excluir(id)
        st.success("livros excluído com sucesso")
        time.sleep(0.5)
        st.rerun()