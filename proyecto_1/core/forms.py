from django import forms
from core.models import Proyecto, Cargo


class GenerarDocumentosForm(forms.Form):

    nombre = forms.CharField(label="Nombre completo")
    TIPOS_ID = [
        ("CC", "Cédula de ciudadanía"),
        ("CE", "Cédula de extranjería"),
        ("PEP", "Permiso especial de permanencia"),
        ("PPT", "Pasaporte"),
    ]

    tipo_identificacion = forms.ChoiceField(
        label="Tipo de identificación",
        choices=[("", "Seleccione...")] + TIPOS_ID
    )
    numero_identificacion = forms.CharField(label="Número de identificación")

    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        label="Proyecto"
    )

    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        label="Cargo",
        help_text="Seleccione el cargo. Se generarán los documentos globales y los específicos para este cargo."
    )