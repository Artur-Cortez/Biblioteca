import imp
import streamlit as st
import pandas as pd
from views import View
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from urllib.parse import quote


class ManterLivroUI:
  def main():
    st.header("Cadastro de Livros")
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
    with tab1: ManterLivroUI.listar()
    with tab2: ManterLivroUI.inserir()
    with tab3: ManterLivroUI.atualizar()
    with tab4: ManterLivroUI.excluir()

  def listar():
    livros = View.livro_listar()
    if len(livros) == 0:
      st.write("Nenhum livro cadastrado")
    else:
      dic = []
      for obj in livros: dic.append(obj.__dict__)
      df = pd.DataFrame(dic)
      st.dataframe(df)

  def inserir():

    def pegar_url(book_name):
            book_name = book_name.upper()
            base_url = 'https://www.livrariacultura.com.br/busca/?ft='
            encoded_book_name = quote(book_name)
            search_link = f'{base_url}{encoded_book_name}&originalText={encoded_book_name}'
            return search_link
         
    titulo_livro = st.text_input("Insira o título EXATO do livro com acentuação")

    buscar = st.button("buscar")
    
    if st.session_state.get('button') != True:
      st.session_state['button'] = buscar

    if st.session_state['button'] == True:
    
      #O selenium será executado sem abrir a janela do chrome
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

      el_desc = WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.ID, "info-product"))
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
      desc = el_desc.get_attribute('innerText')
      desc_formatada = desc.replace("Informações do produto", "", 1)

      st.session_state["titulo"] = titulo_livro
      st.session_state["img_url"] = img_url
      st.session_state["autor"] = autor
      st.session_state["ano"] = ano
      st.session_state["desc"] = desc_formatada

      st.markdown(f'### Título: {titulo_livro}')
      st.image(img_url)

      st.text_area("", desc_formatada)
      st.markdown(f'##### Autor: {autor}')
      st.markdown(f'##### Ano: {ano}')



      if st.button("Inserir"):
          st.session_state['button'] = False
          try:
              View.livro_inserir(st.session_state["titulo_livro"], st.session_state["autor"], st.session_state[ano], st.session_state[img_url], st.session_state[desc], 999)
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
      desc = st.text_input("Informe a sinopse correta", op.get_desc())
      url_img = st.text_input("Cole aqui o url correto da capa*", op.get_url_img())
      genero = st.text_input("Informe o gênero correto do livro", View.genero_listar_id(op.get_idGenero()))
      if st.button("Atualizar"):
        try:
          id = op.get_id()
          View.livro_atualizar(id, titulo, autor, ano, desc, url_img, genero.get_id())
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