import json
from streamlit import write
import datetime

class Emprestimo:
    def __init__(self, id, idExemplar, idUsuario, dataEmprestimo, dataDevolucao):
        self.__id, self.__idExemplar = id, idExemplar
        self.__idUsuario = idUsuario
        self.__dataEmprestimo = dataEmprestimo
        self.__dataDevolucao = dataDevolucao

    def set_id(self, id): self.__id = id
    def set_idExemplar(self, idExemplar): self.__idExemplar = idExemplar
    def set_idUsuario(self, idUsuario): self.__idUsuario = idUsuario
    def set_dataEmprestimo(self, dataEmprestimo): self.__dataEmprestimo = dataEmprestimo
    def set_dataDevolucao(self): 
        self.__dataDevolucao = self.__dataEmprestimo + datetime.timedelta(days=14)

    def get_id(self): return self.__id
    def get_idExemplar(self): return self.__idExemplar
    def get_idUsuario(self): return self.__idUsuario
    def get_dataEmprestimo(self): return self.__dataEmprestimo
    def get_dataDevolucao(self): return self.__dataDevolucao

    def __str__(self): return f"{self.__id} - {self.__idExemplar} - {self.__idUsuario} - {self.__dataEmprestimo} - {self.__dataDevolucao}"

class NEmprestimo:
    
    __emprestimos = []

    @classmethod
    def Inserir(cls, obj):
        cls.Abrir()
        id = 0
        for l in cls.__emprestimos:
            if l.get_id() > id: id = l.get_id()
        obj.set_id(id + 1)
        cls.__emprestimos.append(obj)
        cls.Salvar()

    @classmethod
    def Listar(cls):
        cls.Abrir()
        return cls.__emprestimos

    @classmethod
    def Listar_Id(cls, id):
        cls.Abrir()
        for l in cls.__emprestimos:
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
            cls.__emprestimos.remove(aux)
            cls.Salvar()

    @classmethod
    def Abrir(cls):
        cls.__emprestimos = []
    
        try:
            with open("Biblioteca/models/emprestimos.json", mode="r") as arquivo:
                Emprestimos_json = json.load(arquivo)
                for obj in Emprestimos_json:
                    aux = Emprestimo(obj["_Emprestimo__id"], obj["_Emprestimo__idExemplar"], obj["_Emprestimo__idUsuario"], datetime.datetime.strptime(obj["_Emprestimo__dataEmprestimo"], "%d/%m/%Y"),  datetime.datetime.strptime(obj["_Emprestimo__dataDevolucao"], "%d/%m/%Y") )
                    cls.__emprestimos.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("Biblioteca/models/emprestimos.json", mode="w") as arquivo:
            json.dump(cls.__emprestimos, arquivo, default=vars, indent=4)
