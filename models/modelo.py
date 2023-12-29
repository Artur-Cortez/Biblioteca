from abc import ABC, abstractclassmethod

class Modelo(ABC):
  objetos = []

  @classmethod
  def Inserir(cls, obj):
    cls.Abrir()
    id = 0
    for aux in cls.objetos:
      if aux._id > id: id = aux._id
    obj._id = id + 1
    cls.objetos.append(obj)
    cls.Salvar()

  @classmethod
  def Listar(cls):
    cls.Abrir()
    return cls.objetos

  @classmethod
  def Listar_Id(cls, id):
    cls.Abrir()
    for obj in cls.objetos:
      if obj.get_id() == id: return obj
    return None

  @classmethod
  def Atualizar(cls, obj):
    cls.Abrir()
    aux = cls.Listar_Id(obj._id)
    cls.objetos.remove(aux)
    cls.objetos.append(obj)
    cls.Salvar()

  @classmethod
  def Excluir(cls, obj):
    cls.Abrir()
    aux = cls.Listar_Id(obj._id)
    cls.objetos.remove(aux)
    cls.Salvar()

  @abstractclassmethod
  def Abrir(cls):
    pass

  @abstractclassmethod
  def Salvar(cls):
    pass