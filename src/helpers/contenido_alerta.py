from datetime import datetime

def contenido_alerta(nombre_colmena):
    contenido_alerta = {
        "temperatura": [
            {
                "temperatura_baja": 
                    {
                        "titulo": "Temperatura baja", 
                        "descripcion": f"La temperatura interna de {nombre_colmena} está por debajo de lo esperado.",
                        "tipo_alerta": "advertencia",
                        "estado_alerta": "pendiente",
                        "fecha": datetime.now().strftime("%d-%m-%Y")
                    }
            },
            {
                "temperatura_alta": 
                    {
                        "titulo": "Temperatura alta", 
                        "descripcion": f"La temperatura interna de {nombre_colmena} es superior al rango óptimo.",
                        "tipo_alerta": "advertencia",
                        "estado_alerta": "pendiente",
                        "fecha": datetime.now().strftime("%d-%m-%Y")
                    }
            },
            {
                "temperatura_optima": 
                    {
                        "titulo": "Temperatura optima", 
                        "descripcion": f"La temperatura está dentro del rango ideal para la salud de {nombre_colmena}.",
                        "tipo_alerta": "informativa",
                        "estado_alerta": "pendiente",
                        "fecha": datetime.now().strftime("%d-%m-%Y")
                    }
            }
        ],
        "humedad": [
            {
                "humedad_baja":
                    {
                        "titulo": "Humedad baja",
                        "descripcion": f"La humedad interna de {nombre_colmena} es menor a la necesaria para un desarrollo saludable de la cría",
                        "tipo_alerta": "advertencia",
                        "estado_alerta": "pendiente",
                        "fecha": datetime.now().strftime("%d-%m-%Y")
                    }
            },
            {
                "humedad_alta":
                    {
                        "titulo": "Humedad alta",
                        "descripcion": f"Elevado nivel de humedad en {nombre_colmena}, puede causar aparición de hongos y enfermedades.",
                        "tipo_alerta": "advertencia",
                        "estado_alerta": "pendiente",
                        "fecha": datetime.now().strftime("%d-%m-%Y")
                    }
            },
            {
                "humedad_optima":
                    {
                        "titulo": "Humedad optima",
                        "descripcion": f"Humedad dentro del rango ideal para la salud de {nombre_colmena}.",
                        "tipo_alerta": "informativa",
                        "estado_alerta": "pendiente",
                        "fecha": datetime.now().strftime("%d-%m-%Y")
                    }
            }
        ],
        "peso": [
            {
                "peso_bajo":
                    {
                        "titulo": "Peso bajo",
                        "descripcion": f"El peso de {nombre_colmena} podría indicar una baja productividad o una escasa reserva de miel.",
                        "tipo_alerta": "advertencia",
                        "estado_alerta": "pendiente",
                        "fecha": datetime.now().strftime("%d-%m-%Y")
                    }
            },
            {
                "peso_optimo":
                    {
                        "titulo": "Peso optimo",
                        "descripcion": f"El peso de {nombre_colmena} indica la posibilidad de extracción de miel.",
                        "tipo_alerta": "informativa",
                        "estado_alerta": "pendiente",
                        "fecha": datetime.now().strftime("%d-%m-%Y")
                    }
            }
        ]
    }
    return contenido_alerta