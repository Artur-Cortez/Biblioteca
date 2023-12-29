import json
from streamlit import write
from models.modelo import Modelo

class Genero:
    def __init__(self, id, nome):
        self.__id = id
        self.__nome = nome
    def set_id(self, id): self.__id = id
    def set_nome(self, nome): self.__nome = nome
    
    def get_id(self): return self.__id
    def get_nome(self): return self.__nome

class NGenero(Modelo):

    @classmethod
    def Abrir(cls):
        cls.objetos = []
    
        try:
            with open("Biblioteca/models/generos.json", mode="r", encoding="utf-8") as arquivo:
                generos_json = json.load(arquivo)
                for obj in generos_json:
                    aux = Genero(obj["_Genero__id"], obj["_Genero__nome"])
                    cls.objetos.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("Biblioteca/models/generos.json", mode="w", encoding="utf-8") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars, indent=4)
