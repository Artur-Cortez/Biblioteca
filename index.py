from templates.manterclienteUI import ManterClienteUI
from templates.manterexemplarUI import ManterExemplarUI
from templates.mantergeneroUI import ManterGeneroUI
from templates.manteremprestimoUI import ManterEmprestimoUI
from templates.manterLivroUI import ManterLivroUI

from templates.loginUI import LoginUI
from templates.abrircontaUI import AbrirContaUI
from templates.editarperfilUI import EditarPerfilUI

from templates.pesquisarlivrosUI import PesquisarLivrosUI
from templates.fazeremprestimoUI import FazerEmprestimoUI
from templates.meusemprestimosUI import MeusEmprestimosUI
from templates.devolucaoUI import DevolucaoUI

from views import View
import streamlit as st

class IndexUI:
    def menu_visitante():
        st.set_page_config(
            page_title="Biblioteca CNAT",
            page_icon="🧊",
            layout="wide",
            initial_sidebar_state="auto",
            menu_items={
                'Get Help': 'https://www.extremelycoolapp.com/help',
                'Report a bug': "https://www.extremelycoolapp.com/bug",
                'About': "# This is a header. This is an *extremely* cool app!"
            }
                )
        op = st.sidebar.selectbox("Menu", ["Login", "Abrir conta"])
        if op == "Login": LoginUI.main()
        if op == "Abrir conta": AbrirContaUI.main()

    def menu_admin():
        op = st.sidebar.selectbox("Menu", ["Manter Gêneros", "Manter Clientes", "Manter Livros", "Manter Empréstimos", "Manter Exemplares", "Devoluções", "Editar perfil"])
        if op == "Manter Gêneros": ManterGeneroUI.main()
        if op == "Manter Clientes": ManterClienteUI.main()
        if op == "Manter Livros": ManterLivroUI.main()
        if op == "Manter Empréstimos": ManterEmprestimoUI.main()
        if op == "Manter Exemplares": ManterExemplarUI.main()
        if op == "Devoluções": DevolucaoUI.main()
        if op == "Editar perfil": EditarPerfilUI.main()
      

    def menu_cliente():
        op = st.sidebar.selectbox("Menu", ["Pesquisar livros", "Fazer empréstimo","Meus empréstimos", "Editar perfil"])
        if op == "Pesquisar livros" : PesquisarLivrosUI.main()
        if op == "Fazer empréstimo": FazerEmprestimoUI.main()
        if op == "Editar perfil": EditarPerfilUI.main()
        if op == "Meus empréstimos": MeusEmprestimosUI.main()
 

    def btn_logout():
        if st.sidebar.button("Logout"):
            del st.session_state["cliente_id"]
            del st.session_state["cliente_nome"]
            del st.session_state["cliente_email"]
            del st.session_state["cliente_matricula"]
            del st.session_state["cliente_senha"]
            st.rerun()

    def sidebar():
        if "cliente_id" not in st.session_state:
            IndexUI.menu_visitante()   
        else:
            st.sidebar.write("Bem-vindo(a), " + st.session_state["cliente_nome"])
            if st.session_state["cliente_nome"] == "admin":
                IndexUI.menu_admin()
            else: IndexUI.menu_cliente()
            IndexUI.btn_logout()  

    def main():
        View.cliente_admin()
        IndexUI.sidebar()

IndexUI.main()