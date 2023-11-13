import json

class Exemplar:
    def __init__(self, id, idLivro, idCliente, dataEmprestimo, dataDevolucao):
        self.__id, self.__idLivro = id, idLivro
        self.__idCliente = idCliente
        self.__dataEmprestimo = dataEmprestimo
        self.__dataDevolucao = dataDevolucao

    def set_id(self, id): self.__id = id
    def set_idCliente(self, idCLiente): self.__idCliente = idCLiente
    def set_idLivro(self, idLivro): self.__idLivro = idLivro
    def set_dataEmprestimo(self, dataEmprestimo): self.__dataEmprestimo = dataEmprestimo
    def set_dataDevolucao(self, dataDevolucao): self.__dataDevolucao =  dataDevolucao

    def get_id(self): return self.__id
    def get_idCliente(self): return self.__idCliente
    def get_idLivro(self): return self.__idLivro
    def get_dataEmprestimo(self): return self.__dataEmprestimo
    def get_dataDevolucao(self): return self.__dataDevolucao