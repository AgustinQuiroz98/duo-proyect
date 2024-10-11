from config.db import connectToMySQL

class Usuario:
  def __init__(self, data):
    self.idUsuario = data["idUsuarios"]
    self.nombre = data["nombre"]
    self.email = data["email"]
    self.password = data["password"]
    self.linkedin = data["linkedin"]
    self.cargo = data["cargo"]
    self.imagenPerfil = data["imagenPerfil"]

  @classmethod
  def checkEmailExists(cls, email):
    query = "SELECT * FROM Usuarios WHERE email=%(email)s;"
    results = connectToMySQL("congressy_db").query_db(query, {"email": email})
    usuarios = []
    for usuario in results:
        usuarios.append(cls(usuario))
    return usuarios
  
  @classmethod
  def createUser(cls, data):
    query = """
    INSERT INTO Usuarios (
      `nombre`,
      `email`,
      `password`)
      VALUES
      (
        %(nombre)s,
        %(email)s,
        %(password)s
      );"""
    result = connectToMySQL("congressy_db").query_db(query, data)
    return result
  
  @classmethod
  def editUser(cls, data):
    query = """UPDATE Usuarios
    SET
      `nombre` = %(nombre)s,
      `email` = %(email)s,
      `linkedin` = %(linkedin)s,
      `cargo` = %(cargo)s,
      `imagenPerfil` = %(imagenPerfil)s
      WHERE `idUsuarios` = %(id)s;"""
    result = connectToMySQL("congressy_db").query_db(query, data)
    return result
  
  @classmethod
  def getUserById(cls, id):
    query = "SELECT * FROM Usuarios WHERE idUsuarios=%(id)s;"
    results = connectToMySQL("congressy_db").query_db(query, {"id": id})
    usuarios = []
    for usuario in results:
        usuarios.append(cls(usuario))
    return usuarios
    