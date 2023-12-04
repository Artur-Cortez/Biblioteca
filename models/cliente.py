import json
from streamlit import write

class Cliente:
    def __init__(self, id, nome, email, senha):
        self.__id, self.__nome = id, nome
        self.__email, self.__senha = email, senha

    def set_id(self, id): self.__id = id
    def set_nome(self, nome): self.__nome = nome
    def set_email(self, email): self.__email = email
    def set_senha(self, senha): self.__senha = senha

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_email(self): return self.__email
    def get_senha(self): return self.__senha

    def __str__(self): return f"{self.__id} - {self.__nome} - {self.__email}"

class NCliente:
    
    __clientes = []

    @classmethod
    def Inserir(cls, obj):
        cls.Abrir()
        id = 0
        for l in cls.__clientes:
            if l.get_id() > id: id = l.get_id()
        obj.set_id(id + 1)
        cls.__clientes.append(obj)
        cls.Salvar()

    @classmethod
    def Listar(cls):
        cls.Abrir()
        return cls.__clientes

    @classmethod
    def Listar_Id(cls, id):
        cls.Abrir()
        for l in cls.__clientes:
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
            cls.__clientes.remove(aux)
            cls.Salvar()

    @classmethod
    def Abrir(cls):
        cls.__clientes = []
    
        try:
            with open("/models/clientes.json", mode="r") as arquivo:
                Clientes_json = json.load(arquivo)
                for obj in Clientes_json:
                    aux = Cliente(obj["_Cliente__id"], obj["_Cliente__idGenero"], obj["_Cliente__nome"], obj["_Cliente__autor"], obj["_Cliente__data"])
                    cls.__clientes.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("/models/clientes.json", mode="w") as arquivo:
            json.dump(cls.__clientes, arquivo, default=vars, indent=4)
