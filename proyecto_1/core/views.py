from django.shortcuts import render
from django.http import FileResponse
from pathlib import Path

from .forms import GenerarDocumentosForm
from .services.document_service import generar_documentos_proyecto


def generar_documentos_view(request):

    if request.method == "POST":
        form = GenerarDocumentosForm(request.POST)

        if form.is_valid():
            persona = form.cleaned_data["persona"]
            proyecto = form.cleaned_data["proyecto"]

            datos = {
                "{{ nombre }}": persona.nombre_persona,
                "{{ tipo_id }}": persona.tipo_identificacion,
                "{{ numero_id }}": persona.numero_identificacion,
            }

            pdf_final = generar_documentos_proyecto(
                persona,
                proyecto,
                datos
            )

            # 🔥 AQUÍ ESTA LA CLAVE 🔥
            return FileResponse(
                open(pdf_final, "rb"),
                as_attachment=True,
                filename=Path(pdf_final).name,
                content_type="application/pdf"
            )

    else:
        form = GenerarDocumentosForm()

    return render(request, "core/generar_documentos.html", {"form": form})
