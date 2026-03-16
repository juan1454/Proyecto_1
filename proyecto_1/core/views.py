from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import FileResponse
from pathlib import Path

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
            }

            usuario = str(request.user.id)
            
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

    else:
        form = GenerarDocumentosForm()

    return render(request, "core/generar_documentos.html", {"form": form})
