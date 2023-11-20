import json
from streamlit import write

class Usuario:
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

class NUsuario:
    
    __usuarios = []

    @classmethod
    def Inserir(cls, obj):
        cls.Abrir()
        id = 0
        for l in cls.__usuarios:
            if l.get_id() > id: id = l.get_id()
        obj.set_id(id + 1)
        cls.__usuarios.append(obj)
        cls.Salvar()

    @classmethod
    def Listar(cls):
        cls.Abrir()
        return cls.__usuarios

    @classmethod
    def Listar_Id(cls, id):
        cls.Abrir()
        for l in cls.__usuarios:
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
            cls.__usuarios.remove(aux)
            cls.Salvar()

    @classmethod
    def Abrir(cls):
        cls.__usuarios = []
    
        try:
            with open("/models/Usuarios.json", mode="r") as arquivo:
                Usuarios_json = json.load(arquivo)
                for obj in Usuarios_json:
                    aux = Usuario(obj["_Usuario__id"], obj["_Usuario__idGenero"], obj["_Usuario__nome"], obj["_Usuario__autor"], obj["_Usuario__data"])
                    cls.__usuarios.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("/models/Usuarios.json", mode="w") as arquivo:
            json.dump(cls.__usuarios, arquivo, default=vars, indent=4)
