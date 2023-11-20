import json
from streamlit import write
class Livro:
    def __init__(self, id, idGenero, nome, autor, data):
        self.__id, self.__idGenero = id, idGenero
        self.__nome, self.__autor, self.__data = nome, autor, data

    def set_id(self, id): self.__id = id
    def set_idGenero(self, idGenero): self.__idGenero = idGenero
    def set_nome(self, nome): self.__nome = nome
    def set_autor(self, autor): self.__autor = autor
    def set_data(self, data): self.__data = data
    
    def get_id(self): return self.__id
    def get_idGenero(self): return self.__idGenero
    def get_nome(self): return self.__nome
    def get_autor(self): return self.__autor
    def get_data(self): return self.__data

    def __str__(self): return f"Id: {self.__id} - Id do gênero: {self.__idGenero} - Nome: {self.__nome} - Autor: {self.__autor} - Data de lançamento: {self.__data}"

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
            aux.set_nome(obj.get_nome())
            aux.set_autor(obj.get_autor())
            aux.set_data(obj.get_data())
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
            with open("/models/livros.json", mode="r") as arquivo:
                livros_json = json.load(arquivo)
                for obj in livros_json:
                    aux = Livro(obj["_Livro__id"], obj["_Livro__idGenero"], obj["_Livro__nome"], obj["_Livro__autor"], obj["_Livro__data"])
                    cls.__livros.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("/models/livros.json", mode="w") as arquivo:
            json.dump(cls.__livros, arquivo, default=vars, indent=4)
