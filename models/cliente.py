import json
from streamlit import write
from models.modelo import Modelo
import datetime

class Cliente:
    def __init__(self, id: int, nome: str, email: str,
                  matricula: str, senha: str, 
                  dias_timeout: int, timeout_inicio: datetime.date):

        self.__id, self.__nome, self.__email = id, nome, email
        self.__matricula, self.__senha = matricula, senha
        self.__dias_timeout = dias_timeout
        self.__timeout_inicio = timeout_inicio

    def set_id(self, id): self.__id = id
    def set_nome(self, nome): self.__nome = nome
    def set_email(self, email): self.__email = email
    def set_matricula(self, matricula): self.__matricula = matricula
    def set_senha(self, senha): self.__senha = senha
    def set_dias_timeout(self, dias_timeout): self.__dias_timeout = dias_timeout
    def set_timeout_inicio(self, timeout_inicio): self.__timeout_inicio = timeout_inicio

    def get_id(self) -> int: 
        return self.__id
    
    def get_nome(self) -> str: 
        return self.__nome
    
    def get_email(self) -> str: 
        return self.__email
    
    def get_matricula(self) -> str: 
        return self.__matricula
    
    def get_senha(self) -> str: 
        return self.__senha
    
    def get_dias_timeout(self) -> int: 
        return self.__dias_timeout
    
    def get_timeout_inicio(self) -> datetime.date: 
        return self.__timeout_inicio
    

    def __str__(self): 
        return f"{self.__id} - {self.__nome} - {self.__matricula} - {self.__email}"


    def to_json(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "email": self.__email,
            "matricula": self.__matricula,
            "senha": self.__senha,
            "dias_timeout": self.__dias_timeout,
            "timeout_inicio": datetime.datetime.strftime(self.__timeout_inicio, "%d/%m/%Y")
        }

class NCliente(Modelo):
    
    @classmethod
    def Abrir(cls):
        cls.objetos = []
    
        try:
            with open("Biblioteca/models/clientes.json", mode="r") as arquivo:
                Clientes_json = json.load(arquivo)
                for obj in Clientes_json:
                    aux = Cliente(obj["id"], obj["nome"], obj["email"], obj["matricula"], obj["senha"], obj["dias_timeout"], datetime.datetime.strptime(obj["timeout_inicio"], "%d/%m/%Y"))
                    cls.objetos.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("Biblioteca/models/clientes.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=Cliente.to_json, indent=4)
