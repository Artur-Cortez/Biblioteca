import streamlit as st
import pandas as pd
from views import View
import time
import json

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
                       
                 
  def inserir():
    
    nome_livro = st.text_input("Digite o nome do livro a ser inserido : )")

    buscar = st.button("buscar")
    if st.session_state.get("botao") != True:
       st.session_state["botao"] = buscar

    if st.session_state["botao"] == True:
      lista_itens = View.livros_buscar(nome_livro)       

      # Lista para armazenar as strings das divs 'card'
      cards = []
      listona = []
      
            # Construindo a string da div 'card'
            # card_str = (
            #     f"""<div class='card' style='border: 1px solid rgba(200, 200, 200, 0.9); 
            #     border-radius: 0.5rem;
            #     padding: calc(1em - 1px); 
            #     margin-right: 3em;
            #     margin-bottom: 3em;
            #     width: 15vw;
            #     text-align: center;
            #     ' >"""
            # )

            # Dicionario
            
          


            # if cover_image_url:
            #     card_str += f"<img src='{cover_image_url}' style='width: 128px; height: 188px;'>"
            # else:
            #     card_str += f"<p>Cover Image: N/A</p>"
                
            # Adicionando elementos dentro da div 'card'
            # card_str += f"<p>{title}</p>"
            # card_str += f"<p>{author}</p>"
            # card_str += f"<p>Gêneros: {categories}</p>"


            if categories == []:
                card_str += f"<p>Não foram encontradas categorias/gêneros para esse livro</p>"

            card_str += f"<p>Data de publicação: {data_publicacao}</p>"


            card_str += "</div>"

            # Adicionando a string da div 'card' à lista
            cards.append(card_str)
            listona.append(listinha)

        # Unindo todas as strings das divs 'card' em uma única string
        cards_str = "".join(cards)

        # Construindo a string da div 'container' e exibindo
        container_str = f"<div id='container' style='display: flex; flex-wrap: wrap;'>{cards_str}</div>"
        st.markdown(container_str, unsafe_allow_html=True)

        #title, author, cover_image_url, categories, data_publicacao
        try:
          if "executed" not in st.session_state:
            View.livro_inserir(listona[0][0], listona[0][1], listona[0][4], listona[0][2], 999, listona[0][3])
            st.write("Livro inserido com sucesso")
            time.sleep(1)
            st.session_state.executed = True
            st.rerun()

        except ValueError as error:
            st.write(f"Erro: {error}")


              
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