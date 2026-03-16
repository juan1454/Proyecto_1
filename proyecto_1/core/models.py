from django.db import models
from django.db.models import Max
    
class Persona(models.Model):
    TIPOS_IDENTIFICACION = [
    ('CC', 'Cédula de ciudadanía'),
    ('TI', 'Tarjeta de identidad'),
    ('CE', 'Cédula de extranjería'),
    ('PA', 'Pasaporte'),
    ]
    tipo_identificacion = models.CharField(
        max_length=2,
        choices=TIPOS_IDENTIFICACION
    )
    numero_identificacion = models.CharField(max_length=20)
    nombre_persona = models.CharField(max_length=75)
    fecha_nacimiento = models.DateField()
    fecha_expedicion = models.DateField()
    numero_telefono = models.CharField(max_length=15,blank=True,null=True)
    numero_telefono2 = models.CharField(max_length=15,blank=True,null=True)
    numero_emergencia = models.CharField(max_length=15,blank=True,null=True)
    eps = models.CharField(max_length=25, blank=True, null=True)
    pension = models.CharField(max_length=25, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('tipo_identificacion', 'numero_identificacion')


    def __str__(self):
        return f"{self.tipo_identificacion} {self.numero_identificacion} {self.nombre_persona}"

class Proyecto(models.Model):

    codigo_proyecto = models.CharField(
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.codigo_proyecto

class Cargo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class TipoDocumento(models.Model):

    nombre = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.nombre
    
class Plantilla(models.Model):

    nombre = models.CharField(max_length=50, unique=True)

    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        related_name="plantillas"
    )

    tipo_archivo = models.CharField(
        max_length=5,
        choices=[
            ('WORD', 'Documento Word'),
            ('EXCEL', 'Archivo Excel')
        ]
    )

    archivo = models.FileField(upload_to='plantillas/')

    es_global = models.BooleanField(default=True)

    cargos = models.ManyToManyField(
        Cargo,
        related_name="plantillas",
        blank=True,
        help_text="Selecciona los cargos que deben firmar esta plantilla. Si lo dejas vacío, será una plantilla global para todos los cargos en este proyecto."
    )

    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class ProyectoPlantilla(models.Model):

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name="configuracion_plantillas"
    )

    plantilla = models.ForeignKey(
        Plantilla,
        on_delete=models.CASCADE
    )

    orden = models.PositiveIntegerField(default=0)

    activa = models.BooleanField(default=True)

    class Meta:
        unique_together = ("proyecto", "plantilla")
        ordering = ["orden"]

    def __str__(self):
        return f"{self.proyecto} - {self.plantilla.nombre}"

    def save(self, *args, **kwargs):

        if self.orden is None:

            ultimo = ProyectoPlantilla.objects.filter(
                proyecto=self.proyecto
            ).aggregate(Max("orden"))["orden__max"]

            self.orden = (ultimo or 0) + 1

        super().save(*args, **kwargs)