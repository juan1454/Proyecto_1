
from django import forms
from core.models import Persona, Proyecto


class GenerarDocumentosForm(forms.Form):
    persona = forms.ModelChoiceField(
        queryset=Persona.objects.all(),
        label="Persona"
    )

    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        label="Proyecto"
    )
