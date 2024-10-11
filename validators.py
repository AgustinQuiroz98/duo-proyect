from models.usuario import Usuario
from utils import check_email, transformDate
from datetime import datetime

def validate_user_data(form):
  errors = []

  if (len(form["nombre"]) < 2):
    errors.append("El largo del nombre debe ser mayor a 2 caracteres")
      
  if not check_email(form["email"]):
    errors.append("El email no es un email válido")
      
  if form["password"] != form["password2"]:
    errors.append("Las contraseñas no coinciden")
      
  users = Usuario.checkEmailExists(form["email"])
  if len(users) > 0:
    errors.append("Usuario con email ya creado")
      
  return errors

def validate_congress_data(form):
  errors = []
  
  if (len(form["nombre"]) < 3):
    errors.append("El largo del nombre de tarea debe ser mayor a 2 caracteres")
  
  if (transformDate(form["fecha"]) < datetime.now().date()):
    errors.append(f'La fecha ingresada es invalida {transformDate(form["fecha"])}' )

  if ( len(form["hora_inicio"]) < 3):
    errors.append("Debe ingresar una Hora de inicio")

  if ( len(form["hora_termino"]) < 3):
    errors.append("Debe ingresar una Hora de termino")

  if(len(form["linkUbicacion"]) < 3):
    errors.append("Debe ingresar un link de Ubicacion")

  if ( len(form["tipo"]) < 3):
    errors.append("Debe ingresar un tipo de conferencia")
  
  if(form["tipo"] == 'private' and len(form["linkInscripcion"]) < 3):
    errors.append("Debe ingresar un link de inscripcion en el caso de que sea conferencia privada")
      
  return errors