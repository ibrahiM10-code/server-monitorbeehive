from pymongo import MongoClient
from src.helpers.serializadores import genera_colmena_id
from datetime import datetime
from src.helpers.pipelines import get_pipeline_sensores_colmenas, get_pipeline_sensores_colmena_by_apicultor, get_pipeline_sensores_colmena, get_pipeline_sensores_by_dia
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGODB_ATLAS_CONNECTION"))
db = client[os.getenv("MONGODB_ATLAS_DBNAME")]

######################### APICULTORES #########################
# Agrega un nuevo apicultor.
def add_apicultor(datos):
    coleccion = db["apicultor"]
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

# Retorna un apicultor por su RUT.
def get_apicultor(rut):
    coleccion = db["apicultor"]
    apicultor = coleccion.find_one({"rut": rut})
    return apicultor

# Retorna todos los apicultores.
def get_apicultores():
    coleccion = db["apicultor"]
    apicultores = list(coleccion.find())
    return apicultores

# Retorna apicultor en base a su email.
def get_apicultor_email(email):
    coleccion = db["apicultor"]
    correo = list(coleccion.find({"email": email}))
    return correo

# Resetea la clave de la cuenta de un apicultor.
def reset_password(email, nueva_password):
    coleccion = db["apicultor"]
    reset = coleccion.update_one({"email": email}, {"$set": {"password": nueva_password}})
    return reset.modified_count

# Agrega y actualiza el campo expoPushToken.
def add_push_token(user_id, expo_push_token):
    coleccion = db["apicultor"]
    push_token = coleccion.update_one({"_id": ObjectId(user_id)}, {"$set": {"expoPushToken": expo_push_token}})
    return push_token.matched_count

# Retorna el expoPushToken de acuerdo al id del apicultor.
def get_expo_push_token(userId):
    coleccion = db["apicultor"]
    push_token = list(coleccion.find({"_id": ObjectId(userId)}, {"expoPushToken": 1}))
    print(type(ObjectId(userId)), push_token)
    return push_token

# Retorna el id del apicultar de acuerdo al id de la colmena.
def get_apicultor_by_colmena(colmena_id):
    coleccion = db["colmena"]
    apicultor = list(coleccion.find({"colmena_id": colmena_id}, {"id_apicultor": 1}))
    return apicultor
######################### COLMENAS #########################

# Ingresar colmenas.
def add_colmena(datos, fecha, hora):
    coleccion = db["colmena"]
    datos["colmena_id"] = genera_colmena_id()
    resultado = coleccion.insert_one(datos)
    print(fecha, hora)
    add_datos_sensores(datos["colmena_id"], fecha, hora)
    return resultado.inserted_id

# Retorna todas las colmenas.
def get_colmenas():
    pipeline = get_pipeline_sensores_colmenas()
    colmenas = list(db.sensores.aggregate(pipeline))
    return colmenas

# Retorna las colmenas a partir del id del apicultor.
def get_colmena_by_id_apicultor(apicultor_id):
    pipeline = get_pipeline_sensores_colmena_by_apicultor(apicultor_id)
    colmena = list(db.sensores.aggregate(pipeline))
    return colmena

# Retorna la colmena correspondiente a su id.
def get_colmena_particular(colmena_id):
    pipeline = get_pipeline_sensores_colmena(colmena_id)
    colmena = list(db.sensores.aggregate(pipeline))
    return colmena

# Retorna las colmenas a partir de su id.
def get_colmena_info(colmena_id):
    coleccion = db["colmena"]
    colmena = list(coleccion.find({"colmena_id": colmena_id}))
    return {
            "nombre_colmena": colmena[0]["nombre_colmena"],
            "nombre_apiario": colmena[0]["nombre_apiario"],
            "foto_colmena": colmena[0]["foto_colmena"]
        }

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
    resultado = coleccion.insert_one({"temperatura": 0, "humedad": 0, "peso": 0, "sonido": 0, "fecha": datetime.strptime(fecha, "%d-%m-%Y"), "hora": hora, "colmena_id": colmena_id})
    return resultado.inserted_id

# Retorna los datos de sensores de una colmena.
def get_datos_sensores(colmena_id):
    coleccion = db["sensores"]
    datos_sensores = list(coleccion.find({"colmena_id": colmena_id}))
    return datos_sensores

