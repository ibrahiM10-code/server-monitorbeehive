from flask import Blueprint, request, jsonify
from src.database.db_mongo import add_umbrales, get_umbrales, update_umbrales, get_apicultor_by_id
from src.utils.tokenManagement import TokenManager
from src.helpers.serializadores import serialize_umbrales

main = Blueprint("umbrales", __name__)

@main.route("/agregar-umbrales/<string:id_apicultor>", methods=["POST"])
def agregar_umbrales(id_apicultor):
    acceso = TokenManager.verificar_token(request.headers)
    datos = request.json
    print("Datos", type(datos))
    if acceso:
        if not datos:
            return jsonify({"error": "Datos no proporcionados"}), 400
        try:
            umbrales_definidos = add_umbrales(datos, id_apicultor)
            return jsonify({"message": "Umbrales definidos correctamente"}), 201
        except Exception as e:
            print(e)
            return jsonify({"error": f"{e}"}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401
    
@main.route("/obtener-umbrales/<string:id_apicultor>", methods=["GET"])
def obtener_umbrales(id_apicultor):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            rol_apicultor = get_apicultor_by_id(id_apicultor)
            if rol_apicultor["rol"] == "Administrador":
                umbrales = serialize_umbrales(get_umbrales(id_apicultor))
                return jsonify(umbrales), 200
            elif rol_apicultor["rol"] == "Apicultor":
                return jsonify({"error": "Este rol no tiene permitido realizar esta acción"}), 403
        except Exception as e:
            print(e)
            return jsonify({"error": f"{e}"}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401
    
@main.route("/actualizar-umbrales/<string:id_apicultor>", methods=["PUT"])
def actualizar_umbrales(id_apicultor):
    acceso = TokenManager.verificar_token(request.headers)
    datos = request.json
    if acceso:
        if not datos:
            return jsonify({"error": "Datos no proporcionados"}), 400
        try:
            update_fields = {
                key: datos[key]
                for key in ["temperatura_minima", "temperatura_maxima", "humedad_minima", "humedad_maxima", "peso_minimo", "peso_maximo"]
                if key in datos
            }
            rol_apicultor = get_apicultor_by_id(id_apicultor)
            if rol_apicultor["rol"] == "Administrador":
                umbrales_modificados = update_umbrales(id_apicultor, update_fields)
                if umbrales_modificados > 0:
                    return jsonify({"message": "Umbrales actualizados correctamente."}), 200
                else:
                    return jsonify({"message": "No se hicieron cambios en los umbrales definidos."}), 204
            elif rol_apicultor["rol"] == "Apicultor":
                return jsonify({"error": "Este rol no tiene permitido realizar esta acción."}), 403
        except Exception as e:
            print(e)
            return jsonify({"error": f"{e}"}), 500
    else:
        return jsonify({"error": "Token inválido o expirado."}), 401