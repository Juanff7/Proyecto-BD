from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from datetime import datetime

def generar_pdf_entradas(data, nombre_archivo="reporte_entradas.pdf"):

    carpeta = "PDFS"
    os.makedirs(carpeta, exist_ok=True)

    ruta_pdf = os.path.join(carpeta, nombre_archivo)
    pdf = SimpleDocTemplate(ruta_pdf, pagesize=letter)

    titulo = [["Reporte de Entradas (Compras)"]]
    tabla_titulo = Table(titulo)
    tabla_titulo.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))

    encabezado = ["ID Entrada", "Proveedor", "Fecha", "Producto", "Cantidad", "Costo Unit", "Subtotal"]
    filas = [encabezado]

    for e in data:
        filas.append([
            e["id_entrada"],
            e["proveedor"],
            e["fecha"],
            e["producto"],
            e["cantidad"],
            f"${e['costo_unit']}",
            f"${e['sub_total']}",
        ])

    tabla = Table(filas)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    pdf.build([tabla_titulo, tabla])
    return ruta_pdf
