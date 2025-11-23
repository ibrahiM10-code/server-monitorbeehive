from flask import Blueprint, request, jsonify
from src.database.db_mongo import get_colmena_device_serial, add_colmena_device_serial, get_colmenas_con_placa
from src.helpers.serializadores import serialize_colmenas_dvs

main = Blueprint("rpi", __name__)

@main.route("/registrar-placa", methods=["POST"])
def registra_placa():
    data = request.json
    serial = data["device_serial"]
    try:
        colmenas_con_placa = get_colmenas_con_placa()
        print(len(colmenas_con_placa))
        if len(colmenas_con_placa) > 0:
            existing = serialize_colmenas_dvs(get_colmena_device_serial(serial))
            print("EXISTING: ", existing)    
            if existing:
                return jsonify({"message": f"La colmena {existing[0]["colmena_id"]} ya tiene la placa {existing[0]["device_serial"]} asignada."}), 409
            else:
                count, colmena = add_colmena_device_serial(serial)
                colmena_serializada = serialize_colmenas_dvs(colmena)
                if count == 1:
                    return jsonify({"message": f"La placa {serial} ha sido asignada correctamente a {colmena_serializada[0]["nombre_colmena"]}.", "colmena_id": colmena_serializada[0]["colmena_id"]}), 201
        else:
            return jsonify({"message": "Todas las colmenas ya tienen una placa asignada."}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": e})