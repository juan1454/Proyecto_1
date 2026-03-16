# core/services/pdf_merger.py

from pypdf import PdfWriter
from pathlib import Path
from django.conf import settings
from datetime import datetime
import time

def esperar_archivo_listo(ruta, timeout=10):
    inicio = time.time()

    while True:
        if ruta.exists():
            try:
                with open(ruta, "rb"):
                    return True
            except PermissionError:
                pass

        if time.time() - inicio > timeout:
            return False

        time.sleep(0.2)
# generador del nombre del archivo
def generar_nombre_pdf(numero_id):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"Doc_Final_{numero_id}_{timestamp}.pdf"


def unir_pdfs(rutas_pdfs, numero_id, usuario):

    if not rutas_pdfs:
        raise ValueError("No hay PDFs para unir")

    writer = PdfWriter()

    for ruta in rutas_pdfs:

        ruta = Path(ruta)

        if not esperar_archivo_listo(ruta):
            print(f"⚠️ Archivo no listo o inexistente: {ruta}")
            continue

        try:
            writer.append(str(ruta))
        except Exception as e:
            print(f"⚠️ Error leyendo {ruta}: {e}")
            continue

    # carpeta salida
    salida_dir = Path(settings.MEDIA_ROOT) / "documentos_generados" / usuario
    salida_dir.mkdir(parents=True, exist_ok=True)
    # nombre que obtendrá el archivo
    nombre_pdf = generar_nombre_pdf(numero_id)
    ruta_final = salida_dir / nombre_pdf

    writer.write(ruta_final)
    writer.close()

    return ruta_final
