from flask import Blueprint, request, jsonify
from src.database.db_mongo import get_datos_sensores, update_datos_sensores, add_historial_sensores, get_ultimos_historial_sensores, get_historial_diario, get_expo_push_token, get_apicultor_by_colmena
from src.utils.tokenManagement import TokenManager
from src.helpers.serializadores import serialize_sensores, serialize_historial_sensores_diario
from src.helpers.generar_alerta import generar_alerta
from datetime import datetime
import pytz

main = Blueprint("sensores", __name__)

@main.route("/obtener-sensores/<string:colmena_id>", methods=["GET"])
def obtener_sensores(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            datos_sensores = get_datos_sensores(colmena_id)
            if not datos_sensores:
                return jsonify({"message": "No se encontraron datos de sensores para esta colmena"}), 404
            datos_sensores = serialize_sensores(datos_sensores)
            return jsonify(datos_sensores), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/obtener-ultimos-sensores/<string:colmena_id>", methods=["GET"])
def obtener_ultimos_sensores(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            historial_sensores = get_ultimos_historial_sensores(colmena_id)
            if not historial_sensores:
                return jsonify({"message": "No se encontraron datos de sensores para esta colmena"}), 404
            historial_sensores = serialize_sensores(historial_sensores)
            return jsonify(historial_sensores), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/obtener-historial-diario/<string:colmena_id>", methods=["GET"])
def obtenet_historial_diario(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            historial_sensores = get_historial_diario(colmena_id)
            if not historial_sensores:
                return jsonify({"message": "No se encontraron datos de sensores para esta colmena"}), 404
            historial_sensores = serialize_historial_sensores_diario(historial_sensores)
            return jsonify(historial_sensores), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/actualizar-sensores/<string:colmena_id>", methods=["PUT"])
def actualizar_sensores(colmena_id):
    datos = request.json
    print(datos)
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400
    try:
        update_fields = {}
        if "temperatura" in datos:
            update_fields["temperatura"] = datos["temperatura"]
        if "humedad" in datos:
            update_fields["humedad"] = datos["humedad"]
        if "peso" in datos:
            update_fields["peso"] = datos["peso"]
        # if "sonido" in datos:
        #     update_fields["sonido"] = datos["sonido"]
        santiago_tz = pytz.timezone("America/Santiago")
        try:
                if isinstance(datos["fecha"], str):
                    # Parse the date and make it timezone aware
                    fecha_dt = datetime.strptime(datos["fecha"], "%d-%m-%Y")
                    fecha_aware = santiago_tz.localize(fecha_dt)
                    update_fields["fecha"] = fecha_aware
                elif isinstance(datos["fecha"], datetime):
                    if datos["fecha"].tzinfo is None:
                        # Make naive datetime timezone aware
                        update_fields["fecha"] = santiago_tz.localize(datos["fecha"])
                    else:
                        update_fields["fecha"] = datos["fecha"]
                else:
                    return jsonify({"error": "Formato de fecha inválido"}), 400
        except ValueError as e:
                return jsonify({"error": f"Error al procesar la fecha: {str(e)}"}), 400
        if "hora" in datos:
            update_fields["hora"] = datos["hora"]
        # if "analisis_sonido" in datos:
        #     update_fields["analisis_sonido"] = datos["analisis_sonido"]
        apicultor_id = get_apicultor_by_colmena(colmena_id)[0]["id_apicultor"]
        resultado = update_datos_sensores(colmena_id, update_fields)
        expo_push_token = get_expo_push_token(apicultor_id)
        print(expo_push_token)
        if apicultor_id and resultado:
            add_historial_sensores(colmena_id, update_fields)
            if "expoPushToken" in expo_push_token[0].keys():
                expo_push_token = expo_push_token[0]["expoPushToken"]
                generar_alerta(update_fields, colmena_id, apicultor_id, expo_push_token)
                print("Notificacion enviada al celular del apicultor!")
            else:
                generar_alerta(update_fields, colmena_id, apicultor_id)
                print("Este usuario no puede recibir notificaciones a su celular.")
            return jsonify({"message": "Datos de sensores actualizados exitosamente"}), 200
        else:
            return jsonify({"error": "No se encontró el sensor con el ID proporcionado"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    