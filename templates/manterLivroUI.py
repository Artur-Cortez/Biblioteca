
import streamlit as st
import pandas as pd
from views import View
import time
import random

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

    View.exibir_livros()


  def inserir():
    selecionados = []

    texto_da_busca = st.text_input("Digite o nome do livro a ser inserido : )")
    col1, col2 = st.columns(2)
    with col1:
      buscar = st.button("buscar")
      if st.session_state.get("botao") != True:
        st.session_state["botao"] = buscar

    if st.session_state["botao"] == True:
      #retorna lista de dicionarios, cada dict sendo um livro
      lista_itens = View.livros_buscar(texto_da_busca)
      if lista_itens != []:

        sublista = [lista_itens[k : k + 3] for k in range(0, len(lista_itens), 3)]

        for box_l in sublista:
          cols = st.columns(3, gap="large")

          for j, livro in enumerate(box_l):
            indice_aux = lista_itens.index(livro)
            if lista_itens.index(livro) < len(lista_itens):
              with cols[j]:

                with stylable_container(
                  key="container_with_border",
                  css_styles="""
                      {
                          border: 1px solid rgba(255, 255, 255, 0.7);
                          border-radius: 0.5rem;
                          padding-top: 1em;
                          padding-bottom: 1em;
                          text-align: center;
                          margin-bottom: 1em;
                        
                      }
                      """,
                ):

                  capa = livro["cover_image_url"]
                  if capa is None:
                      st.write("Não foi possível achar a capa")
                  else:
                      script = st.markdown(f"""
                          <style>
                          .image_container {{
                              display: flex;
                              justify-content: center;
                          }}
                          .image_container img {{
                              max-width: 100%;
                              height: auto;
                          }}
                          </style>
                          <div class="image_container">
                              <img src="{capa}">
                          </div>
                      """, unsafe_allow_html=True)
                  
                  titulo = livro["titulo"]
                  autor = livro["autor"]
                  ano_publicacao = livro['ano_publicacao']
                  categorias = livro['categorias']

                  st.markdown(f"#### {titulo}")
                  st.markdown(f"###### {autor}")
                  st.markdown(f"###### {ano_publicacao}")

                  # #genero encontrado
                  genero_correspondente = View.generos_buscar(categorias[0] if categorias != [] else "")
                  st.markdown(f"###### Gênero: {genero_correspondente}")

                  checkbox = st.checkbox("Inserir", key=f"{indice_aux}")
                  if checkbox:
                    dic = {
                      "titulo": titulo,
                      "autor": autor,
                      "ano_publicacao": ano_publicacao,
                      "url_img": capa,
                      "idGenero": View.buscar_por_nome(genero_correspondente, "genero").get_id()
                    }
                    selecionados.append(dic)
                  

    with col2:
      if st.session_state["botao"] == True:
        with stylable_container(
                    key="teste",
                    css_styles="""
                        {
            
                            padding-bottom: 1em;
                            text-align: right;
                          
                        }
                        """,
                  ):
                    if st.button("Finalizar seleção e cadastrar"):
                      #st.write(selecionados)
                      for s in selecionados:
                        View.livro_inserir(**s)
                        st.success("Livro(s) cadastrados com sucesso")
                      time.sleep(0.5)
                      st.rerun()

      

  def atualizar():
    livros = View.livro_listar()
    if len(livros) == 0:
      st.write("Nenhum livro cadastrado")
    else:
      op = st.selectbox("Atualização de livros", livros)
      titulo = st.text_input("Informe o título correto", op.get_titulo())
      autor = st.text_input("Informe o nome correto do autor", op.get_autor())
      data_de_publicacao = st.text_input("Informe o data_de_publicacao correto de publicação", op.get_ano_publicacao())
      url_img = st.text_input("Cole aqui o url correto da capa*", op.get_url_img())
      genero = st.text_input("Informe o gênero correto do livro", View.genero_listar_id(op.get_idGenero()).get_nome())
      if st.button("Atualizar"):
        try:
          id = op.get_id()
          View.livro_atualizar(id, titulo, autor, data_de_publicacao, url_img, genero.get_id())
          st.success("Livro atualizado com sucesso")
          st.session_state['button'] = False
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