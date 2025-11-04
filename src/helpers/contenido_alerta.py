from datetime import datetime

contenido_alerta = {
    "temperatura": [
        {
            "temperatura_baja": 
                {
                    "titulo": "Temperatura baja", 
                    "descripcion": "La temperatura interna de colmena está por debajo de lo esperado.",
                    "tipo_alerta": "advertencia",
                    "estado_alerta": "pendiente",
                    "fecha": str(datetime.now().strftime("%d-%m-%Y"))
                 }
        },
        {
            "temperatura_alta": 
                {
                    "titulo": "Temperatura alta", 
                    "descripcion": "La temperatura interna de colmena es superior al rango óptimo.",
                    "tipo_alerta": "advertencia",
                    "estado_alerta": "pendiente",
                    "fecha": str(datetime.now().strftime("%d-%m-%Y"))
                 }
        },
        {
            "temperatura_optima": 
                {
                    "titulo": "Temperatura optima", 
                    "descripcion": "La temperatura está dentro del rango ideal para la salud de colmena.",
                    "tipo_alerta": "informativa",
                    "estado_alerta": "pendiente",
                    "fecha": str(datetime.now().strftime("%d-%m-%Y"))
                 }
        }
    ],
    "humedad": [
        {
            "humedad_baja":
                {
                    "titulo": "Humedad baja",
                    "descripcion": "La humedad interna de colmena es menor a la necesaria para un desarrollo saludable de la cría",
                    "tipo_alerta": "advertencia",
                    "estado_alerta": "pendiente",
                    "fecha": str(datetime.now().strftime("%d-%m-%Y"))
                }
        },
        {
            "humedad_alta":
                {
                    "titulo": "Humedad alta",
                    "descripcion": "Elevado nivel de humedad en colmena, puede causar aparición de hongos y enfermedades.",
                    "tipo_alerta": "advertencia",
                    "estado_alerta": "pendiente",
                    "fecha": str(datetime.now().strftime("%d-%m-%Y"))
                }
        },
        {
            "humedad_optima":
                {
                    "titulo": "Humedad optima",
                    "descripcion": "Humedad dentro del rango ideal para la salud de colmena.",
                    "tipo_alerta": "informativa",
                    "estado_alerta": "pendiente",
                    "fecha": str(datetime.now().strftime("%d-%m-%Y"))
                }
        }
    ],
    "peso": [
        {
            "peso_bajo":
                {
                    "titulo": "Peso bajo",
                    "descripcion": "El peso de colmena podría indicar una baja productividad o una escasa reserva de miel.",
                    "tipo_alerta": "advertencia",
                    "estado_alerta": "pendiente",
                    "fecha": str(datetime.now().strftime("%d-%m-%Y"))
                }
        },
        {
            "peso_optimo":
                {
                    "titulo": "Peso optimo",
                    "descripcion": "El peso de colmena indica la posibilidad de extracción de miel.",
                    "tipo_alerta": "informativa",
                    "estado_alerta": "pendiente",
                    "fecha": str(datetime.now().strftime("%d-%m-%Y"))
                }
        }
    ]
}