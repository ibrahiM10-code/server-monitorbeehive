from pymongo import MongoClient
from src.helpers.serializadores import genera_colmena_id

client = MongoClient("mongodb://localhost:27017/")
db = client["monitorBeehive"]

######################### APICULTORES #########################
# Agrega un nuevo apicultor.
def add_apicultor(datos):
    coleccion = db["apicultor"]
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

# Retorna un apicultor por su RUT y password.
def get_apicultor(rut, password):
    coleccion = db["apicultor"]
    apicultor = coleccion.find_one({"rut": rut, "password": password})
    return apicultor

# Retorna todos los apicultores.
def get_apicultores():
    coleccion = db["apicultor"]
    apicultores = list(coleccion.find())
    return apicultores

######################### COLMENAS #########################

# Ingresar colmenas.
def add_colmena(datos, fecha, hora):
    coleccion = db["colmena"]
    datos["colmena_id"] = genera_colmena_id()
    resultado = coleccion.insert_one(datos)
    add_datos_sensores(datos["colmena_id"], fecha, hora)
    return resultado.inserted_id

# Retorna todas las colmenas.
def get_colmenas():
    coleccion = db["colmena"]
    colmenas = list(coleccion.find())
    return colmenas

# Retorna las colmenas a partir del id del apicultor.
def get_colmena_by_id(apicultor_id):
    coleccion = db["colmena"]
    colmena = list(coleccion.find({"id_apicultor": apicultor_id}))
    return colmena

# Retorna el id de la última colmena ingresada.
def get_id_ultima_colmena():
    coleccion = db["colmena"]
    ultima_colmena = coleccion.find().sort("colmena_id", -1).limit(1)
    return ultima_colmena[0]["colmena_id"]

# Actualiza los datos de una colmena.
def update_colmena(colmena_id, update_fields: dict):
    coleccion = db["colmena"]
    resultado = coleccion.update_one({"colmena_id": colmena_id}, {"$set": update_fields})
    return resultado.modified_count

# Elimina una colmena por su ID.
def delete_colmena(colmena_id):
    coleccion = db["colmena"]
    colmena_eliminada = coleccion.delete_one({"colmena_id": colmena_id})
    delete_datos_sensores(colmena_id)
    delete_alerta(colmena_id)
    return colmena_eliminada.deleted_count

######################### SENSORES #########################

# Ingresa datos de sensores a una colmena.
def add_datos_sensores(colmena_id, fecha, hora):
    coleccion = db["sensores"]
    resultado = coleccion.insert_one({"temperatura": 0, "humedad": 0, "peso": 0, "sonido": 0, "fecha": fecha, "hora": hora, "colmena_id": colmena_id})
    return resultado.inserted_id

# Retorna los datos de sensores de una colmena.
def get_datos_sensores(colmena_id):
    coleccion = db["sensores"]
    datos_sensores = list(coleccion.find({"colmena_id": colmena_id}))
    return datos_sensores

# Actualiza los datos de sensores de una colmena.
def update_datos_sensores(colmena_id, update_fields: dict): 
    coleccion = db["sensores"]
    resultado = coleccion.update_many({"colmena_id": colmena_id}, {"$set": update_fields})
    return resultado.modified_count

# Elimina los datos de sensores de una colmena.
def delete_datos_sensores(colmena_id):
    coleccion = db["sensores"]
    sensores_eliminados = coleccion.delete_many({"colmena_id": colmena_id})
    return sensores_eliminados.deleted_count

# Agrega el ultimo registro de sensores al historial de datos de sensores.
def add_historial_sensores(colmena_id, datos):
    coleccion = db["historial_sensores"]
    datos["colmena_id"] = colmena_id
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

def get_historial_sensores(colmena_id):
    coleccion = db["historial_sensores"]
    historial = list(coleccion.find({"colmena_id": colmena_id}))
    return historial

######################### ALERTAS #########################

# Ingresa datos de una alerta a una colmena.
def add_alerta(datos):
    coleccion = db["alertas"]
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

# Retorna las alertas de una colmena.
def get_alertas(colmena_id):
    coleccion = db["alertas"]
    datos_alertas = list(coleccion.find({"colmena_id": colmena_id}))
    return datos_alertas

# Actualiza el estado de una alerta.
def update_alerta(alerta_id, estado):
    coleccion = db["alertas"]
    resultado = coleccion.update_one({"_id": alerta_id}, {"$set": {"estado_alerta": estado}})
    return resultado.modified_count

# Elimna una alerta.
def delete_alerta(colmena_id):
    coleccion = db["alertas"]
    alerta_eliminada = coleccion.delete_one({"colmena_id": colmena_id})
    return alerta_eliminada.deleted_count

######################### REPORTES #########################

# Guarda la descripcion del reporte, id del historico de sensores y el id de la colmena.
def add_reporte(colmena_id, descripcion):
    coleccion = db["reportes"]
    datos_reporte = {
        "colmena_id": colmena_id,
        "descripcion": descripcion
    }
    resultado = coleccion.insert_one(datos_reporte)
    return resultado.inserted_id