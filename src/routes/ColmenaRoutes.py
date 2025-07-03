from bson import ObjectId
from flask import Blueprint, request, jsonify
from src.database.db_mongo import add_colmena, get_colmena_by_id
from src.utils.tokenManagement import TokenManager

main = Blueprint("colmenas", __name__)
@main.route("/agregar-colmena", methods=["POST"])
def agregar_colmena():
    datos = request.json
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        if not datos:
            return jsonify({"error": "Datos no proporcionados"}), 400
        try:
            nueva_colmena = {
                "nombre_colmena": datos["nombre_colmena"],
                "nombre_apiario": datos["nombre_apiario"],
                # "foto_colmena": datos["foto_colmena"],
                # "datos_sensores": [ObjectId(sid) for sid in datos.get("datos_sensores", [])],
                # "alertas": [ObjectId(aid) for aid in datos.get("alertas", [])],
                # "reportes": [ObjectId(rid) for rid in datos.get("reportes", [])],
                "id_apicultor": ObjectId(datos["id_apicultor"])
            }
            colmena_id = add_colmena(nueva_colmena)
            return jsonify({"message": "Colmena agregada exitosamente", "id": str(colmena_id)}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401
    


def serialize_colmenas(colmenas):
    for colmena in colmenas:
        colmena["_id"] = str(colmena["_id"])
        if "id_apicultor" in colmena and isinstance(colmena["id_apicultor"], ObjectId):
            colmena["id_apicultor"] = str(colmena["id_apicultor"])
    return colmenas

@main.route("/obtener-colmenas/<string:id_apicultor>", methods=["GET"])
def obtener_colmenas(id_apicultor):
    acceso = TokenManager.verificar_token(request.headers)
    print(acceso, id_apicultor)
    if acceso:
        try:
            colmenas = get_colmena_by_id(ObjectId(id_apicultor))
            if not colmenas:
                return jsonify({"message": "No se encontraron colmenas para este apicultor"}), 404
            colmenas = serialize_colmenas(colmenas)
            return jsonify(colmenas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401
