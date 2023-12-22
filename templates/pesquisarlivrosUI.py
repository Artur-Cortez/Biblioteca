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

        # st.session_state["default"] = []

        # if opcoes == "Buscar por título":
        #     func = View.livro_searchbox_titulo
        #     st.session_state["default"] = [livro.get_titulo() for livro in View.livro_listar()]
       

        # elif opcoes == "Buscar por autor":
        #     func = View.livro_searchbox_autor
        #     st.session_state["default"] = [livro.get_autor() for livro in View.livro_listar()]
            
        # else:
          
        #     func = View.livro_searchbox_genero
        #     st.session_state["default"] = [View.genero_listar_id(l.get_idGenero()).get_nome() for l in View.livro_listar()]
        with stylable_container(
                key="container",
                css_styles="""
                    {
                        display: flex;
                        justify-content: center;
                      
                    }
                    """,
              ):
                st.text_input("oi")
                st.button("ola")
           
            # titulo = st_searchbox(
            # func,
            # key="livro_searchbox",
            # clearable=True,
            # placeholder = "Busque por um livro...",
            # default_options= st.session_state["default"])

        
  

