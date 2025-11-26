from flask import Blueprint, request, jsonify
from src.database.db_mongo import add_apicultor, get_apicultor, get_apicultor_email, reset_password, add_push_token
from src.utils.tokenManagement import TokenManager
from src.helpers.encriptar_clave import encriptar_clave
from src.helpers.evaluar_clave import evaluar_clave
from src.helpers.enviar_correo import enviar_correo

main = Blueprint("auth", __name__)

@main.route("/registrar-administrador", methods=["POST"])
def registrar_administrador():
    datos = request.json
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400

    try:
        datos["password"] = encriptar_clave(datos["password"])
        datos["rol"] = "Administrador"
        id_apicultor = add_apicultor(datos)
        return jsonify({"message": "Apicultor registrado exitosamente", "id": str(id_apicultor)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/registrar-apicultor", methods=["POST"])
def registrar_apicultor():
    datos = request.json
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400

    try:
        datos["password"] = encriptar_clave(datos["password"])
        datos["rol"] = "Apicultor"
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
            return jsonify({"token": token, "user": str(apicultor["_id"]), "rol": apicultor["rol"]}, 200)
        else:
            return jsonify({"error": "Clave no proporcionada"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/envia-correo-codigo", methods=["POST"])
def envia_correo_codigo():
    datos = request.json
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400
    try:
        apicultor = get_apicultor(datos["rut"])
        if not apicultor:
            return jsonify({"error": "No existe un apicultor registrado con este rut."}), 404
        else:
            resultado = enviar_correo(apicultor["email"], datos["codigo"])
            if resultado:
                return jsonify({"message": "Correo enviado existosamente.", "email": apicultor["email"]}), 200
            else:
                return jsonify({"error": "El correo no ha podido ser enviado correctamente"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route("/resetear-clave", methods=["POST"])
def resetear_clave():
    datos = request.json
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400
    try:
        nueva_password_encriptada = encriptar_clave(datos["nueva_password"])
        reseteo = reset_password(datos["email"], nueva_password_encriptada)
        if reseteo != 1:
            return jsonify({"error": "La clave  no ha podido ser reseteada correctamente"}), 400
        else:
            return jsonify({"message": "Clave de apicultor reseteada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route("/registra-expo-push-token", methods=["POST"])
def registra_expo_push_token():
    acceso = TokenManager.verificar_token(request.headers);
    datos = request.json
    print(datos)
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400
    if acceso:
        try:
            agregar_push_token = add_push_token(datos["userId"], datos["expoPushToken"])
            print(agregar_push_token)
            if agregar_push_token != 1:
                return jsonify({"error": "No se ha podido agregar el push token correctamente."}), 400
            else:
                return jsonify({"message": "expoPushToken asignado a apicultor correctamente."}), 200
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500