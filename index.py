from templates.manterclienteUI import ManterClienteUI
from templates.manterexemplarUI import ManterExemplarUI
from templates.mantergeneroUI import ManterGeneroUI
from templates.manteremprestimoUI import ManterEmprestimoUI
from templates.manterLivroUI import ManterLivroUI

from templates.loginUI import LoginUI
from templates.abrircontaUI import AbrirContaUI
from templates.editarperfilUI import EditarPerfilUI

from templates.paginaclienteUI import PaginaClienteUI

from views import View
import streamlit as st

class IndexUI:
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", ["Login", "Abrir Conta"])
        if op == "Login": LoginUI.main()
        if op == "Abrir Conta": AbrirContaUI.main()

    def menu_admin():
        op = st.sidebar.selectbox("Menu", ["Manter Gêneros", "Manter Clientes", "Manter Livros", "Manter Empréstimos", "Manter Exemplares", "Editar perfil"])
        if op == "Manter Gêneros": ManterGeneroUI.main()
        if op == "Manter Clientes": ManterClienteUI.main()
        if op == "Manter Livros": ManterLivroUI.main()
        if op == "Manter Empréstimos": ManterEmprestimoUI.main()
        if op == "Manter Exemplares": ManterExemplarUI.main()

        if op == "Editar perfil": EditarPerfilUI.main()
      

    def menu_cliente():
        op = st.sidebar.selectbox("Menu", ["Página de usuário" ,"Editar perfil"])
        if op == "Página de usuário" : PaginaClienteUI.main()
        if op == "Editar perfil": EditarPerfilUI.main()
 

    def btn_logout():
        if st.sidebar.button("Logout"):
            del st.session_state["cliente_id"]
            del st.session_state["cliente_nome"]
            del st.session_state["cliente_email"]
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