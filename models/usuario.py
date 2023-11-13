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
