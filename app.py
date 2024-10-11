from flask import Flask, render_template, redirect, request, session, send_from_directory, jsonify # type: ignore
from flask_bcrypt import Bcrypt # type: ignore

from validators import validate_user_data, validate_congress_data
from utils import transformDate

from models.usuario import Usuario
from models.conferencia import Conferencia

import os
import json

app = Flask(__name__)
app.secret_key = "H4N S0L0"

bcrypt = Bcrypt(app)


UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
  os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def loginForm():
  return render_template("login.html")

@app.route("/login/", methods=["POST"])
def loginUser():
  email = request.form.get("email")
  password = request.form.get("password")
  
  errors = []
  
  users = Usuario.checkEmailExists(email)
  
  if (len(users) == 0):
    errors.append("No existe un usuario con esta combinación de email y password")
    return render_template("login.html", login_errors=errors)
  
  user = users[0]
  
  compare = bcrypt.check_password_hash(user.password, password)
  if (not compare):
    errors.append("No existe un usuario con esta combinación de email y password")
      
  if len(errors) > 0:
    return render_template("login.html", login_errors=errors)
  
  session["id"] = user.idUsuario
  session["nombre"] = f"{user.nombre}"
  session["imagenPerfil"] = user.imagenPerfil
  
  return redirect("/congress/")

@app.route("/register/", methods=["GET"])
def registerForm():
  return render_template("register.html")

@app.route("/register/", methods=["POST"])
def registerUser():
  form = request.form.to_dict()
  errors = validate_user_data(form)

  if len(errors) > 0:
    return render_template("register.html", register_errors=errors)
  
  form["password"] =  bcrypt.generate_password_hash(form["password"]) 
  Usuario.createUser(form)

  message = ["usuario creado con éxito !"]

  return render_template("login.html", status=message)

@app.route("/congress/", methods=["GET"])
def congressView():
  if not session:
    return redirect("/")
  
  user_id = session["id"]
  conferencias = Conferencia.getCongressForCongressView(user_id)

  return render_template("congress.html", conferencias=conferencias)

@app.route("/create/", methods=["GET"])
def createCongressView():
  if not session:
    return redirect("/")
  
  return render_template("create_congress.html")

@app.route('/uploads/<filename>')
def uploads(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/create/", methods=["POST"])
def createCongress():
  if not session:
    return redirect("/")
  
  form = request.form.to_dict()

  #logica para guardar imagen congreso
  archivo = request.files.get('imagen')

  if archivo and archivo.filename != '':
    nombre_archivo = archivo.filename
    ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
    archivo.save(ruta_archivo)
    form["imagen"] = nombre_archivo

  #logica para agregar a una lista de diccionarios la informacion de speakers y contenido
  imagenes_a_guardar = []
  archivos_contenido_a_guardar = []
  speakers = []
  contenidos = []
  i = 1
  j = 1

  #Speakers
  while True:
    nombre = request.form.get(f'nombreSpeaker{i}')
    email = request.form.get(f'emailSpeaker{i}')
    linkedin = request.form.get(f'linkedinSpeaker{i}')
    cargo = request.form.get(f'cargoSpeaker{i}')
    empresa = request.form.get(f'empresaSpeaker{i}')
    
    archivo_imagen = request.files.get(f'imagenSpeaker{i}')
    imagen_nombre = ''
    
    if not nombre:
      break

    print(archivo_imagen)
    if archivo_imagen and archivo_imagen.filename != '':
      imagen_nombre = archivo_imagen.filename
      imagenes_a_guardar.append((archivo_imagen, imagen_nombre))

    
    speaker = {
      'nombre': nombre,
      'email': email,
      'linkedin': linkedin,
      'cargo': cargo,
      'empresa': empresa,
      'imagen': imagen_nombre
    }
    speakers.append(speaker)
    i += 1 
  
  for archivo, nombre_archivo in imagenes_a_guardar:
    ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
    archivo.save(ruta_archivo)

  #Contenidos
  while True:
    contenido_archivo = request.files.get(f'contenido-{j}')
    contenido_texto = request.form.get(f'contenido-{j}')

    if not contenido_archivo and not contenido_texto:
      break
    print({'contenido': contenido_archivo,'contenido_texto':contenido_texto, 'j':j})
    if contenido_archivo and contenido_archivo.filename != '':
      archivo_nombre = contenido_archivo.filename
      archivos_contenido_a_guardar.append((contenido_archivo, archivo_nombre))
      contenido = {
        'tipo': 'file',
        'contenido': archivo_nombre
      }
    else:
      contenido = {
        'tipo': 'text',
        'contenido': contenido_texto
      }

    contenidos.append(contenido)
    j += 1

  for archivo, nombre_archivo in archivos_contenido_a_guardar:
    ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
    archivo.save(ruta_archivo)

  # Procesar los datos o hacer algo con ellos
  print("Speakers:", speakers)
  print("Contenidos:", contenidos)

  form["speaker"] = json.dumps(speakers)
  form["contenido"] = json.dumps(contenidos)

  print("Form Speakers:", form["speaker"])
  print("Form Contenidos:", form["contenido"])

  errors = validate_congress_data(form)
  if(len(errors) > 0):
    print('muchos errores')
    return jsonify({"status": "401", "errors": errors}), 400
  
  form["fecha"] = transformDate(form["fecha"])
  form["user_id"] = session["id"]
  Conferencia.createCongress(form)


  message = ["Conferencia creada con éxito !"]

  return jsonify({"status": "200", "message": message}), 200
  # return redirect("congress.html")



@app.route("/congress/<id>/", methods=["GET"])
def congressViewByID(id):
  
  if not session:
    return redirect("/")
  
  congress = Conferencia.getCongressById(id)

  if(len(congress) == 0):
    return redirect('/congress/')
  
  congress_info = congress[0]
  congress_info.speaker = json.loads(congress_info.speaker)
  congress_info.contenido = json.loads(congress_info.contenido)
  print(congress_info.contenido)

  
  return render_template("view_congress.html", conferencia=congress_info)

@app.route("/profile/", methods=["GET"])
def profileView():
  
  if not session:
    return redirect("/")
  
  usuario = Usuario.getUserById(session["id"])

  if(len(usuario) == 0):
    return redirect('/congress/')
  
  user_info = usuario[0]
  return render_template("profile.html", usuario=user_info)

@app.route("/profile/", methods=["POST"])
def editProfile():
  
  if not session:
    return redirect("/")
  
  form = request.form.to_dict()

  form["id"] = session["id"]

  
  
  archivo = request.files.get('imagenPerfil')

  if archivo and archivo.filename != '':
    nombre_archivo = archivo.filename
    ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
    archivo.save(ruta_archivo)
    form["imagenPerfil"] = nombre_archivo
    session['imagenPerfil'] = nombre_archivo
    print(session['imagenPerfil'])

  Usuario.editUser(form)
  message = ['perfil editado con exito']
  return jsonify({"status": "200", "message": message}), 200

@app.route("/logout/", methods=["GET"])
def logoutProfile():
  session.clear()
  return redirect('/')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=8080)