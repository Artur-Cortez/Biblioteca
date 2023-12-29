import json
from streamlit import write
import datetime
from models.modelo import Modelo

class Emprestimo:
    def __init__(self, id, idExemplar, idUsuario, dataEmprestimo, prazoDevolucao, dataDevolucao):
        self.__id, self.__idExemplar = id, idExemplar
        self.__idUsuario = idUsuario
        self.__dataEmprestimo = dataEmprestimo
        self.__prazoDevolucao = prazoDevolucao
        self.__dataDevolucao = dataDevolucao

    def set_id(self, id): self.__id = id
    def set_idExemplar(self, idExemplar): self.__idExemplar = idExemplar
    def set_idUsuario(self, idUsuario): self.__idUsuario = idUsuario
    def set_dataEmprestimo(self, dataEmprestimo): self.__dataEmprestimo = dataEmprestimo
    def set_prazoDevolucao(self, prazoDevolucao): self.__prazoDevolucao = prazoDevolucao
    def set_dataDevolucao(self, dataDevolucao): self.__dataDevolucao = dataDevolucao

    def get_id(self): return self.__id
    def get_idExemplar(self): return self.__idExemplar
    def get_idUsuario(self): return self.__idUsuario
    def get_dataEmprestimo(self): return self.__dataEmprestimo
    def get_prazoDevolucao(self): return self.__prazoDevolucao
    def get_dataDevolucao(self): return self.__dataDevolucao

    def to_json(self):
        pass

    def __str__(self): return f"{self.__id} - {self.__idExemplar} - {self.__idUsuario} - {self.__dataEmprestimo} - {self.__prazoDevolucao} - {self.__dataDevolucao}"

    

class NEmprestimo(Modelo):


    @classmethod
    def Abrir(cls):
        cls.objetos = []
    
        try:
            with open("Biblioteca/models/emprestimos.json", mode="r") as arquivo:
                Emprestimos_json = json.load(arquivo)
                for obj in Emprestimos_json:
                    aux = Emprestimo(obj["_Emprestimo__id"], 
                    obj["_Emprestimo__idExemplar"], 
                    obj["_Emprestimo__idUsuario"], 
                    datetime.datetime.strptime(obj["_Emprestimo__dataEmprestimo"], "%d/%m/%Y"), 
                    datetime.datetime.strptime(obj["_Emprestimo__prazoDevolucao"], "%d/%m/%Y"),  
                    datetime.datetime.strptime(obj["_Emprestimo__dataDevolucao"], "%d/%m/%Y") )
                    cls.objetos.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("Biblioteca/models/emprestimos.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars, indent=4)
