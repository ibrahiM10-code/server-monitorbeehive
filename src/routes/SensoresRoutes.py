from flask import Blueprint, request, jsonify
from src.database.db_mongo import add_datos_sensores, get_id_ultima_colmena, get_datos_sensores
from src.utils.tokenManagement import TokenManager
from src.helpers.funciones import serialize_sensores

main = Blueprint("sensores", __name__)

@main.route("/agregar-sensores", methods=["POST"])
def agregar_sensores():
    datos = request.json
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400
    try:
        datos_sensores = {
            "colmena_id": get_id_ultima_colmena(),
            "temperatura": datos["temperatura"],
            "humedad": datos["humedad"],
            "peso": datos["peso"],
            "sonido": datos["sonido"],
            "fecha": datos["fecha"],
            "hora": datos["hora"]
        }
        sensor_id = add_datos_sensores(datos_sensores)
        return jsonify({"message": "Datos de sensores agregados exitosamente", "id": str(sensor_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route("/obtener-sensores/<string:colmena_id>", methods=["GET"])
def obtener_sensores(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    print(acceso, colmena_id)
    if acceso:
        try:
            datos_sensores = get_datos_sensores(colmena_id)
            if not datos_sensores:
                return jsonify({"message": "No se encontraron datos de sensores para esta colmena"}), 200
            datos_sensores = serialize_sensores(datos_sensores)
            return jsonify(datos_sensores), 200
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Token inválido o expirado"}), 401
