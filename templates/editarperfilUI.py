import streamlit as st
from views import View
from time import sleep
class EditarPerfilUI:
  def main():
    st.header("Editar perfil")
    EditarPerfilUI.editar()

  def editar():
      if st.session_state["cliente_nome"] != 'admin':
        nome = st.text_input("Informe o novo nome", st.session_state["cliente_nome"])
      else: nome = "admin"
      email = st.text_input("Informe o novo e-mail", st.session_state["cliente_email"])
      fone = st.text_input("Informe o novo fone", st.session_state["cliente_fone"])
      senha = st.text_input("Informe a nova senha", st.session_state["cliente_senha"], type="password")
      if st.button("Atualizar"):
        id = st.session_state["cliente_id"]
        View.cliente_atualizar(id, nome, email, fone, senha)
        st.session_state["cliente_nome"] = nome #Atualização "automática" do nome de usuario na barra lateral
        st.success("Dados atualizado com sucesso")
        sleep(0.5)
        st.rerun()