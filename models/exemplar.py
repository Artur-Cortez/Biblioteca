import json

class Exemplar:
    def __init__(self, id, idLivro, idCliente, dataEmprestimo, dataDevolucao):
        self.__id, self.__idLivro = id, idLivro
 
    def set_id(self, id): self.__id = id
    def set_idLivro(self, idLivro): self.__idLivro = idLivro

    def get_id(self): return self.__id
    def get_idLivro(self): return self.__idLivro

    def __str__(self): return f"{self.__id} - {self.__idLivro}"