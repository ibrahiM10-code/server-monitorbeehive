from bson import ObjectId
from flask import Blueprint, request, jsonify
from src.database.db_mongo import add_colmena, get_colmena_by_id_apicultor, update_colmena, delete_colmena, get_colmenas, get_colmena_particular, get_apicultor_by_id
from src.utils.tokenManagement import TokenManager
from src.helpers.serializadores import serialize_colmenas, serialize_colmenas_admin
from datetime import datetime

main = Blueprint("colmenas", __name__)

@main.route("/agregar-colmena", methods=["POST"])
def agregar_colmena():
    datos = request.form
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        if not datos:
            return jsonify({"error": "Datos no proporcionados"}), 400
        try:
            nombre_colmena = datos["nombre_colmena"]
            foto_colmena = request.files["foto_colmena"]
            ruta_foto_colmena = None
            if foto_colmena:
                fecha_actual = datetime.now().strftime("%Y%m%d")
                ruta_foto_colmena = f"images/{datos["nombre_colmena"].replace(" ","-")}-{fecha_actual}.jpeg"
                foto_colmena.save(f"static/{ruta_foto_colmena}")
            nueva_colmena = {
                "nombre_colmena": nombre_colmena,
                "nombre_apiario": datos["nombre_apiario"],
                "foto_colmena": ruta_foto_colmena,
                "id_apicultor": ObjectId(datos["id_apicultor"])
            }
            colmena_id = add_colmena(nueva_colmena, datetime.now().strftime("%d-%m-%Y"), datetime.now().strftime("%H:%M"))
            return jsonify({"message": "Colmena agregada exitosamente", "id": str(colmena_id)}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/obtener-colmenas/<string:id_apicultor>", methods=["GET"])
def obtener_colmenas(id_apicultor):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            rol_apicultor = get_apicultor_by_id(id_apicultor)
            if rol_apicultor["rol"] == "Apicultor":
                colmenas = get_colmena_by_id_apicultor(ObjectId(id_apicultor))
            elif rol_apicultor["rol"] == "Administrador":
                colmenas = get_colmenas()
            if not colmenas:
                return jsonify({"message": "No se encontraron colmenas para este apicultor"}), 204
            colmenas = serialize_colmenas(colmenas, ObjectId)
            return jsonify(colmenas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401
    
@main.route("/obtener-colmena-particular/<string:colmena_id>", methods=["GET"])
def obtener_colmena_particular(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            colmenas = get_colmena_particular(colmena_id=colmena_id)
            if not colmenas:
                return jsonify({"message": "No se encontraron colmenas con este id."}), 204
            colmenas = serialize_colmenas_admin(colmenas)
            return jsonify(colmenas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401

@main.route("/actualizar-colmena/<string:colmena_id>", methods=["PUT"])
def actualizar_colmena(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        datos = request.form    
        try:
            update_fields = {}
            if "nombre_colmena" in datos:
                update_fields["nombre_colmena"] = datos["nombre_colmena"]
            if "nombre_apiario" in datos:
                update_fields["nombre_apiario"] = datos["nombre_apiario"]
            if "foto_colmena" in request.files:
                foto_colmena = request.files["foto_colmena"]
                fecha_actual = datetime.now().strftime("%Y%m%d")
                ruta_foto_colmena = f"images/{datos['nombre_colmena'].replace(' ', '-')}-{fecha_actual}.jpeg"
                foto_colmena.save(f"static/{ruta_foto_colmena}")
                update_fields["foto_colmena"] = ruta_foto_colmena
            
            if not update_fields:
                return jsonify({"error": "No se proporcionaron campos para actualizar"}), 400
            
            modified_count = update_colmena(colmena_id, update_fields)
            if modified_count > 0:
                return jsonify({"message": "Colmena actualizada exitosamente"}), 200
            else:
                return jsonify({"message": "No se realizaron cambios en la colmena"}), 204
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401
    
@main.route("/eliminar-colmena/<string:colmena_id>", methods=["DELETE"])
def eliminar_colmena(colmena_id):
    acceso = TokenManager.verificar_token(request.headers)
    if acceso:
        try:
            deleted_count = delete_colmena(colmena_id)
            if deleted_count > 0:
                return jsonify({"message": "Colmena eliminada exitosamente", "documentos_eliminados": deleted_count}), 200
            else:
                return jsonify({"message": "No se encontró la colmena para eliminar"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Token inválido o expirado"}), 401