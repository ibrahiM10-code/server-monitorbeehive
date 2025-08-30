from flask import Blueprint, request, jsonify
from src.database.db_mongo import add_apicultor, get_apicultor
from src.utils.tokenManagement import TokenManager
from src.helpers.encriptar_clave import encriptar_clave
from src.helpers.evaluar_clave import evaluar_clave

main = Blueprint("auth", __name__)

@main.route("/registrar-apicultor", methods=["POST"])
def registrar_apicultor():
    print(request.json)
    datos = request.json
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400

    try:
        datos["password"] = encriptar_clave(datos["password"])
        id_apicultor = add_apicultor(datos)
        return jsonify({"message": "Apicultor registrado exitosamente", "id": str(id_apicultor)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route("/login", methods=["POST"])
def login():
    datos = request.json
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400
    try:
        apicultor = get_apicultor(datos["rut"])
        if not apicultor:
            return jsonify({"error": "Apicultor no encontrado"}), 404
        resultado = evaluar_clave(datos["password"], apicultor["password"])
        if resultado:    
            token = TokenManager.generar_token(apicultor)
            return jsonify({"token": token, "user": str(apicultor["_id"])}, 200)
        else:
            return jsonify({"error": "Clave no proporcionada"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
