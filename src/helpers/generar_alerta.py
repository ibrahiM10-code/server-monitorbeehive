from src.helpers.contenido_alerta import contenido_alerta
from src.database.db_mongo import add_alerta
from src.helpers.sendPushNotification import send_push_notification
from datetime import datetime
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