# Actualiza los datos de sensores de una colmena.
def update_datos_sensores(colmena_id, update_fields: dict): 
    coleccion = db["sensores"]
    update_fields["fecha"] = datetime.strptime(update_fields["fecha"], "%d-%m-%Y")
    resultado = coleccion.update_many({"colmena_id": colmena_id}, {"$set": update_fields})
    return resultado.modified_count

# Elimina los datos de sensores de una colmena.
def delete_datos_sensores(colmena_id):
    coleccion = db["sensores"]
    sensores_eliminados = coleccion.delete_one({"colmena_id": colmena_id})
    return sensores_eliminados.deleted_count

# Agrega el ultimo registro de sensores al historial de datos de sensores.
def add_historial_sensores(colmena_id, datos):
    coleccion = db["historial_sensores"]
    datos["colmena_id"] = colmena_id
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

# Retorna el historial de datos de sensores de una colmena.
def get_historial_sensores(colmena_id):
    coleccion = db["historial_sensores"]
    historial = list(coleccion.find({"colmena_id": colmena_id}))
    return historial

# Retorna el historial de datos de sensores de una colmena filtrado por fecha.
def get_historial_sensores_by_fecha(colmena_id, fecha):
    coleccion = db["historial_sensores"]
    historial = list(coleccion.find({"colmena_id": colmena_id, "fecha": fecha}))
    return historial

# Retorna los últimos 5 registros del historial de datos de sensores de una colmena.
def get_ultimos_historial_sensores(colmena_id):
    coleccion = db["historial_sensores"]
    historial = list(coleccion.find({"colmena_id": colmena_id}).sort("_id", -1).limit(5))
    return historial

# Retorna el promedio de los datos sensorizados en un dia.
def get_historial_diario(colmena_id):
    pipeline = get_pipeline_sensores_by_dia(colmena_id)
    historial_diario = list(db.historial_sensores.aggregate(pipeline))
    return historial_diario

def delete_historial_sensores(colmena_id):
    coleccion = db["historial_sensores"]
    sensores_eliminados = coleccion.delete_many({"colmena_id": colmena_id})
    return sensores_eliminados.deleted_count

######################### ALERTAS #########################

# Ingresa datos de una alerta a una colmena.
def add_alerta(datos, colmena_id, id_apicultor):
    coleccion = db["alertas"]
    datos["fecha"] = datetime.strptime(datos["fecha"], "%d-%m-%Y")
    datos["colmena_id"] = colmena_id
    datos["id_apicultor"] = ObjectId(id_apicultor)
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

# Retorna las alertas de una colmena en especifico.
def get_alertas_particular(colmena_id):
    coleccion = db["alertas"]
    datos_alertas = list(coleccion.find({"colmena_id": colmena_id}))
    return datos_alertas

# Retorna todas las alertas de las colmenas asignadas a un apicultor.
def get_alertas_by_apicultor(apicultor_id):
    coleccion = db["alertas"]
    datos_alertas = list(coleccion.find({"id_apicultor": apicultor_id}))
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
def add_reporte(colmena_id, descripcion, apicultor_id):
    coleccion = db["reportes"]
    datos_reporte = {
        "colmena_id": colmena_id,
        "apicultor_id": ObjectId(apicultor_id),
        "descripcion": descripcion,
        "datos_registrados": [r["_id"] for r in get_historial_sensores(colmena_id)],
        "fecha_descarga": datetime.now().strftime("%d-%m-%Y"),
        "hora_descarga": datetime.now().strftime("%H:%M")
    }
    resultado = coleccion.insert_one(datos_reporte)
    return resultado.inserted_id

# Retorna los reportes descargados de las colmenas de un apicultor.
def get_reportes(apicultor_id):
    coleccion = db["reportes"]
    reportes = list(coleccion.find({"apicultor_id": apicultor_id}))
    return reportes

# Retorna los reportes filtrados por fecha.
def get_reportes_by_fecha(colmena_id, fecha):
    coleccion = db["reportes"]
    reportes = list(coleccion.find({"colmena_id": colmena_id, "fecha_descarga": fecha}))
    return reportes