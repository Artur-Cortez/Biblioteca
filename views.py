from models.genero import Genero, NGenero
from models.livro import Livro, NLivro
from models.exemplar import Exemplar, NExemplar
from models.emprestimo import Emprestimo, NEmprestimo
from models.cliente import Cliente, NCliente
import datetime
import streamlit as st

class View:
  def cliente_inserir(nome, email, senha):
    if nome == '' or email == '' or senha == '': 
        raise ValueError("Campo(s) obrigatório(s) vazio(s)")

    for i in View.cliente_listar():
        if i.get_email() == email:
            raise ValueError("Email já cadastrado")
    cliente = Cliente(0, nome, email, senha)    
    NCliente.Inserir(cliente)

  def cliente_listar():
    return NCliente.Listar()
  
  def cliente_listar_id(id):
    return NCliente.Listar_Id(id)

  def cliente_atualizar(id, nome, email, senha):
    if nome == '' or email == '' or senha == '': 
      raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    cliente = Cliente(id, nome, email, senha)
    NCliente.Atualizar(cliente)
    
  def cliente_excluir(id):
    cliente = Cliente(id, "", "", "", "")
    NCliente.Excluir(cliente)    

  def cliente_admin():
    for cliente in View.cliente_listar():
      if cliente.get_nome() == "admin": return
    View.cliente_inserir("admin", "admin", "admin")

  def cliente_login(email, senha):
    for cliente in View.cliente_listar():
      if cliente.get_email() == email and cliente.get_senha() == senha:
        return cliente
    return None
  

  def genero_inserir(nome):
    if nome == '': 
        raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    genero = Genero(0, nome)    
    NCliente.Inserir(genero)

  def genero_listar():
    return NGenero.Listar()
  
  def genero_listar_id(id):
    return NGenero.Listar_Id(id)

  def genero_atualizar(id, nome):
    if nome == '': 
      raise ValueError("Campo obrigatório vazio")
    genero = Genero(id, nome)
    NCliente.Atualizar(genero)
    
  def genero_excluir(id):
    genero = Genero(id, "", "", "", "")
    NGenero.Excluir(genero)


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
    livro = Livro(id, "", "", "", "")
    NLivro.Excluir(livro) 
