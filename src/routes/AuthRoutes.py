from flask import Blueprint, request, jsonify
from src.database.db_mongo import add_apicultor, get_apicultor
from src.utils.tokenManagement import TokenManager

main = Blueprint("auth", __name__)

@main.route("/registrar-apicultor", methods=["POST"])
def registrar_apicultor():
    print(request.json)
    datos = request.json
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400

    try:
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
        apicultor = get_apicultor(datos["rut"], datos["password"])
        if not apicultor:
            return jsonify({"error": "Apicultor no encontrado"}), 404
        else:
            print("Apicultor encontrado:", apicultor)
            token = TokenManager.generar_token(apicultor)
            return jsonify({"token": token, "user": str(apicultor["_id"])}, 200)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
