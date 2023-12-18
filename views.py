import json
from tkinter import W
from models.genero import Genero, NGenero
from models.livro import Livro, NLivro
from models.exemplar import Exemplar, NExemplar
from models.emprestimo import Emprestimo, NEmprestimo
from models.cliente import Cliente, NCliente
import datetime
import streamlit as st

import pandas as pd

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

  def buscar_por_nome(nome, modelo):
    metodo_listar = getattr(View, f"{modelo}_listar", None)
    if metodo_listar and callable(metodo_listar):
        # Chama dinamicamente o método de listar
        resultados = metodo_listar()

        for obj in resultados:
            if obj.get_nome() == nome:
                return obj

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
    exemplar = Exemplar(0, idlivro)    
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


  def emprestimo_inserir(idExemplar, idUsuario, dataEmprestimo, dataDevolucao):
    if idExemplar == None or idUsuario == None or dataEmprestimo == None: 
      raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    
    emprestimo = Emprestimo(0, idExemplar, idUsuario, dataEmprestimo, dataDevolucao)   
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



  def livro_inserir(titulo, autor, data_de_publicacao, url_img, idGenero, categorias):
    if titulo == '' or autor == '' or data_de_publicacao == '' or url_img == '' or idGenero == '': 
        raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    livro = Livro(0, titulo, autor, data_de_publicacao, url_img, idGenero, categorias)    
    NLivro.Inserir(livro)

  def livro_listar():
    return NLivro.Listar()
  
  def livro_listar_id(id):
    return NLivro.Listar_Id(id)

  def livro_atualizar(id, titulo, autor, data_de_publicacao, url_img, idGenero, categorias):
    if titulo == '' or autor == '' or data_de_publicacao == '' or url_img == '' or idGenero == '': 
      raise ValueError("Campo obrigatório vazio")
    livro = Livro(id, titulo, autor, data_de_publicacao, url_img, idGenero, categorias)
    NLivro.Atualizar(livro)
    
  def livro_excluir(id):
    livro = Livro(id,"", "", "", "", "")
    NLivro.Excluir(livro)

  def livro_extrair_autor(volume_info):
      autores = volume_info.get("authors", [])
      return ", ".join(autores) if autores else "N/A"

  def livro_extrair_capa(volume_info):
      image_links = volume_info.get("imageLinks", {})
      return image_links.get("thumbnail") if image_links else None

  #irá retornar um json com resultados já do jeito que queremos
  def livros_buscar(entrada):

    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": entrada}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        livros_encontrados = []

        data = response.json()
        lista_itens = data.get("items", [])
        for item in lista_itens:

          volume_info = item.get("volumeInfo", {})
          titulo = volume_info.get("title", "N/A")
          autor = View.livro_extrair_autor(volume_info)
          cover_image_url = View.livro_extrair_capa(volume_info)
          categories = volume_info.get('categories', [])
          ano_publicacao = volume_info.get("publishedDate", "N/A")[0:4] 

          dic = {
            "titulo": titulo,
            "autor": autor,
            "cover_image_url": cover_image_url,
            "categorias": categories,
            "ano_publicacao": ano_publicacao
          }

          livros_encontrados.append(dic)

        with open("teste.json", mode="w") as arquivo:
          json.dump(livros_encontrados, arquivo, indent=4)

        return livros_encontrados

    else:
        st.write(f"Erro ao fazer a solicitação. Código de status: {response.status_code}")
        return None
  
