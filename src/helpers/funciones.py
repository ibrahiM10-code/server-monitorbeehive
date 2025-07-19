from flask import url_for
from datetime import datetime
import hashlib

def serialize_colmenas(colmenas, ObjectId):
    for colmena in colmenas:
        colmena["_id"] = str(colmena["_id"])
        if "id_apicultor" in colmena and isinstance(colmena["id_apicultor"], ObjectId):
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

def genera_colmena_id():
    now = datetime.now().strftime("%Y%m%d")
    hash_corto = hashlib.sha1(now.encode()).hexdigest()[:6]
    return f"colmena_{now}_{hash_corto}" 