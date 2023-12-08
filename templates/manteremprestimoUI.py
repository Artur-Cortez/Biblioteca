import streamlit as st
import pandas as pd
from views import View
import time

class ManterEmprestimoUI:
  def main():
    st.header("Cadastro de Empréstimos")
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
    with tab1: ManterEmprestimoUI.listar()
    with tab2: ManterEmprestimoUI.inserir()
    with tab3: ManterEmprestimoUI.atualizar()
    with tab4: ManterEmprestimoUI.excluir()

  def listar():
    emprestimos = View.emprestimo_listar()
    if len(emprestimos) == 0:
      st.write("Nenhum empréstimo cadastrado")
    else:
      dic = []
      for obj in emprestimos: dic.append(obj.__dict__)
      df = pd.DataFrame(dic)
      st.dataframe(df)

  def inserir():
    nome = st.text_input("Informe o nome")
    email = st.text_input("Informe o e-mail")
    senha = st.text_input("Informe a senha", type="password")
    if st.button("Inserir"):
      try:
        View.emprestimo_inserir(nome, email, senha)
        st.success("Cliente inserido com sucesso")
      except ValueError as error:
        st.write(f"Erro: {error}")

  def atualizar():
    emprestimos = View.emprestimo_listar()
    if len(emprestimos) == 0:
      st.write("Nenhum emprestimo cadastrado")
    else:
      op = st.selectbox("Atualização de Clientes", emprestimos)
      nome = st.text_input("Informe o novo nome", op.get_nome())
      email = st.text_input("Informe o novo e-mail", op.get_email())

      senha = st.text_input("Informe a nova senha")
      if st.button("Atualizar"):
        try:
          id = op.get_id()
          View.emprestimo_atualizar(id, nome, email, senha)
          st.success("Cliente atualizado com sucesso")
          time.sleep(0.5)
          st.rerun()
        except ValueError as error:
          st.write(f"Erro: {error}")

  def excluir():
    emprestimos = View.emprestimo_listar()
    if len(emprestimos) == 0:
      st.write("Nenhum emprestimo cadastrado")
    else:
      op = st.selectbox("Exclusão de Clientes", emprestimos)
      if st.button("Excluir"):
        id = op.get_id()
        View.emprestimo_excluir(id)
        st.success("Cliente excluído com sucesso")
        time.sleep(0.5)
        st.rerun()