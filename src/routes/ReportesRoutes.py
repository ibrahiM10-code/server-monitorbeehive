from flask import Blueprint, request, jsonify,send_file
from src.database.db_mongo import get_historial_sensores, get_datos_sensores, add_reporte
from src.utils.tokenManagement import TokenManager
from src.helpers.pdf_manager import genera_pdf
from src.helpers.evaluar_sensores import clasificar_estado_sensores, evalua_datos_sensores

main = Blueprint("reportes", __name__)

@main.route("/obtener-reporte/<string:colmena_id>", methods=["GET"])
def obtener_reporte(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            print("Getting historial sensores")
            datos_historicos = get_historial_sensores(colmena_id)
            print("Getting datos actuales")
            datos_actuales = get_datos_sensores(colmena_id)
            print("Generating registros")
            if not datos_historicos or not datos_actuales:
                return jsonify({"message": "No se encontraron datos de sensores para esta colmena"}), 200
            registros = [
                [r['hora'], r['temperatura'] + " °C", r['humedad'] + "%", r['sonido'] +  "mhz", r['peso'] + "kg"] for r in datos_historicos
            ]
            print("Clasifying sensor data")
            datos_clasificados = clasificar_estado_sensores(temperatura=int(datos_actuales[0]['temperatura']),
                                                      humedad=int(datos_actuales[0]['humedad']),
                                                      peso_diario=float(datos_actuales[0]['peso']),
                                                      sonido=datos_actuales[0]['analisis_sonido'])
            print("Evaluating sensor data")
            descripcion = evalua_datos_sensores(datos_clasificados)
            print("Adding report to database")
            add_reporte(colmena_id, descripcion)
            print("Generating PDF")
            pdf_stream  = genera_pdf(registros, descripcion, datos_actuales)
            print("Sending file")
            pdf_stream.seek(0)
            return send_file(pdf_stream, mimetype="application/pdf", as_attachment=True, download_name="reporte_colmena.pdf")
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401

# Agregar ruta que permita enviar la descripcion del estado actual de la colmena.
@main.route("descripcion-colmena/<string:colmena_id>", methods=["GET"])
def descripcion_colmena(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            datos_actuales = get_datos_sensores(colmena_id)
            if not datos_actuales:
                return jsonify({"message": "No se encontraron datos de sensores para esta colmena"}), 200
            datos_clasificados = clasificar_estado_sensores(temperatura=int(datos_actuales[0]['temperatura']),
                                                      humedad=int(datos_actuales[0]['humedad']),
                                                      peso_diario=float(datos_actuales[0]['peso']),
                                                      sonido=datos_actuales[0]['analisis_sonido'])
            descripcion = evalua_datos_sensores(datos_clasificados)
            return jsonify({"descripcion": descripcion}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401