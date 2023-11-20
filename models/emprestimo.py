import json

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
    def set_dataDevolucao(self, dataDevolucao): self.__dataDevolucao =  dataDevolucao

    def get_id(self): return self.__id
    def get_idExemplar(self): return self.__idExemplar
    def get_idUsuario(self): return self.__idUsuario
    def get_dataEmprestimo(self): return self.__dataEmprestimo
    def get_dataDevolucao(self): return self.__dataDevolucao

    def __str__(self): return f"{self.__id} - {self.__idExemplar} - {self.__idUsuario} - {self.__dataEmprestimo} - {self.__dataDevolucao}"