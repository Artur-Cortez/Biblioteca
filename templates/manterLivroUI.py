import streamlit as st
import pandas as pd
from views import View
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote


class ManterLivroUI:
  def main():
    st.header("Cadastro de Clientes")
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
         
    titulo_livro = st.text_input("Insira o título do livro com acentuação")
          
    if st.button("buscar"):
      #O selenium será executado sem abrir a janela do chrome
      opcoes = ChromeOptions()
      opcoes.add_argument("--headless-new")
      driver = webdriver.Chrome(options=opcoes)
      driver.get(pegar_url(titulo_livro.upper()))
      
      elemento = WebDriverWait(driver, 10).until(
          EC.presence_of_all_elements_located((By.LINK_TEXT, titulo_livro.upper()))
      )
      ActionChains(driver).click(elemento[0]).perform()

      img = WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.ID, "image-main"))
      )
      img_url = img.get_attribute('src')

      el_desc = WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.ID, "info-product"))
      )
      
      li_autor = WebDriverWait(driver, 20).until(
          EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#Autor span"))
      )
      li_ano = WebDriverWait(driver, 20).until(
          EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#Ano span"))
      )
      autor = li_autor[1].get_attribute('innerText')
      ano = li_ano[1].get_attribute('innerText')
      desc = el_desc.get_attribute('innerText')
      desc_formatada = desc.replace("Informações do produto", "", 1)

      st.write(f'Título: {titulo_livro}')
      st.image(img_url)
      st.write(f'Desc: \n{desc_formatada}')
      st.write(f'Autor: {autor}')
      st.write(f'Ano: {ano}')

      if st.button("Inserir"):
          try:
              View.livro_inserir(titulo_livro, autor, ano, img_url, desc, 999)
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
      op = st.selectbox("Atualização de Clientes", livros)
      nome = st.text_input("Informe o novo nome", op.get_nome())
      email = st.text_input("Informe o novo e-mail", op.get_email())

      senha = st.text_input("Informe a nova senha")
      if st.button("Atualizar"):
        try:
          id = op.get_id()
          View.livro_atualizar(id, nome, email, senha)
          st.success("Cliente atualizado com sucesso")
          time.sleep(0.5)
          st.rerun()
        except ValueError as error:
          st.write(f"Erro: {error}")

  def excluir():
    livros = View.livro_listar()
    if len(livros) == 0:
      st.write("Nenhum livro cadastrado")
    else:
      op = st.selectbox("Exclusão de Clientes", livros)
      if st.button("Excluir"):
        id = op.get_id()
        View.livro_excluir(id)
        st.success("Cliente excluído com sucesso")
        time.sleep(0.5)
        st.rerun()