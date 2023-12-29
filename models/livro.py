import json
from streamlit import write
from models.modelo import Modelo

class Livro:
    def __init__(self, id, titulo, autor, ano_publicacao, url_img, idGenero):
        self.__id, self.__idGenero = id, idGenero
        self.__titulo, self.__autor, self.__ano_publicacao = titulo, autor, ano_publicacao
        self.__url_img = url_img

    def set_id(self, id): self.__id = id
    def set_idGenero(self, idGenero): self.__idGenero = idGenero
    def set_titulo(self, titulo): self.__titulo = titulo
    def set_autor(self, autor): self.__autor = autor
    def set_ano_publicacao(self, ano_publicacao): self.__ano_publicacao = ano_publicacao
    def set_url_img(self, url_img): self.__url_img = url_img


    def get_id(self): return self.__id
    def get_idGenero(self): return self.__idGenero
    def get_titulo(self): return self.__titulo
    def get_autor(self): return self.__autor
    def get_ano_publicacao(self): return self.__ano_publicacao
    def get_url_img(self): return self.__url_img
  

    def __str__(self): return f"""
    Id: {self.__id} | Id do gênero: {self.__idGenero} | Titulo: {self.__titulo} |
    Autor: {self.__autor} | Data de lançamento: {self.__ano_publicacao}
    
    """

class NLivro(Modelo):

    @classmethod
    def Abrir(cls):
        cls.objetos = []

        try:
            with open("Biblioteca/models/livros.json", mode="r") as arquivo:
                livros_json = json.load(arquivo)
                for obj in livros_json:
                    aux = Livro(obj["_Livro__id"], obj["_Livro__titulo"], obj["_Livro__autor"], obj["_Livro__ano_publicacao"], obj["_Livro__url_img"], obj["_Livro__idGenero"])
                    cls.objetos.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("Biblioteca/models/livros.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars, indent=4)
