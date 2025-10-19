from fpdf import FPDF
from datetime import datetime
from src.database.db_mongo import get_historial_sensores
from io import BytesIO

# Agregar por encima de la descripcion "Descripción del estado actual de la colmena".
# Junto a esto tambien indicar los datos que estan presentando los sensores al momento de generar el reporte.
# Agregar por encima de la tabla "Datos registrados durante el día".

class ReporteColmena(FPDF):
    def __init__(self, fecha_actual=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fecha_actual = fecha_actual
        
    def fecha_a_texto(self, fecha_str):
        meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
        dt = datetime.strptime(fecha_str, "%d-%m-%Y")
        return f"{dt.day} de {meses[dt.month-1]}, {dt.year}"
    
    def header(self):
        self.add_font("Manrope-Bold", "", "./static/font/Manrope-Bold.ttf", uni=True)
        # Fecha (esquina superior izquierda)
        self.set_font("Manrope-Bold", "",12)
        self.cell(100, 10, f"{self.fecha_a_texto(self.fecha_actual)}", ln=False, align="L")

        # Imagen + Nombre de la app (esquina superior derecha)
        self.image("./static/images/logo-app.png", x=155, y=7, w=15)
        self.set_xy(172, 10)
        self.set_font("Manrope-Bold", "",12)
        self.cell(30, 10, "Monitor Beehive", ln=False, align="L")
        self.ln(20)

    def footer(self):
        self.add_font("Manrope", "", "./static/font/Manrope-Regular.ttf", uni=True)
        self.set_y(-15)
        self.set_font("Manrope", "",8)
        self.cell(0, 10, f"MonitorBeehive", align="C")
        
    def descripcion_estado(self, texto, sensores_actuales):
        self.add_font("Manrope-Bold", "", "./static/font/Manrope-Bold.ttf", uni=True)
        self.add_font("Manrope", "", "./static/font/Manrope-Regular.ttf", uni=True)
        # 🟡 Título de la sección
        self.set_font("Manrope-Bold", "",12)
        self.cell(0, 10, "Estado actual de la colmena.", ln=True)

        # 📝 Primero va la descripción textual
        self.set_font("Manrope", "", 12)
        self.multi_cell(0, 10, texto)
        self.ln(4)

        # 📈 Luego van los datos actuales del sensor
        sensores_texto = (
            f"Estado actual de la colmena a las {sensores_actuales['hora']} horas: "
            f"Temperatura: {sensores_actuales['temperatura']}°C, "
            f"Humedad: {sensores_actuales['humedad']}%, "
            f"Sonido: {sensores_actuales['sonido']} dB, "
            f"Peso: {sensores_actuales['peso']} kg."
        )
        self.multi_cell(0, 10, sensores_texto)
        self.ln(6)
        
    def descripcion_estado_historico(self, texto):
        self.add_font("Manrope-Bold", "", "./static/font/Manrope-Bold.ttf", uni=True)
        self.add_font("Manrope", "", "./static/font/Manrope-Regular.ttf", uni=True)
        # 🟡 Título de la sección
        self.set_font("Manrope-Bold", "",12)
        self.cell(0, 10, "Estado actual de la colmena.", ln=True)

        # 📝 Primero va la descripción textual
        self.set_font("Manrope", "", 12)
        self.multi_cell(0, 10, texto)
        self.ln(4)

    def tabla_registros(self, registros, columnas):
        self.add_font("Manrope-Bold", "", "./static/font/Manrope-Bold.ttf", uni=True)
        self.add_font("Manrope", "", "./static/font/Manrope-Regular.ttf", uni=True)
        # Título antes de la tabla
        self.set_font("Manrope-Bold", "",12)
        self.cell(0, 10, "Datos registrados durante el transcurso del día.", ln=True)
        self.ln(4)

        # Tabla
        col_width = (self.w - 2 * self.l_margin) / len(columnas)
        for col in columnas:
            self.cell(col_width, 10, col, border=1, align="C")
        self.ln()

        self.set_font("Manrope", "", 12)
        for fila in registros:
            for valor in fila:
                self.cell(col_width, 10, str(valor), border=1, align="C")
            self.ln()

def genera_pdf(registros, descripcion, datos_actuales, fecha_filtro):
    columnas = ["Hora", "Temperatura", "Humedad", "Peso"]
    if datos_actuales != "" and 'fecha' in datos_actuales[0] and fecha_filtro == "":
        fecha_actual = datos_actuales[0]['fecha']
    else:
        fecha_actual = fecha_filtro
    pdf = ReporteColmena(fecha_actual=fecha_actual)
    pdf.add_page()
    if datos_actuales == "":
        pdf.descripcion_estado_historico(descripcion)
    else:
        pdf.descripcion_estado(descripcion, datos_actuales[0])
    pdf.tabla_registros(registros, columnas)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_bytes)