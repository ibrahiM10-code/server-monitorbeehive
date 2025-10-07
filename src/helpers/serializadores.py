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
            print("URL generada: ",colmena["foto_colmena_url"])
        if isinstance(colmena["temperatura"], Decimal128):
            colmena["temperatura"] = float(colmena["temperatura"].to_decimal())
        if isinstance(colmena["humedad"], Decimal128):
            colmena["humedad"] = float(colmena["humedad"].to_decimal())
        if isinstance(colmena["peso"], Decimal128):
            colmena["peso"] = float(colmena["peso"].to_decimal())
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
        if isinstance(colmena["temperatura"], Decimal128):
            colmena["temperatura"] = float(colmena["temperatura"].to_decimal())
        if isinstance(colmena["humedad"], Decimal128):
            colmena["humedad"] = float(colmena["humedad"].to_decimal())
        if isinstance(colmena["peso"], Decimal128):
            colmena["peso"] = float(colmena["peso"].to_decimal())
    return colmenas

# --- Modificación clave aquí para el gráfico del frontend ---
def serialize_sensores(sensores):
    for sensor in sensores:
        if "_id" in sensor:
            sensor["_id"] = str(sensor["_id"])
        
        # Serializar el nuevo campo 'timestamp' a 'fecha' (formato ISO)
        if "timestamp" in sensor and isinstance(sensor["timestamp"], datetime):
            # Convierte el objeto datetime (BSON Date) a una cadena ISO 8601
            sensor["fecha"] = sensor["timestamp"].isoformat()
            # Elimina el campo timestamp original para la respuesta JSON
            del sensor["timestamp"]
            
        # Asegúrate de eliminar 'hora' y 'fecha' si persisten de datos antiguos
        if "hora" in sensor:
            del sensor["hora"]
        if "fecha" in sensor and not isinstance(sensor.get("fecha"), str):
            # Si 'fecha' no es una cadena (es el antiguo datetime sin hora), elimínala
            del sensor["fecha"]
            
        # Serialización de las métricas numéricas (se mantienen)
        if isinstance(sensor["temperatura"], Decimal128):
            sensor["temperatura"] = float(sensor["temperatura"].to_decimal())
        if isinstance(sensor["humedad"], Decimal128):
            sensor["humedad"] = float(sensor["humedad"].to_decimal())
        if isinstance(sensor["peso"], Decimal128):
            sensor["peso"] = float(sensor["peso"].to_decimal())
    return sensores
# -----------------------------------------------------------

def serialize_historial_sensores_diario(sensores_diarios):
    for sensor in sensores_diarios:
        if "sensor_id" in sensor:
            sensor["sensor_id"] = str(sensor["sensor_id"])
            
        # Recomendación: Si el resultado de la agregación tiene una clave de fecha (ej. '_id.day'),
        # deberías serializarla aquí también.
            
        if isinstance(sensor["temperatura_promedio"], Decimal128):
            sensor["temperatura_promedio"] = float(sensor["temperatura_promedio"].to_decimal())
        if isinstance(sensor["humedad_promedio"], Decimal128):
            sensor["humedad_promedio"] = float(sensor["humedad_promedio"].to_decimal())
        if isinstance(sensor["peso_promedio"], Decimal128):
            sensor["peso_promedio"] = float(sensor["peso_promedio"].to_decimal())
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

def genera_colmena_id():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    hash_corto = hashlib.sha1(now.encode()).hexdigest()[:6]
    return f"colmena_{now}_{hash_corto}"