from flask import url_for
from datetime import datetime
import hashlib
import uuid # <-- NUEVA IMPORTACIÓN PARA GENERAR ID ÚNICO

def serialize_colmenas(colmenas, ObjectId):
    for colmena in colmenas:
        colmena["_id"] = str(colmena["_id"])
        if "id_apicultor" in colmena and isinstance(colmena["id_apicultor"], ObjectId):
            colmena["id_apicultor"] = str(colmena["id_apicultor"])
        if "foto_colmena" in colmena and colmena["foto_colmena"]:
            colmena["foto_colmena_url"] = url_for('static', filename=colmena["foto_colmena"], _external=True)
            print("URL generada: ",colmena["foto_colmena_url"])
    return colmenas

def serialize_colmenas_admin(colmenas):
    for colmena in colmenas:
        if "_id" in colmena:
            colmena["_id"] = str(colmena["_id"])
        if "id_apicultor" in colmena:
            colmena["id_apicultor"] = str(colmena["id_apicultor"])
        if "foto_colmena" in colmena and colmena["foto_colmena"]:
            colmena["foto_colmena_url"] = url_for('static', filename=colmena["foto_colmena"], _external=True)
            print("URL generada: ",colmena["foto_colmena_url"])
    return colmenas

def serialize_sensores(sensores):
    for sensor in sensores:
        if "_id" in sensor:
            sensor["_id"] = str(sensor["_id"])
    return sensores

def serialize_alertas(alertas):
    for alerta in alertas:
        if "_id" in alerta:
            alerta["_id"] = str(alerta["_id"])
            alerta["id_apicultor"] =str(alerta["id_apicultor"])
    return alertas

def serialize_reportes(reportes, ObjectId):
    serialized = []
    for reporte in reportes:
        rep = dict(reporte)
        if "_id" in rep:
            rep["_id"] = str(rep["_id"])
        if "apicultor_id" in rep and isinstance(rep["apicultor_id"], ObjectId):
            rep["apicultor_id"] = str(rep["apicultor_id"])
        if "datos_registrados" in rep and isinstance(rep["datos_registrados"], list):
            rep["datos_registrados"] = [str(x) if isinstance(x, ObjectId) else x for x in rep["datos_registrados"]]
        serialized.append(rep)
    return serialized

def genera_colmena_id():
    # CÓDIGO CORREGIDO: Genera un UUID para un identificador totalmente único.
    # Esto reemplaza el hash basado en la fecha que era estático por día.
    return str(uuid.uuid4().hex)