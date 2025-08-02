from src.helpers.descripciones import mensajes

def evalua_datos_sensores(datos_sensores):
    match datos_sensores:
        case {"peso": p, "temperatura": t, "humedad": h, "sonido": s} if p == "optimo" and t == "optimo" and h == "optimo" and s == "optimo":
            return mensajes[0]["estado_optimo"]
        case {"peso": "bajo", "temperatura": "optimo", "humedad": "optimo", "sonido": "optimo"}:
            return mensajes[1]["peso_bajo"]
        case {"peso": "alto", "temperatura": "optimo", "humedad": "optimo", "sonido": "optimo"}:
            return mensajes[2]["peso_alto"]
        case {"peso": "optimo", "temperatura": "alta", "humedad": "optimo", "sonido": "optimo"}:
            return mensajes[3]["temperatura_alta"]
        case {"peso": "optimo", "temperatura": "baja", "humedad": "optimo", "sonido": "optimo"}:
            return mensajes[4]["temperatura_baja"]
        case {"peso": "optimo", "temperatura": "optimo", "humedad": "alta", "sonido": "optimo"}:
            return mensajes[5]["humedad_alta"]
        case {"peso": "optimo", "temperatura": "optimo", "humedad": "baja", "sonido": "optimo"}:
            return mensajes[6]["humedad_baja"]
        case {"peso": "optimo", "temperatura": "optimo", "humedad": "optimo", "sonido": "anomalo"}:
            return mensajes[7]["sonido_anomalo"]
        case {"peso": "bajo", "temperatura": "alta", "humedad": "optimo", "sonido": "optimo"}:
            return mensajes[8]["peso_bajo_temp_alta"]
        case {"peso": "bajo", "temperatura": "baja", "humedad": "optimo", "sonido": "optimo"}:
            return mensajes[9]["peso_bajo_temp_baja"]
        case {"peso": "bajo", "temperatura": "optimo", "humedad": "alta", "sonido": "optimo"}:
            return mensajes[10]["peso_bajo_hum_alta"]
        case {"peso": "bajo", "temperatura": "optimo", "humedad": "baja", "sonido": "optimo"}:
            return mensajes[11]["peso_bajo_hum_baja"]
        case {"peso": "bajo", "temperatura": "optimo", "humedad": "optimo", "sonido": "anomalo"}:
            return mensajes[12]["peso_bajo_sonido_anomalo"]
        case {"peso": "optimo", "temperatura": "alta", "humedad": "alta", "sonido": "optimo"}:
            return mensajes[13]["temp_alta_hum_alta"]
        case {"peso": "optimo", "temperatura": "alta", "humedad": "baja", "sonido": "optimo"}:
            return mensajes[14]["temp_alta_hum_baja"]
        case {"peso": "optimo", "temperatura": "baja", "humedad": "baja", "sonido": "optimo"}:
            return mensajes[15]["temp_baja_hum_baja"]
        case {"peso": "optimo", "temperatura": "baja", "humedad": "alta", "sonido": "optimo"}:
            return mensajes[16]["temp_baja_hum_alta"]
        case {"peso": "optimo", "temperatura": "alta", "humedad": "optimo", "sonido": "anomalo"}:
            return mensajes[17]["temp_alta_sonido_anomalo"]
        case {"peso": "optimo", "temperatura": "baja", "humedad": "optimo", "sonido": "anomalo"}:
            return mensajes[18]["temp_baja_sonido_anomalo"]
        case {"peso": "optimo", "temperatura": "optimo", "humedad": "alta", "sonido": "anomalo"}:
            return mensajes[19]["hum_alta_sonido_anomalo"]
        case {"peso": "optimo", "temperatura": "optimo", "humedad": "baja", "sonido": "anomalo"}:
            return mensajes[20]["hum_baja_sonido_anomalo"]
        case {"peso": "bajo", "temperatura": "alta", "humedad": "alta", "sonido": "optimo"}:
            return mensajes[21]["peso_bajo_temp_alta_hum_alta"]
        case {"peso": "bajo", "temperatura": "alta", "humedad": "optimo", "sonido": "anomalo"}:
            return mensajes[22]["peso_bajo_temp_alta_sonido_anomalo"]
        case {"peso": "bajo", "temperatura": "optimo", "humedad": "alta", "sonido": "anomalo"}:
            return mensajes[23]["peso_bajo_hum_alta_sonido_anomalo"]
        case {"peso": "optimo", "temperatura": "alta", "humedad": "alta", "sonido": "anomalo"}:
            return mensajes[24]["temp_alta_hum_alta_sonido_anomalo"]
        case {"peso": "optimo", "temperatura": "baja", "humedad": "baja", "sonido": "anomalo"}:
            return mensajes[25]["temp_baja_hum_baja_sonido_anomalo"]
        case {"peso": "bajo", "temperatura": "baja", "humedad": "baja", "sonido": "anomalo"}:
            return mensajes[-1]["caso_critico"]
        case _:
            return mensajes[-1]["caso_critico"]
        
def clasificar_estado_sensores(temperatura, humedad, peso_diario, sonido):
    # Clasificación de temperatura (°C)
    if temperatura < 33:
        temp_estado = "baja"
    elif temperatura > 35:
        temp_estado = "alta"
    else:
        temp_estado = "optimo"

    # Clasificación de humedad relativa (%)
    if humedad < 40:
        hum_estado = "baja"
    elif humedad > 70:
        hum_estado = "alta"
    else:
        hum_estado = "optimo"

    # Clasificación de peso diario (kg)
    if peso_diario <= 0.3:
        peso_estado = "bajo"
    else:
        peso_estado = "optimo"

    # Clasificación de sonido
    if sonido == "con reina":
        sonido_estado = "optimo"
    else:
        sonido_estado = "anomalo"

    return {
        "peso": peso_estado,
        "temperatura": temp_estado,
        "humedad": hum_estado,
        "sonido": sonido_estado
    }