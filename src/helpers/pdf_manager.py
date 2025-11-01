from fpdf import FPDF
from datetime import datetime
from src.database.db_mongo import get_historial_sensores
from io import BytesIO

class ReporteColmena(FPDF):
    def __init__(self, fecha_actual=None,*args, **kwargs):
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
        
    def descripcion_estado(self, texto, sensores_actuales, colmena_id):
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
                # Link CSV descargable.
        self.set_font("Manrope", "", 10)
        self.set_text_color(0, 0, 255)  # Blue color for the link
        csv_text = "Descargar datos en formato CSV"
        link = f"https://server-monitorbeehive.onrender.com/reportes/descargar-csv/{colmena_id}"  # You'll need to pass colmena_id
        text_width = self.get_string_width(csv_text)
        self.cell(text_width + 10, 10, csv_text, ln=True, link=link, border=0)  # Added width and removed align
        
        self.set_text_color(0, 0, 0)  # Reset to black
        self.ln(4)
        
    def descripcion_estado_historico(self, texto, colmena_id):
        self.add_font("Manrope-Bold", "", "./static/font/Manrope-Bold.ttf", uni=True)
        self.add_font("Manrope", "", "./static/font/Manrope-Regular.ttf", uni=True)
        # 🟡 Título de la sección
        self.set_font("Manrope-Bold", "",12)
        self.cell(0, 10, "Estado actual de la colmena.", ln=True)

        # 📝 Primero va la descripción textual
        self.set_font("Manrope", "", 12)
        self.multi_cell(0, 10, texto)
        self.ln(4)
        self.set_font("Manrope", "", 10)
        self.set_text_color(0, 0, 255)  # Blue color for the link
        csv_text = "Descargar datos en formato CSV"
        link = f"https://server-monitorbeehive.onrender.com/reportes/descargar-csv/{colmena_id}"  # You'll need to pass colmena_id
        text_width = self.get_string_width(csv_text)
        self.cell(text_width + 10, 10, csv_text, ln=True, link=link, border=0)  # Added width and removed align
        
        self.set_text_color(0, 0, 0)  # Reset to black
        self.ln(4)
    
    def lista_observaciones(self, observaciones):
        self.add_font("Manrope-Bold", "", "./static/font/Manrope-Bold.ttf", uni=True)
        self.add_font("Manrope", "", "./static/font/Manrope-Regular.ttf", uni=True)
        
        self.set_font("Manrope-Bold", "", 12)
        self.cell(0, 10, "Observaciones del apicultor:", ln=True)
        self.ln(2)
        
        self.set_font("Manrope", "", 12)
        
        if observaciones and len(observaciones) > 0:
            for observacion in observaciones:
                bullet_width = self.get_string_width("• ")
                self.cell(bullet_width, 10, "• ", ln=False)
                self.multi_cell(0, 10, observacion)
                self.ln(2)
        else:
            self.cell(0, 10, "No hay observaciones registradas.", ln=True)
        
        self.ln(4)

def genera_pdf(colmena_id, descripcion, datos_actuales, observaciones_reporte, fecha_filtro):
    if datos_actuales != "" and 'fecha' in datos_actuales[0] and fecha_filtro == "":
        fecha_actual = datos_actuales[0]['fecha']
    else:
        fecha_actual = fecha_filtro
    pdf = ReporteColmena(fecha_actual=fecha_actual)
    pdf.add_page()
    if datos_actuales == "":
        pdf.descripcion_estado_historico(descripcion, colmena_id)
    else:
        pdf.descripcion_estado(descripcion, datos_actuales[0], colmena_id)
    if not observaciones_reporte == None:
        observaciones_reporte = observaciones_reporte.split(",")
        pdf.lista_observaciones(observaciones_reporte)
    else:
        pdf.lista_observaciones(None)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_bytes)