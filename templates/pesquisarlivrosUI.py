import streamlit as st
from views import View
from streamlit_searchbox import st_searchbox
from streamlit_extras.stylable_container import stylable_container
import time

class PesquisarLivrosUI:
    def main():
        PesquisarLivrosUI.Pesquisar()

    def Pesquisar():
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)

        st.session_state["default"] = []
        opcoes = st.radio("", ["Buscar por título", "Buscar por autor", "Buscar por genero"])
        
        if opcoes == "Buscar por título":
            func = View.livro_searchbox_titulo
            st.session_state["default"] = [livro.get_titulo() for livro in View.livro_listar()]
       

        elif opcoes == "Buscar por autor":
            func = View.livro_searchbox_autor
            st.session_state["default"] = [livro.get_autor() for livro in View.livro_listar()]
            
        else:
          
            func = View.livro_searchbox_genero
            st.session_state["default"] = [View.genero_listar_id(l.get_idGenero()).get_nome() for l in View.livro_listar()]
           
        search = st_searchbox(
        func,
        key="livro_searchbox",
        clearable=True,
        placeholder = "Busque por um livro...",
        default_options= st.session_state["default"])


        if st.button("Buscar"):
            if opcoes == "Buscar por título":                
                livro = View.livro_buscar_por_nome(search)

                if livro == None:
                    st.write("Livro não encontrado")

                else:
    
                    idLivro = livro.get_id()
                    
                    st.write(f"Exemplares disponíveis: {View.exemplares_disponiveis(idLivro)}")

                    url = livro.get_url_img()
                    st.image(url)

                    titulo = livro.get_titulo()
                    autor = livro.get_autor()
                    ano_publicacao = livro.get_ano_publicacao()
                    genero = View.genero_listar_id(livro.get_idGenero()).get_nome()

                    st.markdown(f"#### {titulo}")
                    st.markdown(f"###### {autor}")
                    st.markdown(f"###### {ano_publicacao}")
                    st.markdown(f"###### Gênero: {genero}")

            elif opcoes == "Buscar por autor":
                autor = search

                

            
                
               

        
  

