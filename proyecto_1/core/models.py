from django.db import models


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
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
    PROYECTOS_DISPONIBLES = [
        ('CIP', "Ciprés"),
        ('TBC', "Tribeca"),
        ('BV', "Buena vista"),
    ]
    codigo_proyecto =models.CharField(
        max_length=9,
        choices=PROYECTOS_DISPONIBLES,
        unique=True
    )

    usa_dotacion = models.BooleanField(default=False)
    usa_perfil_sociodemografico = models.BooleanField(default=False)
    usa_capacitacion = models.BooleanField(default=False)
    usa_asistencia = models.BooleanField(default=False)

    def __str__(self):
        return self.get_codigo_proyecto_display()
    
class Plantilla(models.Model):

    TIPO_ARCHIVO = [
        ('WORD', 'Documento Word'),
        ('EXCEL', 'Archivo Excel'),
    ]

    TIPO_DOCUMENTO = [
        ('contrato', 'Contrato'),
        ('dotacion', 'Dotación'),
        ('perfil', 'Perfil Sociodemográfico'),
        ('capacitacion', 'Capacitación'),
        ('asistencia', 'Asistencia'),
    ]

    nombre = models.CharField(max_length=50)

    tipo_documento = models.CharField(
        max_length=20,
        choices=TIPO_DOCUMENTO
    )

    tipo_archivo = models.CharField(
        max_length=5,
        choices=TIPO_ARCHIVO
    )

    archivo = models.FileField(upload_to='plantillas/')

    proyectos = models.ManyToManyField(
        Proyecto,
        related_name='plantillas'
    )

    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo_documento})"
