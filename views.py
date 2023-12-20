import json
from models.genero import Genero, NGenero
from models.livro import Livro, NLivro
from models.exemplar import Exemplar, NExemplar
from models.emprestimo import Emprestimo, NEmprestimo
from models.cliente import Cliente, NCliente

import streamlit as st

import pandas as pd

from translate import Translator
from streamlit_extras.stylable_container import stylable_container

#http request
import requests


class View:

  def buscar_por_nome(nome, modelo):
    metodo_listar = getattr(View, f"{modelo}_listar", None)
    if metodo_listar and callable(metodo_listar):
        # Chama dinamicamente o método de listar
        resultados = metodo_listar()

        for obj in resultados:
            if obj.get_nome() == nome:
                return obj
        else: return None

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

  def generos_buscar(categoria):
    with open("Biblioteca/templates/traducao.json", mode="r", encoding="utf-8") as arquivo:
        traducoes = json.load(arquivo)
        if categoria != "":
            if categoria.upper() in traducoes:
                return traducoes[categoria.upper()]
            
            translator = Translator(to_lang="pt")
            novo_valor = translator.translate(categoria)
            traducoes[categoria.upper()] = novo_valor
            View.genero_inserir(traducoes[categoria.upper()])
            with open("Biblioteca/templates/traducao.json", mode="w", encoding="utf-8") as arquivo:
                json.dump(traducoes, arquivo, indent=4)
            return traducoes[categoria.upper()]
      
      

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

  def livro_inserir(titulo, autor, ano_publicacao, url_img, idGenero):
    if titulo == '' or autor == '' or ano_publicacao == '' or url_img == '' or idGenero == '': 
        raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    livro = Livro(0, titulo, autor, ano_publicacao, url_img, idGenero)    
    NLivro.Inserir(livro)

  def livro_listar():
    return NLivro.Listar()
  
  def livro_listar_id(id):
    return NLivro.Listar_Id(id)

  def livro_atualizar(id, titulo, autor, data_de_publicacao, url_img, idGenero):
    if titulo == '' or autor == '' or data_de_publicacao == '' or url_img == '' or idGenero == '': 
      raise ValueError("Campo obrigatório vazio")
    livro = Livro(id, titulo, autor, data_de_publicacao, url_img, idGenero)
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
        lista_livros = data.get("items", [])
        for item in lista_livros:

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

  def exibir_livros():

    lista_livros = View.livro_listar()
    if lista_livros != []:

      sublista = [lista_livros[k : k + 3] for k in range(0, len(lista_livros), 3)]

      for linha in sublista:
        cols = st.columns(3, gap="large")

        for j, livro in enumerate(linha):
          if lista_livros.index(livro) < len(lista_livros):
            with cols[j]:

              with stylable_container(
                key="container_with_border",
                css_styles="""
                    {
                        border: 1px solid rgba(255, 255, 255, 0.7);
                        border-radius: 0.5rem;
                        padding-top: 1em;
                        padding-bottom: 1em;
                        text-align: center;
                        margin-bottom: 1em;
                      
                    }
                    """,
              ):

                capa = livro.get_url_img()
                if capa is None:
                    st.write("Não foi possível achar a capa")
                else:
                    script = st.markdown(f"""
                        <style>
                        .image_container {{
                            display: flex;
                            justify-content: center;
                        }}
                        .image_container img {{
                            max-width: 100%;
                            height: auto;
                        }}
                        </style>
                        <div class="image_container">
                            <img src="{capa}">
                        </div>
                    """, unsafe_allow_html=True)
                
                titulo = livro.get_titulo()
                autor = livro.get_autor()
                ano_publicacao = livro.get_ano_publicacao()
                genero = View.genero_listar_id(livro.get_idGenero()).get_nome()

                st.markdown(f"#### {titulo}")
                st.markdown(f"###### {autor}")
                st.markdown(f"###### {ano_publicacao}")
                st.markdown(f"###### Gênero: {genero}")

