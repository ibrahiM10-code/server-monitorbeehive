from pymongo import MongoClient
from src.helpers.serializadores import genera_colmena_id
from datetime import datetime
from src.helpers.pipelines import get_pipeline_sensores_colmenas, get_pipeline_sensores_colmena_by_apicultor, get_pipeline_sensores_colmena, get_pipeline_sensores_by_dia
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["monitorBeehive"]

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

# --- Función Auxiliar para la Creación de Timestamp ---
# Asume que recibe la fecha en formato 'DD-MM-YYYY' y la hora en 'HH:MM:SS'
def _create_timestamp(fecha_str, hora_str):
    """Combina cadenas de fecha y hora en un único objeto datetime."""
    # Podrías necesitar agregar segundos si la hora solo incluye HH:MM
    if len(hora_str.split(':')) == 2:
        hora_str += ":00" 
        
    fecha_hora_str = f"{fecha_str} {hora_str}"
    try:
        # Crea el objeto datetime
        return datetime.strptime(fecha_hora_str, "%d-%m-%Y %H:%M:%S")
    except ValueError:
        # Manejo de error si el formato no coincide (opcional)
        print(f"Error al parsear fecha/hora: {fecha_hora_str}")
        return None

# --- Funciones de la Base de Datos Modificadas ---

# Ingresa datos de sensores a una colmena. (Modificada para usar 'timestamp')
def add_datos_sensores(colmena_id, fecha, hora):
    coleccion = db["sensores"]
    timestamp = _create_timestamp(fecha, hora)
    if timestamp is None:
        return None # O manejar el error de otra manera
        
    resultado = coleccion.insert_one({
        "temperatura": 0, 
        "humedad": 0, 
        "peso": 0, 
        "sonido": 0, 
        "timestamp": timestamp, # Nuevo campo único
        "colmena_id": colmena_id
        # Eliminamos "fecha" y "hora" separadas
    })
    return resultado.inserted_id

# Retorna los datos de sensores de una colmena. (No requiere cambios funcionales aquí)
def get_datos_sensores(colmena_id):
    coleccion = db["sensores"]
    # Retornará el campo 'timestamp' de tipo BSON Date
    datos_sensores = list(coleccion.find({"colmena_id": colmena_id}))
    return datos_sensores

# Actualiza los datos de sensores de una colmena. (Modificada para usar 'timestamp')
def update_datos_sensores(colmena_id, update_fields: dict): 
    coleccion = db["sensores"]
    
    # CRÍTICO: Combina 'fecha' y 'hora' en 'timestamp' si están presentes
    if "fecha" in update_fields and "hora" in update_fields:
        update_fields["timestamp"] = _create_timestamp(update_fields["fecha"], update_fields["hora"])
        del update_fields["fecha"]
        del update_fields["hora"]
        
    # El resto de campos (temp, humedad, etc.) se agregan directamente
    
    # Si el timestamp no pudo ser creado, podría devolver un error o simplemente no actualizar
    if "timestamp" not in update_fields or update_fields["timestamp"] is None:
        # Podrías querer lanzar una excepción o registrar un error aquí
        print("Error: No se pudo crear el timestamp para la actualización.")
        return 0 
    
    resultado = coleccion.update_many({"colmena_id": colmena_id}, {"$set": update_fields})
    return resultado.modified_count

# Elimina los datos de sensores de una colmena. (No requiere cambios)
def delete_datos_sensores(colmena_id):
    coleccion = db["sensores"]
    sensores_eliminados = coleccion.delete_many({"colmena_id": colmena_id})
    return sensores_eliminados.deleted_count

# Agrega el ultimo registro de sensores al historial de datos de sensores. (Modificada para usar 'timestamp')
def add_historial_sensores(colmena_id, datos):
    coleccion = db["historial_sensores"]
    
    # CRÍTICO: Crear el timestamp y eliminar campos separados antes de insertar en el historial
    if "fecha" in datos and "hora" in datos:
        datos["timestamp"] = _create_timestamp(datos["fecha"], datos["hora"])
        del datos["fecha"]
        del datos["hora"]
        
    # Si el timestamp no existe, no insertes el registro o loguea el error
    if "timestamp" not in datos or datos["timestamp"] is None:
        print("Error: Registro de historial ignorado debido a timestamp inválido.")
        return None

    datos["colmena_id"] = colmena_id
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

# Retorna el historial de datos de sensores de una colmena. (Modificada para ordenar por 'timestamp')
def get_historial_sensores(colmena_id):
    coleccion = db["historial_sensores"]
    # Ordena por timestamp ascendente (más antiguo primero) para el gráfico de series de tiempo
    historial = list(coleccion.find({"colmena_id": colmena_id}).sort("timestamp", 1)) 
    return historial

# Retorna el historial de datos de sensores de una colmena filtrado por fecha. 
# ADVERTENCIA: Esta función ahora requerirá que 'fecha' sea un objeto datetime para coincidir con 'timestamp'.
# Se recomienda modificar esta función para filtrar por un rango de timestamps (día completo).
def get_historial_sensores_by_fecha(colmena_id, fecha_inicio: datetime, fecha_fin: datetime):
    coleccion = db["historial_sensores"]
    # Filtra por un rango de timestamps (ej. el día completo)
    historial = list(coleccion.find({
        "colmena_id": colmena_id, 
        "timestamp": {"$gte": fecha_inicio, "$lt": fecha_fin}
    }).sort("timestamp", 1))
    return historial

# Retorna los últimos 5 registros del historial de datos de sensores de una colmena. (Modificada para ordenar por 'timestamp')
def get_ultimos_historial_sensores(colmena_id):
    coleccion = db["historial_sensores"]
    # Ordena por timestamp descendente (más reciente primero)
    historial = list(coleccion.find({"colmena_id": colmena_id}).sort("timestamp", -1).limit(5))
    return historial

# Retorna el historial diario usando el pipeline de agregación. 
# ADVERTENCIA: El pipeline deberá actualizarse para agrupar usando el campo 'timestamp'.
def get_historial_diario(colmena_id):
    # La función get_pipeline_sensores_by_dia debe actualizarse para usar el campo 'timestamp'
    pipeline = get_pipeline_sensores_by_dia(colmena_id)
    historial_diario = list(db.historial_sensores.aggregate(pipeline))
    return historial_diario

######################### ALERTAS #########################

# Ingresa datos de una alerta a una colmena.
def add_alerta(datos):
    coleccion = db["alertas"]
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