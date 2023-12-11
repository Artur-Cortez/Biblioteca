from models.genero import Genero, NGenero
from models.livro import Livro, NLivro
from models.exemplar import Exemplar, NExemplar
from models.emprestimo import Emprestimo, NEmprestimo
from models.cliente import Cliente, NCliente
import datetime
import streamlit as st

import pandas as pd

#edicao de imagem
from PIL import Image

#http request
import requests
from io import BytesIO

class View:
  def cliente_inserir(nome, email, matricula, senha):
    if nome == '' or email == '' or senha == '': 
        raise ValueError("Campo(s) obrigatório(s) vazio(s)")

    for i in View.cliente_listar():
        if i.get_email() == email:
            raise ValueError("Email já cadastrado")
    cliente = Cliente(0, nome, email, matricula, senha)    
    NCliente.Inserir(cliente)

  def cliente_listar():
    return NCliente.Listar()
  
  def cliente_listar_id(id):
    return NCliente.Listar_Id(id)

  def cliente_atualizar(id, nome, email, senha):
    if nome == '' or email == '' or senha == '': 
      raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    cliente = Cliente(id, nome, email, View.cliente_listar_id(id).get_matricula(), senha)
    NCliente.Atualizar(cliente)
    
  def cliente_excluir(id):
    cliente = Cliente(id, "", "", "", "")
    NCliente.Excluir(cliente)    

  def cliente_admin():
    for cliente in View.cliente_listar():
      if cliente.get_nome() == "admin": return
    View.cliente_inserir("admin", "admin", "admin", "admin")

  def cliente_login(matricula, senha):
    for cliente in View.cliente_listar():
      if cliente.get_matricula() == matricula and cliente.get_senha() == senha:
        return cliente
    return None
  

  def genero_inserir(nome):
    if nome == '': 
        raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    genero = Genero(0, nome)    
    NGenero.Inserir(genero)

  def genero_listar():
    return NGenero.Listar()
  
  def genero_listar_id(id):
    return NGenero.Listar_Id(id)

  def genero_atualizar(id, nome):
    if nome == '': 
      raise ValueError("Campo obrigatório vazio")
    genero = Genero(id, nome)
    NGenero.Atualizar(genero)
    
  def genero_excluir(id):
    genero = Genero(id, "")
    NGenero.Excluir(genero)



  def exemplar_inserir(idlivro):
    if idlivro == None: 
        raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    exemplar = exemplar(0, idlivro)    
    NExemplar.Inserir(exemplar)

  def exemplar_listar():
    return NExemplar.Listar()
  
  def exemplar_listar_id(id):
    return NExemplar.Listar_Id(id)

  def exemplar_atualizar(id, nome):
    if nome == '': 
      raise ValueError("Campo obrigatório vazio")
    exemplar = Exemplar(id, nome)
    NExemplar.Atualizar(exemplar)
    
  def exemplar_excluir(id):
    exemplar = Exemplar(id, "")
    NExemplar.Excluir(exemplar)


  def emprestimo_inserir(idExemplar, idUsuario, dataEmprestimo):
    if idExemplar == None or idUsuario == None or dataEmprestimo == None: 
      raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    
    emprestimo = emprestimo(0, idExemplar, idUsuario, dataEmprestimo)   
    NEmprestimo.Inserir(emprestimo)

  def emprestimo_listar():
    return NEmprestimo.Listar()
  
  def emprestimo_listar_id(id):
    return NEmprestimo.Listar_Id(id)

  def emprestimo_atualizar(id, nome):
    if nome == '': 
      raise ValueError("Campo obrigatório vazio")
    emprestimo = Emprestimo(id, nome)
    NEmprestimo.Atualizar(emprestimo)
    
  def emprestimo_excluir(id):
    emprestimo = Emprestimo(id, "")
    NEmprestimo.Excluir(emprestimo)



  def livro_inserir(titulo, autor, ano, descricao, url_img, idGenero):
    if titulo == '' or autor == '' or ano == '' or descricao == '' or url_img == '' or idGenero == '': 
        raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    livro = Livro(0, titulo, autor, ano, descricao, url_img, idGenero)    
    NLivro.Inserir(livro)

  def livro_listar():
    return NLivro.Listar()
  
  def livro_listar_id(id):
    return NLivro.Listar_Id(id)

  def livro_atualizar(id, titulo, autor, ano, descricao, url_img, idGenero):
    if titulo == '' or autor == '' or ano == '' or descricao == '' or url_img == '' or idGenero == '': 
      raise ValueError("Campo obrigatório vazio")
    livro = Livro(id, titulo, autor, ano, descricao, url_img, idGenero)
    NLivro.Atualizar(livro)
    
  def livro_excluir(id):
    livro = Livro(id,"", "", "", "", "", "")
    NLivro.Excluir(livro)

  def exibir_img_crop_via_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        imagem_bytes = BytesIO(response.content)
        imagem = Image.open(imagem_bytes)
        imagem_cropada = imagem.crop((47, 0, imagem.width-47, imagem.height))
    else:
        st.write(f"Erro ao baixar a imagem. Código de status: {response.status_code}")
    return st.image(imagem_cropada)
  
  
    



