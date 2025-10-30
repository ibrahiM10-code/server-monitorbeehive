import csv

def generar_csv(registros_sensores: list):
    with open("out.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Hora", "Temperatura", "Humedad", "Peso"])
        writer.writerows(registros_sensores)