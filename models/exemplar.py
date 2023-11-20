import json
from streamlit import write

class Exemplar:
    def __init__(self, id, idExemplar, idCliente, dataEmprestimo, dataDevolucao):
        self.__id, self.__idExemplar = id, idExemplar
 
    def set_id(self, id): self.__id = id
    def set_idExemplar(self, idExemplar): self.__idExemplar = idExemplar

    def get_id(self): return self.__id
    def get_idExemplar(self): return self.__idExemplar

    def __str__(self): return f"{self.__id} - {self.__idExemplar}"

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
            with open("/models/Exemplares.json", mode="r") as arquivo:
                Exemplares_json = json.load(arquivo)
                for obj in Exemplares_json:
                    aux = Exemplar(obj["_Exemplar__id"], obj["_Exemplar__idGenero"], obj["_Exemplar__nome"], obj["_Exemplar__autor"], obj["_Exemplar__data"])
                    cls.__Exemplares.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("/models/Exemplares.json", mode="w") as arquivo:
            json.dump(cls.__Exemplares, arquivo, default=vars, indent=4)
