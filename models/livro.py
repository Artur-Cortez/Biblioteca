import json
from streamlit import write
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

class NLivro:

    __livros = []

    @classmethod
    def Inserir(cls, obj):
        cls.Abrir()
        id = 0
        for l in cls.__livros:
            if l.get_id() > id: id = l.get_id()
        obj.set_id(id + 1)
        cls.__livros.append(obj)
        cls.Salvar()

    @classmethod
    def Listar(cls):
        cls.Abrir()
        return cls.__livros

    @classmethod
    def Listar_Id(cls, id):
        cls.Abrir()
        for l in cls.__livros:
            if l.get_id() == id: return l
        return None

    @classmethod
    def Atualizar(cls, obj):
        cls.Abrir()
        aux = cls.Listar_Id(obj.get_id())
        if aux is not None:
            aux.set_idGenero(obj.get_idGenero())
            aux.set_titulo(obj.get_titulo())
            aux.set_autor(obj.get_autor())
            aux.set_ano_publicacao(obj.get_ano_publicacao())
            cls.Salvar()

    @classmethod
    def Excluir(cls, obj):
        cls.Abrir()
        aux = cls.Listar_Id(obj.get_id())
        if aux is not None:
            cls.__livros.remove(aux)
            cls.Salvar()

    @classmethod
    def Abrir(cls):
        cls.__livros = []

        try:
            with open("Biblioteca/models/livros.json", mode="r") as arquivo:
                livros_json = json.load(arquivo)
                for obj in livros_json:
                    aux = Livro(obj["_Livro__id"], obj["_Livro__titulo"], obj["_Livro__autor"], obj["_Livro__ano_publicacao"], obj["_Livro__url_img"], obj["_Livro__idGenero"])
                    cls.__livros.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("Biblioteca/models/livros.json", mode="w") as arquivo:
            json.dump(cls.__livros, arquivo, default=vars, indent=4)
