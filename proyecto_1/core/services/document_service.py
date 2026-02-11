# core/services/document_service.py
from pathlib import Path
from django.conf import Settings

from core.services.document_generator import generar_word_desde_plantilla
from core.services.excel_generator import generar_excel_desde_plantilla
from core.services.pdf_generator import convertir_a_pdf
from core.services.pdf_merger import unir_pdfs


def generar_documentos_proyecto(persona, proyecto, datos):
    """
    Genera TODOS los documentos asociados a un proyecto
    y retorna una lista con las rutas generadas
    """

    rutas_generadas = []
    pdfs = []

    plantillas = proyecto.plantillas.filter(activa=True)

    for plantilla in plantillas:
        # Control word
        if plantilla.tipo_archivo == "WORD":
            ruta = generar_word_desde_plantilla(
                plantilla,
                datos,
                persona,
                plantilla.tipo_documento
            )
        # Control para excel
        elif plantilla.tipo_archivo == "EXCEL":
            ruta = generar_excel_desde_plantilla(
                plantilla,
                datos,
                persona,
                plantilla.tipo_documento
            )

        rutas_generadas.append(ruta)


    # convertir todos a pdf
    for ruta in rutas_generadas:
        pdf = convertir_a_pdf(ruta)
        pdfs.append(pdf)

    # unir pdfs
    pdf_final = unir_pdfs(pdfs, persona)

    return pdf_final