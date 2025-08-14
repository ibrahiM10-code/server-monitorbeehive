from flask import Blueprint, request, jsonify
from src.database.db_mongo import get_datos_sensores, update_datos_sensores, add_historial_sensores
from src.utils.tokenManagement import TokenManager
from src.helpers.serializadores import serialize_sensores

main = Blueprint("sensores", __name__)

@main.route("/obtener-sensores/<string:colmena_id>", methods=["GET"])
def obtener_sensores(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    print(acceso, colmena_id)
    if acceso:
        try:
            datos_sensores = get_datos_sensores(colmena_id)
            if not datos_sensores:
                return jsonify({"message": "No se encontraron datos de sensores para esta colmena"}), 404
            datos_sensores = serialize_sensores(datos_sensores)
            return jsonify(datos_sensores), 200
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/actualizar-sensores/<string:colmena_id>", methods=["PUT"])
def actualizar_sensores(colmena_id):
    datos = request.json
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
        if "sonido" in datos:
            update_fields["sonido"] = datos["sonido"]
        if "fecha" in datos:
            update_fields["fecha"] = datos["fecha"]
        if "hora" in datos:
            update_fields["hora"] = datos["hora"]
        if "analisis_sonido" in datos:
            update_fields["analisis_sonido"] = datos["analisis_sonido"]
        resultado = update_datos_sensores(colmena_id, update_fields)
        if resultado:
            add_historial_sensores(colmena_id, update_fields)
            return jsonify({"message": "Datos de sensores actualizados exitosamente"}), 200
        else:
            return jsonify({"error": "No se encontró el sensor con el ID proporcionado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    