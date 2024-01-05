import streamlit as st
import pandas as pd
from views import View
import time
import datetime

class ManterClienteUI:
  def main():
    st.header("Cadastro de Clientes")
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
    with tab1: ManterClienteUI.listar()
    with tab2: ManterClienteUI.inserir()
    with tab3: ManterClienteUI.atualizar()
    with tab4: ManterClienteUI.excluir()

  def listar():
    clientes = View.cliente_listar()
    if len(clientes) == 0:
      st.write("Nenhum cliente cadastrado")
    else:
      dic = []
      for obj in clientes:

        id = obj.get_id()
        nome = obj.get_nome()
        email = obj.get_email()
        matricula = obj.get_matricula()
        senha = obj.get_senha()
        dic.append([id, nome, email, matricula, senha])
      df = pd.DataFrame(dic, columns=["Id", "Nome", "E-mail", "Matrícula", "Senha"])
      st.dataframe(df, hide_index=True)

  def inserir():
    nome = st.text_input("Informe o nome")
    email = st.text_input("Informe o e-mail")
    matricula = st.text_input("Informe a matrícula") 
    senha = st.text_input("Informe a senha", type="password")
    if st.button("Inserir"):
      try:
        hoje = datetime.datetime.today()
        View.cliente_inserir(nome, email, matricula, senha)
        st.success("Cliente inserido com sucesso")
        time.sleep(0.5)
        st.rerun()
      except ValueError as error:
        st.write(f"Erro: {error}")

  def atualizar():
    clientes = View.cliente_listar()
    if len(clientes) == 0:
      st.write("Nenhum cliente cadastrado")
    else:
      op = st.selectbox("Atualização de Clientes", clientes)
      nome = st.text_input("Informe o novo nome", op.get_nome())
      email = st.text_input("Informe o novo e-mail", op.get_email())
      matricula = st.text_input("Informe a nova matrícula", op.get_matricula())
      senha = st.text_input("Informe a nova senha")
      if st.button("Atualizar"):
        try:
          id = op.get_id()
          View.cliente_atualizar(id, nome, email, senha, matricula, op.get_dias_timeout(), op.get_timeout_inicio())
          st.success("Cliente atualizado com sucesso")
          time.sleep(0.5)
          st.rerun()
        except ValueError as error:
          st.write(f"Erro: {error}")

  def excluir():
    clientes = View.cliente_listar()
    if len(clientes) == 0:
      st.write("Nenhum cliente cadastrado")
    else:
      op = st.selectbox("Exclusão de Clientes", clientes)
      if st.button("Excluir"):
        id = op.get_id()
        View.cliente_excluir(id)
        st.success("Cliente excluído com sucesso")
        time.sleep(0.5)
        st.rerun()