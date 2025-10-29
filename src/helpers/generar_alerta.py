from src.helpers.contenido_alerta import contenido_alerta
from src.database.db_mongo import add_alerta
from src.helpers.sendPushNotification import send_push_notification

def generar_alerta(datos_sensores, colmena_id, userId, expo_push_token=""):
    alerta_temp = evalua_temperatura(float(str(datos_sensores["temperatura"])), colmena_id, userId)
    alerta_hum = evalua_humedad(float(str(datos_sensores["humedad"])), colmena_id, userId)
    alerta_peso = evalua_peso(float(str(datos_sensores["peso"])), colmena_id, userId)
    alertas = [alerta_temp, alerta_hum, alerta_peso]
    if not expo_push_token == "":
        for alerta in alertas:
            result = send_push_notification(expo_push_token, alerta["titulo"], alerta["descripcion"])
        return result
    return True
    
def evalua_temperatura(temperatura, colmena_id, userId):
    if temperatura < 33:
        alerta_temp = contenido_alerta["temperatura"][0]["temperatura_baja"]
    elif temperatura > 35:
        alerta_temp = contenido_alerta["temperatura"][1]["temperatura_alta"]
    else:
        alerta_temp = contenido_alerta["temperatura"][2]["temperatura_optima"]
    add_alerta(alerta_temp, colmena_id, userId)
    return alerta_temp

def evalua_humedad(humedad, colmena_id, userId):
    if humedad < 40:
        alerta_hum = contenido_alerta["humedad"][0]["humedad_baja"]
    elif humedad > 70:
        alerta_hum = contenido_alerta["humedad"][1]["humedad_alta"]
    else:
        alerta_hum = contenido_alerta["humedad"][2]["humedad_optima"]
    add_alerta(alerta_hum, colmena_id, userId)
    return alerta_hum

def evalua_peso(peso, colmena_id, userId):
    if peso <= 0.3:
        alerta_peso = contenido_alerta["peso"][0]["peso_bajo"]
    else:
        alerta_peso = contenido_alerta["peso"][1]["peso_optimo"]
    add_alerta(alerta_peso, colmena_id, userId)
    return alerta_peso
