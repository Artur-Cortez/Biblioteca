import streamlit as st
import pandas as pd
from views import View
import time
import numpy as np
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from urllib.parse import quote

import requests


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
    
    livros = View.livro_listar()
    if len(livros) == 0:
      st.write("Nenhum livro cadastrado")
    else:
      
      table_cells = []
      for livro in livros:
          table_cells.append(f"""
              <td class="grid-item">
                  <img src="{livro.get_url_img()}" alt="Capa do livro">
                  <p>{livro.get_titulo()}</p>
                  <p>{livro.get_autor()}</p>
              </td>
          """)

      # Criar as linhas da tabela
      table_rows = []
      for i in range(0, len(table_cells), 4):
          table_rows.append('<tr>' + ''.join(table_cells[i:i+4]) + '</tr>')

      # Criar a tabela HTML
      table_html = f"""
          <style>
              .tabela {{
                width: 15vw;
              }}
              .grid-item {{
                  border: 1px solid rgba(255, 51, 63, 0.2);
                  border-radius: 0.5rem;
                  padding: calc(1em - 1px);
                  text-align: center;
                  width: 15vw;
              }}
          </style>
          <table class="tabela">
              {''.join(table_rows)}
          </table>
      """

      # Exibir a tabela HTML
      st.components.v1.html(table_html, width=1500, height=1000)

      
      # grade = grid(4)
      # n_linhas = 1 + len(livros) // 4

      # for linha in range(n_linhas):
      #   for coluna in range(4):
      #     index = linha * 4 + coluna
          
      #     if index < len(livros):
      #           livro = livros[index]
                
                       
                 
  def inserir():

    def search_books(query):
      base_url = "https://www.googleapis.com/books/v1/volumes"
      params = {"q": query}

      response = requests.get(base_url, params=params)

      if response.status_code == 200:
          data = response.json()
          with open('resultados.json', mode="w") as arquivo:
            json.dump(data, arquivo, indent=4)
          return data
      else:
          print(f"Erro ao fazer a solicitação. Código de status: {response.status_code}")
          return None

    def extract_author(volume_info):
        authors = volume_info.get("authors", [])
        return ", ".join(authors) if authors else "N/A"

    def extract_cover_image(volume_info):
        image_links = volume_info.get("imageLinks", {})
        return image_links.get("thumbnail") if image_links else None
    
    nome_livro = st.text_input("Digite o nome do livro a ser inserido : )")

    buscar = st.button("buscar")
    if st.session_state.get("botao") != True:
       st.session_state["botao"] = buscar

    if st.session_state["botao"] == True:
      query_result = search_books(nome_livro)

    

      if query_result:
        lista_itens = query_result.get("items", [])

        # Lista para armazenar as strings das divs 'card'
        cards = []

        for item in lista_itens:
            # Construindo a string da div 'card'
            card_str = (
                f"""<div class='card' style='border: 1px solid rgba(200, 200, 200, 0.9); 
                border-radius: 0.5rem;
                padding: calc(1em - 1px); 
                margin-right: 3em;
                margin-bottom: 3em;
                width: 15vw;
                text-align: center;
                ' >"""
            )

            # Dicionario
            volume_info = item.get("volumeInfo", {})

            title = volume_info.get("title", "N/A")
            author = extract_author(volume_info)
            cover_image_url = extract_cover_image(volume_info)
            categories = volume_info.get('categories', [])
            data_publicacao = volume_info.get("publishedDate", "N/A")

            if cover_image_url:
                card_str += f"<img src='{cover_image_url}' style='width: 128px; height: 188px;'>"
            else:
                card_str += f"<p>Cover Image: N/A</p>"
            # Adicionando elementos dentro da div 'card'
            card_str += f"<p>{title}</p>"
            card_str += f"<p>{author}</p>"


            if categories == []:
                card_str += f"<p>Não foram encontradas categorias para esse livro</p>"

            card_str += f"<p>Data de publicação: {data_publicacao}</p>"

          
            card_str += "</div>"

            # Adicionando a string da div 'card' à lista
            cards.append(card_str)

        # Unindo todas as strings das divs 'card' em uma única string
        cards_str = "".join(cards)

        # Construindo a string da div 'container' e exibindo
        container_str = f"<div id='container' style='display: flex; flex-wrap: wrap;'>{cards_str}</div>"
        st.markdown(container_str, unsafe_allow_html=True)


               
              # if st.button('Inserir'):
              #   st.session_state['button'] = False

              #   try:
              #       View.livro_inserir(st.session_state["titulo"], st.session_state["autor"], st.session_state["data_de_publicacao"], st.session_state["img_url"], 999)
              #       st.write("Livro inserido com sucesso")
              #       time.sleep(1)
              #       st.rerun()
              #   except ValueError as error:
              #       st.write(f"Erro: {error}")


              
      else:
          st.write("A pesquisa não foi bem-sucedida.")
      

   
    

  def atualizar():
    livros = View.livro_listar()
    if len(livros) == 0:
      st.write("Nenhum livro cadastrado")
    else:
      op = st.selectbox("Atualização de livros", livros)
      titulo = st.text_input("Informe o título correto", op.get_titulo())
      autor = st.text_input("Informe o nome correto do autor", op.get_autor())
      data_de_publicacao = st.text_input("Informe o data_de_publicacao correto de publicação", op.get_data_de_publicacao())
      url_img = st.text_input("Cole aqui o url correto da capa*", op.get_url_img())
      genero = st.text_input("Informe o gênero correto do livro", View.genero_listar_id(op.get_idGenero()))
      if st.button("Atualizar"):
        try:
          id = op.get_id()
          View.livro_atualizar(id, titulo, autor, data_de_publicacao, url_img, genero.get_id())
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