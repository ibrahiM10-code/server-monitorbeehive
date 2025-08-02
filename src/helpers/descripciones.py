mensajes = [
    {
        "estado_optimo": "La colmena presenta condiciones óptimas: el peso sugiere una buena producción de miel, la temperatura y la humedad interna están dentro del rango ideal, y el sonido captado confirma la presencia de la abeja reina y una colonia estable. No se requieren acciones inmediatas."
    },
    {
        "peso_bajo": "El peso de la colmena es inferior al ideal, lo que podría indicar baja actividad productiva o escasez de miel. Sin embargo, la temperatura, la humedad y el sonido interno se encuentran en niveles adecuados, lo que sugiere que la salud general de la colonia se mantiene. Se recomienda monitorear la evolución del peso en los próximos días."
    },
    {
        "peso_alto": "El peso de la colmena es elevado, lo que podría indicar una producción abundante de miel. La temperatura y humedad son óptimas, y el sonido asegura la presencia de la reina. Se sugiere preparar una revisión para posible cosecha y asegurar que la estructura soporte el peso."
    },
    {
        "temperatura_alta": "Se ha detectado una temperatura interna superior al rango ideal, lo que puede causar estrés térmico en la colonia. No obstante, el peso, la humedad y el sonido están en niveles adecuados, y la reina sigue presente. Se recomienda verificar la ventilación de la colmena o proporcionar sombra temporal."
    },
    {
        "temperatura_baja": "La temperatura interna se encuentra por debajo de los niveles ideales, lo que podría afectar el desarrollo de la cría. Sin embargo, el peso es adecuado, la humedad está controlada y el sonido indica estabilidad en la colonia. Se recomienda evaluar el aislamiento de la colmena."
    },
    {
        "humedad_alta": "Se detecta un nivel alto de humedad, lo cual podría favorecer la aparición de hongos. Aun así, la temperatura es correcta, el peso indica buena actividad, y el sonido asegura la presencia de la reina. Revisa la ventilación y posibles fuentes de condensación."
    },
    {
        "humedad_baja": "La humedad es inferior al rango esperado, lo que puede interferir con el desarrollo de la cría. No obstante, el resto de parámetros (peso, temperatura, sonido) son óptimos. Monitorea la evolución de la humedad y considera revisar el entorno climático externo."
    },
    {
        "sonido_anomalo": "El sonido detectado presenta patrones que podrían indicar la ausencia de la abeja reina. A pesar de ello, el peso, la temperatura y la humedad se mantienen dentro de los valores adecuados. Se recomienda realizar una inspección visual para confirmar la situación"
    },
    {
        "peso_bajo_temp_alta": "El peso de la colmena es inferior al ideal, indicando baja reserva de miel o baja actividad. Además, la temperatura interna está por encima del rango óptimo, lo que puede causar estrés térmico. Por otro lado, la humedad y el sonido interno se encuentran en niveles adecuados, y la abeja reina sigue presente. Se recomienda inspección para evaluar alimentación y ventilación."
    },
    {
        "peso_bajo_temp_baja": "El peso de la colmena es inferior al ideal, indicando baja reserva de miel o baja actividad. Además, la temperatura interna está por debajo del rango óptimo. Por otro lado, la humedad y el sonido interno se encuentran en niveles adecuados, y la abeja reina sigue presente. Se recomienda inspección para evaluar alimentación y ventilación."
    },
    {
        "peso_bajo_hum_alta": "La colmena muestra peso bajo, lo cual sugiere escasas reservas. También se observa humedad elevada, lo que podría favorecer hongos y enfermedades. Aún así, la temperatura y el sonido son óptimos, y la reina permanece activa. Se sugiere revisar la ventilación y considerar suplementación alimenticia"
    },
    {
        "peso_bajo_hum_baja": "La colmena muestra peso bajo, lo cual sugiere escasas reservas. También se observa humedad baja, lo que puede afectar en el desarrollo de las crías. Aún así, la temperatura y el sonido son óptimos, y la reina permanece activa. Se sugiere revisar la ventilación y considerar suplementación alimenticia."
    },
    {
        "peso_bajo_sonido_anomalo": "Hay un peso insuficiente en la colmena y el sonido detectado es anómalo, lo que podría indicar ausencia de la reina. La temperatura y humedad, sin embargo, están en rangos ideales. Esto sugiere un riesgo mayor a nivel de estructura social: es recomendable inspección urgente para verificar presencia de la reina y reforzar la colmena."
    },
    {
        "temp_alta_hum_alta": "Tanto la temperatura como la humedad están por encima de los niveles óptimos, creando un ambiente potencialmente perjudicial para la colonia. No obstante, el peso indica buena producción y el sonido confirma la presencia de la reina. Será necesario mejorar ventilación y corregir el microclima."
    },
    {
        "temp_alta_hum_baja": "La temperatura está por encima de los niveles óptimos, creando un ambiente potencialmente perjudicial para la colonia, mientras que la humedad presenta un nivel por debajo del óptimo. No obstante, el peso indica buena producción y el sonido confirma la presencia de la reina. Será necesario mejorar ventilación y corregir el microclima."
    },
    {
        "temp_baja_hum_baja": "La temperatura está por debajo del rango ideal, y la humedad también es baja, lo que puede comprometer la incubación y salud de las crías. El peso se mantiene adecuado y el sonido indica presencia de la reina. Se recomienda evaluar el aislamiento y condiciones climáticas externas."
    },
    {
        "temp_baja_hum_alta": "La temperatura interna es baja, lo que puede afectar el desarrollo de la cría, mientras que la humedad es alta, lo que podría favorecer hongos. El peso es adecuado y el sonido indica la presencia de la abeja reina. Se recomienda evaluar el aislamiento y la ventilación para equilibrar las condiciones internas."
    },
    {
        "temp_alta_sonido_anomalo": "La temperatura interna está elevada y el sonido registrado presenta anomalías, posiblemente por ausencia de reina o estrés en la colonia. Sin embargo, el peso es adecuado y la humedad está dentro del rango ideal. Recomendamos inspección visual inmediata y evaluar ventilación o sombra."
    },
    {
        "temp_baja_sonido_anomalo": "Se observa temperatura interna baja, junto con un patrón de sonido irregular que podría deberse a falta de reina o colmena debilitada. El peso y la humedad, en cambio, están en rango óptimo. Conviene realizar inspección visual y mejorar el aislamiento."
    },
    {
        "hum_alta_sonido_anomalo": "Se detecta alta humedad dentro de la colmena junto con ruido anómalo que podría indicar falta de reina. El peso y la temperatura continúan estables y óptimos. Ante estos indicadores, resulta crítico revisar tanto el microclima como el estado de la estructura social."
    },
    {
        "hum_baja_sonido_anomalo": "La humedad en la colmena es inferior a lo esperado, y el sonido indica posible ausencia de reina. No obstante, el peso y la temperatura siguen adecuados. Este escenario requerirá revisión del entorno y del estado de la colonia."
    },
    {
        "peso_bajo_temp_alta_hum_alta": "Se registran tres condiciones adversas: peso bajo, temperatura y humedad elevadas. Esto crea un ambiente múltiple de riesgo para la colonia. Solo el sonido se mantiene dentro de lo esperado, lo que indica posible presencia de reina. Es imprescindible una inspección exhaustiva y corrección del microclima e hidratación."
    },
    {
        "peso_bajo_temp_alta_sonido_anomalo": "Peso inadecuado, temperatura alta y sonido irregular (posible ausencia de reina) representan una situación crítica. Solo la humedad se encuentra óptima. Requiere intervención urgente en alimentación, ventilación y revisión de la reina."
    },
    {
        "peso_bajo_hum_alta_sonido_anomalo": "Peso bajo, humedad elevada y sonido anómalo son señales de un estado preocupante. Solo la temperatura se mantiene estable. Es urgente revisar estructura sanitaria, presencia de la reina y condiciones de humedad."
    },
    {
        "temp_alta_hum_alta_sonido_anomalo": "Tres indicadores fuera de rango: temperatura elevada, humedad excesiva y ruido anómalo. El peso, sin embargo, sigue siendo adecuado. Se requiere revisar ventilación, microclima, e inspección de la reina."
    },
    {
        "temp_baja_hum_baja_sonido_anomalo": "La temperatura y humedad están por debajo de los niveles necesarios y, además, el sonido evidencia posibles problemas estructurales en la colmena. Solo el peso permanece óptimo. Se sugiere aislamiento, humidificación y verificación de la colonia."
    },
    {
        "caso_critico": "El peso es insuficiente, la temperatura y humedad no están en rango, y el sonido interno sugiere posible ausencia de abeja reina. Este es un caso de máximo riesgo: la colmena se encuentra en estado crítico y necesita intervención inmediata para evitar la pérdida de la colonia."
    }
]