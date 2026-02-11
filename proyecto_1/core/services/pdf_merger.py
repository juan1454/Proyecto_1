# core/services/pdf_merger.py

from pypdf import PdfWriter
from pathlib import Path
from django.conf import settings
from datetime import datetime

# generador del nombre del archivo
def generar_nombre_pdf(persona):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return (
        f"FINAL_"
        f"{persona.tipo_identificacion}_"
        f"{persona.numero_identificacion}_"
        f"{timestamp}.pdf"
    )


def unir_pdfs(rutas_pdfs, persona):

    if not rutas_pdfs:
        raise ValueError("No hay PDFs para unir")

    writer = PdfWriter()

    for ruta in rutas_pdfs:

        ruta = Path(ruta)

        # ✅ validar existencia
        if not ruta.exists():
            print(f"⚠️ Archivo no encontrado: {ruta}")
            continue

        try:
            writer.append(str(ruta))

        except Exception as e:
            print(f"⚠️ Error leyendo {ruta}: {e}")
            continue

    # carpeta salida
    salida_dir = Path(settings.MEDIA_ROOT) / "documentos_generados"
    salida_dir.mkdir(exist_ok=True)
    # nombre que obtendrá el archivo
    nombre_pdf = generar_nombre_pdf(persona)
    ruta_final = salida_dir / nombre_pdf

    writer.write(ruta_final)
    writer.close()

    return ruta_final
