from django.urls import path
from core.views import generar_documentos_view

urlpatterns = [
    path("generar-documentos/", generar_documentos_view, name="generar_documentos"),
]