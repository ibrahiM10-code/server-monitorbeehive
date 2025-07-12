from flask import url_for

def serialize_colmenas(colmenas, ObjectId):
    for colmena in colmenas:
        colmena["_id"] = str(colmena["_id"])
        if "id_apicultor" in colmena and isinstance(colmena["id_apicultor"], ObjectId):
            colmena["id_apicultor"] = str(colmena["id_apicultor"])
        if "foto_colmena" in colmena and colmena["foto_colmena"]:
            colmena["foto_colmena_url"] = url_for('static', filename=colmena["foto_colmena"], _external=True)
            print("URL generada: ",colmena["foto_colmena_url"])
    return colmenas