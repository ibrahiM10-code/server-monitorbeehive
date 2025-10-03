from bson import ObjectId

def get_pipeline_sensores_colmena_by_apicultor(apicultor_id):    
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

def get_pipeline_sensores_colmenas():    
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

def get_pipeline_sensores_colmena(colmena_id):    
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
            "$match": {"colmena_info.colmena_id": colmena_id}
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
                "analisis_sonido": 1,
                "id_apicultor": "$colmena_info.id_apicultor",
                "nombre_colmena": "$colmena_info.nombre_colmena",
                "nombre_apiario": "$colmena_info.nombre_apiario",
                "foto_colmena": "$colmena_info.foto_colmena"
            }
        }
    ]
    return sensores_colmena

def get_pipeline_sensores_by_dia(colmena_id):
    sensores_by_dia = [
        {
            "$match": {"colmena_id": colmena_id}    
        },
        {
            "$group": {
            "_id": { "fecha": "$fecha" },
            "temperatura_promedio": { "$avg": "$temperatura" },
            "humedad_promedio": { "$avg": "$humedad" },
            "peso_promedio": {"$avg": "$peso"},
            "count": { "$sum": 1 }
            }
        },
        {
            "$project": {
            "_id": 0,
            "fecha": "$_id.fecha",
            "temperatura_promedio": 1,
            "humedad_promedio": 1,
            "peso_promedio": 1,
            "count": 1
            }
        },
        { "$sort": { "fecha": 1 } }
    ]
    return sensores_by_dia