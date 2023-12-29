import json
from streamlit import write
from models.modelo import Modelo

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

class NExemplar(Modelo):

    @classmethod
    def Abrir(cls):
        cls.objetos = []
    
        try:
            with open("Biblioteca/models/exemplares.json", mode="r") as arquivo:
                Exemplares_json = json.load(arquivo)
                for obj in Exemplares_json:
                    aux = Exemplar(obj["_Exemplar__id"], obj["_Exemplar__idLivro"], obj["_Exemplar__emprestado"])
                    cls.objetos.append(aux)
        except FileNotFoundError as f:
            write(f)

    @classmethod
    def Salvar(cls):
        with open("Biblioteca/models/exemplares.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default=vars, indent=4)
