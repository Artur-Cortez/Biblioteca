from pickle import NONE
import streamlit as st
import pandas as pd
from views import View
import time

from streamlit_extras.stylable_container import stylable_container


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

    texto_da_busca = st.text_input("Digite o nome do livro a ser inserido : )")


    buscar = st.button("buscar")
    if st.session_state.get("botao") != True:
       st.session_state["botao"] = buscar

    if st.session_state["botao"] == True:
      #retorna lista de dicionarios, cada dict sendo um livro
      lista_itens = View.livros_buscar(texto_da_busca)

      sublista = [lista_itens[k : k + 3] for k in range(0, len(lista_itens), 3)]

      for box_l in sublista:
        cols = st.columns(3)

        for j, livro in enumerate(box_l):
          if lista_itens.index(livro) < len(lista_itens):
            with cols[j]:

              with stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 1px solid rgba(255, 255, 255, 0.7);
                        border-radius: 0.5rem;
                        padding-bottom: 2em;
                        text-align: center;
                    }
                    """,
              ):

                capa = livro["cover_image_url"]
                if capa == None:
                  st.write("Não foi possível achar a capa")
                else: st.image(capa)
                titulo = livro["titulo"]
                autor = livro["autor"]
                ano_publicacao = livro['ano_publicacao']
                categorias = livro['categorias']

                st.markdown(f"#### {titulo}")
                st.markdown(f"###### {autor}")
                st.markdown(f"###### {ano_publicacao}")
                st.markdown(f"###### Cat. encontradas: {categorias}")

                if st.checkbox("Setar manualmente o gênero?", key=f"{titulo}{j}checkbox"):
                  genero = st.text_input("Insira o gênero do livro:", key=f"{titulo}{j}input")


                botao_inserir = st.button("Inserir", key=f"{titulo}{j}botao")
                if botao_inserir:
                  #achar idGenero
                  generos = View.genero_listar()

                  idGenero = None
                  if View.buscar_nome(genero)
                    

                  if idGenero == None:
                    View.genero_inserir(genero)
                    idGenero = 

                  View.livro_inserir(titulo, autor, ano_publicacao, capa, )


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