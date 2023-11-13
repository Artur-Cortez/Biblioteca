import json
from streamlit import write

class Genero:
    def __init__(self, id, nome):
        self.__id = id
        self.__nome = nome
    def set_id(self, id): self.__id = id
    def set_nome(self, nome): self.__nome = nome
    
    def get_id(self): return self.__id
    def get_nome(self): return self.__nome

class NGenero:

    __generos = []

    @classmethod
    def Inserir(cls, obj):
        cls.Abrir()
        id = 0
        for g in cls.__generos:
            if g.get_id() > id: id = g.get_id()
        obj.set_id(id + 1)
        cls.__generos.append(obj)
        cls.Salvar()

    @classmethod
    def Listar(cls):
        cls.Abrir()
        return cls.__generos

    @classmethod
    def Listar_Id(cls, id):
        cls.Abrir()
        for g in cls.__generos:
            if g.get_id() == id: return g
        return None

    @classmethod
    def Atualizar(cls, obj):
        cls.Abrir()
        aux = cls.Listar_Id(obj.get_id())
        if aux is not None:
            aux.set_nome(obj.get_nome())
            cls.Salvar()

    @classmethod
    def Excluir(cls, obj):
        cls.Abrir()
        aux = cls.Listar_Id(obj.get_id())
        if aux is not None:
            cls.__generos.remove(aux)
            cls.Salvar()

    @classmethod
    def Abrir(cls):
        cls.__generos = []
    
        try:
            with open("tlgd/models/generos.json", mode="r") as arquivo:
                generos_json = json.load(arquivo)
                for obj in generos_json:
                    aux = Genero(obj["_Genero__id"], obj["_Genero__nome"])
                    cls.__generos.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("tlgd/models/generos.json", mode="w") as arquivo:
            json.dump(cls.__generos, arquivo, default=vars, indent=4)
