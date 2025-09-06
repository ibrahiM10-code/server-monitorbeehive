
def get_pipeline_sensores_colmena(apicultor_id):    
    sensores_colmena = [
        {
            "$lookup": {
                "from": "colmena",
                "localField": "colmena_id",
                "foreignField": "colmena_id",
                "as": "colmena_info"
            }
        },
        {
            "$unwind": "$colmena_info"
        },
        {
            "$match": {
                "colmena_info.id_apicultor": apicultor_id
            }
        },
        {
            "$project": {
                "_id": 1,
                "temperatura": 1,
                "humedad": 1,
                "fecha": 1,
                "colmena_id": 1,
                "hora": 1,
                "sonido": 1,
                "peso": 1,
                "id_apicultor": "$colmena_info.id_apicultor",
                "nombre_colmena": "$colmena_info.nombre_colmena",
                "nombre_apiario": "$colmena_info.nombre_apiario",
                "foto_colmena": "$colmena_info.foto_colmena"
            }
        }
    ]
    return sensores_colmena