import json
from streamlit import write
from models.modelo import Modelo


class Cliente:
    def __init__(self, id, nome, email, matricula, senha, timeout):
        self.__id, self.__nome = id, nome
        self.__email, self.__senha = email, senha
        self.__matricula = matricula
        self.__timeout = timeout

    def set_id(self, id): self.__id = id
    def set_nome(self, nome): self.__nome = nome
    def set_email(self, email): self.__email = email
    def set_matricula(self, matricula): self.__matricula = matricula
    def set_senha(self, senha): self.__senha = senha
    def set_timeout(self, timeout): self.__timeout = timeout

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_email(self): return self.__email
    def get_matricula(self): return self.__matricula
    def get_senha(self): return self.__senha
    def get_timeout(self): return self.__timeout

    def __str__(self): return f"{self.__id} - {self.__nome} - {self.__matricula} - {self.__email} - {self.__timeout}"

class NCliente(Modelo):
    
    @classmethod
    def Abrir(cls):
        cls.objetos = []
    
        try:
            with open("Biblioteca/models/clientes.json", mode="r") as arquivo:
                Clientes_json = json.load(arquivo)
                for obj in Clientes_json:
                    aux = Cliente(obj["_Cliente__id"], obj["_Cliente__nome"], obj["_Cliente__email"], obj["_Cliente__matricula"], obj["_Cliente__senha"], obj["_Cliente__timeout"])
                    cls.objetos.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("Biblioteca/models/clientes.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars, indent=4)
