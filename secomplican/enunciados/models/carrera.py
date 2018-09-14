from django.db import models

from enunciados.models.models import Materia


NOMBRE_MAX_LENGTH = 1023


class Universidad(models.Model):
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    slug = models.SlugField(max_length=NOMBRE_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.nombre


class Carrera(models.Model):
    nombre = models.CharField()
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia, through='MateriaCarrera')

    def __str__(self):
        return self.nombre


class MateriaCarrera(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    slug = models.SlugField(max_length=NOMBRE_MAX_LENGTH)
    optativa = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        unique_together = (('carrera', 'materia'), ('carrera', 'slug'))
