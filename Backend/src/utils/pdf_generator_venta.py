# src/utils/pdf_generator_venta.py

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from datetime import datetime


def generar_pdf_ventas(data, nombre_archivo="reporte_ventas.pdf"):
    """
    Genera un PDF en formato tabla para un reporte de ventas.
    data → lista de diccionarios
    """

    carpeta = "PDFS"
    os.makedirs(carpeta, exist_ok=True)
    ruta_pdf = os.path.join(carpeta, nombre_archivo)

    # Crear documento
    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
    elementos = []

    estilos = getSampleStyleSheet()
    titulo = Paragraph("<b>REPORTE DE VENTAS</b>", estilos["Title"])
    fecha_gen = Paragraph(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                          estilos["Normal"])

    elementos.append(titulo)
    elementos.append(Spacer(1, 12))
    elementos.append(fecha_gen)
    elementos.append(Spacer(1, 20))

    # Encabezados de la tabla
    encabezados = ["ID Venta", "Fecha", "Cliente", "Empleado", "Total"]

    # Convertir los datos en filas de tabla
    filas = [encabezados]

    for v in data:
        filas.append([
            v.get("ID Venta", ""),
            v.get("Fecha", ""),
            v.get("Cliente", ""),
            v.get("Empleado", ""),
            v.get("Total", ""),
        ])

    # Crear tabla
    tabla = Table(filas, colWidths=[70, 80, 120, 120, 60])

    # Estilos
    tabla.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        # Celdas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.whitesmoke, colors.lightgrey]),
    ]))

    elementos.append(tabla)

    doc.build(elementos)

    return ruta_pdf
