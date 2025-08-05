from bson import ObjectId
from flask import Blueprint, request, jsonify
from src.database.db_mongo import add_alerta, get_alertas_particular, update_alerta, get_alertas_by_apicultor
from src.utils.tokenManagement import TokenManager
from src.helpers.serializadores import serialize_alertas
from datetime import datetime

main = Blueprint("alertas", __name__)

@main.route("/agregar-alerta", methods=["POST"])
def agregar_alerta():
    datos = request.json
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        if not datos:
            return jsonify({"error": "Datos no proporcionados"}), 400
        try:
            nueva_alerta = {
                "colmena_id": datos["colmena_id"],
                "titulo_alerta": datos["titulo_alerta"],
                "descripcion_alerta": datos["descripcion_alerta"],
                "fecha": datos["fecha"],
                "estado_alerta": datos["estado_alerta"],
                "tipo_alerta": datos["tipo_alerta"]
            }
            alerta_id = add_alerta(nueva_alerta)
            return jsonify({"message": "Alerta agregada exitosamente", "id": str(alerta_id)}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/obtener-alertas-particular/<string:colmena_id>", methods=["GET"])
def obtener_alertas(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            datos_alertas = get_alertas_particular(colmena_id)
            if not datos_alertas:
                return jsonify({"message": "No se encontraron alertas para esta colmena"}), 200
            alertas_serializadas = serialize_alertas(datos_alertas)
            return jsonify(alertas_serializadas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/obtener-alertas-apicultor/<string:id_apicultor>", methods=["GET"])
def obtener_alertas_apicultor(id_apicultor):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            datos_alertas = get_alertas_by_apicultor(ObjectId(id_apicultor))
            if not datos_alertas:
                return jsonify({"message": "No se encontraron alertas para este apicultor"}), 200
            alertas_serializadas = serialize_alertas(datos_alertas)
            return jsonify(alertas_serializadas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/actualizar-alerta/<string:alerta_id>", methods=["PUT"])
def actualizar_alerta(alerta_id):
    datos = request.json
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        if not datos or "estado_alerta" not in datos:
            return jsonify({"error": "Datos no proporcionados o estado de alerta no especificado"}), 400
        try:
            resultado = update_alerta(ObjectId(alerta_id), datos["estado_alerta"])
            if resultado:
                return jsonify({"message": "Alerta actualizada exitosamente"}), 200
            else:
                return jsonify({"error": "No se encontró la alerta con el ID proporcionado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401