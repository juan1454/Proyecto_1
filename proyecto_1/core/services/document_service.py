# core/services/document_service.py
from pathlib import Path
from django.conf import settings


from core.services.document_generator import generar_word_desde_plantilla
from core.services.excel_generator import generar_excel_desde_plantilla
from core.services.pdf_generator import convertir_a_pdf
from core.services.pdf_merger import unir_pdfs


def generar_documentos_proyecto(numero_id, proyecto, cargo, datos, usuario):
    """
    Genera TODOS los documentos asociados a un proyecto y cargo

    y retorna una lista con las rutas generadas
    """
    limpiar_documentos_generados(usuario)  
    rutas_generadas = []
    pdfs = []   

    # Filter configurations by active, project, and matching cargo or global
    from django.db.models import Q

    configuraciones = proyecto.configuracion_plantillas.filter(
        activa=True
    ).filter(
        Q(plantilla__cargos=cargo) | Q(plantilla__cargos__isnull=True)
    ).select_related("plantilla").order_by("orden").distinct()

    for config in configuraciones:

        plantilla = config.plantilla

        if plantilla.tipo_archivo == "WORD":
            ruta = generar_word_desde_plantilla(
                plantilla,
                datos,
                numero_id,
                usuario,
            )

        elif plantilla.tipo_archivo == "EXCEL":
            ruta = generar_excel_desde_plantilla(
                plantilla,
                datos,
                numero_id,
                usuario,
            )

        rutas_generadas.append(ruta)

    # convertir todos a pdf
    for ruta in rutas_generadas:
        pdf = convertir_a_pdf(ruta)
        pdfs.append(pdf)

    # unir pdfs
    pdf_final = unir_pdfs(pdfs, numero_id, usuario)

    return pdf_final



def limpiar_documentos_generados(usuario):
    carpeta = Path(settings.MEDIA_ROOT) / "documentos_generados" / usuario

    if carpeta.exists():
        for archivo in carpeta.iterdir():
            if archivo.is_file():
                archivo.unlink()  # elimina archivo


