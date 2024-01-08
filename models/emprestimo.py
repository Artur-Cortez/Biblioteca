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
        return {
            "id": self.__id,
            "idExemplar": self.__idExemplar,
            "idUsuario": self.__idUsuario,
            "dataEmprestimo": datetime.datetime.strftime(self.__dataEmprestimo,  "%d/%m/%Y"),
            "prazoDevolucao": datetime.datetime.strftime(self.__prazoDevolucao,  "%d/%m/%Y"),
            "dataDevolucao": datetime.datetime.strftime(self.__dataDevolucao,  "%d/%m/%Y"),
        }

    def __str__(self): return f"""ID: {self.__id} _||_ ID.Ex: {self.__idExemplar} _||_ idUsu{self.__idUsuario} _||_ D.Empre: {datetime.datetime.strftime(self.__dataEmprestimo,  '%d/%m/%Y')}  _||_  Prazo_Devo: {datetime.datetime.strftime(self.__prazoDevolucao,  '%d/%m/%Y')}  _||_  Data Devol: {'A ser devolvido' if self.__dataDevolucao == datetime.datetime(1900, 1, 1) else datetime.datetime.strftime(self.__dataDevolucao,  '%d/%m/%Y')}"""

    

class NEmprestimo(Modelo):


    @classmethod
    def Abrir(cls):
        cls.objetos = []
    
        try:
            with open("Biblioteca/models/emprestimos.json", mode="r") as arquivo:
                Emprestimos_json = json.load(arquivo)
                for obj in Emprestimos_json:
                    aux = Emprestimo(obj["id"], 
                    obj["idExemplar"], 
                    obj["idUsuario"], 
                    datetime.datetime.strptime(obj["dataEmprestimo"], "%d/%m/%Y"), 
                    datetime.datetime.strptime(obj["prazoDevolucao"], "%d/%m/%Y"),  
                    datetime.datetime.strptime(obj["dataDevolucao"], "%d/%m/%Y") )
                    cls.objetos.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("Biblioteca/models/emprestimos.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=Emprestimo.to_json, indent=4)
