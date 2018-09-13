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

    def __str__(self):
        return self.nombre


class CarreraMateria(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    slug = models.SlugField(max_length=NOMBRE_MAX_LENGTH, unique=True)
    optativa = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
