import streamlit as st
import pandas as pd
from views import View
import time
import numpy as np

from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container


class PaginaInicialUI:
    def main():

        

        my_grid = grid(3, vertical_align="bottom")

        dic = []      
        for i in View.livro_listar():
            url_img = i.get_url_img()
            titulo = i.get_titulo()
            autor = i.get_autor()
            
            with stylable_container (
            key=f"container_{titulo}_{autor}",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }
                """,
            ):
                View.exibir_img_crop_via_url(url_img)
                st.header(titulo)
                st.header(autor)
            


    
        
    
        
  




    
    
        
        
        
        

            
        
        
        
            


