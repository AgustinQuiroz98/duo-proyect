from config.db import connectToMySQL
# from models.usuario import Usuario
import json

class Conferencia:
  def __init__(self, data):
    self.idConferencias = data["idConferencias"]
    self.imagen = data["imagen"]
    self.nombre = data["nombre"]
    self.fecha = data["fecha"]
    self.hora_inicio = data["hora_inicio"]
    self.hora_termino = data["hora_termino"]
    self.tipo = data["tipo"]
    self.linkInscripcion = data["linkInscripcion"]
    self.linkUbicacion = data["linkUbicacion"]
    self.speaker = data["speaker"]
    self.contenido = data["contenido"]
    self.usuario = data["user_id"]


  @classmethod
  def getAllCurrentCongress(cls):
    query = "SELECT * FROM Conferencias WHERE fecha >= CURRENT_DATE;"
    results = connectToMySQL("congressy_db").query_db(query)
    conferencias = []
    for result in results:
      conferencia = cls(result)
      # data = result
      # data["idUsuarios"] = data["user_id"]

      # usuario = Usuario(data)
      
      # conferencia.usuario = usuario

      conferencias.append(conferencia)
    return conferencias
  
  @classmethod
  def getCongressForCongressView(cls):
    query = """
    SELECT * FROM Conferencias WHERE fecha >= CURRENT_DATE ORDER BY fecha DESC LIMIT 4; 
    """
    results = connectToMySQL("congressy_db").query_db(query)
    conferencias = []
    for result in results:
      conferencia = cls(result)
      conferencias.append(conferencia)
    return conferencias
  
  @classmethod
  def getCongressForMyCongressView(cls, id):
    query = """
    SELECT * FROM Conferencias WHERE fecha >= CURRENT_DATE AND user_id = %(id)s ORDER BY fecha DESC LIMIT 4; 
    """
    results = connectToMySQL("congressy_db").query_db(query, {"id" : id})
    conferencias = []
    for result in results:
      conferencia = cls(result)
      conferencias.append(conferencia)
    return conferencias
  
  @classmethod
  def createCongress(cls, data):
    query = """INSERT INTO Conferencias
      (`imagen`,
      `nombre`,
      `fecha`,
      `hora_inicio`,
      `hora_termino`,
      `tipo`,
      `linkInscripcion`,
      `linkUbicacion`,
      `speaker`,
      `contenido`,
      `user_id`)
      VALUES
      (%(imagen)s,
      %(nombre)s,
      %(fecha)s,
      %(hora_inicio)s,
      %(hora_termino)s,
      %(tipo)s,
      %(linkInscripcion)s,
      %(linkUbicacion)s,
      %(speaker)s,
      %(contenido)s,
      %(user_id)s);
    """
    result = connectToMySQL("congressy_db").query_db(query, data)
    return result
  
  @classmethod
  def getCongressById(cls, id):
    query = "SELECT * FROM Conferencias WHERE idConferencias = %(id)s;"
    results = connectToMySQL("congressy_db").query_db(query, {"id":id})
    conferencias = []
    for result in results:
      conferencia = cls(result)

      conferencias.append(conferencia)
    return conferencias