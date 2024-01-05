import json
from models.genero import Genero, NGenero
from models.livro import Livro, NLivro
from models.exemplar import Exemplar, NExemplar
from models.emprestimo import Emprestimo, NEmprestimo
from models.cliente import Cliente, NCliente

import streamlit as st
import pandas as pd
import datetime
import random

from translate import Translator
from streamlit_extras.stylable_container import stylable_container


#http request
import requests


class View:

  def cliente_inserir(nome, email, matricula, senha):
    if nome == '' or email == '' or senha == '': 
        raise ValueError("Campo(s) obrigatório(s) vazio(s)")

    for i in View.cliente_listar():
        if i.get_email() == email:
            raise ValueError("Email já cadastrado")
    cliente = Cliente(0, nome, email, matricula, senha, 0)    
    NCliente.Inserir(cliente)

  def cliente_listar():
    return NCliente.Listar()
  
  def cliente_listar_id(id):
    return NCliente.Listar_Id(id)

  def cliente_atualizar(id, nome, email, senha, matricula, timeout):
    if nome == '' or email == '' or senha == '': 
      raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    cliente = Cliente(id, nome, email, matricula, senha, timeout)
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

  
  # Recebe uma categoria (atributo de um livro do google books) 
  # e cria um objeto Genero com esse mesmo nome  
  def generos_buscar(categoria):
    with open("Biblioteca/templates/traducao.json", mode="r", encoding="utf-8") as arquivo:
        
        # Arquivo json com chaves como a categoria em inglês
        # e com o valor correspondente em portugues
        # Fizemos algumas traduções manualmente, especialmente pq o tradutor fazia algumas estranhas,
        # Mas agora não compensa mais, apesar de ser possível
        traducoes = json.load(arquivo)

        if categoria != "":
            #Verifica se a string passada já existe no arquivo e retorna o valor em portugues correspondente
            if categoria.upper() in traducoes:
                return traducoes[categoria.upper()]
            
            translator = Translator(to_lang="pt")
            novo_valor = translator.translate(categoria)
            traducoes[categoria.upper()] = novo_valor
            View.genero_inserir(traducoes[categoria.upper()])
            with open("Biblioteca/templates/traducao.json", mode="w", encoding="utf-8") as arquivo:
                json.dump(traducoes, arquivo, indent=4)

            # Se teve que ser feita nova inserção, após salvar, retorne essa valor, agr salvo
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

  def exemplar_inserir(idlivro, emprestado):
    if idlivro == None: 
        raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    exemplar = Exemplar(0, idlivro, emprestado)    
    NExemplar.Inserir(exemplar)

  def exemplar_listar():
    return NExemplar.Listar()
  
  def exemplar_listar_id(id):
    return NExemplar.Listar_Id(id)

  def exemplar_atualizar(id, idLivro, emprestado):
    exemplar = Exemplar(id, idLivro, emprestado)
    NExemplar.Atualizar(exemplar)
    
  def exemplar_excluir(id):
    exemplar = Exemplar(id, "")
    NExemplar.Excluir(exemplar)

  def emprestimo_inserir(idExemplar, idUsuario, dataEmprestimo):
    if idExemplar == None or idUsuario == None or dataEmprestimo == None: 
      raise ValueError("Campo(s) obrigatório(s) vazio(s)")
    
    prazoDevolucao = dataEmprestimo +  datetime.timedelta(days=14)
    dataDevolucao = datetime.date(1900, 1, 1)   # Dummy value

    emprestimo = Emprestimo(0, idExemplar, idUsuario, dataEmprestimo, prazoDevolucao, dataDevolucao)   
    NEmprestimo.Inserir(emprestimo)

  def emprestimo_listar():
    return NEmprestimo.Listar()
  
  def emprestimo_listar_id(id):
    return NEmprestimo.Listar_Id(id)

  def emprestimo_atualizar(id, idExemplar, idUsuario, dataEmprestimo, prazoDevolucao, dataDevolucao):
    if id == '': 
      raise ValueError("Campo obrigatório vazio")
    emprestimo = Emprestimo(id, idExemplar, idUsuario, dataEmprestimo, prazoDevolucao, dataDevolucao)
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

  def emprestimos_do_usuario(idCliente):
    lista = []
    emprestimos = View.emprestimo_listar()
    for e in emprestimos:
       if e.get_idUsuario() == idCliente:
          lista.append(e)
    return lista

  #operacao do admin
  def devolucao_livro(idEmprestimo, idCliente):

      e = View.emprestimo_listar_id(idEmprestimo)
      idExemplar = e.get_idExemplar()
      dataEmprestimo = e.get_dataEmprestimo()
      prazoDevolucao = e.get_prazoDevolucao()
      c = View.cliente_listar_id(idCliente)
      hoje = datetime.date.today()
      
      
      timeout = (datetime.timedelta(days=hoje.day) - datetime.timedelta(days=prazoDevolucao.day)).days

      if timeout < 0: timeout = 0

      View.cliente_atualizar(idCliente, c.get_nome(), c.get_email(), c.get_senha(), c.get_matricula(), timeout)
      View.emprestimo_atualizar(idEmprestimo, idExemplar, idCliente, dataEmprestimo, prazoDevolucao, hoje)
      View.exemplar_atualizar(idExemplar, View.exemplar_listar_id(idExemplar).get_idLivro(), False)

  # Busca um objeto de algum modelo, exceto livro,
  # que possua um atributo nome igual a string passada na func
  def buscar_por_nome(nome, modelo):
    metodo_listar = getattr(View, f"{modelo}_listar", None)
    if metodo_listar and callable(metodo_listar):
        # Chama dinamicamente o método de listar
        resultados = metodo_listar()

        for obj in resultados:
            if obj.get_nome() == nome:
                return obj
        else: return None 

  def livro_buscar_por_titulo(titulo):
    metodo_listar = getattr(View, f"livro_listar", None)
    if metodo_listar and callable(metodo_listar):
        # Chama dinamicamente o método de listar
        resultados = metodo_listar()

        for obj in resultados:
            if obj.get_titulo() == titulo:
                return obj
        else: return None 
           
  #Consulta da api do google livros
  def livros_buscar(texto_busca) -> dict:

    def livro_extrair_autor(volume_info):
      # Se houver mais de um item nessa lista,
      # Ele vai transformar em uma string, 
      # Separando-os por vírgula
      autores = volume_info.get("authors", [])
      return ", ".join(autores) if autores else "N/A"

    def livro_extrair_capa(volume_info):
        image_links = volume_info.get("imageLinks", {})
        return image_links.get("thumbnail") if image_links else None
    

    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": texto_busca}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        livros_encontrados = []

        data = response.json()
        lista_livros = data.get("items", [])
        for item in lista_livros:

          volume_info = item.get("volumeInfo", {})
          titulo = volume_info.get("title", "N/A")
          autor = livro_extrair_autor(volume_info)
          cover_image_url = livro_extrair_capa(volume_info)
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

        return livros_encontrados

    else:
        st.write(f"Erro ao fazer a solicitação. Código de status: {response.status_code}")
        return None

  #Usada em manterLivrosUI e pesquisarLivrosUI
  def exibir_livros(lista_livros) -> None:
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

    #Usada em pesquisarlivrosUI
  
  #Usadas em pesquisarlivrosUI:
  def exemplares_disponiveis(idLivro) -> int:
     cont = 0
     for exemplar in View.exemplar_listar():
        if exemplar.get_idLivro() == idLivro and exemplar.get_emprestado() != False:
          cont += 1
     return cont

  #Usada somente em manterEmprestimoUI e fazerEmprestimoUI
  def exemplares_disponiveis_por_titulo(titulo) -> list:
     idLivro = View.livro_buscar_por_titulo(titulo).get_id()
     lista = []

     for exemplar in View.exemplar_listar():
        if exemplar.get_emprestado() == False and exemplar.get_idLivro() == idLivro:
           lista.append(exemplar)
     return lista
     
  #Usada em manterEmprestimoUI
  def insercao_emprestimo(listaExemplares, dataEmprestimo):
     if len(listaExemplares) == 0:
        st.error("Não há mais exemplares disponíveis desse livro. Sorry")
        return
     e = random.choice(listaExemplares)
     id = e.get_id()
     View.emprestimo_inserir(id, st.session_state["cliente_id"], dataEmprestimo)
     View.exemplar_atualizar(id, e.get_idLivro(), emprestado=True)

  # 3 Funções referentes as opções que o user pode escolher
  def pesquisar_por_titulo(nome):
     metodo_listar = getattr(View, "livro_listar", None)
     if metodo_listar and callable(metodo_listar):
          # Chama dinamicamente o método de listar
          resultados = metodo_listar()

          for obj in resultados:
              if obj.get_titulo() == nome:
                  return obj
          else: return None

  def pesquisar_por_autor(autor) -> list:
     return [livro for livro in View.livro_listar() if livro.get_autor().lower() == autor.lower()]
  
  def pesquisar_por_genero(genero) -> list:
     return [livro for livro in View.livro_listar() 
             if View.genero_listar_id(livro.get_idGenero()).get_nome().lower()]

