from flask import url_for
from datetime import datetime
from bson.decimal128 import Decimal128
import hashlib

def serialize_colmenas(colmenas, ObjectId):
    for colmena in colmenas:
        colmena["_id"] = str(colmena["_id"])
        if "id_apicultor" in colmena and isinstance(colmena["id_apicultor"], ObjectId):
            colmena["id_apicultor"] = str(colmena["id_apicultor"])
        if "foto_colmena" in colmena and colmena["foto_colmena"]:
            colmena["foto_colmena_url"] = url_for('static', filename=colmena["foto_colmena"], _external=True)
        if isinstance(colmena["temperatura"], Decimal128):
            colmena["temperatura"] = float(str(colmena["temperatura"]))
        if isinstance(colmena["humedad"], Decimal128):
            colmena["humedad"] = float(str(colmena["humedad"]))
        if isinstance(colmena["peso"], Decimal128):
            colmena["peso"] = float(str(colmena["peso"]))
    return colmenas

def serialize_colmenas_admin(colmenas):
    for colmena in colmenas:
        if "_id" in colmena:
            colmena["_id"] = str(colmena["_id"])
        if "id_apicultor" in colmena:
            colmena["id_apicultor"] = str(colmena["id_apicultor"])
        if "foto_colmena" in colmena and colmena["foto_colmena"]:
            colmena["foto_colmena_url"] = url_for('static', filename=colmena["foto_colmena"], _external=True)
        if isinstance(colmena["temperatura"], Decimal128):
            colmena["temperatura"] = float(str(colmena["temperatura"]))
        if isinstance(colmena["humedad"], Decimal128):
            colmena["humedad"] = float(str(colmena["humedad"]))
        if isinstance(colmena["peso"], Decimal128):
            colmena["peso"] = float(str(colmena["peso"]))
    return colmenas

def serialize_sensores(sensores):
    for sensor in sensores:
        if "_id" in sensor:
            sensor["_id"] = str(sensor["_id"])
        if isinstance(sensor["temperatura"], Decimal128):
            sensor["temperatura"] = float(str(sensor["temperatura"]))
        if isinstance(sensor["humedad"], Decimal128):
            sensor["humedad"] = float(str(sensor["humedad"]))
        if isinstance(sensor["peso"], Decimal128):
            sensor["peso"] = float(str(sensor["peso"]))
        if "fecha" in sensor:
            sensor["fecha"] = sensor["fecha"].strftime("%d-%m-%Y")
    return sensores

def serialize_historial_sensores_diario(sensores_diarios):
    for sensor in sensores_diarios:
        if "sensor_id" in sensor:
            sensor["sensor_id"] = str(sensor["sensor_id"])
        if isinstance(sensor["temperatura_promedio"], Decimal128):
            sensor["temperatura_promedio"] = float(str(sensor["temperatura_promedio"]))
        if isinstance(sensor["humedad_promedio"], Decimal128):
            sensor["humedad_promedio"] = float(str(sensor["humedad_promedio"]))
        if isinstance(sensor["peso_promedio"], Decimal128):
            sensor["peso_promedio"] = float(str(sensor["peso_promedio"]))
    return sensores_diarios

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

def serialize_umbrales(umbrales):
    for umbral in umbrales:
        if "_id" in umbral:
            umbral["_id"] = str(umbral["_id"])
        if "id_apicultor_admin" in umbral:
            umbral["id_apicultor_admin"] = str(umbral["id_apicultor_admin"])
    return umbrales

def genera_colmena_id():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    hash_corto = hashlib.sha1(now.encode()).hexdigest()[:6]
    return f"colmena_{now}_{hash_corto}" 