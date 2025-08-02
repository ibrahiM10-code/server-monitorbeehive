from fpdf import FPDF
from datetime import datetime
from src.database.db_mongo import get_historial_sensores
from io import BytesIO

# Agregar por encima de la descripcion "Descripción del estado actual de la colmena".
# Junto a esto tambien indicar los datos que estan presentando los sensores al momento de generar el reporte.
# Agregar por encima de la tabla "Datos registrados durante el día".

class ReporteColmena(FPDF):
    def header(self):
        # Fecha (esquina superior izquierda)
        self.set_font("Arial", "B", 12)
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        self.cell(100, 10, f"Fecha: {fecha_actual}", ln=False, align="L")

        # Imagen + Nombre de la app (esquina superior derecha)
        self.image("./static/images/logo-app.png", x=155, y=7, w=15)  # Ajusta la ruta y tamaño
        self.set_xy(172, 10)
        self.set_font("Arial", "B", 12)
        self.cell(30, 10, "Monitor Beehive", ln=False, align="L")

        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def descripcion_estado(self, texto):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, texto)
        self.ln(6)

    def tabla_registros(self, registros, columnas):
        self.set_font("Arial", "B", 12)
        col_width = (self.w - 2 * self.l_margin) / len(columnas)

        # Encabezado
        for col in columnas:
            self.cell(col_width, 10, col, border=1, align="C")
        self.ln()

        # Filas
        self.set_font("Arial", "", 12)
        for fila in registros:
            for valor in fila:
                self.cell(col_width, 10, str(valor), border=1, align="C")
            self.ln()

def genera_pdf(registros, descripcion):
    columnas = ["Hora", "Temperatura", "Humedad", "Sonido", "Peso"]
    pdf = ReporteColmena()
    pdf.add_page()
    pdf.descripcion_estado(descripcion)
    pdf.tabla_registros(registros, columnas)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_bytes)