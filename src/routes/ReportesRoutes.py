from flask import Blueprint, request, jsonify,send_file
from src.database.db_mongo import get_historial_sensores, get_datos_sensores, add_reporte, get_reportes, get_historial_sensores_by_fecha, get_reportes_by_fecha, get_colmena_info
from src.utils.tokenManagement import TokenManager
from src.helpers.pdf_manager import genera_pdf
from src.helpers.evaluar_sensores import clasificar_estado_sensores, evalua_datos_sensores
from src.helpers.serializadores import serialize_reportes, serialize_sensores
from src.helpers.generar_csv import generar_csv
from bson import ObjectId, Decimal128
from io import StringIO, BytesIO
import csv
main = Blueprint("reportes", __name__)

@main.route("/obtener-reporte/<string:colmena_id>/<string:apicultor_id>", methods=["GET"])
def obtener_reporte(colmena_id, apicultor_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            print("Getting historial sensores")
            datos_historicos = serialize_sensores(get_historial_sensores(colmena_id))
            print("Datos Historicos: ", datos_historicos)
            print("Getting datos actuales")
            datos_actuales = serialize_sensores(get_datos_sensores(colmena_id))
            print("Generating registros")
            if not datos_historicos or not datos_actuales:
                return jsonify({"message": "No se encontraron datos de sensores para esta colmena"}), 404
            registros = [
                [r['hora'], str(r['temperatura']) + " °C", str(r['humedad']) + "%", str(r['peso']) + "kg"] for r in datos_historicos
            ]
            print(datos_actuales)
            print("Clasifying sensor data")
            datos_clasificados = clasificar_estado_sensores(temperatura=int(datos_actuales[0]['temperatura']),
                                                      humedad=int(datos_actuales[0]['humedad']),
                                                      peso_diario=float(datos_actuales[0]['peso']))
            print("Evaluating sensor data")
            descripcion = evalua_datos_sensores(datos_clasificados)
            # print("Adding report to database")
            # add_reporte(colmena_id, descripcion, apicultor_id)
            print("Generating PDF")
            pdf_stream  = genera_pdf(colmena_id, descripcion, datos_actuales, fecha_filtro="")
            print("Sending file")
            pdf_stream.seek(0)
            return send_file(pdf_stream, mimetype="application/pdf", as_attachment=True, download_name="reporte_colmena.pdf")
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/descargar-csv/<string:colmena_id>", methods=["GET"])
def descargar_csv(colmena_id):

    try:
        datos_historicos = serialize_sensores(get_historial_sensores(colmena_id))
        if not datos_historicos:
            return jsonify({"message": "No se encontraron datos para esta colmena"}), 404

        string_io = StringIO()
        writer = csv.writer(string_io)
        writer.writerow(["Hora", "Temperatura", "Humedad", "Peso"])
        for dato in datos_historicos:
            writer.writerow([
                dato['hora'],
                str(dato['temperatura']),
                str(dato['humedad']),
                str(dato['peso'])
            ])
            
        # Convert to bytes and create BytesIO
        output = BytesIO()
        output.write(string_io.getvalue().encode('utf-8'))
        output.seek(0)

        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'datos_colmena_{colmena_id}.csv'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/descripcion-colmena/<string:colmena_id>", methods=["GET"])
def descripcion_colmena(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            datos_actuales = get_datos_sensores(colmena_id)
            if not datos_actuales:
                return jsonify({"message": "No se encontraron datos de sensores para esta colmena"}), 404
            datos_clasificados = clasificar_estado_sensores(temperatura=float(datos_actuales[0]['temperatura']),
                                                      humedad=float(datos_actuales[0]['humedad']),
                                                      peso_diario=float(datos_actuales[0]['peso']),
                                                      )
            descripcion = evalua_datos_sensores(datos_clasificados)
            return jsonify({"descripcion": descripcion}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401
    
@main.route("/reportes-colmenas/<string:apicultor_id>", methods=["GET"])
def get_reportes_colmenas(apicultor_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            reportes = get_reportes(ObjectId(apicultor_id))
            if not reportes:
                return jsonify({"message": "No se encontraron reportes para esta colmena."}), 204
            reportes_serializados = serialize_reportes(reportes, ObjectId)
            
            for reporte in reportes_serializados:
                colmena_id = reporte['colmena_id']
                colmena_info = get_colmena_info(colmena_id)
                reporte.update(colmena_info)
            return jsonify(reportes_serializados), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401
    
@main.route("/descargar-reporte/<string:colmena_id>/<string:fecha_filtro>", methods=["GET"])
def descargar_reporte(colmena_id, fecha_filtro):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            datos_historicos = get_historial_sensores_by_fecha(colmena_id, fecha_filtro)
            if not datos_historicos:
                return jsonify({"message": "No se encontraron datos de sensores para esta colmena en la fecha especificada"}), 404
            reporte_consultado = get_reportes_by_fecha(colmena_id, fecha_filtro)
            if not reporte_consultado:
                return jsonify({"message": "No se encontraron reportes para esta colmena en la fecha especificada"}), 404
            descripcion = reporte_consultado[0]['descripcion']
            pdf_stream  = genera_pdf(colmena_id, descripcion, datos_actuales="", fecha_filtro=fecha_filtro)
            print("Sending file")
            pdf_stream.seek(0)
            return send_file(pdf_stream, mimetype="application/pdf", as_attachment=True, download_name="reporte_colmena.pdf")
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401
    
@main.route("/filtrar-reportes/<string:colmena_id>/<string:fecha_filtro>", methods=["GET"])
def filtrar_reportes(colmena_id, fecha_filtro):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            reportes = get_reportes_by_fecha(colmena_id, fecha_filtro)
            if not reportes:
                return jsonify({"message": "No se encontraron reportes para esta colmena en la fecha especificada"}), 204
            reportes_serializados = serialize_reportes(reportes, ObjectId)
            for reporte in reportes_serializados:
                colmena_id = reporte['colmena_id']
                colmena_info = get_colmena_info(colmena_id)
                reporte.update(colmena_info)
            return jsonify(reportes_serializados), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401