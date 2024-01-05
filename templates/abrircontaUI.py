import streamlit as st
import pandas as pd
from views import View
import time
import datetime

class AbrirContaUI:
  def main():
    st.header("Abrir Conta no Sistema")
    AbrirContaUI.inserir()
  
  def inserir():
    nome = st.text_input("Informe o nome")
    email = st.text_input("Informe o e-mail escolar")
    matricula = st.text_input("Informe a matrícula")
    senha = st.text_input("Informe a senha", type="password")
    senha1 = st.text_input("Confirme a senha", type="password")
    if st.button("Inserir"):
      try:
        if senha != senha1:
          st.error("Os campos de senha não correspondem")
        else:
          hoje = datetime.datetime.today()
          View.cliente_inserir(nome, email, matricula, senha, 0, datetime.datetime.strftime(hoje, "%d/%m/%Y"))
          st.success("Conta criada com sucesso")
          time.sleep(0.5)
          st.rerun()
      except ValueError as error:
            st.write(f"Erro: {error}")