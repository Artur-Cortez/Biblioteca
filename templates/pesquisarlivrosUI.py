import streamlit as st
from views import View
from streamlit_searchbox import st_searchbox
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.add_vertical_space import add_vertical_space

import time, datetime

class PesquisarLivrosUI:
    def main():
        PesquisarLivrosUI.Pesquisar()

    def Pesquisar():
        st.header("Faça uma busca")

        st.session_state["default"] = []
        opcoes = st.radio("", ["Buscar por título", "Buscar por autor", "Buscar por genero"], horizontal=True)
        
        if opcoes == "Buscar por título":
            func = View.livro_searchbox_titulo
            st.session_state["default"] = [livro.get_titulo() for livro in View.livro_listar()]
       

        elif opcoes == "Buscar por autor":
            func = View.livro_searchbox_autor
            st.session_state["default"] = [livro.get_autor() for livro in View.livro_listar()]
            
        else:         
            func = View.livro_searchbox_genero
            st.session_state["default"] = [View.genero_listar_id(l.get_idGenero()).get_nome() for l in View.livro_listar()]
           
        searchbox = st_searchbox(
                                func,
                                key="livro_searchbox",
                                clearable=True,
                                placeholder = "Busque por um livro...",
                                default_options= st.session_state["default"]
                            )
        if st.checkbox("Filtrar busca por ano de publicação?"):
            c1, c2 = st.columns(2)
            with c1: ano_inicial =  st.text_input("Digite o ano inicial", 1800)
            with c2: ano_final = st.text_input("Digite o ano final", datetime.datetime.today().year)
        else: 
            ano_inicial = 1800
            ano_final = datetime.datetime.today().year
        buscar = st.button("Buscar")
        add_vertical_space(1) 
        if buscar:
            if opcoes == "Buscar por título":                
                livro = View.pesquisar_por_titulo(searchbox, ano_inicial, ano_final)

                if livro == None:
                    st.write("Livro com esse título não encontrado")

                else:
                    #Hack para alinhar da maneira desejada st widgets
                    gap1, col1, col2, gap2 = st.columns([1.5, 3.5, 3.5, 1.5])

                    with col1:
                        add_vertical_space(2)
                        url = livro.get_url_img()
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
                            <img src="{url}">
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:

                        titulo = livro.get_titulo()
                        autor = livro.get_autor()
                        ano_publicacao = livro.get_ano_publicacao()
                        genero = View.genero_listar_id(livro.get_idGenero()).get_nome()

                        add_vertical_space(2)
                        st.markdown(f"##### Título: {titulo}")
                        st.markdown(f"##### Autor: {autor}")
                        st.markdown(f"##### {ano_publicacao}")
                        st.markdown(f"##### Gênero: {genero}")

                        idLivro = livro.get_id()
                        st.markdown(f"### Exemplares disponíveis: {View.num_exemplares_disponiveis(idLivro)}") 
  

            elif opcoes == "Buscar por autor":

                nome_autor = searchbox
                lista_livros = View.pesquisar_por_autor(nome_autor, ano_inicial, ano_final)

                if len(lista_livros) == 0:
                    st.write("Não foram encontrados livros desse autor")
                else:
                    View.exibir_livros(lista_livros)
            
            else:
                nome_genero = searchbox
                lista_livros = View.pesquisar_por_genero(nome_genero, ano_inicial, ano_final)

                if len(lista_livros) == 0:
                    st.write("Não foram encontrados livros desse gênero")
                else:
                    View.exibir_livros(lista_livros)



                

            
                
               

        
  

