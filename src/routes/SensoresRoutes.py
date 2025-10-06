from flask import Blueprint, request, jsonify
# Se asume que 'get_historial_sensores' ya está disponible en db_mongo
from src.database.db_mongo import get_datos_sensores, update_datos_sensores, add_historial_sensores, get_ultimos_historial_sensores, get_historial_diario, get_historial_sensores 
from src.utils.tokenManagement import TokenManager
from src.helpers.serializadores import serialize_sensores, serialize_historial_sensores_diario

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

# --- RUTA MODIFICADA: Ahora obtiene el historial COMPLETO para el gráfico ---
@main.route("/obtener-historial-completo/<string:colmena_id>", methods=["GET"])
def obtener_historial_completo(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            # 🚨 CAMBIO CLAVE: Llama a la función que obtiene TODO el historial (para el gráfico)
            historial_sensores = get_historial_sensores(colmena_id)
            
            if not historial_sensores:
                return jsonify({"message": "No se encontraron datos históricos para esta colmena"}), 404
            
            # 'serialize_sensores' convierte el 'timestamp' a 'fecha' (ISO 8601)
            historial_sensores = serialize_sensores(historial_sensores)
            return jsonify(historial_sensores), 200
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Token inválido o expirado"}), 401
# -------------------------------------------------------------------------

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
            print(e)
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/actualizar-sensores/<string:colmena_id>", methods=["PUT"])
def actualizar_sensores(colmena_id):
    datos = request.json
    if not datos:
        return jsonify({"error": "Datos no proporcionados"}), 400
        
    # 🚨 RECOMENDACIÓN DE SEGURIDAD: Añadir verificación de clave/token de dispositivo si es posible.
    # Por ejemplo, verificar un 'Device-Token' en los headers.
    
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
            
        # 🚨 Importante: Incluir 'fecha' y 'hora' para que 'update_datos_sensores' pueda crear el 'timestamp'
        if "fecha" in datos:
            update_fields["fecha"] = datos["fecha"]
        if "hora" in datos:
            update_fields["hora"] = datos["hora"]
            
        if "analisis_sonido" in datos:
            update_fields["analisis_sonido"] = datos["analisis_sonido"]
            
        resultado = update_datos_sensores(colmena_id, update_fields)
        if resultado:
            # Asegura que el historial se agregue con los mismos campos (incluyendo fecha/hora)
            add_historial_sensores(colmena_id, update_fields)
            return jsonify({"message": "Datos de sensores actualizados exitosamente"}), 200
        else:
            return jsonify({"error": "No se encontró el sensor con el ID proporcionado"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500