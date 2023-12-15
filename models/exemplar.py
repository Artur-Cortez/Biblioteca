import json
from streamlit import write

class Exemplar:
    def __init__(self, id, idLivro, emprestado):
        self.__id, self.__idLivro = id, idLivro
        self.__emprestado = False
 
    def set_id(self, id): self.__id = id
    def set_idLivro(self, idLivro): self.__idLivro = idLivro
    def set_emprestado(self, emprestado): self.__emprestado = emprestado

    def get_id(self): return self.__id
    def get_idLivro(self): return self.__idLivro
    def get_emprestado(self): return self.__emprestado

    def __str__(self): return f"{self.__id} - {self.__idLivro} - {self.__emprestado}"

class NExemplar:
    
    __Exemplares = []

    @classmethod
    def Inserir(cls, obj):
        cls.Abrir()
        id = 0
        for l in cls.__Exemplares:
            if l.get_id() > id: id = l.get_id()
        obj.set_id(id + 1)
        cls.__Exemplares.append(obj)
        cls.Salvar()

    @classmethod
    def Listar(cls):
        cls.Abrir()
        return cls.__Exemplares

    @classmethod
    def Listar_Id(cls, id):
        cls.Abrir()
        for l in cls.__Exemplares:
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
            cls.__Exemplares.remove(aux)
            cls.Salvar()

    @classmethod
    def Abrir(cls):
        cls.__Exemplares = []
    
        try:
            with open("Biblioteca/models/exemplares.json", mode="r") as arquivo:
                Exemplares_json = json.load(arquivo)
                for obj in Exemplares_json:
                    aux = Exemplar(obj["_Exemplar__id"], obj["_Exemplar__idLivro"], obj["_Exemplar__emprestado"])
                    cls.__Exemplares.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("Biblioteca/models/exemplares.json", mode="w") as arquivo:
            json.dump(cls.__Exemplares, arquivo, default=vars, indent=4)
