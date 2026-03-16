from django.contrib import admin
from .models import Proyecto, Plantilla, Persona, TipoDocumento, ProyectoPlantilla, Cargo
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase

admin.site.register(Persona)
admin.site.register(TipoDocumento)
@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)

# Register your models here.

class ProyectoPlantillaInline(SortableInlineAdminMixin, admin.TabularInline):

    model = ProyectoPlantilla
    extra = 1
    sortable_field_name = "orden"
    autocomplete_fields = ["plantilla"]
    fields = ("plantilla", "orden", "activa")

@admin.register(Proyecto)
class ProyectoAdmin(SortableAdminBase, admin.ModelAdmin):

    list_display = ("codigo_proyecto",)

    inlines = [ProyectoPlantillaInline]

@admin.register(Plantilla)
class PlantillaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo_documento", "es_global", "activa")
    list_filter = ("tipo_documento", "es_global", "activa")
    search_fields = ("nombre",)
    filter_horizontal = ("cargos",)