# FUNÇÕES PARA SEARCHBOXES

  ## Usado em manterEmprestimoUI e fazerEmprestimoUI
  def exemplar_searchbox_titulo(termo_de_busca: str) -> list:
    exemplares = View.exemplar_listar()
    lista = []
    for exemplar in exemplares:
        titulo = View.livro_listar_id(exemplar.get_idLivro()).get_titulo()

        if ( exemplar.get_emprestado() == False and termo_de_busca.lower() in titulo.lower()
            and titulo not in lista ): 
          lista.append(titulo)     
        
    return lista
  
  ## Usado em pesquisarlivrosUI
  def livro_searchbox_titulo(termo_de_busca: str) -> list:
    livros = View.livro_listar()
    return [livro.get_titulo() for livro in livros if termo_de_busca.lower() in livro.get_titulo().lower()]

  ## Usado em pesquisarlivrosUI. 
  ## Assim, já se sabe logo se na biblioteca tem livro de tal autor ou não
  def livro_searchbox_autor(termo_de_busca: str) -> list:
    livros = View.livro_listar()
    lista = []

    for livro in livros:            
      if termo_de_busca.lower() in livro.get_autor().lower() and livro.get_autor() not in lista:
                  
         lista.append(livro.get_autor())
    return lista
  
  ## FUNDAMENTAL (devido a quantia de gêneros). Usada em pesquisarlivrosUI
  def livro_searchbox_genero(termo_de_busca: str) -> list:
    generos = View.genero_listar()
    return [genero.get_nome() for genero in generos if termo_de_busca.lower() in genero.get_nome().lower()]