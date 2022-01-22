from pyexpat import model
from django.db import models

# Create your models here.
class Mascota(models.Model):

    SEXO_OPCIONES=[('M','Macho'),('H','Hembra')]

    nombre = models.CharField(max_length=80)
    remitente = models.CharField(max_length=100)
    especie = models.CharField(max_length=30)
    raza = models.CharField(max_length=30,blank=True,null=True)
    descripcion = models.TextField()

    sexo = models.CharField(max_length=1, choices=SEXO_OPCIONES,blank=True)

    fecha_llegada = models.DateTimeField()

    edad = models.IntegerField(null=True)

    vacunas = models.ManyToManyField('Vacuna',blank=True)

class Vacuna(models.Model):

    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


