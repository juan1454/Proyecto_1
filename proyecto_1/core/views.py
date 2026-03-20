from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import FileResponse
from django.contrib import messages
from pathlib import Path
import subprocess

from .forms import GenerarDocumentosForm
from .services.document_service import generar_documentos_proyecto

@login_required
def generar_documentos_view(request):

    if request.method == "POST":
        form = GenerarDocumentosForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            tipo_id = form.cleaned_data["tipo_identificacion"]
            numero_id = form.cleaned_data["numero_identificacion"]
            proyecto = form.cleaned_data["proyecto"]
            cargo = form.cleaned_data["cargo"]

            datos = {
                "{{ nombre }}": nombre,
                "{{ tipo_id }}": tipo_id,
                "{{ numero_id }}": numero_id,
                "{{ cargo }}": cargo.nombre,
            }

            usuario = str(request.user.id)
            
            try:
                pdf_final = generar_documentos_proyecto(
                    numero_id=numero_id,
                    proyecto=proyecto,
                    cargo=cargo,
                    datos=datos,
                    usuario=usuario
                )

                return FileResponse(
                    open(pdf_final, "rb"),
                    as_attachment=True,
                    filename=Path(pdf_final).name,
                    content_type="application/pdf"
                )
            except subprocess.TimeoutExpired:
                messages.error(request, "La generación de documentos tardó demasiado tiempo y fue cancelada. Por favor, intenta de nuevo.")
            except Exception as e:
                import logging
                logging.getLogger(__name__).error("Error al generar documentos", exc_info=True)
                messages.error(request, "Hubo un problema procesando los documentos (es posible que LibreOffice esté saturado). Por favor intenta más tarde.")

    else:
        form = GenerarDocumentosForm()

    return render(request, "core/generar_documentos.html", {"form": form})
